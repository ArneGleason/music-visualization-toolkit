#!/usr/bin/env python3
"""
Contact sheet for storyboard stills named after their setup.

    ./.venv/bin/python3 tools/board_contact.py

Reads board/frames/<setup>[_<variant>].{png,jpg,jpeg,webp} and writes
board/contact.html: one row per setup in shotlist order, every variant side
by side, with the cuts and lyric the setup covers. Setups with no still yet
render as a labelled gap, so the sheet doubles as a progress report.
"""
from __future__ import annotations

import collections
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402

FRAMES = ROOT / "board" / "frames"
OUT = ROOT / "board" / "contact.html"
EXT = {".png", ".jpg", ".jpeg", ".webp"}

CSS = """
body{margin:0;padding:24px;background:#0b0c10;color:#d7dbe3;
     font:13px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
h1{font-size:20px;margin:0 0 4px} .sub{color:#858d9b;margin-bottom:20px}
.row{display:grid;grid-template-columns:220px 1fr;gap:16px;padding:14px 0;
     border-top:1px solid #262b36;align-items:start}
.meta b{display:block;font-size:14px;color:#fff} .meta{color:#9ca4b2}
.meta i{display:block;color:#d2aa65;font-style:normal;margin-top:4px}
.imgs{display:flex;gap:10px;flex-wrap:wrap}
.imgs img{width:360px;aspect-ratio:16/9;object-fit:cover;background:#13151b;
          border:1px solid #262b36;border-radius:4px}
.gap{width:360px;aspect-ratio:16/9;display:grid;place-items:center;color:#5b6270;
     border:1px dashed #343b49;border-radius:4px}
"""


def main():
    shots = load(ROOT / "shots" / "shotlist.json")["shots"]
    order, info = [], {}
    for s in shots:
        su = s.get("setup")
        if not su:
            continue
        if su not in info:
            order.append(su)
            info[su] = {"cuts": [], "lyric": s.get("lyric") or ""}
        info[su]["cuts"].append(f"{s['id']} ({s['dur_sec']:.1f}s)")

    files = collections.defaultdict(list)
    for p in sorted(FRAMES.glob("*")):
        if p.suffix.lower() in EXT:
            key = re.sub(r"_(\d+|[a-z])$", "", p.stem)
            files[key].append(p)

    rows = []
    for su in order:
        imgs = "".join(
            f'<a href="frames/{html.escape(p.name)}"><img src="frames/{html.escape(p.name)}" '
            f'title="{html.escape(p.name)}"></a>' for p in files.get(su, []))
        if not imgs:
            imgs = '<div class="gap">not generated</div>'
        m = info[su]
        rows.append(
            f'<div class="row"><div class="meta"><b>{html.escape(su)}</b>'
            f'{html.escape(", ".join(m["cuts"]))}'
            f'{"<i>" + html.escape(m["lyric"]) + "</i>" if m["lyric"] else ""}'
            f'</div><div class="imgs">{imgs}</div></div>')

    done = sum(1 for su in order if files.get(su))
    OUT.write_text(
        f"<!doctype html><meta charset=utf-8><title>Storyboard contact</title>"
        f"<style>{CSS}</style><h1>Storyboard contact sheet</h1>"
        f'<div class="sub">{done} of {len(order)} setups have stills · '
        f'{sum(len(v) for v in files.values())} images in board/frames/</div>'
        + "".join(rows), encoding="utf-8")
    print(f"wrote {OUT}  ({done}/{len(order)} setups)")


if __name__ == "__main__":
    main()
