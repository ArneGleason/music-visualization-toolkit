"""Rebase known footage links without changing native layers or timing."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROJECT = BASE / "generated/animatic/Let-the-Phone-Book-Sing-lyric-animatic-v001.ecproj"


def make_portable(project=PROJECT):
    obj = json.loads(project.read_text(encoding="utf-8"))
    replacements = {"master.wav": "../source/master.wav",
                    "timing-overview.png": "assets/timing-overview.png"}
    found = []

    def visit(value):
        if isinstance(value, dict):
            path = value.get("path")
            if isinstance(path, str):
                name = path.replace("\\", "/").rsplit("/", 1)[-1]
                if name in replacements:
                    relative = replacements[name]
                    if not (project.parent / relative).is_file():
                        raise ValueError(f"Missing portable asset: {relative}")
                    value["path"] = relative
                    found.append(relative)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(obj)
    if set(found) != set(replacements.values()):
        raise ValueError(f"Expected master and waveform footage links, got {found}")
    project.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")
    return found


if __name__ == "__main__":
    print(make_portable())
