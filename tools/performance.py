#!/usr/bin/env python3
"""Build compact, DAW-aligned performance controls for vector renderers.

Envelopes control large movement elsewhere. This export adds two finer layers:
spelling-derived mouth articulation and band-limited, polarity-preserving audio
signals suitable for narrow oscilloscope-like deformation of drawn contours.
"""
from __future__ import annotations

import argparse
import array
import math
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dawproject import TempoCurve, parse_tempo, read_project_xml  # noqa: E402
from mvlib import load, save  # noqa: E402
from waveforms import _origin_beat, _stem  # noqa: E402


VISEME = {
    "a": (.95, .78, .05, .00, 1.6), "aa": (1, .80, .05, .00, 1.9),
    "ai": (.80, .90, .05, .10, 1.8), "e": (.55, .95, .00, .20, 1.5),
    "ea": (.60, .95, .00, .15, 1.8), "ee": (.35, 1, .00, .30, 1.8),
    "i": (.42, .90, .00, .25, 1.4), "o": (.75, .18, .92, .00, 1.6),
    "oo": (.40, .08, 1, .00, 1.8), "ou": (.65, .15, .95, .00, 1.8),
    "ow": (.70, .20, .90, .00, 1.8), "oi": (.65, .55, .60, .05, 1.8),
    "u": (.48, .12, .92, .00, 1.5), "y": (.45, .85, .05, .20, 1.2),
    "m": (.02, .48, .15, .00, .7), "b": (.05, .50, .15, .00, .6),
    "p": (.04, .50, .15, .00, .6), "f": (.18, .62, .05, .90, .8),
    "v": (.18, .62, .05, .85, .8), "th": (.26, .72, .00, .80, .9),
    "s": (.14, .88, .00, .88, .9), "z": (.16, .86, .00, .85, .9),
    "sh": (.34, .34, .70, .40, 1), "ch": (.32, .36, .68, .45, .9),
    "j": (.32, .40, .62, .40, .9), "t": (.28, .70, .05, .45, .6),
    "d": (.30, .68, .05, .40, .6), "n": (.26, .66, .05, .35, .7),
    "l": (.38, .62, .05, .30, .9), "r": (.40, .34, .58, .10, 1),
    "w": (.30, .10, .95, .00, 1), "k": (.36, .56, .10, .10, .6),
    "g": (.36, .56, .10, .10, .6), "h": (.45, .55, .10, .00, .5),
    "c": (.32, .62, .08, .30, .6), "q": (.30, .12, .92, .00, .6),
    "x": (.20, .80, .00, .70, .8),
}
DIGRAPHS = ("th", "sh", "ch", "ph", "wh", "ck", "ng", "qu", "oo", "ee",
             "ea", "ou", "ow", "oi", "oy", "ai", "ay", "au", "aw")
DIGRAPH_AS = {"ph": "f", "wh": "w", "ck": "k", "ng": "n", "qu": "w",
               "oy": "oi", "ay": "ai", "au": "ow", "aw": "ow"}
TONGUE = {
    "th": (1, .92), "l": (.88, .76), "t": (.54, .68), "d": (.54, .68),
    "n": (.48, .64), "s": (.34, .58), "z": (.34, .58), "r": (.46, -.05),
    "sh": (.24, .18), "ch": (.28, .22), "j": (.28, .20),
    "k": (.38, -.76), "g": (.38, -.76), "a": (.12, -.10),
    "aa": (.14, -.12), "e": (.12, .42), "ea": (.12, .46),
    "ee": (.12, .52), "i": (.10, .48), "y": (.10, .42),
    "o": (.10, -.42), "oo": (.10, -.52), "ou": (.10, -.46),
    "ow": (.10, -.44), "u": (.10, -.50),
}
REST = (.06, .50, .20, .00, .00, .00)


