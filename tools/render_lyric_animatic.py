#!/usr/bin/env python3
"""Render the full flat-lyric animatic in bounded Blender sections.

Section rendering keeps Blender from holding every animated glyph mesh in one
dependency graph. All keys use absolute song frames, so a phrase crossing a
section boundary is reproduced identically on both sides. The final movie gets
one clean audio encode from the original master rather than concatenated AAC.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(command):
    print(" ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--choreography", default="shots/lyric_motion_full.json")
    ap.add_argument("--favorites", default="shots/still_favorites.md")
    ap.add_argument("--out", default="out/blender_animatic_flat_lyrics_v01.mp4")
    ap.add_argument("--segment-frames", type=int, default=720)
    ap.add_argument("--proxy", action="store_true", default=True)
    ap.add_argument("--allow-clips", action="store_true",
                    help="use assigned motion clips when present; default is a stable all-stills animatic")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    choreography = json.loads((ROOT / args.choreography).read_text(encoding="utf-8"))
    start = int(choreography.get("start", 0))
    end = int(choreography["end"])
    fps = float(choreography["fps"])
    out = ROOT / args.out
    parts_dir = ROOT / "out" / "_lyric_animatic_parts" / out.stem
    parts_dir.mkdir(parents=True, exist_ok=True)
    parts = []

    for index, first in enumerate(range(start, end + 1, args.segment_frames)):
        last = min(end, first + args.segment_frames - 1)
        part = parts_dir / f"part_{index:03d}_{first:05d}_{last:05d}.mp4"
        parts.append(part)
        if part.exists() and part.stat().st_size > 100_000 and not args.force:
            print(f"[segment] reuse {part.relative_to(ROOT)}", flush=True)
            continue
        command = [sys.executable, "tools/blender_comp.py"]
        if args.proxy:
            command.append("--proxy")
        if not args.allow_clips:
            command.append("--stills-only")
        command += [
            "--start", str(first), "--end", str(last),
            "--lyric-flat", args.choreography,
            "--favorites", args.favorites,
            "--out", str(part.relative_to(ROOT)),
        ]
        run(command)

    concat_file = parts_dir / "concat.txt"
    concat_file.write_text("".join(
        f"file '{part.as_posix().replace("'", "'\\''")}'\n" for part in parts),
        encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    frame_count = end - start + 1
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-i", str(ROOT / "audio" / "song.wav"),
         "-map", "0:v:0", "-map", "1:a:0", "-vf",
         f"fps={fps:g},tpad=stop_mode=clone:stop_duration={2.0 / fps:.9f}",
         "-frames:v", str(frame_count), "-c:v", "libx264", "-preset", "medium",
         "-crf", "16", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k",
         "-movflags", "+faststart", str(out)])
    print(f"[lyric_animatic] wrote {out.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
