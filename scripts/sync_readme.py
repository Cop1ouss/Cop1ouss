#!/usr/bin/env python3
"""Rewrites the journey block in README.md from docs/data/journey.json.

Runs automatically in GitHub Actions whenever journey.json changes.
Run it by hand with:  python3 scripts/sync_readme.py
© 2026 Dajoni Gomez · Uncook™
"""
import json
import pathlib
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DATA = ROOT / "docs" / "data" / "journey.json"
START, END = "<!-- JOURNEY:START -->", "<!-- JOURNEY:END -->"
MARK = {"done": "✓", "active": "▶", "planned": "○"}
TRACK = {"networking": "Networking", "security": "Security", "systems": "Systems", "cloud": "Cloud", "career": "Career"}


def when(d: str) -> str:
    parts = d.split("-")
    if len(parts) == 1:
        return parts[0]
    return date(int(parts[0]), int(parts[1]), 1).strftime("%b %Y")


def main() -> None:
    entries = json.loads(DATA.read_text(encoding="utf-8"))["entries"]
    logged = sorted((e for e in entries if e["status"] != "planned"), key=lambda e: e["date"], reverse=True)[:6]
    planned = [e for e in entries if e["status"] == "planned"]
    rows = ["| When | | Milestone | Track |", "| --- | --- | --- | --- |"]
    rows += [f"| {when(e['date'])} | {MARK[e['status']]} | **{e['title']}** | {TRACK.get(e['track'], e['track'])} |" for e in logged]
    block = "\n".join([
        START,
        *rows,
        "",
        "**Next up:** " + " · ".join(e["title"] for e in planned),
        END,
    ])
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit("README.md is missing the JOURNEY markers")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(head + block + tail, encoding="utf-8")
    print(f"README journey block updated: {len(logged)} recent, {len(planned)} planned")


if __name__ == "__main__":
    main()
