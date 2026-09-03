#!/usr/bin/env python3
"""
Export beat-locked overlay cues for the Blender composite.

    python tools/overlay_cues.py            -> generated/overlay_cues.json

Reads the compiled register (projects/<slug>/generated/timeline.compiled.json),
the bar grid (analysis/beatmap.json), the sections and the shot list, and
writes one flat, frame-accurate cue file at the OUTPUT fps (shots/plan.json,
24 by default). Everything downstream that has to hit the music reads this
file, never the register directly:

  beats     every beat with its bar number and a downbeat flag
  lyrics    each lyric line: on/off frames, text, speaker
  sections  section starts (the register's scene lane, as cut by shotplan)
  choreo    choreography spans (id, frames, drivers) for later element work
  shots     the cut itself: shot id, setup, start/end frame

Frames are rounded from seconds at the output fps; the register's own frame
numbers are at its native 60 fps and are not used here.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402


def frame(sec: float, fps: float) -> int:
    return int(round(sec * fps))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=pathlib.Path,
                    default=ROOT / "projects" / "rivers-of-mars" / "project.json")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "generated" / "overlay_cues.json")
    a = ap.parse_args()

    plan = load(ROOT / "shots" / "plan.json")
    fps = float(plan.get("fps", 24))
    compiled = load(a.project.parent / "generated" / "timeline.compiled.json")
    beatmap = load(ROOT / "analysis" / "beatmap.json")
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    shotlist = load(ROOT / "shots" / "shotlist.json")

    duration = float(beatmap.get("duration_sec") or shotlist.get("duration_sec"))
    total = int(math.ceil(duration * fps))

    beats = []
    for bar in beatmap["bars"]:
        for i, sec in enumerate(bar["beats"]):
            if sec < 0:
                continue
            beats.append({"frame": frame(sec, fps), "sec": round(sec, 4),
                          "bar": bar["bar"], "beat": i + 1, "downbeat": i == 0})

    tracks = {t["id"]: t["items"] for t in compiled["tracks"]}
    lyrics = [{"id": it["id"], "on": frame(it["startSec"], fps), "off": frame(it["endSec"], fps),
               "text": it["text"], "speaker": it.get("speaker", "")}
              for it in tracks.get("lyrics", []) if it.get("startSec") is not None]
    choreo = [{"id": it["id"], "on": frame(it["startSec"], fps), "off": frame(it["endSec"], fps),
               "drivers": it.get("drivers", []),
               "shot": (it.get("blocking") or {}).get("rendererShot")}
              for it in tracks.get("choreography", []) if it.get("startSec") is not None]
    secs = [{"id": s["id"], "frame": frame(s["start_sec"], fps), "sec": s["start_sec"]} for s in sections]
    shots = [{"id": s["id"], "setup": s.get("setup"), "section": s["section"],
              "start": frame(s["start_sec"], fps), "end": frame(s["end_sec"], fps),
              "lyric": s.get("lyric", "")} for s in shotlist["shots"]]
    # make the cut gapless at the output fps: each shot ends where the next begins
    for s, nxt in zip(shots, shots[1:]):
        s["end"] = nxt["start"]
    if shots:
        shots[-1]["end"] = max(shots[-1]["end"], total)

    out = {"fps": fps, "frames": total, "duration_sec": duration,
           "beats": beats, "lyrics": lyrics, "sections": secs, "choreo": choreo, "shots": shots}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"wrote {a.out}: {total} frames @ {fps:g} fps, {len(beats)} beats, "
          f"{len(lyrics)} lyric lines, {len(secs)} sections, {len(choreo)} choreo spans, {len(shots)} shots")


if __name__ == "__main__":
    main()
