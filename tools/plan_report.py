#!/usr/bin/env python3
"""
Print the cut structure. What the animatic looks like, as numbers.

    python3 tools/plan_report.py        (or: ./run.sh plan)

One line per section: where it starts, how many cuts, how long each is, and
how that reads in musical terms. Faster than scrubbing a video when you just
want to know whether a rule took effect.
"""
from __future__ import annotations

import collections
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, Beatmap, load  # noqa: E402


def musical(dur, bar_sec, beat_sec):
    """Name a duration musically. Tolerance scales with the value, because a
    fluctuating tempo map makes '2 bars' land anywhere in a ~50ms window."""
    tol = max(0.05, dur * 0.04)
    for n in (1, 2, 3, 4, 6, 8):
        if abs(dur - bar_sec * n) < tol:
            return f"{n} bar" + ("s" if n > 1 else "")
    for n in (1, 2, 3):
        if abs(dur - beat_sec * n) < tol:
            return f"{n} beat" + ("s" if n > 1 else "")
    if abs(dur - beat_sec / 2) < tol:
        return "1/2 beat"
    return f"{dur / beat_sec:.1f} beats"


def main():
    sl = load(ROOT / "shots" / "shotlist.json")
    bm = Beatmap.load()

    def local_bar(sec):
        """Bar and beat length where this shot lives — the tempo map moves."""
        bars = bm.d["bars"]
        cur = bars[0]
        for b in bars:
            if b["sec"] <= sec + 1e-6:
                cur = b
            else:
                nxt = b
                return nxt["sec"] - cur["sec"], (nxt["sec"] - cur["sec"]) / cur["num"]
        beat = cur["beats"][1] - cur["beats"][0]
        return beat * cur["num"], beat

    groups = collections.OrderedDict()
    for s in sl["shots"]:
        groups.setdefault(s["section"], []).append(s)

    print(f"\n  {sl['duration_sec']:.1f}s · {len(sl['shots'])} cuts · "
          f"{len({s.get('setup') or s['id'] for s in sl['shots']})} setups · {sl['fps']}fps\n")
    print(f"  {'section':14s} {'starts':>8s}  {'cuts':>5s}  {'each':>7s}   rhythm")
    print("  " + "-" * 58)
    for name, shots in groups.items():
        durs = sorted(round(s["dur_sec"], 2) for s in shots)
        each = f"{durs[0]:.2f}s" if durs[0] == durs[-1] else f"{durs[0]:.2f}-{durs[-1]:.2f}s"
        names = {musical(s["dur_sec"], *local_bar(s["start_sec"])) for s in shots}
        rhythm = names.pop() if len(names) == 1 else " + ".join(sorted(names)[:3])
        mins, secs = divmod(shots[0]["start_sec"], 60)
        print(f"  {name:14s} {int(mins)}:{secs:05.2f}  {len(shots):5d}  {each:>7s}   {rhythm}")
    print()
    print("  audition one:   ./run.sh section <name>")
    print()


if __name__ == "__main__":
    main()
