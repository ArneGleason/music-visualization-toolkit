#!/usr/bin/env python3
"""
Render the animatic as a live HUD — beat-accurate, updated every frame.

    ./run.sh                      whole song
    ./run.sh section final-chorus  one section

The static slates in previz.py show a shot's lyric from the moment the shot
starts, which can be two bars before the line is actually sung. That reads as
the visuals anticipating the audio. This renders per-frame instead, so:

  * the lyric appears on the beat it is SUNG, not when its shot begins
  * a 16th-note pip row and a beat flash track the pulse continuously
  * bar.beat.16th counts up live, so you can see the grid against the audio
  * a countdown shows how long until the next cut
  * a timeline strip shows sections, every cut, and the playhead

Frames are piped straight to ffmpeg as raw RGB — nothing hits disk.
"""
from __future__ import annotations

import argparse
import bisect
import pathlib
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402

BG = (14, 15, 18)
INK = (240, 238, 232)
DIM = (108, 116, 124)
MID = (162, 170, 178)
ACCENT = (228, 186, 108)
HOT = (232, 108, 84)
SECTION_HUES = [(96, 132, 148), (150, 118, 152), (128, 148, 108), (176, 132, 96),
                (110, 140, 168), (156, 112, 112), (120, 154, 140), (168, 152, 100)]

# Font resolution has to survive macOS, Linux, and whatever Pillow is installed.
# Tried in order; first one that actually loads wins. Never fatal.
CANDIDATES = {
    "bold": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "reg": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "mono": [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ],
}

_cache = {}
_resolved = {}


def _default(size):
    try:
        return ImageFont.load_default(size)      # Pillow >= 10.1
    except TypeError:
        return ImageFont.load_default()


def font(kind, size):
    key = (kind, size)
    if key in _cache:
        return _cache[key]
    size = max(1, int(size))
    for path in CANDIDATES[kind]:
        if not pathlib.Path(path).exists():
            continue
        try:
            f = ImageFont.truetype(path, size)
        except Exception:
            continue
        _resolved.setdefault(kind, path)
        _cache[key] = f
        return f
    _resolved.setdefault(kind, "(Pillow default — text will look rough)")
    _cache[key] = _default(size)
    return _cache[key]


def report_fonts():
    for kind in ("bold", "reg", "mono"):
        font(kind, 24)
    for kind, path in _resolved.items():
        print(f"  font {kind:5s} {path}")


def tc(sec, fps):
    f = max(0, int(round(sec * fps)))
    return f"{f // (60 * int(fps)):02d}:{(f // int(fps)) % 60:02d}:{f % int(fps):02d}"


# ------------------------------------------------------------------ grid ----

class Grid:
    """Frame time -> bar / beat / sixteenth, with phase for the pulse."""

    def __init__(self, bars):
        self.bars = bars
        self.starts = [b["sec"] for b in bars]

    def at(self, t):
        i = bisect.bisect_right(self.starts, t) - 1
        i = max(0, min(i, len(self.bars) - 1))
        b = self.bars[i]
        beats = b["beats"]
        nxt = self.bars[i + 1]["sec"] if i + 1 < len(self.bars) else beats[-1] + (beats[-1] - beats[-2])
        edges = beats + [nxt]
        j = bisect.bisect_right(edges, t) - 1
        j = max(0, min(j, len(beats) - 1))
        beat_len = edges[j + 1] - edges[j]
        phase = (t - edges[j]) / beat_len if beat_len > 0 else 0.0
        phase = min(max(phase, 0.0), 0.9999)
        return {"bar": b["bar"], "beat": j + 1, "num": b["num"],
                "sixteenth": int(phase * 4) + 1, "phase": phase,
                "bar_phase": (j + phase) / b["num"], "beat_len": beat_len}


# ------------------------------------------------------------------ draw ----

