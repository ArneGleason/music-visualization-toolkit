"""Keep author spelling, acoustic candidates and musical/frame positions separate."""
from array import array
import csv
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from timeline import MusicalGrid, compile_timeline
from PIL import Image, ImageDraw


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    timeline = load(BASE / "timeline.json")
    author = timeline["tracks"][0]["items"]
    lead = load(BASE / "generated/transcription/alignment-v002/words.json")
    master = load(BASE / "generated/transcription/master-crosscheck-v002/words.json")
    mapping = load(BASE / "lyrics/alignment-token-map-v001.json")
    grid = MusicalGrid(load(BASE / "generated/beatmap.json"))
    config = load(BASE / "project.json")
    fps = config["render"]["fps"]
    duration = grid.duration
    # Cover the entire master with whole video frames. The final extra display
    # frame is technical padding, not a new musical/lyric event.
    frames = math.ceil(duration * fps)
    spoken = []
    for a, b in zip(lead["words"], master["words"]):
        assert a["text"] == b["text"]
        selected = dict(a)
        selected["flags"] = list(a["flags"])
        selected["masterCrosscheck"] = {k: b[k] for k in ["start", "end", "alignment_score"]}
        selected["edgeSource"] = "active_lead_ctc"
        # The first attack can precede the enabled dry stem's clip edge. Keep
        # the final-master candidate, visibly flagged, instead of clipping it.
        if a["id"] == "section-01-w001" and b["start"] < a["start"] - .2:
            selected.update(start=b["start"], end=b["end"], edgeSource="master_ctc_opening_candidate")
            selected["flags"].append("opening_attack_review")
        if abs(a["start"] - b["start"]) > .12:
            selected["flags"].append("master_start_disagreement")
        if abs(a["end"] - b["end"]) > .2:
            selected["flags"].append("master_end_disagreement")
        for key in ["start", "end"]:
            position = grid.position(selected[key]).text()
            selected["musical" + key.title()] = position
        selected["startFrame"] = round(grid.sec(selected["musicalStart"]) * fps)
        selected["endFrameExclusive"] = max(selected["startFrame"] + 1,
            round(grid.sec(selected["musicalEnd"]) * fps))
        spoken.append(selected)
    assert len(spoken) == 306
    section_words = {p["id"]: [w for w in spoken if w["phrase_id"] == p["id"]] for p in lead["phrases"]}
    lines = []
    for source in author:
        entries = [m for m in mapping if m["lineId"] == source["id"]]
        raw_tokens = source["text"].split()
        display_tokens = []
        for token in raw_tokens:
            if token == "—":
                display_tokens[-1] += " —"
            else:
                display_tokens.append(token)
        assert len(entries) == len(display_tokens)
        display_words = []
        for index, (entry, display) in enumerate(zip(entries, display_tokens), 1):
            words = section_words[f"section-{entry['section']:02}"][entry["startTokenIndex"]:entry["endTokenIndexExclusive"]]
            assert [w["text"] for w in words] == entry["spokenWords"]
            a, b = min(w["start"] for w in words), max(w["end"] for w in words)
            flags = sorted({f for w in words for f in w["flags"]})
            if len(words) > 1:
                flags.append("numeric_pronunciation_review")
            display_words.append({"id": f"{source['id']}-w{index:03}", "text": display,
                "start": a, "end": b, "sourceStart": a, "sourceEnd": b,
                "musicalStart": grid.position(a).text(), "musicalEnd": grid.position(b).text(),
                "startFrame": round(grid.sec(grid.position(a)) * fps),
                "endFrameExclusive": max(round(grid.sec(grid.position(a)) * fps) + 1, round(grid.sec(grid.position(b)) * fps)),
                "spokenWordIds": [w["id"] for w in words], "flags": flags,
                "status": "machine_candidate_needs_listening"})
        assert " ".join(w["text"] for w in display_words) == source["text"]
        a, b = min(w["start"] for w in display_words), max(w["end"] for w in display_words)
        line = {**source, "start": grid.position(a).text(), "end": grid.position(b).text(),
                "sourceStart": a, "sourceEnd": b, "words": display_words,
                "timingStatus": "machine_candidate_needs_listening", "timingSource": "generated/transcription/alignment-v002/words.json"}
        lines.append(line)
    timeline["tracks"][0].update(label="Author lyrics — acoustic timing draft", items=lines)
    timeline["provenance"].update(status="first_timed_draft_not_listening_approved",
        wordTimingPolicy="Independent CTC edges; no beat snapping, next-onset filling or invented repeats. Original numeric spelling retained.")
    write(BASE / "timeline.json", timeline)
    compiled = compile_timeline(config, BASE)
    # Address listings get individual pages. Four-line refrains stay together.
    groups = []
    for section in range(1, 10):
        part = [l for l in lines if l["section"] == f"section {section}"]
        chunks = [[l] for l in part] if section in [2, 4, 6, 8] else [part[i:i+4] for i in range(0, len(part), 4)]
        groups.extend(chunks)
    pages = []
    for group in groups:
        page = {"id": f"page-{len(pages)+1:03}", "lineIds": [l["id"] for l in group],
                "lines": group, "words": [w for l in group for w in l["words"]],
                "start": min(l["sourceStart"] for l in group), "end": max(l["sourceEnd"] for l in group)}
        if pages and page["start"] < pages[-1]["end"]:
            previous = pages[-1]
            previous["lineIds"] += page["lineIds"]
            previous["lines"] += page["lines"]
            previous["words"] += page["words"]
            previous["end"] = max(previous["end"], page["end"])
        else:
            pages.append(page)
    for i, page in enumerate(pages):
        previous_end = pages[i-1]["end"] if i else 0
        next_start = pages[i+1]["start"] if i+1 < len(pages) else duration
        page["displayStartFrame"] = max(0, round(max(previous_end, page["start"] - .3) * fps))
        page["displayEndFrameExclusive"] = min(frames, round(min(next_start, page["end"] + .45) * fps))
    for i, page in enumerate(pages[:-1]):
        # A hold must end at the next page's preview, rather than at its vocal
        # attack; otherwise the rest label can reappear over that next page.
        page["displayEndFrameExclusive"] = min(page["displayEndFrameExclusive"], pages[i+1]["displayStartFrame"])
    out = BASE / "generated/animatic"
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    fonts = ROOT / "projects/together-anyways/generated/animatic/assets"
    for name in ["BarlowSemiCondensed-SemiBold.ttf", "OFL.txt"]:
        if not (assets / name).is_file():
            shutil.copy2(fonts / name, assets / name)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(BASE / "generated/source/master.wav"),
        "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    samples = array("h")
    samples.frombytes(pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    env = []
    for i in range(frames):
        chunk = samples[i*2000:(i+1)*2000]
        env.append(math.sqrt(sum(v*v for v in chunk)/max(1, len(chunk))) / 32768)
    image = Image.new("RGBA", (1280, 720))
    draw = ImageDraw.Draw(image)
    for x in range(64, 1216, 3):
        v = env[min(frames-1, round((x-64)/1152*(frames-1)))]
        height = max(1, 38 * min(1, v * 3))
        draw.line((x, 640-height, x, 640+height), fill=(65, 150, 150, 190), width=2)
    beats = []
    for bar in grid.data["bars"]:
        for j, sec in enumerate(bar["beats"], 1):
            if 0 <= sec < duration:
                beat = {"time": sec, "bar": bar["bar"], "beat": j}
                beats.append(beat)
                x = 64 + 1152 * sec/duration
                draw.line((x, 686, x, 699 if j == 1 else 692), fill=(230, 220, 190, 150))
    image.save(assets / "timing-overview.png")
    data = {"title": config["title"], "fps": fps, "frames": frames, "duration": duration,
        "pages": pages, "phrases": lines, "spokenWords": spoken, "beats": beats,
        "reviewStatus": "Machine timing draft; numbers, variants, attacks and held endings require listening approval"}
    write(assets / "lyric-timing.json", data)
    write(BASE / "generated/lyric-timing-v001.json", data)
    with (BASE / "generated/lyric-timing-v001.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "section", "start_seconds", "end_seconds", "start_bar_beat", "end_bar_beat", "text", "status"])
        for line in lines:
            writer.writerow([line["id"], line["section"], line["sourceStart"], line["sourceEnd"], line["start"], line["end"], line["text"], line["timingStatus"]])
    print(json.dumps({"lines": len(lines), "displayTokens": sum(len(l["words"]) for l in lines),
        "spokenWordCandidates": len(spoken), "pages": len(pages), "frames": frames,
        "timingStatus": data["reviewStatus"]}, indent=2))


if __name__ == "__main__":
    main()
