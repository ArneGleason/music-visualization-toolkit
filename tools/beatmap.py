#!/usr/bin/env python3
"""
Build the timing armature from the Bitwig MIDI export.

    python3 tools/beatmap.py midi/song.mid [--audio audio/song.wav]

Writes analysis/beatmap.json:
  tempo map, time-signature map, a bar/beat -> seconds grid, any markers
  found in the MIDI, per-track note counts, and per-bar note density.

Density is the useful bit for shot planning: it shows you where the
arrangement thickens and thins, which is where cuts want to live.
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import sys

import mido

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, save, run  # noqa: E402


def build(midi_path: pathlib.Path, audio_path: pathlib.Path | None, tail_bars: int = 2) -> dict:
    mid = mido.MidiFile(midi_path)
    ppq = mid.ticks_per_beat

    # --- flatten to absolute ticks -------------------------------------
    tempos, tsigs, markers, notes = [], [], [], []
    track_names = {}
    for ti, track in enumerate(mid.tracks):
        t = 0
        name = None
        for msg in track:
            t += msg.time
            if msg.type == "track_name":
                name = msg.name.strip() or None
                track_names[ti] = name
            elif msg.type == "set_tempo":
                tempos.append((t, msg.tempo))
            elif msg.type == "time_signature":
                tsigs.append((t, msg.numerator, msg.denominator))
            elif msg.type in ("marker", "text", "cue_marker"):
                txt = getattr(msg, "text", "").strip()
                if txt:
                    markers.append((t, txt, msg.type))
            elif msg.type == "note_on" and msg.velocity > 0:
                notes.append((t, msg.note, msg.velocity, ti))
    tempos = sorted(set(tempos)) or [(0, 500000)]
    if tempos[0][0] != 0:
        tempos.insert(0, (0, tempos[0][1]))
    tsigs = sorted(set(tsigs)) or [(0, 4, 4)]
    if tsigs[0][0] != 0:
        tsigs.insert(0, (0, 4, 4))

    # --- tick -> seconds ------------------------------------------------
    anchors = [(0, 0.0, tempos[0][1])]
    for tick, tempo in tempos[1:]:
        ptick, psec, ptempo = anchors[-1]
        anchors.append((tick, psec + (tick - ptick) / ppq * (ptempo / 1e6), tempo))

    def sec(tick: float) -> float:
        a = anchors[0]
        for cand in anchors:
            if cand[0] <= tick:
                a = cand
            else:
                break
        return a[1] + (tick - a[0]) / ppq * (a[2] / 1e6)

    def tsig_at(tick):
        cur = tsigs[0]
        for c in tsigs:
            if c[0] <= tick:
                cur = c
            else:
                break
        return cur[1], cur[2]

    # --- how long? -------------------------------------------------------
    last_tick = max([t for t, *_ in notes] + [t for t, *_ in tempos] + [0])
    total_sec = None
    if audio_path and audio_path.exists():
        out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                   "-of", "csv=p=0", str(audio_path)]).stdout.strip()
        total_sec = float(out)

    # --- bar grid ---------------------------------------------------------
    bars, bar_no, tick = [], 1, 0
    limit_sec = (total_sec or sec(last_tick)) + 0.5
    while sec(tick) <= limit_sec and bar_no < 2000:
        num, den = tsig_at(tick)
        beat_ticks = ppq * 4 / den
        beats = [round(sec(tick + i * beat_ticks), 6) for i in range(num)]
        bars.append({"bar": bar_no, "tick": tick, "sec": beats[0],
                     "num": num, "den": den, "beats": beats})
        tick = int(tick + num * beat_ticks)
        bar_no += 1
    for _ in range(tail_bars):  # a couple of bars past the end, for safe snapping
        num, den = tsig_at(tick)
        beat_ticks = ppq * 4 / den
        beats = [round(sec(tick + i * beat_ticks), 6) for i in range(num)]
        bars.append({"bar": bar_no, "tick": tick, "sec": beats[0],
                     "num": num, "den": den, "beats": beats})
        tick = int(tick + num * beat_ticks)
        bar_no += 1

    # --- density ----------------------------------------------------------
    edges = [(b["bar"], b["tick"]) for b in bars] + [(bar_no, tick)]
    density = []
    for (bn, start), (_, end) in zip(edges, edges[1:]):
        per = collections.Counter()
        for nt, _pitch, _vel, ti in notes:
            if start <= nt < end:
                per[track_names.get(ti) or f"track{ti}"] += 1
        if per:
            density.append({"bar": bn, "total": sum(per.values()), "tracks": dict(per)})

    tracks = collections.Counter()
    for _t, _p, _v, ti in notes:
        tracks[track_names.get(ti) or f"track{ti}"] += 1

    return {
        "source_midi": str(midi_path),
        "source_audio": str(audio_path) if audio_path else None,
        "ppq": ppq,
        "duration_sec": round(total_sec or sec(last_tick), 6),
        "midi_end_sec": round(sec(last_tick), 6),
        "tempo_map": [{"tick": t, "sec": round(sec(t), 6),
                       "bpm": round(60e6 / tempo, 5)} for t, tempo in tempos],
        "time_signatures": [{"tick": t, "sec": round(sec(t), 6),
                             "num": n, "den": d} for t, n, d in tsigs],
        "markers": [{"tick": t, "sec": round(sec(t), 6), "text": txt, "kind": k}
                    for t, txt, k in sorted(markers)],
        "tracks": [{"name": n, "notes": c} for n, c in tracks.most_common()],
        "bars": bars,
        "density": density,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midi", type=pathlib.Path)
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "analysis" / "beatmap.json")
    a = ap.parse_args()

    bm = build(a.midi, a.audio if a.audio and a.audio.exists() else None)
    save(a.out, bm)

    bpms = sorted({t["bpm"] for t in bm["tempo_map"]})
    print(f"  tempo      {bpms[0]:g}" + (f" .. {bpms[-1]:g} ({len(bm['tempo_map'])} changes)"
                                         if len(bpms) > 1 else " (constant)"))
    print(f"  meter      " + ", ".join(f"{t['num']}/{t['den']}" for t in bm["time_signatures"]))
    print(f"  bars       {len(bm['bars'])}")
    print(f"  duration   {bm['duration_sec']:.2f}s"
          f"   (midi ends {bm['midi_end_sec']:.2f}s)")
    print(f"  tracks     " + ", ".join(t["name"] for t in bm["tracks"][:12]))
    if bm["markers"]:
        print("  markers    " + ", ".join(f"{m['text']}@{m['sec']:.1f}s" for m in bm["markers"][:12]))
    else:
        print("  markers    none found -- write shots/sections.json by hand")
    drift = bm["midi_end_sec"] - bm["duration_sec"]
    if bm["source_audio"] and abs(drift) > 1.0:
        print(f"\n  !! MIDI ends {drift:+.2f}s vs audio. Run tools/clickcheck.py before trusting the grid.")


if __name__ == "__main__":
    main()
