#!/usr/bin/env python3
"""
Turn bar/beat-marked lyrics into timed lyrics, and derive sections.

    python3 tools/lyrics.py lyrics/lyrics.md

Input format (write this in Bitwig against your markers):

    ## Intro            <- section header, runs until the next header
    ## Verse 1
    [9.1]  I woke up on the wrong side of the sun
           and the rest of it came undone      <- unmarked: interpolated
    [13.1] Pockets keep

Rules:
  * `## Name` starts a section at the next lyric position (or `## Name @ 5.1`
    to pin it explicitly -- do this for instrumental sections).
  * `[bar.beat]` pins a line. Fractional beats are fine: [9.2.5]
  * Unmarked lines are spaced evenly between the pinned lines around them,
    which is usually close enough for on-screen text and shot planning.
  * `%` at the end of a line marks a hard visual accent worth cutting on.

Writes analysis/lyrics.json and, if headers are present, shots/sections.json.
For word-level timing (only needed if you want per-word visual hits), run a
forced aligner on the isolated vocal stem -- see docs/ALIGNMENT.md.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, Beatmap, save  # noqa: E402

MARK = re.compile(r"^\s*\[([0-9]+(?:\.[0-9]+){0,2})\]\s*(.*)$")
HEAD = re.compile(r"^\s*#{1,3}\s*(.+?)\s*(?:@\s*([0-9]+(?:\.[0-9]+){0,2})\s*)?$")


def parse(text: str):
    lines, sections = [], []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("//"):
            continue
        h = HEAD.match(raw)
        if h and not MARK.match(raw):
            sections.append({"name": h.group(1), "at": h.group(2), "index": len(lines)})
            continue
        m = MARK.match(raw)
        at, txt = (m.group(1), m.group(2)) if m else (None, raw.strip())
        accent = txt.rstrip().endswith("%")
        lines.append({"at": at, "text": txt.rstrip().rstrip("%").strip(), "accent": accent})
    return lines, sections


def interpolate(lines, bm: Beatmap):
    """Fill in seconds for unmarked lines by even spacing between pins."""
    for ln in lines:
        ln["sec"] = bm.sec(ln["at"]) if ln["at"] else None
    pins = [i for i, ln in enumerate(lines) if ln["sec"] is not None]
    if not pins:
        raise SystemExit("no [bar.beat] markers found -- pin at least the first line of each section")
    for a, b in zip(pins, pins[1:]):
        gap = b - a
        if gap < 2:
            continue
        t0, t1 = lines[a]["sec"], lines[b]["sec"]
        for k in range(1, gap):
            lines[a + k]["sec"] = t0 + (t1 - t0) * k / gap
            lines[a + k]["interpolated"] = True
    # trailing unmarked lines: extend at the average line spacing
    if pins[-1] < len(lines) - 1:
        step = 2.0
        if len(pins) > 1:
            step = (lines[pins[-1]]["sec"] - lines[pins[0]]["sec"]) / max(1, pins[-1] - pins[0])
        for k in range(pins[-1] + 1, len(lines)):
            lines[k]["sec"] = lines[k - 1]["sec"] + step
            lines[k]["interpolated"] = True
    for ln in lines:
        ln["barbeat"] = ln["at"] or bm.nearest_barbeat(ln["sec"])
        ln.pop("at", None)
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lyrics", type=pathlib.Path, nargs="?", default=ROOT / "lyrics" / "lyrics.md")
    a = ap.parse_args()

    bm = Beatmap.load()
    lines, heads = parse(a.lyrics.read_text())
    lines = interpolate(lines, bm)
    for i, ln in enumerate(lines):
        ln["id"] = f"L{i + 1:03d}"
        ln["sec"] = round(ln["sec"], 4)
        ln["end_sec"] = round(lines[i + 1]["sec"] if i + 1 < len(lines) else min(ln["sec"] + 4, bm.duration), 4)

    # sections: pinned time, else the first lyric line that follows the header
    sections = []
    for j, h in enumerate(heads):
        if h["at"]:
            start = bm.sec(h["at"])
        elif h["index"] < len(lines):
            start = lines[h["index"]]["sec"]
        else:
            start = bm.duration
        sections.append({"name": h["name"], "start_sec": round(start, 4),
                         "start_barbeat": h["at"] or bm.nearest_barbeat(start)})
    for s, nxt in zip(sections, sections[1:]):
        s["end_sec"] = nxt["start_sec"]
    if sections:
        sections[-1]["end_sec"] = round(bm.duration, 4)
        for s in sections:
            s["id"] = re.sub(r"[^a-z0-9]+", "-", s["name"].lower()).strip("-")
            s["dur_sec"] = round(s["end_sec"] - s["start_sec"], 4)
        for ln in lines:
            ln["section"] = next((s["id"] for s in sections
                                  if s["start_sec"] <= ln["sec"] < s["end_sec"]), None)

    save(ROOT / "analysis" / "lyrics.json", {"lines": lines})
    if sections:
        save(ROOT / "shots" / "sections.json", {"sections": sections})
        for s in sections:
            print(f"  {s['start_sec']:7.2f}s  {s['dur_sec']:6.2f}s  {s['name']}")
    n_i = sum(1 for ln in lines if ln.get("interpolated"))
    print(f"  {len(lines)} lines ({n_i} interpolated)")


if __name__ == "__main__":
    main()