def draw_frame(base, d, t, g, shot, lyric, nxt_lyric, fps, W, H, s, shot_i, n_shots):
    m = int(60 * s)
    pos = g.at(t)
    decay = (1.0 - pos["phase"]) ** 2.2
    down = pos["beat"] == 1

    # --- pulse: a bright bar top and bottom, biggest on the downbeat --------
    v = decay * (1.0 if down else 0.5)
    col = tuple(int(BG[k] + (ACCENT[k] - BG[k]) * v) for k in range(3))
    d.rectangle([0, 0, W, int(14 * s)], fill=col)
    d.rectangle([0, 0, int(W * v * (1.0 if down else 0.4)), int(14 * s)],
                fill=ACCENT if down else MID)

    # --- top left: which shot (stable, so the eye can ignore it) ------------
    label = f"{shot['id'].upper()}   {shot['section']}"
    if shot.get("setup"):
        label += f"   {shot['setup']}"
    d.text((m, int(46 * s)), label, font=font("bold", int(32 * s)), fill=DIM)

    # --- top right: timecode + live bar.beat.16th ---------------------------
    d.text((W - m, int(40 * s)), tc(t, fps), font=font("mono", int(40 * s)),
           fill=DIM, anchor="ra")
    live = f"{pos['bar']}.{pos['beat']}.{pos['sixteenth']}"
    d.text((W - m, int(90 * s)), live, font=font("mono", int(62 * s)),
           fill=ACCENT if down else INK, anchor="ra")

    # --- lyric: appears on the beat it is SUNG ------------------------------
    y = int(250 * s)
    if lyric:
        age = t - lyric["sec"]
        fade = min(1.0, max(0.0, age) / 0.10)
        c = tuple(int(BG[k] + (INK[k] - BG[k]) * fade) for k in range(3))
        for line in textwrap.wrap(lyric["text"], 32)[:3]:
            d.text((m, y), line, font=font("bold", int(80 * s)), fill=c)
            y += int(100 * s)
    else:
        y += int(100 * s)
    if nxt_lyric:
        beats_away = (nxt_lyric["sec"] - t) / max(pos["beat_len"], 1e-6)
        d.text((m, y + int(16 * s)),
               textwrap.shorten(nxt_lyric["text"], 44, placeholder="\u2026"),
               font=font("reg", int(34 * s)), fill=(84, 90, 96))
        d.text((m, y + int(66 * s)), f"in {beats_away:.1f} beats",
               font=font("mono", int(26 * s)), fill=(62, 68, 74))

    # --- THE PULSE: big beat discs, 16th ticks between them -----------------
    n = pos["num"]
    cy = H - int(250 * s)
    span = W - 2 * m
    r_big = int(30 * s)
    # inset by one radius so beat 1 and the last 16th both fit, and so the
    # playhead below lines up exactly with the disc it is passing
    x0 = m + r_big
    usable = span - 2 * r_big
    step = usable / n
    for k in range(n):
        cx = x0 + step * k
        is_now = (k + 1) == pos["beat"]
        is_one = k == 0
        r = r_big + int(14 * s * decay) if is_now else r_big
        if is_now:
            fill = ACCENT if is_one else INK
        else:
            fill = (46, 50, 56) if not is_one else (70, 62, 48)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
        d.text((cx, cy), str(k + 1), font=font("bold", int(30 * s)),
               fill=BG if is_now else (96, 102, 108), anchor="mm")
        # three 16th ticks after this beat
        for q in range(1, 4):
            tx = cx + step * q / 4
            lit = is_now and pos["sixteenth"] == q + 1
            h = int((20 if lit else 11) * s)
            d.rectangle([tx - int(4 * s), cy - h, tx + int(4 * s), cy + h],
                        fill=INK if lit else (40, 44, 50))

    # --- playhead sweeping the bar ------------------------------------------
    ly = cy + int(62 * s)
    d.rectangle([x0, ly, x0 + usable, ly + int(3 * s)], fill=(34, 38, 44))
    px = x0 + usable * pos["bar_phase"]
    d.rectangle([px - int(2 * s), ly - int(10 * s), px + int(2 * s), ly + int(13 * s)],
                fill=ACCENT)

    # --- cut countdown -------------------------------------------------------
    iy = H - int(140 * s)
    left = shot["end_sec"] - t
    d.text((m, iy), f"cut in {left:4.2f}s",
           font=font("mono", int(34 * s)), fill=HOT if left < 0.35 else MID)
    d.text((W - m, iy), f"shot {shot_i + 1}/{n_shots}   {shot['dur_sec']:.2f}s",
           font=font("mono", int(30 * s)), fill=DIM, anchor="ra")
    by = H - int(94 * s)
    prog = (t - shot["start_sec"]) / max(shot["dur_sec"], 1e-6)
    d.rectangle([m, by, W - m, by + int(9 * s)], fill=(32, 36, 42))
    d.rectangle([m, by, m + span * min(prog, 1.0), by + int(9 * s)],
                fill=HOT if left < 0.35 else MID)
    return base