def _resolve(base: pathlib.Path, value: str | pathlib.Path) -> pathlib.Path:
    path = pathlib.Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def spell_visemes(word: str) -> list[tuple[float, ...]]:
    letters = "".join(c for c in word.lower() if c.isalpha())
    out, i = [], 0
    while i < len(letters):
        pair = letters[i:i + 2]
        if pair in DIGRAPHS:
            key, i = DIGRAPH_AS.get(pair, pair), i + 2
        else:
            key, i = letters[i], i + 1
        if key == "e" and i >= len(letters) and len(out) > 1:
            continue
        value = VISEME.get(key)
        if value:
            tongue, position = TONGUE.get(key, (0, 0))
            out.append((*value[:4], tongue, position, value[4]))
    if out:
        return out
    value = VISEME["a"]
    return [(*value[:4], *TONGUE["a"], value[4])]


def mouth_track(words: list[tuple[float, str]], rate: int, count: int) -> dict:
    target = [list(REST) for _ in range(count)]
    for index, (word_time, text) in enumerate(words):
        next_time = words[index + 1][0] if index + 1 < len(words) else word_time + .45
        span = min(max(.10, next_time - word_time), .95)
        shapes = spell_visemes(text)
        total = sum(shape[6] for shape in shapes) or 1
        elapsed = 0.0
        for shape in shapes:
            start = word_time + span * elapsed / total
            elapsed += shape[6]
            end = word_time + span * elapsed / total
            i0, i1 = int(start * rate), max(int(start * rate) + 1, int(end * rate))
            for frame in range(max(0, i0), min(count, i1)):
                target[frame] = list(shape[:6])
    series = [[0.0] * count for _ in range(6)]
    current = list(REST)
    follow = 1 - math.exp(-1 / (rate * .055))
    for frame in range(count):
        for channel in range(6):
            current[channel] += (target[frame][channel] - current[channel]) * follow
            series[channel][frame] = round(current[channel], 4)
    return dict(zip(("open", "wide", "round", "teeth", "tongue", "tongue_pos"), series))


def word_onsets(compiled: dict) -> list[tuple[float, str]]:
    lyrics = next((track["items"] for track in compiled["tracks"]
                   if track["type"] == "lyrics"), [])
    result = []
    for item in lyrics:
        words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", item.get("text", ""))
        if not words:
            continue
        start, end = float(item["startSec"]), float(item["endSec"])
        weights = [max(1.0, len(re.sub(r"[^A-Za-z]", "", word)) ** .62) for word in words]
        total = sum(weights)
        elapsed = 0.0
        for word, weight in zip(words, weights):
            result.append((start + (end - start) * elapsed / total, word))
            elapsed += weight
    return result


def midi_note_events(root, curve: TempoCurve, zero_sec: float,
                     specs: list[dict]) -> dict[str, list[dict]]:
    """Export a deliberately small set of exact DAW note performances.

    The renderer chooses when to show them; this layer only preserves timing,
    duration, pitch and velocity on the same tempo-ramp clock as the audio.
    """
    names = {track.get("id"): (track.get("name") or "")
             for track in root.iter("Track")}
    lanes_by_name: dict[str, list] = {}
    for lanes in root.iter("Lanes"):
        track_id = lanes.get("track")
        if track_id:
            lanes_by_name.setdefault(names.get(track_id, track_id), []).append(lanes)

    result: dict[str, list[dict]] = {}
    for spec in specs:
        match = str(spec["match"]).strip().lower()
        minimum_velocity = float(spec.get("minVelocity", 0))
        minimum_pitch = int(spec.get("minPitch", 0))
        maximum_pitch = int(spec.get("maxPitch", 127))
        events = []
        seen = set()
        for track_name, lane_groups in lanes_by_name.items():
            if match not in track_name.lower():
                continue
            for lanes in lane_groups:
                for clip in lanes.iter("Clip"):
                    if clip.get("contentTimeUnit") == "seconds":
                        continue
                    base = float(clip.get("time", 0) or 0)
                    play_start = float(clip.get("playStart", 0) or 0)
                    for note in clip.iter("Note"):
                        velocity = float(note.get("vel", .8) or .8)
                        pitch = int(note.get("key", 60))
                        if velocity < minimum_velocity or not minimum_pitch <= pitch <= maximum_pitch:
                            continue
                        beat = base + float(note.get("time", 0) or 0) - play_start
                        duration = max(.001, float(note.get("duration", .25) or .25))
                        on = curve.sec(beat) - zero_sec
                        off = curve.sec(beat + duration) - zero_sec
                        key = (round(on, 6), round(off, 6), pitch,
                               round(velocity, 4), track_name)
                        if key in seen:
                            continue
                        seen.add(key)
                        events.append({
                            "on": round(on, 6),
                            "off": round(max(on + .001, off), 6),
                            "pitch": pitch,
                            "velocity": round(velocity, 4),
                            "track": track_name,
                        })
        result[spec["id"]] = sorted(events, key=lambda event: (event["on"], event["pitch"]))
    return result


