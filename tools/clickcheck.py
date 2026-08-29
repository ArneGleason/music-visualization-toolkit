#!/usr/bin/env python3
"""
Verify the MIDI grid actually lines up with the audio.

    python3 tools/clickcheck.py            # whole song
    python3 tools/clickcheck.py --bars 1 8 # just bars 1-8

Renders a click on every downbeat (high) and beat (low) from beatmap.json,
mixes it under the audio, and writes build/clickcheck.wav. Listen to the
top, middle and end. If the click stays locked, the grid is trustworthy and
everything downstream is frame-accurate. If it drifts, fix it now -- the
usual cause is Bitwig's project tempo not exactly matching the Suno-derived
audio, and the fix is a tempo map or a warp marker in the DAW.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import struct
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, Beatmap, run  # noqa: E402

SR = 48000


def click(freq: float, ms: int = 28, amp: float = 0.75):
    n = int(SR * ms / 1000)
    return [amp * math.sin(2 * math.pi * freq * i / SR) * math.exp(-6.0 * i / n)
            for i in range(n)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--bars", nargs=2, type=int, metavar=("FIRST", "LAST"))
    ap.add_argument("--gain", type=float, default=0.55, help="click level vs music")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "build" / "clickcheck.wav")
    a = ap.parse_args()

    bm = Beatmap.load()
    lo, hi = click(1000.0), click(2000.0)
    total = int((bm.duration + 2) * SR)
    buf = [0.0] * total

    n_hits = 0
    for bar in bm.d["bars"]:
        if a.bars and not (a.bars[0] <= bar["bar"] <= a.bars[1]):
            continue
        for i, t in enumerate(bar["beats"]):
            src = hi if i == 0 else lo
            off = int(t * SR)
            if off + len(src) >= total:
                continue
            for k, s in enumerate(src):
                buf[off + k] += s * a.gain
            n_hits += 1

    tmp = a.out.parent / "_click.wav"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in buf))

    if a.audio.exists():
        run(["ffmpeg", "-y", "-i", str(a.audio), "-i", str(tmp),
             "-filter_complex", "[0:a]volume=0.8[m];[1:a]volume=1.0[c];[m][c]amix=inputs=2:duration=first:normalize=0",
             "-c:a", "pcm_s16le", str(a.out)])
        tmp.unlink()
        print(f"wrote {a.out}  ({n_hits} clicks over the mix)")
    else:
        tmp.rename(a.out)
        print(f"wrote {a.out}  (click only -- no audio at {a.audio})")
    print("Listen at the start, the middle and the last chorus. Drift shows up at the end first.")


if __name__ == "__main__":
    main()
