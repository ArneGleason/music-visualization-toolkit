#!/usr/bin/env python3
"""
Assemble the cut. Frame-accurate, always full length.

    python3 tools/render.py --out out/animatic.mp4      # slates only
    python3 tools/render.py --out out/v01.mp4           # clips where they exist
    python3 tools/render.py --proxy --out out/v01_p.mp4 # fast 720p check
    python3 tools/render.py --only s012 s013            # audition two shots

Every shot with an assigned clip is trimmed from its in-point to exactly the
frame count the music demands, optionally retimed, and conformed to one
codec/size/fps. Shots with no clip fall back to their slate, so this always
produces a watchable 3.5 minutes -- the cut fills in as footage arrives.

The grade (--grade) is applied uniformly to every source. That matters more
than it sounds: a strong shared look is what makes 30 separately-generated
clips read as one film.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, run, to_frames  # noqa: E402

GRADES = {
    "none": "",
    # gentle filmic: slight lift, warm highlights, mild grain, soft vignette
    "film": ("curves=all='0/0.03 0.5/0.5 1/0.97',"
             "eq=saturation=0.92:contrast=1.06,"
             "noise=alls=6:allf=t+u,vignette=PI/5"),
    # 80s/90s video throwback: chroma smear, scanline softness, warm cast
    "throwback": ("scale=iw/2:ih/2,scale=iw*2:ih*2:flags=neighbor,"
                  "curves=all='0/0.05 0.5/0.52 1/0.95',"
                  "eq=saturation=1.12:contrast=1.04:gamma_r=1.03:gamma_b=0.97,"
                  "noise=alls=10:allf=t+u,vignette=PI/4.5"),
    # 50s Technicolor feature: warm lifted curve, rich saturation, fine
    # grain, and a 2.39:1 letterbox drawn inside the 16:9 frame
    "technicolor": ("curves=r='0/0.02 0.5/0.55 1/1':g='0/0.02 0.5/0.5 1/0.98':b='0/0.04 0.5/0.47 1/0.94',"
                    "eq=saturation=1.28:contrast=1.07,"
                    "noise=alls=7:allf=t+u,vignette=PI/5.2,"
                    "drawbox=y=0:w=iw:h=ih*0.128:color=black:t=fill,"
                    "drawbox=y=ih*0.872:w=iw:h=ih*0.128:color=black:t=fill"),
}


def seg_filter(w, h, fps, speed, grade):
    f = []
    if speed and abs(speed - 1.0) > 1e-6:
        f.append(f"setpts={1/speed:.6f}*PTS")
    f.append(f"scale={w}:{h}:force_original_aspect_ratio=increase")
    f.append(f"crop={w}:{h}")
    if GRADES.get(grade):
        f.append(GRADES[grade])
    f.append(f"fps={fps}")
    f.append("setsar=1")
    return ",".join(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "out" / "cut.mp4")
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--proxy", action="store_true", help="720p, fast preset")
    ap.add_argument("--grade", choices=sorted(GRADES), default="none")
    ap.add_argument("--only", nargs="*", help="render just these shot ids")
    ap.add_argument("--section", help="render just this section, with its slice of the audio")
    ap.add_argument("--keep", action="store_true", help="keep intermediate segments")
    a = ap.parse_args()

    sl = load(ROOT / "shots" / "shotlist.json")
    fps = sl["fps"]
    w, h = (1280, 720) if a.proxy else (1920, 1080)
    crf, preset = ("26", "veryfast") if a.proxy else ("18", "medium")

    work = ROOT / "build" / "segments"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    shots = sl["shots"]
    if a.section:
        shots = [s for s in shots if s["section"] == a.section]
        if not shots:
            have = sorted({s["section"] for s in sl["shots"]})
            raise SystemExit(f"no section '{a.section}'. have: {', '.join(have)}")
    if a.only:
        shots = [s for s in shots if s["id"] in a.only]
    audio_offset = shots[0]["start_sec"] if (a.section or a.only) else 0.0
    n_clip = n_slate = 0
    listing = []

    for s in shots:
        frames = to_frames(s["dur_sec"], fps)
        dur = frames / fps
        seg = work / f"{s['id']}.mp4"
        clip = s.get("clip") or {}
        src = clip.get("file")
        src_path = (ROOT / src) if src and not pathlib.Path(src).is_absolute() else (pathlib.Path(src) if src else None)

        common = ["-c:v", "libx264", "-preset", preset, "-crf", crf,
                  "-pix_fmt", "yuv420p", "-r", str(fps), "-an", str(seg)]

        if src_path and src_path.exists():
            speed = clip.get("speed", 1.0) or 1.0
            need = dur * speed  # source seconds consumed
            run(["ffmpeg", "-y", "-ss", f"{clip.get('in_sec', 0.0):.4f}", "-i", str(src_path),
                 "-t", f"{need + 0.5:.4f}",
                 "-vf", seg_filter(w, h, fps, speed, a.grade),
                 "-frames:v", str(frames), *common])
            n_clip += 1
        else:
            slate = ROOT / "build" / "slates" / f"{s['id']}.png"
            if not slate.exists():
                raise SystemExit(f"{s['id']}: no clip and no slate -- run tools/previz.py first")
            vf = f"scale={w}:{h}" + (f",{GRADES[a.grade]}" if False else "") + ",setsar=1"
            run(["ffmpeg", "-y", "-loop", "1", "-i", str(slate), "-t", f"{dur:.4f}",
                 "-vf", vf, "-frames:v", str(frames), *common])
            n_slate += 1
        listing.append(seg)

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p.name}'\n" for p in listing))

    a.out = a.out.resolve()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    # write to a temp file and swap it in: overwriting a file a player has open
    # leaves the player showing a stale (usually black) handle
    tmp_out = a.out.with_name(f".{a.out.stem}.partial{a.out.suffix}")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat)]
    if a.audio.exists():
        cmd += ["-ss", f"{audio_offset:.4f}", "-i", str(a.audio),
                "-c:a", "aac", "-b:a", "256k", "-shortest"]
    cmd += ["-c:v", "copy", "-movflags", "+faststart", str(tmp_out)]
    run(cmd, cwd=work)
    tmp_out.replace(a.out)

    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)

    total = sum(to_frames(s["dur_sec"], fps) for s in shots) / fps
    print(f"wrote {a.out}   {total:.2f}s   {len(shots)} shots"
          f"   ({n_clip} footage, {n_slate} slate)")
    if n_slate and n_clip:
        pct = 100 * n_clip / (n_clip + n_slate)
        print(f"  {pct:.0f}% shot")


if __name__ == "__main__":
    main()
