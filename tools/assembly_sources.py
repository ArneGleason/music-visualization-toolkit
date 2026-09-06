"""Read-only source selection shared by motion assemblers.

Shotlist timing remains authoritative. Protected decisions override picture
selection only and fail closed if the delivery or its timing is not valid.
"""
import json
import pathlib
import subprocess
from functools import lru_cache
from fractions import Fraction


def load_decisions(root):
    path = pathlib.Path(root)/"shots/assembly_decisions.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported assembly decision schema")
    result = {}
    for entry in data["decisions"]:
        if entry["shot_id"] in result:
            raise ValueError("Duplicate assembly decision: "+entry["shot_id"])
        result[entry["shot_id"]] = entry
    return result


@lru_cache(maxsize=32)
def inspect_video(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate,nb_frames", "-of", "json", str(path)])
    stream = json.loads(raw)["streams"][0]
    return float(Fraction(stream["avg_frame_rate"])), int(stream["nb_frames"])


def resolve_clip(root, shot, fps, decisions, start=None, end=None):
    entry = decisions.get(shot["id"])
    if entry is None:
        return dict(shot.get("clip") or {})
    def fail(reason):
        raise ValueError(f"{shot['id']}: protected visualization: {reason}. "
                         "No generated-clip fallback; see docs/ASSEMBLY_DECISIONS.md")
    if entry.get("decision") not in (
            "prefer_procedural_still_composite_over_generated_video",
            "prefer_music_fx_composite_over_untreated_video"):
        fail("unsupported selection policy")
    if entry.get("approval") != "owner_approved_treatment":
        fail("treatment approval missing")
    if entry["setup"] != shot.get("setup"):
        fail("setup changed; review mapping")
    timing = entry["timing_snapshot"]
    expected_start = round(shot["start_sec"]*fps)
    expected_end = round(shot["end_sec"]*fps)
    if ((start is not None and start != expected_start)
            or (end is not None and end != expected_end)):
        fail("cue timing disagrees with shotlist; rebuild/review cues")
    if (fps != timing["fps"] or expected_start != timing["song_start_frame"]
            or expected_end != timing["song_end_frame_exclusive"]
            or shot["frames"] != expected_end-expected_start):
        fail("shot timing changed; re-render synchronized content")
    if entry.get("delivery_status") not in ("delivery_ready", "applied"):
        fail("clean delivery is not ready")
    source = entry.get("delivery_file")
    if not source or not (pathlib.Path(root)/source).is_file():
        fail("clean delivery file is missing")
    actual_fps, frames = inspect_video(str(pathlib.Path(root)/source))
    first, last = timing["source_in_frame"], timing["source_out_frame_exclusive"]
    if (actual_fps != fps or first < 0 or last-first != expected_end-expected_start
            or frames < last):
        fail("delivery frame rate or source coverage is invalid")
    return {"file": source, "in_sec": first/fps, "speed": 1.0,
            "assembly_decision": entry["id"]}
