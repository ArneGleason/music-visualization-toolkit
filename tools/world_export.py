#!/usr/bin/env python3
"""
Export the musical substrate as one compact JSON the 3D world can consume.

    python3 tools/world_export.py        ->  world/data.json

Everything the renderer needs and nothing it doesn't: the bar grid, sections
with their archetype attributes, every kick/snare/hat strike, per-stem
envelopes downsampled to 30 Hz, and the word-level lyric timings.

The important field is `bars`. The record's rotation is locked to it — one
revolution per bar — so a downbeat is always at the same angular position and
the whole disc becomes a clock you can read.
"""
from __future__ import annotations

import argparse
import bisect
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save  # noqa: E402
from stage import (ARCHETYPES, DEFAULT_STYLE, PARAM_KEYS, kit_hits,  # noqa: E402
                   short)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rate", type=int, default=30, help="envelope rate in the export")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "world" / "data.json")
    a = ap.parse_args()

    bm = load(ROOT / "analysis" / "beatmap.json")
    env = load(ROOT / "analysis" / "envelopes.json")
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    lyrics = load(ROOT / "analysis" / "lyrics.json")["lines"]
    style_path = ROOT / "shots" / "stage_style.json"
    style = load(style_path) if style_path.exists() else DEFAULT_STYLE

    dur = bm["duration_sec"]
    bars = [{"n": b["bar"], "t": round(b["sec"], 5)} for b in bm["bars"]
            if -0.001 <= b["sec"] <= dur + 4]
    beats = [round(x, 5) for b in bm["bars"] for x in b["beats"]
             if -0.001 <= x <= dur + 1]

    secs = []
    for s in sections:
        name = style.get(s["id"], "drive")
        arch = ARCHETYPES.get(name, ARCHETYPES["drive"])
        secs.append({
            "id": s["id"], "arch": name,
            "t0": round(s["start_sec"], 4), "t1": round(s["end_sec"], 4),
            "tint": list(arch["tint"]),
            **{k: arch[k] for k in PARAM_KEYS},
        })

    kit = next((v for k, v in env["tracks"].items() if "drum" in k.lower()), None)
    hits = kit_hits(kit, env.get("bands", []), env["rate"]) if kit else \
        {"kick": [], "snare": [], "hat": []}
    hits = {k: [[round(t, 4), round(m, 3)] for t, m in v if 0 <= t <= dur]
            for k, v in hits.items()}

    step = max(1, env["rate"] // a.rate)
    stems = {}
    for name, tr in env["tracks"].items():
        rms = tr["rms"][::step]
        vals = sorted(x for x in tr["rms"] if x > 5)
        norm = max(60.0, vals[int(len(vals) * 0.95)] if vals else 700.0)
        stems[short(name)] = {
            "delta": round(tr["delta_sec"], 5),
            "norm": round(norm, 1),
            "rms": rms,
            "bands": {b: v[::step] for b, v in tr.get("bands", {}).items()},
        }

    words = []
    try:
        from stage import word_onsets
        vox = next((v for k, v in env["tracks"].items() if "lead vocal" in k.lower()), None)
        if vox:
            wmap = word_onsets(lyrics, vox, env["rate"], vox["delta_sec"])
            for ln in lyrics:
                for w, wt in wmap.get(ln["id"], []):
                    words.append([round(wt, 4), w])
            words.sort()
    except Exception as e:                                    # noqa: BLE001
        print(f"  words skipped: {e}")

    data = {
        "duration": round(dur, 5),
        "rate": a.rate,
        "bands": env.get("bands", []),
        "bars": bars,
        "beats": beats,
        "sections": secs,
        "hits": hits,
        "stems": stems,
        "lines": [{"t": round(l["sec"], 4), "t1": round(l["end_sec"], 4),
                   "text": l["text"]} for l in lyrics],
        "words": words,
    }
    save(a.out, data)
    kb = a.out.stat().st_size / 1024
    print(f"  {len(bars)} bars · {len(secs)} sections · "
          f"{sum(len(v) for v in hits.values())} strikes · {len(words)} words · {kb:.0f} KB")


if __name__ == "__main__":
    main()
