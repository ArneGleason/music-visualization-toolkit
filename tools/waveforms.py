#!/usr/bin/env python3
"""Generate compact, silent waveform references for the timeline editor.

Only peak/RMS numbers are written. Stem audio remains outside the repository
and is never served to the browser.
"""
from __future__ import annotations

import argparse
import array
import math
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dawproject import TempoCurve, parse_tempo, read_project_xml  # noqa: E402
from mvlib import load, save  # noqa: E402

DECODE_RATE = 2000


def _resolve(base: pathlib.Path, value: str | pathlib.Path) -> pathlib.Path:
    path = pathlib.Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_project(path: pathlib.Path) -> tuple[dict, pathlib.Path]:
    path = path.resolve()
    project = load(path)
    local = path.with_name("project.local.json")
    if local.exists():
        project = _deep_merge(project, load(local))
    return project, path.parent


def _origin_beat(root, match: str) -> float | None:
    """Project beat corresponding to sample zero for a matched audio track."""
    names = {t.get("id"): (t.get("name") or "") for t in root.iter("Track")}
    candidates = []
    needle = match.casefold()
    for lanes in root.iter("Lanes"):
        name = names.get(lanes.get("track"), "")
        if needle not in name.casefold():
            continue
        for clip in lanes.iter("Clip"):
            if clip.get("contentTimeUnit") == "seconds":
                continue
            if clip.get("time") is None:
                continue
            candidates.append(float(clip.get("time", 0) or 0)
                              - float(clip.get("playStart", 0) or 0))
    if not candidates:
        return None
    # Split clips from one source repeat the same origin. A median is stable
    # in the presence of an alternate take or an accidentally loose clip.
    candidates.sort()
    return candidates[len(candidates) // 2]


def _stem(stem_dir: pathlib.Path, match: str) -> pathlib.Path:
    matches = [p for p in stem_dir.glob("*")
               if p.is_file() and match.casefold() in p.name.casefold()
               and p.suffix.lower() in {".wav", ".aiff", ".flac"}]
    if len(matches) != 1:
        raise ValueError(f"expected one stem matching {match!r}, found {[p.name for p in matches]}")
    return matches[0]


def _envelope(path: pathlib.Path, output_rate: int) -> tuple[list[float], list[float]]:
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(DECODE_RATE),
         "-f", "f32le", "-"], check=True, capture_output=True)
    pcm = array.array("f")
    pcm.frombytes(result.stdout)
    if sys.byteorder != "little":
        pcm.byteswap()
    block = max(1, round(DECODE_RATE / output_rate))
    peaks, rms = [], []
    for start in range(0, len(pcm), block):
        values = pcm[start:start + block]
        if not values:
            break
        peaks.append(max(abs(v) for v in values))
        rms.append(math.sqrt(sum(v * v for v in values) / len(values)))
    nonzero = sorted(v for v in peaks if v > 1e-7)
    norm = nonzero[min(len(nonzero) - 1, int(len(nonzero) * .985))] if nonzero else 1.0
    norm = max(norm, 1e-7)
    return ([round(min(1.0, v / norm), 4) for v in peaks],
            [round(min(1.0, v / norm), 4) for v in rms])


def build(project: dict, project_dir: pathlib.Path, beatmap: dict) -> dict:
    cfg = project.get("referenceWaveforms")
    if not cfg:
        return {"schemaVersion": 1, "rate": 0, "tracks": []}
    daw_path = _resolve(project_dir, project["sources"]["dawproject"])
    audio_path = _resolve(project_dir, project["sources"]["audio"])
    stem_dir = _resolve(project_dir, project["sources"]["stems"])
    root = read_project_xml(daw_path)
    curve: TempoCurve = parse_tempo(root)
    zero_beat = float(beatmap["zero_beat"])
    zero_sec = curve.sec(zero_beat)
    rate = int(cfg.get("samplesPerSecond", 40))
    tracks = []
    for spec in cfg["tracks"]:
        path = audio_path if spec["source"] == "audio" else _stem(stem_dir, spec["match"])
        origin_beat = _origin_beat(root, spec["match"])
        if spec["source"] == "audio":
            # The master clip is the timing authority. If track matching ever
            # fails, its file still begins at the imported mix zero.
            origin_beat = zero_beat if origin_beat is None else origin_beat
        elif origin_beat is None:
            raise ValueError(f"could not align waveform track {spec['label']!r} in DAWproject")
        peak, rms = _envelope(path, rate)
        offset = curve.sec(origin_beat) - zero_sec
        tracks.append({
            "id": spec["id"], "label": spec["label"], "role": spec.get("role", ""),
            "color": spec.get("color", "#aab4ca"), "rate": rate,
            "offsetSec": round(offset, 6), "durationSec": round(len(peak) / rate, 6),
            "peak": peak, "rms": rms,
        })
        print(f"  {spec['label']:<18} {len(peak) / rate:7.3f}s  offset {offset:+.3f}s")
    data = {"schemaVersion": 1, "durationSec": beatmap["duration_sec"],
            "rate": rate, "tracks": tracks}
    save(_resolve(project_dir, cfg["output"]), data)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=pathlib.Path)
    args = ap.parse_args()
    project, project_dir = load_project(args.project)
    beatmap = load(_resolve(project_dir, project["timing"]["beatmap"]))
    build(project, project_dir, beatmap)


if __name__ == "__main__":
    main()
