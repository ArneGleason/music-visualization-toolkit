#!/usr/bin/env python3
"""Build compact, reusable motion clips from Acclaim ASF/AMC capture data.

The visible renderer never has to draw a skeleton. This export preserves a
small set of joint trajectories, root motion, source provenance, and the
capture clock so scene code can reinterpret biological motion as curves,
features, plants, creatures, or other project-native vector forms.

    python tools/motion_capture.py projects/rivers-of-mars/project.json
"""
from __future__ import annotations

import argparse
import dataclasses
import math
import pathlib
import urllib.request

from mvlib import load, save


Matrix = tuple[tuple[float, float, float], ...]
Vector = tuple[float, float, float]


@dataclasses.dataclass
class Bone:
    name: str
    direction: Vector
    length: float
    axis: Vector
    axis_order: str
    dof: tuple[str, ...]
    parent: str = "root"


def _identity() -> Matrix:
    return ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def _multiply(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum(a[row][k] * b[k][column] for k in range(3))
                       for column in range(3)) for row in range(3))


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[column][row] for column in range(3))
                 for row in range(3))


def _apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(matrix[row][column] * vector[column] for column in range(3))
                 for row in range(3))  # type: ignore[return-value]


def _rotation(axis: str, degrees: float) -> Matrix:
    angle = math.radians(degrees)
    cosine, sine = math.cos(angle), math.sin(angle)
    if axis.lower() == "x":
        return ((1, 0, 0), (0, cosine, -sine), (0, sine, cosine))
    if axis.lower() == "y":
        return ((cosine, 0, sine), (0, 1, 0), (-sine, 0, cosine))
    if axis.lower() == "z":
        return ((cosine, -sine, 0), (sine, cosine, 0), (0, 0, 1))
    raise ValueError(f"unknown rotation axis: {axis}")


def euler_matrix(values: list[float] | tuple[float, ...], axes: str) -> Matrix:
    matrix = _identity()
    for value, axis in zip(values, axes):
        matrix = _multiply(matrix, _rotation(axis, value))
    return matrix


def _vector_add(a: Vector, b: Vector) -> Vector:
    return tuple(a[index] + b[index] for index in range(3))  # type: ignore[return-value]


def _vector_subtract(a: Vector, b: Vector) -> Vector:
    return tuple(a[index] - b[index] for index in range(3))  # type: ignore[return-value]


def _vector_scale(vector: Vector, scale: float) -> Vector:
    return tuple(value * scale for value in vector)  # type: ignore[return-value]


def _distance(a: Vector, b: Vector = (0.0, 0.0, 0.0)) -> float:
    return math.sqrt(sum((a[index] - b[index]) ** 2 for index in range(3)))


def parse_asf(path: pathlib.Path) -> tuple[dict[str, Bone], dict[str, list[str]]]:
    """Parse the bone and hierarchy sections needed for forward kinematics."""
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    bones: dict[str, Bone] = {}
    in_bones = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if line == ":bonedata":
            in_bones = True
        elif in_bones and line.startswith(":"):
            break
        elif in_bones and line == "begin":
            fields: dict[str, list[str]] = {}
            index += 1
            while index < len(lines) and lines[index] != "end":
                parts = lines[index].split()
                if parts and parts[0] in {"name", "direction", "length", "axis", "dof"}:
                    fields[parts[0]] = parts[1:]
                index += 1
            name = fields["name"][0]
            direction = tuple(float(value) for value in fields["direction"][:3])
            axis_values = tuple(float(value) for value in fields.get("axis", [0, 0, 0])[:3])
            axis_order = fields.get("axis", [0, 0, 0, "XYZ"])[3]
            bones[name] = Bone(
                name=name,
                direction=direction,  # type: ignore[arg-type]
                length=float(fields["length"][0]),
                axis=axis_values,  # type: ignore[arg-type]
                axis_order=axis_order,
                dof=tuple(fields.get("dof", [])),
            )
        index += 1

    hierarchy: dict[str, list[str]] = {}
    try:
        index = lines.index(":hierarchy") + 1
    except ValueError as exc:
        raise ValueError(f"missing :hierarchy in {path}") from exc
    while index < len(lines):
        line = lines[index]
        if line and line not in {"begin", "end"}:
            parent, *children = line.split()
            hierarchy[parent] = children
            for child in children:
                if child in bones:
                    bones[child].parent = parent
        if line == "end":
            break
        index += 1
    return bones, hierarchy


def parse_amc(path: pathlib.Path) -> list[dict[str, list[float]]]:
    frames: list[dict[str, list[float]]] = []
    current: dict[str, list[float]] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ":")):
            continue
        if line.isdigit():
            if current is not None:
                frames.append(current)
            current = {}
            continue
        if current is None:
            continue
        name, *values = line.split()
        current[name] = [float(value) for value in values]
    if current is not None:
        frames.append(current)
    return frames


def _bone_order(hierarchy: dict[str, list[str]]) -> list[str]:
    ordered: list[str] = []

    def visit(parent: str) -> None:
        for child in hierarchy.get(parent, []):
            ordered.append(child)
            visit(child)

    visit("root")
    return ordered


