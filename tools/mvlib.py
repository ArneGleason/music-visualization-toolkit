"""Shared helpers for the music-video toolkit."""
from __future__ import annotations

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(path) -> dict:
    with open(path) as f:
        return json.load(f)


def save(path, data) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {path}")


def run(cmd, **kw):
    """Run a command, raising on failure, quiet by default."""
    kw.setdefault("check", True)
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    try:
        return subprocess.run(cmd, **kw)
    except subprocess.CalledProcessError as e:
        print(" ".join(str(c) for c in cmd))
        print(e.stderr[-4000:] if e.stderr else "")
        raise


# ---------------------------------------------------------------- bar/beat ---

def parse_barbeat(s: str) -> tuple[int, float]:
    """'12.1' -> (12, 1.0); '12' -> (12, 1.0); '12.2.5' -> (12, 2.5)."""
    s = str(s).strip()
    parts = s.split(".")
    bar = int(parts[0])
    beat = 1.0
    if len(parts) > 1:
        beat = float(parts[1]) + (float("0." + parts[2]) if len(parts) > 2 else 0.0)
    return bar, beat


class Beatmap:
    """Bar/beat <-> seconds, backed by analysis/beatmap.json."""

    def __init__(self, data: dict):
        self.d = data
        self.bars = {b["bar"]: b for b in data["bars"]}
        self.duration = data["duration_sec"]

    @classmethod
    def load(cls, path=None):
        return cls(load(path or ROOT / "analysis" / "beatmap.json"))

    def sec(self, barbeat) -> float:
        """Seconds for a bar.beat position. Fractional beats interpolate."""
        if isinstance(barbeat, (int, float)) and not isinstance(barbeat, bool):
            return float(barbeat)
        bar, beat = parse_barbeat(barbeat)
        b = self.bars.get(bar)
        if b is None:
            raise KeyError(f"bar {bar} not in beatmap (1..{max(self.bars)})")
        beats = b["beats"]
        i = int(beat) - 1
        frac = beat - int(beat)
        if i < 0 or i >= len(beats):
            raise KeyError(f"beat {beat} out of range in bar {bar}")
        t = beats[i]
        if frac == 0:
            return t
        nxt = beats[i + 1] if i + 1 < len(beats) else self.bars.get(bar + 1, {"beats": [t + (t - beats[i - 1] if i else 0.5)]})["beats"][0]
        return t + (nxt - t) * frac

    def snap(self, seconds: float, division: float = 1.0) -> float:
        """Snap a time to the nearest grid point. division=1 beat, 4=bar, 0.5=8th."""
        grid = []
        for b in self.d["bars"]:
            beats = b["beats"]
            step = max(1, int(division)) if division >= 1 else 1
            if division >= 1:
                grid.extend(beats[::step])
            else:
                for i, t in enumerate(beats):
                    nxt = beats[i + 1] if i + 1 < len(beats) else t + (t - beats[i - 1] if i else 0.5)
                    n = int(round(1 / division))
                    grid.extend(t + (nxt - t) * k / n for k in range(n))
        return min(grid, key=lambda t: abs(t - seconds))

    def nearest_barbeat(self, seconds: float) -> str:
        best, bestd = "1.1", 1e9
        for b in self.d["bars"]:
            for i, t in enumerate(b["beats"]):
                if abs(t - seconds) < bestd:
                    best, bestd = f"{b['bar']}.{i + 1}", abs(t - seconds)
        return best


# ------------------------------------------------------------------- frames ---

def to_frames(seconds: float, fps: float) -> int:
    return int(round(seconds * fps))


def frames_to_sec(frames: int, fps: float) -> float:
    return frames / fps
