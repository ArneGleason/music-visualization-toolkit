#!/usr/bin/env python3
"""Project timeline/register compiler and frame-accurate query API.

The editable register stores musical positions (bar.beat.tick). Compilation
resolves every edge through the DAW-derived grid and then rounds it to an
integer video frame. Renderers query the compiled register; they never need
to interpret hand-trimmed floating-point seconds.

    python tools/timeline.py sync projects/rivers-of-mars/project.json
    python tools/timeline.py validate projects/rivers-of-mars/project.json
    python tools/timeline.py query projects/rivers-of-mars/project.json --bar 18.1
"""
from __future__ import annotations

import argparse
import bisect
import copy
import json
import pathlib
import subprocess
import sys
from dataclasses import dataclass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save, to_frames, frames_to_sec  # noqa: E402


def _merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _resolve(base: pathlib.Path, value: str | pathlib.Path) -> pathlib.Path:
    path = pathlib.Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def load_project(path: pathlib.Path) -> tuple[dict, pathlib.Path]:
    path = path.resolve()
    project = load(path)
    local = path.with_name("project.local.json")
    if local.exists():
        project = _merge(project, load(local))
    project["_projectFile"] = str(path)
    project["_projectDir"] = str(path.parent)
    return project, path.parent


@dataclass(frozen=True)
class Position:
    bar: int
    beat: int
    tick: int = 0

    @classmethod
    def parse(cls, value: str | dict) -> "Position":
        if isinstance(value, dict):
            return cls(int(value["bar"]), int(value.get("beat", 1)),
                       int(value.get("tick", 0)))
        parts = str(value).strip().split(".")
        if len(parts) not in (1, 2, 3):
            raise ValueError(f"invalid musical position {value!r}; use bar.beat.tick")
        return cls(int(parts[0]), int(parts[1]) if len(parts) > 1 else 1,
                   int(parts[2]) if len(parts) > 2 else 0)

    def text(self) -> str:
        return f"{self.bar}.{self.beat}" + (f".{self.tick}" if self.tick else "")


class MusicalGrid:
    """Bidirectional bar/beat/tick ↔ seconds mapping from a beatmap."""

    def __init__(self, beatmap: dict):
        self.data = beatmap
        self.ppq = int(beatmap.get("ppq", 960))
        self.duration = float(beatmap["duration_sec"])
        self.by_bar = {int(bar["bar"]): bar for bar in beatmap["bars"]}
        points = []
        for bar in beatmap["bars"]:
            for index, sec in enumerate(bar["beats"]):
                points.append((float(sec), int(bar["bar"]), index + 1))
        # Two tail bars emitted by the import provide interpolation past the
        # final audible beat. Duplicate seconds would make inversion ambiguous.
        self.points = []
        for point in sorted(points):
            if not self.points or abs(point[0] - self.points[-1][0]) > 1e-9:
                self.points.append(point)
        self.seconds = [p[0] for p in self.points]

    def sec(self, value: str | dict | Position) -> float:
        pos = value if isinstance(value, Position) else Position.parse(value)
        bar = self.by_bar.get(pos.bar)
        if not bar:
            raise ValueError(f"bar {pos.bar} is outside the imported grid")
        if pos.beat < 1 or pos.beat > int(bar["num"]):
            raise ValueError(f"beat {pos.beat} is outside bar {pos.bar}")
        if pos.tick < 0 or pos.tick >= self.ppq:
            raise ValueError(f"tick must be in 0..{self.ppq - 1}")
        start = float(bar["beats"][pos.beat - 1])
        if pos.tick == 0:
            return start
        if pos.beat < len(bar["beats"]):
            end = float(bar["beats"][pos.beat])
        else:
            nxt = self.by_bar.get(pos.bar + 1)
            if not nxt:
                raise ValueError(f"bar {pos.bar} has no following beat for interpolation")
            end = float(nxt["beats"][0])
        return start + (end - start) * pos.tick / self.ppq

    def position(self, seconds: float, snap_ticks: int = 0) -> Position:
        i = bisect.bisect_right(self.seconds, float(seconds)) - 1
        i = max(0, min(i, len(self.points) - 2))
        t0, bar, beat = self.points[i]
        t1 = self.points[i + 1][0]
        frac = 0.0 if t1 <= t0 else (float(seconds) - t0) / (t1 - t0)
        tick = int(round(frac * self.ppq))
        if snap_ticks:
            tick = int(round(tick / snap_ticks) * snap_ticks)
        if tick >= self.ppq:
            _, bar, beat = self.points[i + 1]
            tick = 0
        tick = max(0, min(tick, self.ppq - 1))
        return Position(bar, beat, tick)


