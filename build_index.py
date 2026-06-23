#!/usr/bin/env python3
"""Render topics.json into index.html TOPICS markers and update topic count stat.

Usage: python3 build_index.py
Run from the repo root (studio/sites/alonsi-invest/).
Idempotent — safe to re-run.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS_JSON = ROOT / "topics.json"
INDEX_HTML  = ROOT / "index.html"

ACCENT_BG = {
    "teal":   "rgba(0,212,170,.12)",
    "purple": "rgba(108,99,255,.12)",
    "red":    "rgba(255,107,107,.12)",
    "yellow": "rgba(255,217,61,.12)",
}
ACCENT_COLOR = {
    "teal":   "var(--accent2)",
    "purple": "var(--accent)",
    "red":    "var(--accent3)",
    "yellow": "var(--accent4)",
}


def render_card(t: dict) -> str:
    accent = t.get("accent", "teal")
    bg     = ACCENT_BG.get(accent, ACCENT_BG["teal"])
    color  = ACCENT_COLOR.get(accent, ACCENT_COLOR["teal"])
    tags   = "".join(f'\n        <span class="tag">{tag}</span>' for tag in t.get("tags", []))
    return f"""    <a href="{t['slug']}/" class="topic-card done reveal">
      <div class="card-header">
        <div class="card-icon" style="background:{bg}">{t.get('icon','📖')}</div>
        <span class="badge badge-done">✓ เรียนแล้ว</span>
      </div>
      <div>
        <div class="card-title">{t['title']}</div>
        <div class="card-desc">{t['desc']}</div>
      </div>
      <div class="card-tags">{tags}
      </div>
      <div class="card-footer">
        <span>{t.get('meta','')}</span>
        <span class="card-arrow" style="color:{color}">→</span>
      </div>
    </a>"""


def main():
    topics = json.loads(TOPICS_JSON.read_text(encoding="utf-8"))
    done   = [t for t in topics if t.get("status") == "done"]

    cards_html = "\n".join(render_card(t) for t in done)

    html = INDEX_HTML.read_text(encoding="utf-8")

    # Replace between markers
    html = re.sub(
        r'<!-- TOPICS:START -->.*?<!-- TOPICS:END -->',
        f'<!-- TOPICS:START -->\n{cards_html}\n<!-- TOPICS:END -->',
        html,
        flags=re.DOTALL,
    )

    # Update topic count stat
    html = re.sub(
        r'(<!-- STAT:COUNT -->.*?<div class="num">)\d+(</div>)',
        rf'\g<1>{len(done)}\g<2>',
        html,
        flags=re.DOTALL,
    )

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"✓ {len(done)} topic(s) rendered into index.html")


if __name__ == "__main__":
    main()
