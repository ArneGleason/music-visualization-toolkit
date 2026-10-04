"""Compile reviewed alignment candidates into the musical register and Blender data."""
import argparse
import copy
import difflib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dawproject import TempoCurve
from timeline import MusicalGrid, compile_timeline, load_project, validate_timeline


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=pathlib.Path)
    args = parser.parse_args()
    project, base = load_project(args.project)
    bm = json.loads((base / project["timing"]["beatmap"]).read_text(encoding="utf-8"))
    grid = MusicalGrid(bm)
    curve = TempoCurve([(p["beat"],p["bpm"],p["interpolation"]) for p in bm["tempo_map"]])
    fps = project["render"]["fps"]
    count = round(grid.duration*fps)
    timeline_path = base / project["timeline"]
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    imported = base / "generated/transcription/timeline.imported.json"
    if imported.exists() and json.loads(imported.read_text(encoding="utf-8")) != timeline:
        raise ValueError("Timeline changed since first-pass import; preserve those edits rather than re-importing")
    backup = base / "generated/transcription/timeline.before-first-alignment.json"
    if not backup.exists():
        save(backup, timeline)
    aligned = json.loads((base / "generated/transcription/phrases.aligned.json").read_text(encoding="utf-8"))
    # The arranged sheet controls spelling, including intentional typos.
    sheet = [line.strip() for line in (base / "lyrics/arranged.txt").read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.startswith("[")]
    adjustments_path = base / "lyrics/performed-adjustments.json"
    adjustments = json.loads(adjustments_path.read_text(encoding="utf-8")) if adjustments_path.exists() else {}
    raw = {}
    offset = project["vocalOrigin"]["masterSeconds"]
    for role in ("audio", "lead"):
        doc = json.loads((base / f"generated/transcription/{role}.whisper.raw.json").read_text(encoding="utf-8"))
        shift = 0 if role == "audio" else offset
        raw[role] = [{"text":w["word"],"start":w["start"]+shift,"end":w["end"]+shift}
                     for segment in doc["segments"] for w in segment["words"]]
    def normalize(value):
        return re.sub(r"[^a-z0-9]", "", value.lower().replace("’", "'"))

    def matched_edges(row, role):
        a,b = row["roughSpan"]
        candidates = [w for w in raw[role] if w["end"]>a-.15 and w["start"]<b+.15]
        matches = {}
        matcher = difflib.SequenceMatcher(None,[normalize(w["text"]) for w in row["words"]],
                                         [normalize(w["text"]) for w in candidates],autojunk=False)
        for block in matcher.get_matching_blocks():
            for i,j in zip(range(block.a,block.a+block.size),range(block.b,block.b+block.size)):
                matches[i]=candidates[j]
        return matches
    phrases = []
    issues = []

    def frame(t):
        return max(1,min(count+1, round(grid.sec(grid.position(t))*fps)+1))

    for row in aligned:
        words = row["words"]
        if not words:
            issues.append({"id":row["id"], "issue":"No aligned words"})
            continue
        master_edges, lead_edges = matched_edges(row,"audio"), matched_edges(row,"lead")
        for i, word in enumerate(words):
            # Independent master/original-lead agreement takes precedence over
            # forced alignment that can collapse or delay the opening syllable.
            m,l = master_edges.get(i),lead_edges.get(i)
            if m and l and abs(m["start"]-l["start"])<.15 and abs(m["end"]-l["end"])<.2 and m["end"]>m["start"]:
                word["stableStart"],word["stableEnd"] = word["start"],word["end"]
                word["start"],word["end"] = (m["start"]+l["start"])/2,(m["end"]+l["end"])/2
                word["sourceStart"],word["sourceEnd"] = word["start"]-offset,word["end"]-offset
                word["edgeSource"] = "master_and_original_lead_Whisper_agreement"
            else:
                word["edgeSource"] = "stable_ts_forced_alignment; review"
        if row["role"] == "primary":
            row["text"] = sheet[int(row["id"].split("-")[1])-1]
            tokens = row["text"].split()
            if len(tokens) == len(words)+1 and tokens[:2] == ["Every", "thing"]:
                first = words.pop(0)
                middle = first["start"]+(first["end"]-first["start"])*.6
                left, right = copy.deepcopy(first), copy.deepcopy(first)
                left["end"], right["start"] = middle, middle
                for part in (left, right):
                    part["edgeSource"] = "interpolated split of recognized Everything; review"
                words[:0] = [left, right]
            if len(tokens) != len(words):
                raise ValueError(f"Cannot preserve sheet spelling for {row['id']}: word count differs")
            for word, token in zip(words, tokens):
                word["recognizedText"] = word["text"]
                word["text"] = token
        change = adjustments.get(row["id"], {})
        for key in ("text", "role", "reviewStatus", "recognitionBasis"):
            if key in change:
                row[key] = change[key]
        if "words" in change:
            words = copy.deepcopy(change["words"])
            row["words"] = words
            if [w["text"] for w in words] != row["text"].split():
                raise ValueError(f"Performed text/word mismatch: {row['id']}")
        for edge in change.get("wordEdges", []):
            word = words[edge["index"]]
            if word["text"] != edge["text"]:
                raise ValueError(f"Adjustment token mismatch: {row['id']}")
            word.update(start=edge["start"], end=edge["end"], edgeSource=edge["basis"])
        for i, word in enumerate(words):
            word["sourceStart"],word["sourceEnd"] = word["start"]-offset,word["end"]-offset
            word["id"] = row["id"]+f"-w{i+1:02d}"
            word["startFrame"] = frame(word["start"])
            word["endFrameExclusive"] = max(word["startFrame"]+1, frame(word["end"]))
            word["musicalStart"] = grid.position(word["start"]).text()
            word["musicalEnd"] = grid.position(word["end"]).text()
            if word["end"]-word["start"] < .025:
                issues.append({"id":word["id"],"issue":"Very short/zero acoustic edge; review", "seconds":word["start"]})
            if "interpolated" in word["edgeSource"]:
                issues.append({"id":word["id"],"issue":"Interpolated repetition or spelling boundary; review", "seconds":word["start"]})
            if word.get("zoomCue"):
                issues.append({"id":word["id"],"issue":f"Zoom {word['zoomCue']}/9: measured vowel attack; listening verification", "seconds":word["start"]})
        row["start"] = min(w["start"] for w in words)
        row["end"] = max(w["end"] for w in words)
        row["startFrame"] = frame(row["start"])
        row["endFrameExclusive"] = max(row["startFrame"]+1,frame(row["end"]))
        phrases.append(row)
        tracks = [t for t in timeline["tracks"] if t["id"] == ("lyrics" if row["role"]=="primary" else "echoes")]
        track = tracks[0]
        existing = next((x for x in track["items"] if x["id"]==row["id"]), None)
        if existing is None:
            existing = {"id":row["id"],"lyricOrigin":"improv"}
            track["items"].append(existing)
        if existing.get("timingStatus") not in (None,"unplaced","first_pass"):
            continue  # Never overwrite later human review with an automatic rerun.
        existing.update(text=row["text"], start=grid.position(row["start"]).text(),
                        end=grid.position(row["end"]).text(), timingStatus="first_pass",
                        words=words, reviewStatus=row["reviewStatus"],
                        sourceAlignment="generated/transcription/phrases.aligned.json")
    timeline["tracks"][0]["label"] = "Primary lyrics — first alignment pass"
    errors = validate_timeline(timeline,grid)
    if errors:
        raise ValueError(errors)
    save(timeline_path,timeline)
    save(imported,timeline)
    compile_timeline(project,base)
    beats = []
    for bar in bm["bars"]:
        for i,t in enumerate(bar["beats"]):
            if 0 <= t < grid.duration:
                beats.append({"time":t,"bar":bar["bar"],"beat":i+1,
                              "frame":frame(t),"bpm":curve.bpm(bar["beat"]+i)})
    # Frame 1 precedes the first complete beat because the master starts at 2.4.
    if beats and beats[0]["frame"]>1:
        beats.insert(0,{"time":0,"bar":2,"beat":4,"frame":1,"bpm":curve.bpm(bm["zero_beat"])})
    primary = sorted((p for p in phrases if p["role"]=="primary"),key=lambda p:p["start"])
    for a,b in zip(primary,primary[1:]):
        a["endFrameExclusive"] = min(a["endFrameExclusive"],b["startFrame"])
        for w in a["words"]:
            w["endFrameExclusive"]=min(w["endFrameExclusive"],a["endFrameExclusive"])
    data = {"title":project["title"],"fps":fps,"frames":count,"duration":grid.duration,
            "timingResidualSeconds":.0021960440014368,"timingResidualAccepted":True,
            "phrases":sorted(phrases,key=lambda p:p["start"]),"beats":beats,
            "reviewStatus":"first_pass; arranged spelling preserved; interpolated edges require listening review",
            "unplaced":["lyr-024: Loose it. — not independently recognized; possible omitted line/echo"],
            "issues":issues}
    from waveforms import _envelope
    peaks,_ = _envelope(pathlib.Path(project["sources"]["leadRenaissance"]),fps)
    data["envelopes"] = {"lead":[0]*round(offset*fps)+peaks}
    save(base/"generated/animatic/animatic-data.json",data)
    print(len(phrases),"phrases",sum(len(p["words"]) for p in phrases),"words",len(issues),"edge flags",count,"frames")


if __name__ == "__main__":
    main()
