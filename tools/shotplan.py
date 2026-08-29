#!/usr/bin/env python3
"""
Generate the shot list (the EDL) from sections + cutting rules.

    python3 tools/shotplan.py

Reads shots/plan.json, shots/sections.json, analysis/{beatmap,lyrics}.json.
Writes shots/shotlist.json -- the single source of truth for everything
downstream. Prompts, animatic and final render are all derived from it, so
edit the shot list (by hand or by re-running this) and re-render; never edit
the render.

Existing shots are preserved on re-run when --merge is passed: hand-written
descriptions, prompts and assigned clips survive a re-plan as long as the
shot id still exists.

Cutting rules per section (see shots/plan.json):
  cut_every_bars / cut_every_beats   grid the cuts land on
  braid       repeating cycle of shot types, e.g. ["performance","concept"]
  setups      named reusable setups; shots cycle through them, so the same
              generated clip can serve several cuts (this is what keeps the
              credit burn down)
  hold        list of bar.beat positions to force a cut at
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, Beatmap, load, save, to_frames  # noqa: E402


def section_cuts(sec, rules, bm: Beatmap, max_sec: float):
    """Times (seconds) at which this section changes shot."""
    bars = [b for b in bm.d["bars"]
            if sec["start_sec"] - 1e-6 <= b["sec"] < sec["end_sec"] - 1e-6]
    cuts = []
    if rules.get("cut_every_beats"):
        n = int(rules["cut_every_beats"])
        flat = [t for b in bars for t in b["beats"]]
        cuts = flat[::n]
    else:
        n = int(rules.get("cut_every_bars", 2))
        cuts = [b["sec"] for b in bars[::n]]
    for h in rules.get("hold", []):
        cuts.append(bm.sec(h))
    cuts = sorted({round(c, 6) for c in cuts if sec["start_sec"] - 1e-6 <= c < sec["end_sec"]})
    if not cuts or cuts[0] > sec["start_sec"] + 1e-6:
        cuts.insert(0, sec["start_sec"])

    # split anything longer than the model's clip ceiling
    out, edges = [], cuts + [sec["end_sec"]]
    for a, b in zip(edges, edges[1:]):
        out.append(a)
        span = b - a
        if span > max_sec:
            k = int(span // max_sec) + 1
            for i in range(1, k):
                out.append(bm.snap(a + span * i / k, 1))
    return sorted({round(c, 6) for c in out})


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--merge", action="store_true",
                    help="keep descriptions/prompts/clips from the existing shotlist")
    a = ap.parse_args()

    bm = Beatmap.load()
    plan = load(ROOT / "shots" / "plan.json")
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    try:
        lyrics = load(ROOT / "analysis" / "lyrics.json")["lines"]
    except FileNotFoundError:
        lyrics = []

    fps = plan.get("fps", 24)
    max_sec = plan.get("max_shot_sec", 8.0)

    # Sections often begin on a pickup beat ("...take the dive" entering on
    # beat 3). Cuts want downbeats, so snap each boundary back to the bar line
    # at or before it — the pickup lyric stays inside its own section, and the
    # first shot of every section is a whole bar instead of a sliver.
    if plan.get("snap_sections_to_bars", True):
        bar_starts = [b["sec"] for b in bm.d["bars"]]
        for s in sections:
            prior = [t for t in bar_starts if t <= s["start_sec"] + 1e-6]
            if prior:
                s["start_sec"] = round(max(0.0, prior[-1]), 6)
        for s, nxt in zip(sections, sections[1:]):
            s["end_sec"] = nxt["start_sec"]
    prev = {}
    out_path = ROOT / "shots" / "shotlist.json"
    if a.merge and out_path.exists():
        prev = {s["id"]: s for s in load(out_path)["shots"]}

    shots, n = [], 0
    for sec in sections:
        rules = {**plan.get("default", {}), **plan.get("sections", {}).get(sec["id"], {})}
        if rules.get("skip"):
            continue
        cuts = section_cuts(sec, rules, bm, max_sec)
        braid = rules.get("braid") or [rules.get("type", "concept")]
        setups = rules.get("setups") or []
        min_sec = plan.get("min_shot_sec", 0.25)
        # drop cuts that would leave a sliver against the section end
        cuts = [c for c in cuts if sec["end_sec"] - c >= min_sec] or [sec["start_sec"]]
        pairs = [(a_, b_) for a_, b_ in zip(cuts, cuts[1:] + [sec["end_sec"]])
                 if b_ - a_ >= min_sec]
        for i, (start, end) in enumerate(pairs):
            n += 1
            sid = f"s{n:03d}"
            kind = braid[i % len(braid)]
            setup = setups[i % len(setups)] if setups else None
            covered = [l for l in lyrics if start - 1e-6 <= l["sec"] < end - 1e-6]
            shot = {
                "id": sid,
                "section": sec["id"],
                "type": kind,
                "setup": setup,
                "start_barbeat": bm.nearest_barbeat(start),
                "start_sec": round(start, 4),
                "end_sec": round(end, 4),
                "dur_sec": round(end - start, 4),
                "frames": to_frames(end - start, fps),
                "lyric": " / ".join(l["text"] for l in covered),
                "description": "",
                "prompt": "",
                "clip": {"file": None, "in_sec": 0.0, "speed": 1.0},
                "transition": {"type": "cut", "dur_sec": 0.0},
            }
            if a.merge and sid in prev:
                for k in ("description", "prompt", "clip", "transition", "setup", "type"):
                    if prev[sid].get(k):
                        shot[k] = prev[sid][k]
            shots.append(shot)

    save(out_path, {"fps": fps, "duration_sec": bm.duration,
                    "max_shot_sec": max_sec, "shots": shots})

    over = [s for s in shots if s["dur_sec"] > max_sec + 1e-6]
    uniq = len({s.get("setup") or s["id"] for s in shots})
    print(f"  {len(shots)} shots   avg {sum(s['dur_sec'] for s in shots)/len(shots):.2f}s"
          f"   min {min(s['dur_sec'] for s in shots):.2f}s"
          f"   max {max(s['dur_sec'] for s in shots):.2f}s")
    print(f"  {uniq} unique setups to generate  ({len(shots) - uniq} cuts reuse footage)")
    if over:
        print(f"  !! {len(over)} shots exceed {max_sec}s: " + ", ".join(s["id"] for s in over))


if __name__ == "__main__":
    main()
