#!/usr/bin/env python3
"""
Bridge a project's music-video register into the shot pipeline.

    ./.venv/bin/python3 tools/register2sections.py --project projects/rivers-of-mars/project.json

Reads the project's compiled timeline (run `tools/timeline.py sync` first) and
writes:

  shots/sections.json    one section per scene-lane item, with the exact
                         frame-derived start/end seconds from the register
  analysis/lyrics.json   the register's lyric lane as timed lines, so
                         tools/shotplan.py attaches lyric text to every cut
  analysis/beatmap.json  the register's bar grid in the shape mvlib.Beatmap
                         expects (only when missing, or with --force-beatmap)

This makes `tools/shotplan.py` and everything downstream consume the same
frame-accurate grid the vector renderer uses, instead of re-deriving timing.
The register stays the creative source of truth; this tool is one-way.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save  # noqa: E402


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=pathlib.Path, required=True,
                    help="path to projects/<slug>/project.json")
    ap.add_argument("--lane", default="scenes",
                    help="register track id to turn into sections (default: scenes)")
    ap.add_argument("--force-beatmap", action="store_true",
                    help="overwrite analysis/beatmap.json even if it exists")
    a = ap.parse_args()

    project = load(a.project)
    pdir = a.project.parent
    compiled_path = (pdir / project["timing"]["compiledTimeline"]).resolve()
    if not compiled_path.exists():
        raise SystemExit(f"{compiled_path} not found -- run "
                         f"tools/timeline.py sync {a.project} first")
    compiled = load(compiled_path)

    lanes = {t["id"]: t for t in compiled["tracks"]}
    if a.lane not in lanes:
        raise SystemExit(f"lane {a.lane!r} not in register "
                         f"(have: {', '.join(lanes)})")

    sections = []
    for item in lanes[a.lane]["items"]:
        sid = item["id"]
        sid = re.sub(r"^scene-", "", sid)
        # opaque editor-generated ids get a positional name instead
        if re.fullmatch(r"m[a-z0-9]{7,}", sid):
            sid = f"scene-{len(sections) + 1:02d}"
        sections.append({
            "id": slug(sid),
            "name": sid,
            "start_sec": round(item["startSec"], 4),
            "end_sec": round(item["endSec"], 4),
            "dur_sec": round(item["endSec"] - item["startSec"], 4),
            "start_barbeat": str(item.get("start", "")),
            "register_id": item["id"],
        })
    sections.sort(key=lambda s: s["start_sec"])
    save(ROOT / "shots" / "sections.json", {"sections": sections})
    for s in sections:
        print(f"  {s['start_sec']:8.3f}s  {s['dur_sec']:7.3f}s  {s['id']}")

    if "lyrics" in lanes:
        lines = [{
            "sec": round(it["startSec"], 4),
            "end_sec": round(it["endSec"], 4),
            "text": it.get("text", ""),
            "speaker": it.get("speaker"),
        } for it in lanes["lyrics"]["items"]]
        save(ROOT / "analysis" / "lyrics.json", {"lines": lines})

    beatmap_out = ROOT / "analysis" / "beatmap.json"
    if a.force_beatmap or not beatmap_out.exists():
        timing = compiled["timing"]
        save(beatmap_out, {
            "duration_sec": timing["durationSec"],
            "ppq": timing.get("ppq", 960),
            "bars": timing["bars"],
        })
        print(f"  wrote {beatmap_out.relative_to(ROOT)} from the register grid")


if __name__ == "__main__":
    main()