def build_static(shots, sections, duration, W, H, s):
    """The timeline strip at the very bottom — same every frame, so draw once."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    ty = H - int(56 * s)
    th = int(20 * s)
    span = W - 2 * int(60 * s)
    m = int(60 * s)
    for i, sec in enumerate(sections):
        x0 = m + span * sec["start_sec"] / duration
        x1 = m + span * sec["end_sec"] / duration
        d.rectangle([x0, ty, x1 - 1, ty + th], fill=SECTION_HUES[i % len(SECTION_HUES)])
        nm = sec["id"].replace("-", " ")
        if x1 - x0 > len(nm) * 7 * s:
            d.text(((x0 + x1) / 2, ty + th / 2), nm, font=font("reg", int(16 * s)),
                   fill=(18, 20, 22), anchor="mm")
    for sh in shots:
        x = m + span * sh["start_sec"] / duration
        d.rectangle([x, ty - int(6 * s), x + max(1, s), ty], fill=(70, 76, 82))
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "out" / "animatic.mp4")
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--section", help="render just this section")
    ap.add_argument("--width", type=int, default=1280)
    a = ap.parse_args()

    report_fonts()
    sl = load(ROOT / "shots" / "shotlist.json")
    bm = load(ROOT / "analysis" / "beatmap.json")
    lyrics = load(ROOT / "analysis" / "lyrics.json")["lines"]
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    fps = sl["fps"]
    g = Grid(bm["bars"])

    shots = sl["shots"]
    if a.section:
        shots = [x for x in shots if x["section"] == a.section]
        if not shots:
            raise SystemExit(f"no section '{a.section}'. have: "
                             + ", ".join(sorted({x['section'] for x in sl['shots']})))
    t0 = shots[0]["start_sec"]
    t1 = shots[-1]["end_sec"]

    W = a.width
    H = int(W * 9 / 16) // 2 * 2
    s = W / 1920

    static = build_static(sl["shots"], sections, sl["duration_sec"], W, H, s)
    lyr_times = [l["sec"] for l in lyrics]
    shot_starts = [x["start_sec"] for x in shots]

    a.out = a.out.resolve()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = a.out.with_name(f".{a.out.stem}.partial{a.out.suffix}")

    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if a.audio.exists():
        cmd += ["-ss", f"{t0:.4f}", "-i", str(a.audio), "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    n = int(round((t1 - t0) * fps))
    for f in range(n):
        t = t0 + f / fps
        si = max(0, bisect.bisect_right(shot_starts, t) - 1)
        shot = shots[si]
        li = bisect.bisect_right(lyr_times, t) - 1
        cur = lyrics[li] if li >= 0 and t < lyrics[li]["end_sec"] else None
        ni = bisect.bisect_right(lyr_times, t)
        nxt = lyrics[ni] if ni < len(lyrics) else None

        img = static.copy()
        d = ImageDraw.Draw(img)
        draw_frame(img, d, t, g, shot, cur, nxt, fps, W, H, s, si, len(shots))
        proc.stdin.write(img.tobytes())
        if f % (fps * 15) == 0:
            print(f"\r  {t - t0:6.1f}s / {t1 - t0:.1f}s", end="", flush=True)

    proc.stdin.close()
    err = proc.stderr.read().decode()[-1500:]
    if proc.wait() != 0:
        print("\n" + err)
        raise SystemExit("ffmpeg failed")
    tmp.replace(a.out)
    print(f"\rwrote {a.out}   {(t1 - t0):.2f}s   {n} frames   {len(shots)} shots")


if __name__ == "__main__":
    main()
