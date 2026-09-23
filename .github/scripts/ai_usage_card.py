"""Render assets/ai-usage.svg from the public Tokscale API.

Aggregates every submitted day per coding-agent client and draws an
animated bar card. Run by .github/workflows/ai-usage.yml once a day.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "Emirfs"
API = f"https://tokscale.ai/api/users/{USER}"
OUT = Path(__file__).resolve().parents[2] / "assets" / "ai-usage.svg"

# client id -> (display name, vendor, colour)
CLIENTS = {
    "claude": ("Claude Code", "Anthropic", "#D97757"),
    "codex": ("Codex CLI", "OpenAI", "#10A37F"),
    "gemini": ("Gemini CLI", "Google", "#4E8CF7"),
    "antigravity-cli": ("Antigravity CLI", "Google", "#7C9CF5"),
    "opencode": ("OpenCode", "Open source", "#E0A526"),
    "pi": ("Pi", "Open source", "#A78BFA"),
    "omp": ("Oh My Pi", "Open source", "#22C3D8"),
}
FALLBACK_COLOUR = "#8B96A8"


def fetch() -> dict:
    req = urllib.request.Request(API, headers={"User-Agent": f"{USER}-profile-readme"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def aggregate(data: dict) -> list[dict]:
    totals: dict[str, dict] = {}
    for day in data["contributions"]:
        for entry in day["clients"]:
            row = totals.setdefault(entry["client"], {"tokens": 0, "cost": 0.0, "messages": 0})
            row["tokens"] += sum(entry["tokens"].values())
            row["cost"] += entry["cost"]
            row["messages"] += entry["messages"]
    rows = [{"client": k, **v} for k, v in totals.items() if v["tokens"] > 0]
    rows.sort(key=lambda r: r["tokens"], reverse=True)
    return rows


def human(n: float) -> str:
    for unit, size in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= size:
            return f"{n / size:.2f}{unit}"
    return str(int(n))


def money(n: float) -> str:
    return f"${n / 1000:.2f}K" if n >= 1000 else f"${n:.0f}"


def render(data: dict, rows: list[dict]) -> str:
    stats = data["stats"]
    width, pad = 860, 32
    head_h, row_h = 150, 46
    height = head_h + row_h * len(rows) + 58
    bar_x, bar_w = 250, 420
    peak = rows[0]["tokens"]
    total = stats["totalTokens"]
    updated = data["updatedAt"][:10]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="AI token usage by coding agent">',
        "<style>",
        "text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}",
        ".t{fill:#E6EDF3;font-size:20px;font-weight:700}",
        ".s{fill:#8B96A8;font-size:13px}",
        ".k{fill:#E6EDF3;font-size:26px;font-weight:700}",
        ".kl{fill:#8B96A8;font-size:12px;letter-spacing:.4px}",
        ".n{fill:#E6EDF3;font-size:14px;font-weight:600}",
        ".v{fill:#8B96A8;font-size:12px}",
        ".val{fill:#E6EDF3;font-size:13px;font-weight:600}",
        ".bar{transform-box:fill-box;transform-origin:left;transform:scaleX(0);"
        "animation:grow 1.4s cubic-bezier(.2,.8,.2,1) forwards}",
        ".fade{opacity:0;animation:fade .6s ease forwards}",
        "@keyframes grow{to{transform:scaleX(1)}}",
        "@keyframes fade{to{opacity:1}}",
        "</style>",
        f'<rect width="{width}" height="{height}" rx="14" fill="#0D1117"/>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="13.5" '
        'fill="none" stroke="#30363D"/>',
        f'<text x="{pad}" y="44" class="t">AI tokens across coding agents</text>',
        f'<text x="{pad}" y="66" class="s">All-time usage tracked by Tokscale · '
        f"last submission {updated}</text>",
    ]

    kpis = [
        (human(total), "TOTAL TOKENS"),
        (money(stats["totalCost"]), "API-EQUIVALENT COST"),
        (f'{stats["sessionCount"]:,}', "SESSIONS"),
        (str(stats["activeDays"]), "ACTIVE DAYS"),
    ]
    for i, (value, label) in enumerate(kpis):
        x = pad + i * 200
        out.append(f'<text x="{x}" y="112" class="k">{escape(value)}</text>')
        out.append(f'<text x="{x}" y="132" class="kl">{label}</text>')

    for i, row in enumerate(rows):
        name, vendor, colour = CLIENTS.get(row["client"], (row["client"], "", FALLBACK_COLOUR))
        y = head_h + 22 + i * row_h
        delay = f"{0.15 + i * 0.12:.2f}s"
        w = max(4.0, bar_w * row["tokens"] / peak)
        share = 100 * row["tokens"] / total
        out += [
            f'<g class="fade" style="animation-delay:{delay}">',
            f'<circle cx="{pad + 6}" cy="{y - 4}" r="6" fill="{colour}"/>',
            f'<text x="{pad + 22}" y="{y}" class="n">{escape(name)}</text>',
            f'<text x="{pad + 22}" y="{y + 17}" class="v">{escape(vendor)}</text>',
            "</g>",
            f'<rect x="{bar_x}" y="{y - 14}" width="{bar_w}" height="14" rx="7" fill="#161B22"/>',
            f'<rect class="bar" style="animation-delay:{delay}" x="{bar_x}" y="{y - 14}" '
            f'width="{w:.1f}" height="14" rx="7" fill="{colour}"/>',
            f'<g class="fade" style="animation-delay:{delay}">',
            f'<text x="{bar_x + bar_w + 18}" y="{y}" class="val">{human(row["tokens"])}</text>',
            f'<text x="{bar_x + bar_w + 18}" y="{y + 17}" class="v">{share:.1f}% · '
            f'{money(row["cost"])}</text>',
            "</g>",
        ]

    out.append(
        f'<text x="{pad}" y="{height - 22}" class="s">Tokens include cache reads. '
        "Cost is the list-price equivalent, not the amount billed.</text>"
    )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    data = fetch()
    rows = aggregate(data)
    if not rows:
        print("Tokscale returned no client data; keeping the previous card.", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(data, rows), encoding="utf-8")
    print(f"wrote {OUT} ({len(rows)} clients, {human(data['stats']['totalTokens'])} tokens)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
