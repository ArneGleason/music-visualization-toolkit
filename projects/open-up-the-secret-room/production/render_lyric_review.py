"""Render a frame-based lyric timing review from the project register."""
import argparse
import math
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from mvlib import load, to_frames
from timeline import MusicalGrid, load_project


STYLES = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Header,Segoe UI,26,&H00F0E9DD,&H00F0E9DD,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,55,55,38,1
Style: Clock,Consolas,22,&H00C2B6A0,&H00C2B6A0,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,9,55,55,42,1
Style: Lyric,Segoe UI,51,&H00F3EBDB,&H00F3EBDB,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,55,55,0,1
Style: Echo,Segoe UI,34,&H00DAC783,&H00DAC783,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,55,55,0,1
Style: Review,Segoe UI,21,&H008AC4FF,&H008AC4FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,55,55,0,1
Style: Footer,Consolas,20,&H00C2B6A0,&H00C2B6A0,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,1,55,55,38,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_time(frame, fps):
    # Quantize each boundary downward so the event starts on the chosen frame.
    centiseconds = frame * 100 // fps
    seconds, fraction = divmod(centiseconds, 100)
    minutes, second = divmod(seconds, 60)
    hour, minute = divmod(minutes, 60)
    return f"{hour}:{minute:02}:{second:02}.{fraction:02}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--version", type=int, default=1)
    args = parser.parse_args()
    project, base = load_project(args.project)
    beatmap = load(base / project["timing"]["beatmap"])
    timeline = load(base / project["timeline"])
    grid = MusicalGrid(beatmap)
    fps = project["render"]["fps"]
    frame_count = math.ceil(grid.duration * fps)
    length = frame_count / fps
    master = (base / project["sources"]["audio"]).resolve()
    out = base / "generated" / "animatic"
    out.mkdir(exist_ok=True, parents=True)
    name = f"Open-Up-the-Secret-Room-lyric-timing-v{args.version:03d}"
    movie, captions = out / (name + ".mp4"), out / (name + ".ass")
    if movie.exists() or captions.exists():
        parser.error("choose a new --version to preserve the existing render")
    events = []

    def frame(position):
        return to_frames(grid.sec(position), fps)

    def event(start, end, style, text, *, layer=0):
        if start < end:
            times = f"{ass_time(start, fps)},{ass_time(end, fps)}"
            events.append(f"Dialogue: {layer},{times},{style},,0,0,0,,{text}")

    event(0, frame_count, "Header", project["title"])
    beats = [(to_frames(second, fps), bar["bar"], index)
             for bar in beatmap["bars"]
             for index, second in enumerate(bar["beats"], 1)
             if 0 <= second < grid.duration]
    for i, (start, bar, beat) in enumerate(beats):
        end = beats[i + 1][0] if i + 1 < len(beats) else frame_count
        event(start, end, "Clock", f"BAR {bar:03d}   BEAT {beat}")

    tracks = {track["id"]: track["items"] for track in timeline["tracks"]}
    for cue in tracks["lyrics"]:
        number = cue["sourceLine"]
        if cue["timingStatus"] == "unplaced":
            window = cue.get("reviewWindow")
            if window is not None:
                start, end = (to_frames(window[edge], fps) for edge in ("start", "end"))
                event(start, end, "Review", r"{\pos(640,349)}" + f"Check line {number:02d}  |  {cue['text']}")
            continue

        start, end = (frame(cue[edge]) for edge in ("start", "end"))
        text = cue.get("displayText", cue["text"])
        event(start, end, "Footer", f"LINE {number:02d} / {len(tracks['lyrics']):02d}")
        if cue.get("reviewNote"):
            event(start, end, "Review", r"{\pos(640,405)}" + "Check wording or timing")

        # Divide the cue at actual word boundaries, keeping rests unhighlighted.
        boundaries = {start, end}
        spans = []
        for word in cue.get("words", []):
            left = max(start, frame(word["musicalStart"]))
            right = min(end, max(left + 1, frame(word["musicalEnd"])))
            if left >= right:
                continue
            spans.append((left, right, word))
            boundaries.update((left, right))
        edges = sorted(boundaries)
        for left, right in zip(edges, edges[1:]):
            active = next((word for a, b, word in spans if a <= left < b), None)
            marked = text
            if active is not None:
                a, b = active["charStart"], active["charEnd"]
                if text[a:b] == active["text"]:
                    marked = text[:a] + r"{\c&H0079BEFF&}" + text[a:b] + r"{\r}" + text[b:]
            event(left, right, "Lyric", r"{\pos(640,329)}" + marked)

    for cue in tracks.get("echoes", []):
        start, end = (frame(cue[edge]) for edge in ("start", "end"))
        event(start, end, "Echo", r"{\pos(640,467)}" + cue["text"])
        event(start, end, "Review", r"{\pos(640,510)}" + "Echo timing to review")
    captions.write_text(STYLES + "\n".join(events) + "\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-v", "error", "-nostdin", "-n", "-f", "lavfi",
        "-i", f"color=0x122027:s=1280x720:r={fps}:d={length:.6f}",
        "-i", str(master), "-vf", f"ass={captions.name}",
        "-af", f"apad=whole_dur={length:.6f}", "-frames:v", str(frame_count),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", movie.name,
    ], cwd=out, check=True)
    print(f"{movie} ({frame_count} frames at {fps} fps)")


if __name__ == "__main__":
    main()
