#!/usr/bin/env python3
"""
Import a Bitwig DAWproject export: exact tempo grid, markers, lyrics, sections.

    python3 tools/dawproject.py source/Song.dawproject

Replaces beatmap.py for projects that have a real tempo map. Writes
analysis/beatmap.json, lyrics/lyrics.md (all markers pinned to bar.beat) and
shots/sections.json.

Why this exists: a Standard MIDI File's set_tempo is a STEP function. There is
no linear tempo ramp in the MIDI spec, so a DAW with genuine tempo automation
either subdivides it into many small steps on export or silently flattens it.
DAWproject stores the automation as it really is — points with an interpolation
mode and `timeUnit="beats"` — so we can integrate it exactly.

For BPM varying linearly against beat position from T0 at b0 to T1 at b1:

    t = 60 * (b1 - b0) * ln(T1 / T0) / (T1 - T0)          [T0 != T1]
    t = 60 * (b1 - b0) / T0                               [T0 == T1]

No stepping, no accumulated error. `--compare` shows you what the naive
approaches would have cost.
"""
from __future__ import annotations

import argparse
import collections
import math
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, save, run  # noqa: E402

BRACKET = re.compile(r"<\s*([^<>]+?)\s*>")
IGNORE_NAMES = {"untitled", ""}


# ------------------------------------------------------------- tempo curve ---

