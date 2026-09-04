#!/usr/bin/env python3
"""
Build and render the cut in Blender, headless. No browser anywhere.

    python tools/blender_comp.py --proxy --out out/blender_animatic.mp4
    python tools/blender_comp.py --out out/v01_blender.mp4 --lyrics
    python tools/blender_comp.py --overlay-only --out out/overlay/frame_.png

Run as a normal Python script it finds blender.exe and relaunches itself
inside Blender (`blender -b -P tools/blender_comp.py -- <args>`); inside
Blender it builds a Video Sequence Editor scene from the shot list and the
overlay cues and renders it:

  channel 1   the cut: assigned clips trimmed to the exact frame count the
              music demands; otherwise the setup's storyboard still; otherwise
              a slate. Always full length, always frame-accurate.
  channel 2   the master mix (audio/song.wav), muxed into the render.
  channel 3   letterbox (2.39:1 inside 16:9), like the technicolor grade.
  channel 4   beat pulse: one additive white strip whose opacity is keyframed
              on every beat from generated/overlay_cues.json - a hard hit on
              downbeats and section starts, a tick on the other beats.
  channel 5+  lyric captions (--lyrics): one text strip per lyric line, on and
              off on the register's frames, coloured per twin.

The music elements are the point: they land on the register's frames because
the cues were rounded from the same grid the shot list was cut on. Everything
here is data-driven so the next elements (rings, ribbons, drum-wall geometry)
can be added as functions that read the same cue file. --overlay-only renders
channels 3+ over a transparent background as a PNG sequence with alpha, for
compositing over footage rendered elsewhere.

Inputs: shots/shotlist.json, generated/overlay_cues.json (tools/overlay_cues.py),
audio/song.wav, board/frames/<setup>_<variant>.jpg.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

BLENDER_CANDIDATES = [
    os.environ.get("BLENDER", ""),
    r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
    "/Applications/Blender.app/Contents/MacOS/Blender",
    "blender",
]


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="out/blender_animatic.mp4",
                    help="output file; .mp4 for a movie, or a PNG path with a frame_ stem for a sequence")
    ap.add_argument("--proxy", action="store_true", help="1280x720 instead of 1920x1080")
    ap.add_argument("--lyrics", action="store_true", help="add lyric captions")
    ap.add_argument("--overlay-only", action="store_true",
                    help="no footage/audio: render the overlay channels over transparency as PNG+alpha")
    ap.add_argument("--start", type=int, default=None, help="first output frame (0-based), for auditions")
    ap.add_argument("--end", type=int, default=None, help="last output frame (0-based, inclusive)")
    ap.add_argument("--save-blend", default=None, help="also save the .blend for hand tweaking")
    ap.add_argument("--variant-order", default="f,e,d,c,b,a",
                    help="which still variant to prefer per setup when several exist")
    ap.add_argument("--favorites", default=None,
                    help="owner's A/B picks (codex/out/still_favorites.md); a listed setup uses that file")
    ap.add_argument("--letterbox", action="store_true",
                    help="draw 2.39:1 letterbox bars over the frame (off by default: they cropped heads)")
    return ap


# ----------------------------------------------------------------------------
# launcher (plain Python)
# ----------------------------------------------------------------------------
def launch(argv):
    exe = next((c for c in BLENDER_CANDIDATES if c and (pathlib.Path(c).exists() or c == "blender")), None)
    if not exe:
        sys.exit("blender.exe not found; set BLENDER=<path to blender.exe>")
    cmd = [exe, "-b", "--python-exit-code", "1", "-P", str(pathlib.Path(__file__).resolve()), "--", *argv]
    print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
    r = subprocess.run(cmd)
    sys.exit(r.returncode)


# ----------------------------------------------------------------------------
# inside Blender
# ----------------------------------------------------------------------------
def inside_blender(argv):
    import json
    import bpy

    a = build_parser().parse_args(argv)
    cues = json.loads((ROOT / "generated" / "overlay_cues.json").read_text(encoding="utf-8"))
    shotlist = json.loads((ROOT / "shots" / "shotlist.json").read_text(encoding="utf-8"))
    fps = cues["fps"]
    W, H = (1280, 720) if a.proxy else (1920, 1080)
    total = cues["frames"]
    f0 = a.start or 0
    f1 = a.end if a.end is not None else total - 1
    B = lambda f: f + 1  # cue frames are 0-based, Blender frames start at 1

    sc = bpy.context.scene
    sc.name = "RiversOfMars"
    sc.render.fps = int(round(fps)); sc.render.fps_base = 1.0
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = 100
    sc.frame_start, sc.frame_end = B(f0), B(f1)
    se = sc.sequence_editor_create()
    strips = se.strips
    variant_order = [v.strip() for v in a.variant_order.split(",") if v.strip()]

    # ---- channel 1: the cut ------------------------------------------------
    frames_dir = ROOT / "board" / "frames"
    stills_by_setup = {}
    for p in sorted(frames_dir.glob("*.jpg")) + sorted(frames_dir.glob("*.png")):
        key = re.sub(r"_(\d+|[a-z])$", "", p.stem)
        stills_by_setup.setdefault(key, []).append(p)

    # owner's A/B picks (codex/out/still_favorites.md): "| n | `setup` | slate | A | `out/file.jpg` |"
    favorites = {}
    if a.favorites:
        fav_path = pathlib.Path(a.favorites)
        for m in re.finditer(r"^\|\s*\d+\s*\|\s*`([\w-]+)`\s*\|[^|]*\|\s*([AB])\s*\|\s*`([^`]+)`", fav_path.read_text(encoding="utf-8"), re.M):
            f = (fav_path.parent / m.group(3)).resolve()
            if f.exists():
                favorites[m.group(1)] = f

    def pick_still(setup):
        if setup in favorites:
            return favorites[setup]
        cands = stills_by_setup.get(setup or "", [])
        if not cands:
            return None
        rank = {v: i for i, v in enumerate(variant_order)}
        return sorted(cands, key=lambda p: rank.get(p.stem.rsplit("_", 1)[-1], 99))[0]

    def fit(strip, iw, ih):
        s = min(W / iw, H / ih) if iw and ih else 1.0
        strip.transform.scale_x = strip.transform.scale_y = s

    n_clip = n_still = n_slate = 0
    if not a.overlay_only:
        for shot in cues["shots"]:
            fs, fe = shot["start"], shot["end"]
            if fe <= f0 or fs > f1:
                continue
            length = fe - fs
            src = next((s for s in shotlist["shots"] if s["id"] == shot["id"]), {})
            clip = (src.get("clip") or {}).get("file")
            name = f"{shot['id']}_{shot['setup']}"
            if clip and (ROOT / clip).exists():
                st = strips.new_movie(name=name, filepath=str(ROOT / clip), channel=1, frame_start=B(fs))
                in_f = int(round(float((src.get("clip") or {}).get("in_sec") or 0.0) * fps))
                st.frame_offset_start = in_f
                st.frame_final_duration = length
                st.frame_start = B(fs) - in_f
                fit(st, st.elements[0].orig_width if st.elements else W, st.elements[0].orig_height if st.elements else H)
                n_clip += 1
                continue
            still = pick_still(shot["setup"])
            if still:
                st = strips.new_image(name=name, filepath=str(still), channel=1, frame_start=B(fs))
                st.frame_final_duration = length
                el = st.elements[0]
                fit(st, el.orig_width, el.orig_height)
                n_still += 1
            else:
                col = strips.new_effect(name=name, type='COLOR', channel=1, frame_start=B(fs), length=length)
                col.color = (0.08, 0.09, 0.12)
                txt = strips.new_effect(name=name + "_slate", type='TEXT', channel=6, frame_start=B(fs), length=length)
                txt.text = f"{shot['id']}  {shot['setup'] or ''}\n{shot.get('lyric') or ''}"
                txt.font_size = int(H * 0.045); txt.location = (0.5, 0.5); txt.wrap_width = 0.9
                txt.color = (0.85, 0.87, 0.9, 1.0)
                n_slate += 1

        # ---- channel 2: audio ----------------------------------------------
        wav = ROOT / "audio" / "song.wav"
        if wav.exists():
            strips.new_sound(name="master", filepath=str(wav), channel=2, frame_start=B(0))

    # ---- channel 3: letterbox (opt-in: the bars cover the top and bottom of a
    # 16:9 still, which took the heads off the standing shots) ----------------
    bar_h = round(H * 0.128)
    for i, y in enumerate((H / 2 - bar_h / 2, -(H / 2 - bar_h / 2)) if a.letterbox else ()):
        bar = strips.new_effect(name=f"letterbox_{i}", type='COLOR', channel=3, frame_start=B(f0), length=f1 - f0 + 1)
        bar.color = (0, 0, 0)
        bar.transform.scale_y = bar_h / H
        bar.transform.offset_y = y
        bar.blend_type = 'ALPHA_OVER'

    # ---- channel 4: beat pulse ---------------------------------------------
    pulse = strips.new_effect(name="beat_pulse", type='COLOR', channel=4, frame_start=B(f0), length=f1 - f0 + 1)
    pulse.color = (1.0, 0.96, 0.88)
    pulse.blend_type = 'ADD'
    section_frames = {s["frame"] for s in cues["sections"]}

    def key(strip, path, frame, value):
        setattr(strip, path, value)
        strip.keyframe_insert(data_path=path, frame=frame)

    key(pulse, "blend_alpha", B(f0), 0.0)
    for b in cues["beats"]:
        f = b["frame"]
        if f < f0 or f > f1:
            continue
        if f in section_frames:
            peak, decay = 0.55, 8
        elif b["downbeat"]:
            peak, decay = 0.30, 6
        else:
            peak, decay = 0.12, 4
        key(pulse, "blend_alpha", B(f) - 1, 0.0)
        key(pulse, "blend_alpha", B(f), peak)
        key(pulse, "blend_alpha", B(f) + decay, 0.0)

    # ---- channel 5+: lyric captions -------------------------------------------
    if a.lyrics:
        colors = {"Them 1": (1.0, 0.80, 0.35, 1.0), "Them 2": (0.55, 0.92, 1.0, 1.0)}
        for i, ly in enumerate(cues["lyrics"]):
            on, off = ly["on"], max(ly["off"], ly["on"] + 6)
            if off <= f0 or on > f1:
                continue
            t = strips.new_effect(name=f"lyr_{ly['id']}", type='TEXT', channel=5 + (i % 2),
                                  frame_start=B(on), length=off - on)
            t.text = ly["text"]
            t.font_size = int(H * 0.04)
            t.location = (0.5, 0.075)
            t.wrap_width = 0.8
            t.color = colors.get(ly["speaker"], (1, 1, 1, 1))
            t.use_shadow = True; t.shadow_color = (0, 0, 0, 0.8)
            t.blend_type = 'ALPHA_OVER'
            key(t, "blend_alpha", B(on), 0.0)
            key(t, "blend_alpha", B(on) + 3, 1.0)
            key(t, "blend_alpha", B(off) - 5, 1.0)
            key(t, "blend_alpha", B(off) - 1, 0.0)

    # linear interpolation for every keyframe we planted (no bezier overshoot)
    ad = sc.animation_data
    if ad and ad.action:
        act = ad.action
        fcurves = []
        if hasattr(act, "fcurves"):            # Blender < 4.4
            fcurves = list(act.fcurves)
        else:                                   # layered actions (4.4+)
            for layer in act.layers:
                for astrip in layer.strips:
                    for cb in astrip.channelbags:
                        fcurves.extend(cb.fcurves)
        for fc in fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'

    # ---- output ---------------------------------------------------------------
    out = pathlib.Path(a.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    r = sc.render
    r.engine = 'BLENDER_EEVEE'
    r.use_sequencer = True
    if a.overlay_only or out.suffix.lower() == ".png":
        r.film_transparent = True
        r.image_settings.file_format = 'PNG'
        r.image_settings.color_mode = 'RGBA'
        r.filepath = str(out.with_suffix(""))  # Blender appends the frame number
    else:
        if hasattr(r.image_settings, "media_type"):   # Blender 5: video is a media type
            r.image_settings.media_type = 'VIDEO'
        r.image_settings.file_format = 'FFMPEG'
        r.ffmpeg.format = 'MPEG4'
        r.ffmpeg.codec = 'H264'
        r.ffmpeg.constant_rate_factor = 'HIGH'
        r.ffmpeg.audio_codec = 'AAC'
        r.ffmpeg.audio_bitrate = 256
        r.filepath = str(out)
    if a.save_blend:
        bp = pathlib.Path(a.save_blend)
        bp = bp if bp.is_absolute() else ROOT / bp
        bp.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(bp))

    print(f"[blender_comp] {W}x{H} @ {fps:g} fps, frames {sc.frame_start}-{sc.frame_end} "
          f"({sc.frame_end - sc.frame_start + 1}); cut: {n_clip} clips, {n_still} stills, {n_slate} slates; "
          f"{len(cues['beats'])} beats, lyrics={'on' if a.lyrics else 'off'}")
    bpy.ops.render.render(animation=True)
    print(f"[blender_comp] wrote {r.filepath}")


if __name__ == "__main__":
    if "--" in sys.argv:
        inside_blender(sys.argv[sys.argv.index("--") + 1:])
    else:
        try:
            import bpy  # noqa: F401  (inside Blender with no args)
            inside_blender([])
        except ImportError:
            launch(sys.argv[1:])