def audio_signal(path: pathlib.Path, rate: int, highpass: int, lowpass: int) -> list[int]:
    filters = f"highpass=f={highpass},lowpass=f={lowpass},aresample={rate}"
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-af", filters,
         "-f", "f32le", "-"], check=True, capture_output=True)
    pcm = array.array("f")
    pcm.frombytes(result.stdout)
    if sys.byteorder != "little":
        pcm.byteswap()
    nonzero = sorted(abs(value) for value in pcm if abs(value) > 1e-8)
    norm = nonzero[min(len(nonzero) - 1, int(len(nonzero) * .985))] if nonzero else 1
    return [round(max(-1, min(1, value / max(norm, 1e-8))) * 127) for value in pcm]


def build(project: dict, project_dir: pathlib.Path, compiled: dict, beatmap: dict) -> dict:
    config = project.get("performance")
    if not config:
        return {"schemaVersion": 2, "rate": 0, "mouth": {}, "signals": {}, "notes": {}}
    rate = int(config.get("samplesPerSecond", 60))
    signal_rate = int(config.get("signalRate", 720))
    duration = float(compiled["timing"]["durationSec"])
    daw_path = _resolve(project_dir, project["sources"]["dawproject"])
    stem_dir = _resolve(project_dir, project["sources"]["stems"])
    root = read_project_xml(daw_path)
    curve: TempoCurve = parse_tempo(root)
    zero_sec = curve.sec(float(beatmap["zero_beat"]))
    signals = {}
    for spec in config.get("tracks", []):
        path = _stem(stem_dir, spec["match"])
        origin_beat = _origin_beat(root, spec["match"])
        if origin_beat is None:
            raise ValueError(f"could not align performance track {spec['id']!r}")
        samples = audio_signal(path, signal_rate, int(spec["highpass"]), int(spec["lowpass"]))
        signals[spec["id"]] = {
            "rate": signal_rate,
            "offsetSec": round(curve.sec(origin_beat) - zero_sec, 6),
            "samples": samples,
        }
        print(f"  performance {spec['id']:<12} {len(samples) / signal_rate:7.3f}s")
    data = {
        "schemaVersion": 2,
        "durationSec": duration,
        "rate": rate,
        "mouth": mouth_track(word_onsets(compiled), rate, math.ceil(duration * rate) + 1),
        "signals": signals,
        "notes": midi_note_events(root, curve, zero_sec, config.get("noteTracks", [])),
    }
    save(_resolve(project_dir, config["output"]), data)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=pathlib.Path)
    args = parser.parse_args()
    from timeline import load_project
    project, project_dir = load_project(args.project)
    compiled = load(_resolve(project_dir, project["timing"]["compiledTimeline"]))
    beatmap = load(_resolve(project_dir, project["timing"]["beatmap"]))
    build(project, project_dir, compiled, beatmap)


if __name__ == "__main__":
    main()