class TempoCurve:
    """Exact beats <-> seconds for a piecewise tempo automation curve."""

    def __init__(self, points):
        # points: [(beat, bpm, interpolation)], sorted, duplicates at the same
        # beat collapse to the last one (a DAW writes those as a hard jump)
        pts = []
        for b, v, interp in sorted(points, key=lambda p: p[0]):
            if pts and abs(pts[-1][0] - b) < 1e-9:
                pts[-1] = (b, v, interp)
            else:
                pts.append((b, v, interp))
        self.pts = pts
        self.cum = [0.0]
        for (b0, t0, i0), (b1, t1, _) in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + self._span(b0, t0, b1, t1, i0))

    @staticmethod
    def _span(b0, T0, b1, T1, interp="linear"):
        db = b1 - b0
        if db <= 0:
            return 0.0
        if interp != "linear" or abs(T1 - T0) < 1e-9:
            return 60.0 * db / T0            # hold: constant tempo across the span
        return 60.0 * db * math.log(T1 / T0) / (T1 - T0)

    def _index(self, beat):
        lo, hi = 0, len(self.pts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.pts[mid][0] <= beat:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def sec(self, beat: float) -> float:
        i = self._index(beat)
        b0, T0, interp = self.pts[i]
        if i + 1 < len(self.pts):
            b1, T1, _ = self.pts[i + 1]
            if b1 > b0 and interp == "linear":
                f = (beat - b0) / (b1 - b0)
                return self.cum[i] + self._span(b0, T0, beat, T0 + (T1 - T0) * f, interp)
        return self.cum[i] + 60.0 * (beat - b0) / T0

    def bpm(self, beat: float) -> float:
        i = self._index(beat)
        b0, T0, interp = self.pts[i]
        if i + 1 < len(self.pts) and interp == "linear":
            b1, T1, _ = self.pts[i + 1]
            if b1 > b0:
                return T0 + (T1 - T0) * (beat - b0) / (b1 - b0)
        return T0

    @property
    def last_beat(self):
        return self.pts[-1][0]


# ------------------------------------------------------------------ parsing ---

def read_project_xml(path: pathlib.Path) -> ET.Element:
    if path.suffix == ".dawproject" or zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            return ET.fromstring(z.read("project.xml"))
    return ET.parse(path).getroot()


def parse_tempo(root) -> TempoCurve:
    ta = next(iter(root.iter("TempoAutomation")), None)
    if ta is not None:
        unit = ta.get("timeUnit", "beats")
        if unit != "beats":
            print(f"  !! tempo timeUnit is '{unit}', not 'beats' — grid may be wrong")
        pts = [(float(e.get("time")), float(e.get("value")), e.get("interpolation", "linear"))
               for e in ta if e.tag == "RealPoint"]
        if pts:
            if pts[0][0] > 0:
                pts.insert(0, (0.0, pts[0][1], "linear"))
            return TempoCurve(pts)
    t = next(iter(root.iter("Tempo")), None)
    bpm = float(t.get("value")) if t is not None else 120.0
    print(f"  no tempo automation found — assuming constant {bpm:g} bpm")
    return TempoCurve([(0.0, bpm, "hold"), (1e6, bpm, "hold")])


def parse_meter(root):
    ts = next(iter(root.iter("TimeSignature")), None)
    if ts is None:
        return 4, 4
    return int(ts.get("numerator", 4)), int(ts.get("denominator", 4))


def parse_markers(root):
    """-> [(beat, lyric_text_or_None, structure_label_or_None)] deduped."""
    seen, out = set(), []
    for m in root.iter("Marker"):
        beat = float(m.get("time"))
        raw = (m.get("name") or "").strip()
        labels = [g.strip() for g in BRACKET.findall(raw)]
        text = BRACKET.sub("", raw).strip()
        if text.lower() in IGNORE_NAMES:
            text = ""
        if not text and not labels:
            continue                      # placeholder marker, nothing to say
        key = (round(beat, 6), text, tuple(labels))
        if key in seen:
            continue
        seen.add(key)
        out.append((beat, text or None, labels[0] if labels else None))
    return sorted(out, key=lambda x: x[0])


def find_master(root, hint="master"):
    """Locate the bounced master audio clip on the timeline.

    A master bounce is almost never placed at bar 1 — it starts where the
    music starts, which here is beat 14. Its sample 0 is the video's frame 0,
    so the whole grid has to be zeroed there or every cut lands late by the
    offset.

    The clip is also often TRIMMED shorter than the file it points at, because
    the trailing silence gets pulled back in the arrangement. The timeline is
    the intent; the file just has tail on it. So we return the clip's own
    length in beats and let the caller prefer it over the file duration.

    Returns (track_name, start_beat, wav_path, wav_seconds, clip_beats).
    """
    names = {t.get("id"): (t.get("name") or "") for t in root.iter("Track")}
    parent = {c: p for p in root.iter() for c in p}
    best = None
    for f in root.iter("File"):
        path = f.get("path") or ""
        if not path.lower().endswith((".wav", ".aiff", ".flac")):
            continue
        node, lane_track, clips, audio = f, None, [], None
        while node in parent:
            node = parent[node]
            if node.tag == "Clip":
                clips.append(node)
            elif node.tag == "Audio" and audio is None:
                audio = node
            elif node.tag == "Lanes" and node.get("track") and lane_track is None:
                lane_track = node.get("track")
        tname = names.get(lane_track, "")
        if hint.lower() not in tname.lower():
            continue
        inner = [c for c in clips if c.get("contentTimeUnit") != "seconds"]
        placed = inner[0] if inner else clips[0]
        start = float(placed.get("time", 0) or 0)
        beats = float(placed.get("duration")) if placed.get("duration") else None
        dur = float(audio.get("duration")) if audio is not None and audio.get("duration") else None
        cand = (tname, start, path, dur, beats)
        if best is None or (dur or 0) > (best[3] or 0):
            best = cand
    return best


def parse_notes(root):
    """-> [(absolute_beat, track_name)] — approximate, used only for density."""
    notes = []
    for track in root.iter("Track"):
        name = track.get("name") or "track"
        for clip in track.iter("Clip"):
            base = float(clip.get("time", 0) or 0)
            start = float(clip.get("playStart", 0) or 0)
            for n in clip.iter("Note"):
                notes.append((base + float(n.get("time", 0)) - start, name))
    return notes


# ------------------------------------------------------------------- output ---

def barbeat(beat, num):
    bar = int(beat // num) + 1
    b = beat % num + 1
    if abs(b - round(b)) < 1e-6:
        return f"{bar}.{int(round(b))}"
    whole = int(b)
    frac = round(b - whole, 4)
    return f"{bar}.{whole}.{str(frac).split('.')[1]}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=pathlib.Path)
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--compare", action="store_true", help="show what naive timing would cost")
    ap.add_argument("--no-lyrics", action="store_true", help="don't overwrite lyrics/lyrics.md")
    ap.add_argument("--master-track", default="master",
                    help="substring of the track holding the bounced mix (default: master)")
    ap.add_argument("--zero-at", type=float, default=None,
                    help="beat that is 0:00 in the mix; overrides auto-detection")
    ap.add_argument("--no-zero", action="store_true",
                    help="keep project time; do NOT zero the grid at the mix start")
    a = ap.parse_args()

    root = read_project_xml(a.project)
    curve = parse_tempo(root)
    num, den = parse_meter(root)
    markers = parse_markers(root)
    notes = parse_notes(root)

    master = find_master(root, a.master_track)
    zero_beat = 0.0
    if a.zero_at is not None:
        zero_beat = a.zero_at
    elif master and not a.no_zero:
        zero_beat = master[1]
    zero_sec = curve.sec(zero_beat)

    def sec(beat):
        return curve.sec(beat) - zero_sec

    audio_sec = None
    if a.audio.exists():
        audio_sec = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                               "-of", "csv=p=0", str(a.audio)]).stdout.strip())

    end_beat = curve.last_beat
    end_sec = sec(end_beat)
    file_sec = master[3] if master else None
    # the clip's own extent on the timeline wins over the file length
    clip_sec = sec(master[1] + master[4]) if master and master[4] else None
    master_sec = clip_sec or file_sec
    duration = master_sec or audio_sec or end_sec

    # Bar grid. Bar NUMBERS stay in project terms so bar.beat references from
    # Bitwig still match; only the seconds are zeroed. Bars entirely before
    # the mix start are dropped.
    bars, bar_no, beat = [], 1, 0.0
    while sec(beat) <= duration + 0.5 and bar_no < 4000:
        beats = [round(sec(beat + i), 6) for i in range(num)]
        if beats[-1] >= -1e-6:
            bars.append({"bar": bar_no, "beat": beat, "sec": beats[0],
                         "num": num, "den": den, "beats": beats})
        beat += num
        bar_no += 1
    for _ in range(2):
        beats = [round(sec(beat + i), 6) for i in range(num)]
        bars.append({"bar": bar_no, "beat": beat, "sec": beats[0],
                     "num": num, "den": den, "beats": beats})
        beat += num
        bar_no += 1

    density, tracks = [], collections.Counter()
    per_bar = collections.defaultdict(collections.Counter)
    for nb, tname in notes:
        per_bar[int(nb // num) + 1][tname] += 1
        tracks[tname] += 1
    for bn in sorted(per_bar):
        density.append({"bar": bn, "total": sum(per_bar[bn].values()),
                        "tracks": dict(per_bar[bn])})

    bm = {
        "source_dawproject": str(a.project),
        "source_audio": str(a.audio) if audio_sec else None,
        "ppq": 960,
        "duration_sec": round(duration, 6),
        "project_end_sec": round(end_sec, 6),
        "project_end_beat": end_beat,
        "zero_beat": zero_beat,
        "zero_sec_in_project": round(zero_sec, 6),
        "master_track": master[0] if master else None,
        "master_wav": master[2] if master else None,
        "master_sec": master_sec,
        "master_file_sec": file_sec,
        "master_clip_beats": master[4] if master else None,
        "tempo_map": [{"beat": b, "sec": round(sec(b), 6), "bpm": round(v, 6),
                       "interpolation": i} for b, v, i in curve.pts],
        "time_signatures": [{"beat": zero_beat, "sec": 0.0, "num": num, "den": den}],
        "markers": [{"beat": b, "sec": round(sec(b), 6),
                     "text": t or lbl, "kind": "structure" if lbl and not t else "lyric"}
                    for b, t, lbl in markers],
        "tracks": [{"name": n, "notes": c} for n, c in tracks.most_common()],
        "bars": bars,
        "density": density,
    }
    save(ROOT / "analysis" / "beatmap.json", bm)

    bpms = [v for _, v, _ in curve.pts]
    print(f"  tempo      {min(bpms):.2f} – {max(bpms):.2f} bpm over {len(curve.pts)} points")
    print(f"  meter      {num}/{den}")
    print(f"  bars       {len(bars) - 2}")
    if master:
        print(f"  master     {master[0]!r} at beat {master[1]:g} "
              f"= {zero_sec:.4f}s project time  ->  grid zeroed there")
        print(f"             {master[2]}")
        if clip_sec and file_sec and abs(file_sec - clip_sec) > 0.02:
            print(f"             clip runs {clip_sec:.3f}s on the timeline; "
                  f"the file is {file_sec:.3f}s")
            print(f"             -> trimmed by {file_sec - clip_sec:.3f}s, "
                  f"using the timeline. Video ends at {clip_sec:.3f}s.")
        elif master_sec:
            print(f"             {master_sec:.3f}s")
    elif zero_beat:
        print(f"  zeroed at  beat {zero_beat:g} ({zero_sec:.4f}s project time)")
    else:
        print("  !! no master bounce found on the timeline — grid is in PROJECT time.")
        print("     If your mix starts later than bar 1, every cut will be early by that much.")
    print(f"  timeline   {end_sec:.3f}s to project end (beat {end_beat:g})")
    if audio_sec:
        ref = file_sec or master_sec or end_sec
        print(f"  audio      {audio_sec:.3f}s   ({audio_sec - ref:+.3f}s vs the bounce file)")
        if ref and abs(audio_sec - ref) > 0.05:
            print("             !! audio/song.wav is NOT the bounce on the master track")
    print(f"  markers    {len(markers)}  "
          f"({sum(1 for _, t, _ in markers if t)} lyric, "
          f"{sum(1 for _, t, l in markers if l and not t)} structural)")

    if a.compare:
        # all three measured over the same span: mix start -> project end
        step = sum(60.0 * (min(b1, end_beat) - max(b0, zero_beat)) / T0
                   for (b0, T0, _), (b1, _, _) in zip(curve.pts, curve.pts[1:])
                   if b1 > zero_beat and b0 < end_beat)
        flat = 60.0 * (end_beat - zero_beat) / curve.bpm(zero_beat)
        print(f"\n  over the {end_sec:.1f}s of music, from the mix start:")
        print(f"    exact              {end_sec:9.3f}s")
        print(f"    step (MIDI-style)  {step:9.3f}s   {abs(step - end_sec) * 1000:6.0f} ms off")
        print(f"    fixed {curve.bpm(zero_beat):7.3f} bpm  {flat:9.3f}s   {abs(flat - end_sec) * 1000:6.0f} ms off")

    if not a.no_lyrics:
        out = ["// Generated from the DAWproject markers by tools/dawproject.py",
               "// Every line is pinned to its exact bar.beat. Edit the ## section",
               "// headers to name the real song structure, then run:",
               "//     ./.venv/bin/python3 tools/lyrics.py lyrics/lyrics.md",
               ""]
        for b, text, label in markers:
            bb = barbeat(b, num)
            if label and not text:
                out += ["", f"## {label} @ {bb}"]
            elif label:
                out += [f"[{bb}] {text}", f"//   ^ marker also said: <{label}>"]
            else:
                out.append(f"[{bb}] {text}")
        p = ROOT / "lyrics" / "lyrics.md"
        p.write_text("\n".join(out) + "\n")
        print(f"wrote {p}")
        print("  → edit the ## headers into real sections, then run tools/lyrics.py")


if __name__ == "__main__":
    main()
