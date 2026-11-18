"""Render assets/ai-usage.svg: AI token usage grouped by model vendor.

The only source is the public Tokscale API. The local machine keeps it complete and current:

* `%APPDATA%/tokscale/settings.json` → `scanner.extraScanPaths.omp` lists every Oh My Pi profile's
  sessions (`~/.omp/profiles/*/agent/sessions`) and the session backup of retired profiles;
  Tokscale on its own reads only `~/.omp/agent/sessions`.
* `tokscale autosubmit` submits every 3 hours. Submitted day totals never decrease, so usage from
  logs deleted later stays counted.

Usage:
  python .github/scripts/ai_usage_card.py   # CI: re-render from the API
"""

from __future__ import annotations

import json
import urllib.request
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

USER = "Emirfs"
API = f"https://tokscale.ai/api/users/{USER}"
REPO = Path(__file__).resolve().parents[2]
CARD = REPO / "assets" / "ai-usage.svg"

# vendor -> (title, subtitle, colour); order is the fallback sort order
VENDORS = {
    "anthropic": ("Claude", "Anthropic", "#D97757"),
    "openai": ("GPT · Codex", "OpenAI", "#10A37F"),
    "google": ("Gemini", "Google", "#4E8CF7"),
    "deepseek": ("DeepSeek", "DeepSeek", "#6C8CFF"),
    "local": ("Local models", "Ollama", "#A78BFA"),
    "other": ("Other", "", "#8B96A8"),
}
HARNESSES = {
    "claude": "Claude Code",
    "codex": "Codex CLI",
    "gemini": "Gemini CLI",
    "antigravity-cli": "Antigravity CLI",
    "opencode": "OpenCode",
    "pi": "Pi",
    "omp": "Oh My Pi",
    "hermes": "Hermes Agent",
    "antigravity-extension": "Antigravity",
}


def vendor_of(model: str) -> str:
    m = model.lower().split("/")[-1]
    if m.startswith("claude"):
        return "anthropic"
    if m.startswith(("gpt", "codex", "o1", "o3", "o4")):
        return "openai"
    if m.startswith("gemini"):
        return "google"
    if m.startswith("deepseek"):
        return "deepseek"
    if ":" in m or m.startswith(("qwen", "llama", "mistral", "phi")):
        return "local"
    return "other"


def row(day: str, client: str, model: str, tokens: dict, cost: float, messages: int) -> dict:
    return {
        "date": day,
        "client": client,
        "model": model,
        "tokens": int(sum(tokens.get(k, 0) or 0 for k in ("input", "output", "cacheRead", "cacheWrite"))),
        "cost": round(float(cost or 0), 6),
        "messages": int(messages or 0),
    }


def parse(data: dict) -> tuple[list[dict], str]:
    rows = []
    for day in data["contributions"]:
        for entry in day["clients"]:
            for model, m in entry["models"].items():
                rows.append(row(day["date"], entry["client"], model, m, m.get("cost"), m.get("messages")))
    return rows, data["dateRange"]["end"]