def validate_timeline(timeline: dict, grid: MusicalGrid | None = None) -> list[str]:
    errors = []
    if timeline.get("schemaVersion") != 1:
        errors.append("timeline.schemaVersion must be 1")
    tracks = timeline.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        errors.append("timeline.tracks must be a non-empty list")
        return errors
    track_ids, item_ids = set(), set()
    for track in tracks:
        tid = track.get("id")
        if not tid or tid in track_ids:
            errors.append(f"missing or duplicate track id: {tid!r}")
        track_ids.add(tid)
        if track.get("type") not in {"lyrics", "scene", "transition", "choreography", "notes"}:
            errors.append(f"track {tid!r} has unsupported type {track.get('type')!r}")
        for item in track.get("items", []):
            iid = item.get("id")
            if not iid or iid in item_ids:
                errors.append(f"missing or duplicate item id: {iid!r}")
            item_ids.add(iid)
            lyric_origin = item.get("lyricOrigin")
            if lyric_origin is not None and track.get("type") != "lyrics":
                errors.append(f"item {iid!r} has lyricOrigin outside a lyrics track")
            elif lyric_origin not in {None, "sheet", "improv"}:
                errors.append(f"item {iid!r} has unsupported lyricOrigin {lyric_origin!r}")
            start, end, at = item.get("start"), item.get("end"), item.get("at")
            if start is None and at is None:
                if item.get("timingStatus") != "unplaced":
                    errors.append(f"item {iid!r} has no timing and is not marked unplaced")
                continue
            try:
                start_sec = grid.sec(start if start is not None else at) if grid else 0
                if end is not None:
                    end_sec = grid.sec(end) if grid else 1
                    if end_sec <= start_sec:
                        errors.append(f"item {iid!r} ends at or before its start")
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"item {iid!r}: {exc}")
    return errors


def compile_timeline(project: dict, project_dir: pathlib.Path) -> dict:
    timing = project["timing"]
    beatmap_path = _resolve(project_dir, timing["beatmap"])
    timeline_path = _resolve(project_dir, project["timeline"])
    beatmap, timeline = load(beatmap_path), load(timeline_path)
    grid = MusicalGrid(beatmap)
    errors = validate_timeline(timeline, grid)
    if errors:
        raise ValueError("timeline validation failed:\n  - " + "\n  - ".join(errors))
    fps = float(project.get("render", {}).get("fps", 60))
    compiled_tracks = []
    for track in timeline["tracks"]:
        items = []
        for source in track.get("items", []):
            if source.get("timingStatus") == "unplaced":
                continue
            item = copy.deepcopy(source)
            start = source.get("start", source.get("at"))
            start_frame = to_frames(grid.sec(start), fps)
            if source.get("end") is not None:
                end_frame = to_frames(grid.sec(source["end"]), fps)
                end_frame = max(start_frame + 1, end_frame)
            else:
                end_frame = start_frame + 1
            item.update({
                "startFrame": start_frame,
                "endFrame": end_frame,
                "startSec": frames_to_sec(start_frame, fps),
                "endSec": frames_to_sec(end_frame, fps),
            })
            items.append(item)
        items.sort(key=lambda it: (it["startFrame"], it["endFrame"], it["id"]))
        compiled_tracks.append({**{k: v for k, v in track.items() if k != "items"},
                                "items": items})
    compiled = {
        "schemaVersion": 1,
        "project": {"title": project["title"], "slug": project["slug"]},
        "timing": {
            "fps": fps,
            "durationFrames": to_frames(grid.duration, fps),
            "durationSec": frames_to_sec(to_frames(grid.duration, fps), fps),
            "ppq": grid.ppq,
            "zeroBeat": beatmap.get("zero_beat"),
            "tempoMap": beatmap.get("tempo_map", []),
            "bars": beatmap["bars"],
        },
        "tracks": compiled_tracks,
    }
    out = _resolve(project_dir, timing["compiledTimeline"])
    save(out, compiled)
    return compiled