def joint_positions(frame: dict[str, list[float]], bones: dict[str, Bone],
                    hierarchy: dict[str, list[str]]) -> dict[str, Vector]:
    """Resolve one Acclaim pose to endpoint positions in capture space."""
    root = frame.get("root", [0.0] * 6)
    positions: dict[str, Vector] = {"root": tuple(root[:3])}  # type: ignore[dict-item]
    rotations: dict[str, Matrix] = {"root": euler_matrix(root[3:6], "XYZ")}
    for name in _bone_order(hierarchy):
        bone = bones[name]
        axis = euler_matrix(bone.axis, bone.axis_order)
        motion_axes = "".join(channel[-1] for channel in bone.dof
                              if channel.lower().startswith("r"))
        motion_values = frame.get(name, [])[:len(motion_axes)]
        motion = euler_matrix(motion_values, motion_axes)
        local = _multiply(_multiply(_transpose(axis), motion), axis)
        parent_rotation = rotations.get(bone.parent, rotations["root"])
        rotation = _multiply(parent_rotation, local)
        rotations[name] = rotation
        offset = _apply(rotation, _vector_scale(bone.direction, bone.length))
        positions[name] = _vector_add(positions.get(bone.parent, positions["root"]), offset)
    return positions


def _activity_window(poses: list[dict[str, Vector]], joints: list[str],
                     frame_count: int, margin: int) -> int:
    if frame_count >= len(poses):
        return 0
    energy = [0.0] * len(poses)
    for index in range(1, len(poses)):
        root_now, root_before = poses[index]["root"], poses[index - 1]["root"]
        for joint in joints:
            now = _vector_subtract(poses[index][joint], root_now)
            before = _vector_subtract(poses[index - 1][joint], root_before)
            energy[index] += _distance(now, before)
    prefix = [0.0]
    for value in energy:
        prefix.append(prefix[-1] + value)
    low = min(margin, max(0, len(poses) - frame_count))
    high = max(low, len(poses) - frame_count - margin)
    return max(range(low, high + 1),
               key=lambda start: prefix[start + frame_count] - prefix[start])


def _smooth_pose(poses: list[dict[str, Vector]], index: int,
                 joints: list[str]) -> dict[str, Vector]:
    weights = ((-2, 1), (-1, 2), (0, 3), (1, 2), (2, 1))
    result: dict[str, Vector] = {}
    for joint in joints:
        total = [0.0, 0.0, 0.0]
        used = 0
        for offset, weight in weights:
            source = poses[max(0, min(len(poses) - 1, index + offset))][joint]
            for axis in range(3):
                total[axis] += source[axis] * weight
            used += weight
        result[joint] = tuple(value / used for value in total)  # type: ignore[assignment]
    return result


def build_clip(spec: dict, project_dir: pathlib.Path) -> tuple[pathlib.Path, dict]:
    output = (project_dir / spec["output"]).resolve()
    cache_dir = output.parent.parent / "mocap"
    cache_dir.mkdir(parents=True, exist_ok=True)
    skeleton_path = cache_dir / f'{spec["id"]}.asf'
    motion_path = cache_dir / f'{spec["id"]}.amc'
    for url, path in ((spec["skeletonUrl"], skeleton_path),
                      (spec["motionUrl"], motion_path)):
        if not path.exists():
            request = urllib.request.Request(url, headers={"User-Agent": "music-visualization-toolkit"})
            with urllib.request.urlopen(request) as response:  # noqa: S310 - authored URL
                path.write_bytes(response.read())

    bones, hierarchy = parse_asf(skeleton_path)
    source_frames = parse_amc(motion_path)
    poses = [joint_positions(frame, bones, hierarchy) for frame in source_frames]
    source_rate = int(spec.get("sourceRate", 120))
    sample_rate = int(spec.get("sampleRate", 30))
    window_frames = min(len(poses), round(float(spec.get("windowSec", 6)) * source_rate))
    activity_joints = [joint for joint in spec["joints"] if joint != "root"]
    start = _activity_window(poses, activity_joints, window_frames, source_rate)
    stride = max(1, round(source_rate / sample_rate))
    source_indices = list(range(start, min(len(poses), start + window_frames), stride))
    smoothed = [_smooth_pose(poses, index, spec["joints"]) for index in source_indices]

    distances = []
    for pose in smoothed:
        root = pose["root"]
        distances.extend(_distance(point, root) for name, point in pose.items() if name != "root")
    distances.sort()
    scale = distances[min(len(distances) - 1, round(len(distances) * .97))] or 1.0
    origin = smoothed[0]["root"]
    frames, root_motion = [], []
    for pose in smoothed:
        root = pose["root"]
        flattened = []
        for joint in spec["joints"]:
            point = _vector_scale(_vector_subtract(pose[joint], root), 1 / scale)
            flattened.extend(round(value, 5) for value in point)
        frames.append(flattened)
        root_motion.append([round(value / scale, 5)
                            for value in _vector_subtract(root, origin)])

    result = {
        "schemaVersion": 1,
        "id": spec["id"],
        "label": spec.get("label", spec["id"]),
        "source": spec.get("source", {}),
        "sourceRate": source_rate,
        "sampleRate": sample_rate,
        "sourceFrameRange": [start + 1, start + window_frames],
        "sourceTimeRangeSec": [round(start / source_rate, 4),
                               round((start + window_frames) / source_rate, 4)],
        "durationSec": round(len(frames) / sample_rate, 4),
        "joints": spec["joints"],
        "normalization": {"rootRelative": True, "bodyScale": round(scale, 5)},
        "frames": frames,
        "rootMotion": root_motion,
    }
    save(output, result)
    return output, result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    project_path = pathlib.Path(args.project).resolve()
    project = load(project_path)
    specs = project.get("motionClips", [])
    if not specs:
        raise SystemExit(f"no motionClips configured in {project_path}")
    for spec in specs:
        output, clip = build_clip(spec, project_path.parent)
        start, end = clip["sourceTimeRangeSec"]
        print(f'wrote {output}  {clip["durationSec"]:.2f}s @ {clip["sampleRate"]}fps '
              f'(source {start:.2f}-{end:.2f}s)')


if __name__ == "__main__":
    main()