def fetch_server() -> tuple[list[dict], str]:
    req = urllib.request.Request(API, headers={"User-Agent": f"{USER}-profile-readme"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return parse(json.load(resp))


# ---------------------------------------------------------------- render

def human(n: float) -> str:
    for unit, size in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= size:
            return f"{n / size:.2f}{unit}"
    return str(int(n))


def money(n: float) -> str:
    return f"${n / 1000:.2f}K" if n >= 1000 else f"${n:.0f}"


def summarise(rows: list[dict]) -> list[dict]:
    groups: dict[str, dict] = defaultdict(lambda: {"tokens": 0, "cost": 0.0, "via": defaultdict(int)})
    for r in rows:
        g = groups[vendor_of(r["model"])]
        g["tokens"] += r["tokens"]
        g["cost"] += r["cost"]
        g["via"][r["client"]] += r["tokens"]
    out = [{"vendor": v, **g} for v, g in groups.items() if g["tokens"] > 0]
    out.sort(key=lambda g: g["tokens"], reverse=True)
    return out


def render(rows: list[dict], server_end: str) -> str:
    groups = summarise(rows)
    total = sum(g["tokens"] for g in groups)
    cost = sum(g["cost"] for g in groups)
    groups = [g for g in groups if g["tokens"] >= total * 0.001]  # hide rows under 0.1%
    days = len({r["date"] for r in rows})
    messages = sum(r["messages"] for r in rows)

    width, pad = 860, 32
    head_h, row_h = 150, 50
    height = head_h + row_h * len(groups) + 62
    bar_x, bar_w = 250, 420
    peak = groups[0]["tokens"]

    source = f"Tokscale submissions to {server_end}"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="AI token usage by model vendor">',
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
        f'<text x="{pad}" y="44" class="t">AI tokens by model vendor</text>',
        f'<text x="{pad}" y="66" class="s">{escape(source)}</text>',
    ]
    kpis = [
        (human(total), "TOTAL TOKENS"),
        (money(cost), "API-EQUIVALENT COST"),
        (f"{messages:,}", "MODEL RESPONSES"),
        (str(days), "ACTIVE DAYS"),
    ]
    for i, (value, label) in enumerate(kpis):
        x = pad + i * 200
        out.append(f'<text x="{x}" y="112" class="k">{escape(value)}</text>')
        out.append(f'<text x="{x}" y="132" class="kl">{label}</text>')

    for i, g in enumerate(groups):
        title, vendor, colour = VENDORS[g["vendor"]]
        via = sorted(g["via"].items(), key=lambda kv: kv[1], reverse=True)[:3]
        via_text = "via " + ", ".join(HARNESSES.get(c, c) for c, _ in via)
        y = head_h + 24 + i * row_h
        delay = f"{0.15 + i * 0.12:.2f}s"
        w = max(4.0, bar_w * g["tokens"] / peak)
        out += [
            f'<g class="fade" style="animation-delay:{delay}">',
            f'<circle cx="{pad + 6}" cy="{y - 4}" r="6" fill="{colour}"/>',
            f'<text x="{pad + 22}" y="{y}" class="n">{escape(title)}'
            + (f' <tspan class="v">{escape(vendor)}</tspan>' if vendor and vendor != title else "")
            + "</text>",
            f'<text x="{pad + 22}" y="{y + 18}" class="v">{escape(via_text)}</text>',
            "</g>",
            f'<rect x="{bar_x}" y="{y - 14}" width="{bar_w}" height="14" rx="7" fill="#161B22"/>',
            f'<rect class="bar" style="animation-delay:{delay}" x="{bar_x}" y="{y - 14}" '
            f'width="{w:.1f}" height="14" rx="7" fill="{colour}"/>',
            f'<g class="fade" style="animation-delay:{delay}">',
            f'<text x="{bar_x + bar_w + 18}" y="{y}" class="val">{human(g["tokens"])}</text>',
            f'<text x="{bar_x + bar_w + 18}" y="{y + 18}" class="v">'
            f'{100 * g["tokens"] / total:.1f}% · {money(g["cost"])}</text>',
            "</g>",
        ]
    out.append(
        f'<text x="{pad}" y="{height - 24}" class="s">Tokens include cache reads. '
        "Cost is the list-price equivalent, not the amount billed.</text>"
    )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    rows, server_end = fetch_server()
    rows = [r for r in rows if r["tokens"] > 0]
    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(render(rows, server_end), encoding="utf-8")
    for g in summarise(rows):
        print(f'{g["vendor"]:<10}{human(g["tokens"]):>10}{money(g["cost"]):>10}  '
              + ", ".join(f"{HARNESSES.get(c, c)}={human(t)}" for c, t in g["via"].items()))
    print(f"total {human(sum(r['tokens'] for r in rows))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
