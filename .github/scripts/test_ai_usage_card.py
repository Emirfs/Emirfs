"""Usage refresh must not erase history after local session logs are retired."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("ai_usage_card", Path(__file__).with_name("ai_usage_card.py"))
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


class SnapshotRefreshTest(unittest.TestCase):
    def test_refresh_preserves_retired_logs_without_adding_overlapping_totals(self):
        historical = {"date": "2026-09-01", "client": "omp", "model": "gemini-3.8-flash",
                      "tokens": 1000, "cost": 0.01, "messages": 10}
        overlap = {**historical, "date": "2026-10-08", "tokens": 200}
        refreshed = {**overlap, "tokens": 500, "messages": 5}
        hermes = {**historical, "date": "2026-11-17", "client": "hermes", "tokens": 300}
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "usage.json"
            snapshot.write_text(json.dumps({"collected": "2026-10-08", "rows": [historical, overlap]}))
            with (patch.object(usage, "SNAPSHOT", snapshot),
                  patch.object(usage, "tokscale_graph", side_effect=[[hermes], [refreshed]]),
                  patch.object(usage, "hermes_profiles", return_value=[]),
                  patch.object(usage, "merged_omp_home", side_effect=lambda root: root)):
                usage.collect("2026-08-28")
                rows, collected = usage.load_snapshot("2026-08-28")
                self.assertEqual(sum(r["tokens"] for r in rows), 1800)
                self.assertEqual(rows, [historical, refreshed, hermes])
                self.assertIn("1.80K", usage.render(rows, "2026-08-28", collected))
                remaining, _ = usage.load_snapshot("2026-10-08")
                self.assertEqual(remaining, [hermes])

    def test_hermes_profiles_add_to_the_main_home_instead_of_replacing_it(self):
        main = {"date": "2026-11-18", "client": "hermes", "model": "claude-haiku-5-5",
                "tokens": 1000, "cost": 0.5, "messages": 4}
        profile = {**main, "tokens": 250, "cost": 0.25, "messages": 1}
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "usage.json"
            with (patch.object(usage, "SNAPSHOT", snapshot),
                  patch.object(usage, "tokscale_graph", side_effect=[[main], [], [profile]]) as graph,
                  patch.object(usage, "hermes_profiles", return_value=[Path("kodcu")]),
                  patch.object(usage, "merged_omp_home", side_effect=lambda root: root)):
                usage.collect("2026-11-17")
                rows, _ = usage.load_snapshot("2026-11-17")
        self.assertEqual(graph.call_args_list[2].args[3], {"HERMES_HOME": "kodcu"})
        self.assertEqual(rows, [{**main, "tokens": 1250, "cost": 0.75, "messages": 5}])


if __name__ == "__main__":
    unittest.main()
