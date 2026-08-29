#!/usr/bin/env python3
"""Render the approved storyboard frames as a frame-accurate audio animatic.

    ./.venv/bin/python3 tools/storyboard_animatic.py
    ./.venv/bin/python3 tools/storyboard_animatic.py --section recap

This is a review artifact, not a replacement for the canonical cut renderer.
The picture order and start times come from the generated storyboard shot score
(`world/shots.json`); project fps and total duration come from
`shots/shotlist.json`. Every boundary is quantised with ``to_frames``.

Two section boundaries currently contain sub-second gaps where the storyboard
planner discarded an undersized sliver. The preceding board frame deliberately
holds through those gaps, so the preview remains continuous instead of flashing
black or inventing an extra shot.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, run, to_frames  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path,
                    default=ROOT / "out" / "storyboard_animatic.mp4")
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--section", help="render only one storyboard section")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--keep", action="store_true", help="keep disposable segments")
    a = ap.parse_args()

    if a.width < 320 or a.width % 2:
        raise SystemExit("--width must be an even number at least 320")
    if not a.audio.exists():
        raise SystemExit(f"audio not found: {a.audio}")

    score = load(ROOT / "world" / "shots.json")
    canonical = load(ROOT / "shots" / "shotlist.json")
    fps = canonical["fps"]
    duration = canonical["duration_sec"]
    all_shots = score["shots"]
    shots = [s for s in all_shots if not a.section or s["section"] == a.section]
    if not shots:
        have = ", ".join(sorted({s["section"] for s in all_shots}))
        raise SystemExit(f"no section '{a.section}'. have: {have}")

    first_index = all_shots.index(shots[0])
    last_index = all_shots.index(shots[-1])
    start_frame = to_frames(shots[0]["t0"], fps)
    if last_index + 1 < len(all_shots):
        end_frame = to_frames(all_shots[last_index + 1]["t0"], fps)
    else:
        end_frame = to_frames(duration, fps)

    # Hold each image until the next storyboard image begins. This matches its
    # authored start time and covers the two deliberately omitted short slivers.
    entries = []
    extended = []
    for i, shot in enumerate(shots):
        absolute_i = first_index + i
        sf = to_frames(shot["t0"], fps)
        if absolute_i + 1 < len(all_shots) and i + 1 < len(shots):
            ef = to_frames(all_shots[absolute_i + 1]["t0"], fps)
        else:
            ef = end_frame
        frames = ef - sf
        if frames <= 0:
            raise SystemExit(f"{shot['id']}: non-positive duration after frame quantisation")
        expected_end = to_frames(shot["t1"], fps)
        if ef > expected_end:
            extended.append((shot["id"], ef - expected_end))
        image = ROOT / "board" / "frames" / f"{shot['id']}.png"
        if not image.exists():
            raise SystemExit(f"{shot['id']}: missing storyboard image {image}")
        entries.append((shot, image, frames))

    work = ROOT / "build" / "storyboard_segments"
    if work.is_symlink():
        raise SystemExit(f"refusing to replace symlinked work directory: {work}")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    w = a.width
    h = int(w * 9 / 16) // 2 * 2
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
    segments = []
    for n, (shot, image, frames) in enumerate(entries, 1):
        seg = work / f"{shot['id']}.mp4"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-loop", "1", "-framerate", str(fps), "-i", str(image),
             "-vf", vf, "-frames:v", str(frames), "-an",
             "-c:v", "libx264", "-preset", "ultrafast", "-crf", "25",
             "-pix_fmt", "yuv420p", "-r", str(fps), str(seg)])
        segments.append(seg)
        if n % 10 == 0 or n == len(entries):
            print(f"  conformed {n:2d}/{len(entries)} frames")

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p.name}'\n" for p in segments))

    a.out = a.out.resolve()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = a.out.with_name(f".{a.out.stem}.partial{a.out.suffix}")
    total_frames = end_frame - start_frame
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", str(concat),
           "-ss", f"{start_frame / fps:.6f}", "-i", str(a.audio),
           "-map", "0:v:0", "-map", "1:a:0", "-t", f"{total_frames / fps:.6f}",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
           "-movflags", "+faststart", str(tmp)]
    run(cmd, cwd=work)
    tmp.replace(a.out)

    if not a.keep:
        shutil.rmtree(work)

    print(f"wrote {a.out}   {total_frames} frames / {total_frames / fps:.2f}s"
          f"   {len(entries)} storyboard images @ {fps}fps")
    if extended:
        detail = ", ".join(f"{sid} +{n}f" for sid, n in extended)
        print(f"  held across omitted short planner gaps: {detail}")


if __name__ == "__main__":
    main()
