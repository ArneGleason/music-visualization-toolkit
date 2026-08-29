#!/usr/bin/env python3
"""
Pull the stems out of the DAWproject and reduce them to envelopes.

    python3 tools/stems.py source/Song.dawproject

Writes analysis/envelopes.json: for every audio track in the project, a peak
and RMS envelope sampled at --rate Hz, plus the constant time offset between
that stem and the mix.

Why a constant offset works here: every stem clip in this project satisfies
`clip.time - clip.playStart == 11.5 beats`, and the master sits at 14.0. The
audio is unwarped (`algorithm="raw"`) and the tempo map was fitted to it, so

    stem_time = mix_time + (sec(master_beat) - sec(stem_beat))

is exact, not an approximation. The tool checks that invariant per track and
refuses to guess if a track's clips disagree.

Envelopes are stored as integers 0..1000 to keep the file small.
"""
from __future__ import annotations

import argparse
import array
import collections
import pathlib
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, save  # noqa: E402
from dawproject import (TempoCurve, find_master, parse_tempo,  # noqa: E402
                        read_project_xml)


def audio_tracks(root):
    """-> {track_name: (wav_path_in_zip, offset_beat)} for tracks with one offset."""
    names = {t.get("id"): (t.get("name") or "") for t in root.iter("Track")}
    out = {}
    for lanes in root.iter("Lanes"):
        tid = lanes.get("track")
        if not tid:
            continue
        offs, path = set(), None
        for c in lanes.iter("Clip"):
            if c.get("contentTimeUnit") == "seconds":
                continue
            if c.get("time") is not None and c.get("playStart") is not None:
                offs.add(round(float(c.get("time")) - float(c.get("playStart")), 4))
        for f in lanes.iter("File"):
            p = f.get("path") or ""
            if p.lower().endswith((".wav", ".aiff", ".flac")):
                path = p
        if not path or not offs:
            continue
        name = names.get(tid, tid)
        if len(offs) > 1:
            print(f"  skip {name}: clips disagree on offset {sorted(offs)}")
            continue
        out[name] = (path, offs.pop())
    return out


# log-spaced bands. Cheap to get exactly right with ffmpeg's biquads, and
# enough to recover a spectral centroid without pulling in numpy/FFT.
BANDS = [
    ("sub",    None,   80),
    ("low",      80,  250),
    ("lomid",   250,  800),
    ("mid",     800, 2500),
    ("himid",  2500, 6000),
    ("air",    6000, None),
]
BAND_HZ = [55, 140, 450, 1400, 3900, 9000]      # representative centre per band


def _pcm(wav: pathlib.Path, sr: int, af: str | None = None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar", str(sr)]
    if af:
        cmd += ["-af", af]
    cmd += ["-f", "s16le", "-"]
    return subprocess.run(cmd, capture_output=True, check=True).stdout


def _blocks(raw: bytes, sr: int, rate: int):
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    block = max(1, sr // rate)
    return a, block


def band_filter(lo, hi):
    parts = []
    if lo:
        parts.append(f"highpass=f={lo}:poles=2")
    if hi:
        parts.append(f"lowpass=f={hi}:poles=2")
    return ",".join(parts) or "anull"


def band_envelopes(wav: pathlib.Path, rate: int):
    """-> {band_name: [rms 0..1000]} — one ffmpeg pass per band."""
    sr = 48000
    out = {}
    for name, lo, hi in BANDS:
        a, block = _blocks(_pcm(wav, sr, band_filter(lo, hi)), sr, rate)
        vals = []
        for i in range(0, len(a) - block, block):
            chunk = a[i:i + block:4]
            s = 0
            for v in chunk:
                s += v * v
            vals.append(min(1000, int((s / max(1, len(chunk))) ** 0.5 * 1000 / 32768)))
        out[name] = vals
    return out


def envelope(wav: pathlib.Path, rate: int):
    """-> (peaks, rms) at `rate` Hz, values 0..1000."""
    sr = 48000
    raw = _pcm(wav, sr)
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    block = max(1, sr // rate)
    peaks, rms = [], []
    for i in range(0, len(a) - block, block):
        chunk = a[i:i + block]
        pk = max(max(chunk), -min(chunk))
        peaks.append(min(1000, pk * 1000 // 32768))
        s = 0
        for v in chunk[::4]:                     # every 4th sample is plenty
            s += v * v
        n = max(1, len(chunk[::4]))
        rms.append(min(1000, int((s / n) ** 0.5 * 1000 / 32768)))
    return peaks, rms


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=pathlib.Path, nargs="?")
    ap.add_argument("--rate", type=int, default=60, help="envelope samples per second")
    ap.add_argument("--no-bands", action="store_true", help="skip the spectral split")
    a = ap.parse_args()

    proj = a.project or next(iter(sorted((ROOT / "source").glob("*.dawproject"))), None)
    if not proj:
        raise SystemExit("no .dawproject in source/")

    root = read_project_xml(proj)
    curve = parse_tempo(root)
    master = find_master(root)
    zero_beat = master[1] if master else 0.0
    zero_sec = curve.sec(zero_beat)
    tracks = audio_tracks(root)

    out = {"rate": a.rate, "bands": [b[0] for b in BANDS],
           "band_hz": BAND_HZ, "tracks": {}}
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(proj) as z:
            members = set(z.namelist())
            for name, (path, off) in tracks.items():
                if path not in members:
                    print(f"  skip {name}: {path} not in the archive")
                    continue
                if master and path == master[2]:
                    continue                       # that's the mix, not a stem
                dst = pathlib.Path(td) / pathlib.Path(path).name
                dst.write_bytes(z.read(path))
                delta = zero_sec - curve.sec(off)   # stem_time = mix_time + delta
                pk, rm = envelope(dst, a.rate)
                entry = {
                    "file": pathlib.Path(path).name,
                    "offset_beat": off,
                    "delta_sec": round(delta, 6),
                    "peak": pk,
                    "rms": rm,
                }
                if not a.no_bands:
                    entry["bands"] = band_envelopes(dst, a.rate)
                out["tracks"][name] = entry
                dst.unlink()
                secs = len(pk) / a.rate
                print(f"  {name[:48]:48s} {secs:7.1f}s  delta {delta:+.3f}s")

    save(ROOT / "analysis" / "envelopes.json", out)
    print(f"  {len(out['tracks'])} stems at {a.rate} Hz")


if __name__ == "__main__":
    main()
