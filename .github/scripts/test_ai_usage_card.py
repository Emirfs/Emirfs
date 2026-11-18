"""The card must credit models to their vendor whichever harness ran them."""

import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("ai_usage_card", Path(__file__).with_name("ai_usage_card.py"))
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


class AttributionTest(unittest.TestCase):
    def test_oh_my_pi_claude_counts_as_claude_spend(self):
        tokens = {"input": 100, "output": 50, "cacheRead": 800, "cacheWrite": 50}
        data = {"dateRange": {"end": "2026-11-18"}, "contributions": [
            {"date": "2026-11-18", "clients": [
                {"client": "omp", "models": {"claude-opus-5-5": {**tokens, "cost": 2.5, "messages": 3},
                                             "gpt-6-luna": {**tokens, "cost": 0.5, "messages": 1}}},
                {"client": "claude", "models": {"claude-sonnet-5-5": {**tokens, "cost": 1.0, "messages": 2}}},
            ]},
        ]}
        rows, end = usage.parse(data)
        groups = {g["vendor"]: g for g in usage.summarise(rows)}
        self.assertEqual(end, "2026-11-18")
        self.assertEqual(groups["anthropic"]["tokens"], 2000)
        self.assertEqual(groups["anthropic"]["cost"], 3.5)
        self.assertEqual(dict(groups["anthropic"]["via"]), {"omp": 1000, "claude": 1000})
        self.assertEqual(groups["openai"]["tokens"], 1000)
        svg = usage.render(rows, end)
        self.assertIn("via Oh My Pi, Claude Code", svg)
        self.assertIn("66.7% · $4", svg)


if __name__ == "__main__":
    unittest.main()