class TimelineRegister:
    """Renderer-facing lookup over a compiled timeline."""

    def __init__(self, compiled: dict):
        self.data = compiled
        self.fps = float(compiled["timing"]["fps"])

    @classmethod
    def load(cls, path: pathlib.Path) -> "TimelineRegister":
        return cls(load(path))

    def at(self, *, frame: int | None = None, seconds: float | None = None) -> dict:
        if frame is None:
            if seconds is None:
                raise ValueError("frame or seconds is required")
            frame = to_frames(seconds, self.fps)
        result = {"frame": int(frame), "seconds": frames_to_sec(int(frame), self.fps),
                  "lyrics": [], "scenes": [], "transitions": [],
                  "choreography": [], "notes": []}
        keys = {"lyrics": "lyrics", "scene": "scenes", "transition": "transitions",
                "choreography": "choreography", "notes": "notes"}
        for track in self.data["tracks"]:
            bucket = keys[track["type"]]
            for item in track["items"]:
                if item["startFrame"] <= frame < item["endFrame"]:
                    result[bucket].append(item)
        result["scene"] = result["scenes"][-1] if result["scenes"] else None
        result["lyric"] = result["lyrics"][-1] if result["lyrics"] else None
        result["transition"] = result["transitions"][-1] if result["transitions"] else None
        drivers = []
        for item in result["choreography"]:
            drivers.extend(item.get("drivers", []))
        result["drivers"] = sorted(set(drivers))
        return result


def sync_project(project_file: pathlib.Path) -> dict:
    project, project_dir = load_project(project_file)
    source = project["sources"]
    timing = project["timing"]
    daw = _resolve(project_dir, source["dawproject"])
    audio = _resolve(project_dir, source["audio"])
    beatmap = _resolve(project_dir, timing["beatmap"])
    cmd = [sys.executable, str(ROOT / "tools" / "dawproject.py"), str(daw),
           "--audio", str(audio), "--master-track", timing.get("masterTrack", "master"),
           "--duration-source", timing.get("durationSource", "auto"),
           "--beatmap-out", str(beatmap), "--no-lyrics", "--compare"]
    subprocess.run(cmd, check=True)
    if project.get("referenceWaveforms"):
        from waveforms import build as build_waveforms
        build_waveforms(project, project_dir, load(beatmap))
    return compile_timeline(project, project_dir)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("sync", "compile", "validate"):
        p = sub.add_parser(name)
        p.add_argument("project", type=pathlib.Path)
    q = sub.add_parser("query")
    q.add_argument("project", type=pathlib.Path)
    group = q.add_mutually_exclusive_group(required=True)
    group.add_argument("--bar")
    group.add_argument("--seconds", type=float)
    group.add_argument("--frame", type=int)
    args = ap.parse_args()

    project, project_dir = load_project(args.project)
    if args.command == "sync":
        sync_project(args.project)
        return
    if args.command == "validate":
        beatmap = load(_resolve(project_dir, project["timing"]["beatmap"]))
        timeline = load(_resolve(project_dir, project["timeline"]))
        errors = validate_timeline(timeline, MusicalGrid(beatmap))
        if errors:
            raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
        print(f"valid: {project['slug']} ({sum(len(t['items']) for t in timeline['tracks'])} items)")
        return
    compiled = compile_timeline(project, project_dir)
    if args.command == "compile":
        return
    reg = TimelineRegister(compiled)
    if args.bar:
        grid = MusicalGrid(load(_resolve(project_dir, project["timing"]["beatmap"])))
        result = reg.at(seconds=grid.sec(args.bar))
    elif args.seconds is not None:
        result = reg.at(seconds=args.seconds)
    else:
        result = reg.at(frame=args.frame)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
