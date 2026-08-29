#!/usr/bin/env python3
"""
Render a slate for every shot -- the animatic.

    python3 tools/previz.py && python3 tools/render.py --out out/animatic.mp4

Each slate carries the shot id, section, type/setup, bar.beat, timecode,
duration and the lyric on screen at that moment. Cut to the real audio it
gives you 3.5 minutes of the actual edit rhythm for zero credits. Watch it
twice before you generate a single clip: pacing problems are obvious here
and invisible in a spreadsheet.

Slates also act as the fallback in render.py, so you always have a
full-length watchable cut while footage trickles in.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402

FONTS = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
PALETTE = {
    "performance": (26, 22, 34),
    "concept": (18, 28, 30),
    "insert": (32, 26, 18),
}


def font(kind, size):
    p = FONTS[kind]
    return ImageFont.truetype(p, size) if pathlib.Path(p).exists() else ImageFont.load_default(size)


def tc(sec, fps):
    f = int(round(sec * fps))
    return f"{f // (60 * int(fps)):02d}:{(f // int(fps)) % 60:02d}:{f % int(fps):02d}"


def slate(shot, fps, size=(1920, 1080)):
    w, h = size
    img = Image.new("RGB", size, PALETTE.get(shot["type"], (24, 24, 24)))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, w, 8], fill=(190, 170, 120))
    d.text((70, 60), shot["id"].upper(), font=font("bold", 92), fill=(235, 232, 226))
    d.text((70, 172), f"{shot['section']}  ·  {shot['type']}"
           + (f"  ·  {shot['setup']}" if shot.get("setup") else ""),
           font=font("reg", 40), fill=(150, 160, 165))

    right = f"{tc(shot['start_sec'], fps)} → {tc(shot['end_sec'], fps)}"
    d.text((w - 70, 70), right, font=font("mono", 44), fill=(150, 160, 165), anchor="ra")
    d.text((w - 70, 130), f"bar {shot['start_barbeat']}   {shot['dur_sec']:.2f}s   {shot['frames']}f",
           font=font("mono", 36), fill=(120, 128, 132), anchor="ra")

    y = 400
    if shot.get("lyric"):
        for line in textwrap.wrap(shot["lyric"], 42)[:4]:
            d.text((70, y), line, font=font("bold", 66), fill=(240, 236, 228))
            y += 86
    else:
        d.text((70, y), "(instrumental)", font=font("reg", 54), fill=(110, 116, 120))
        y += 86

    if shot.get("description"):
        y = max(y + 40, 760)
        for line in textwrap.wrap(shot["description"], 78)[:3]:
            d.text((70, y), line, font=font("reg", 36), fill=(168, 176, 180))
            y += 50

    if not shot.get("clip", {}).get("file"):
        d.text((70, h - 80), "NO FOOTAGE", font=font("bold", 34), fill=(200, 96, 80))
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--width", type=int, default=1920)
    a = ap.parse_args()

    sl = load(ROOT / "shots" / "shotlist.json")
    fps = sl["fps"]
    outdir = ROOT / "build" / "slates"
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.png"):
        old.unlink()
    size = (a.width, int(a.width * 9 / 16))
    for shot in sl["shots"]:
        slate(shot, fps, size).save(outdir / f"{shot['id']}.png")
    print(f"wrote {len(sl['shots'])} slates to {outdir}")
    print("next: python3 tools/render.py --out out/animatic.mp4")


if __name__ == "__main__":
    main()
