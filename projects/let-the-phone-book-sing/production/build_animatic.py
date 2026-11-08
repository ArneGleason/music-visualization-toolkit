"""Build editable native lyric pages and musical readouts, as in Together Anyways."""
import json
import math
from pathlib import Path
import time
from PIL import ImageFont
from effectcraft_session import Session, BASE, OUT


def main():
    data = json.loads((OUT / "assets/lyric-timing.json").read_text(encoding="utf-8"))
    fps, frames = data["fps"], data["frames"]
    target = OUT / "Let-the-Phone-Book-Sing-lyric-animatic-v001.ecproj"
    session = Session()
    started = time.monotonic()
    cmd = session.command
    ink, paper, muted, red, amber = "#11282d", "#f1dfb6", "#738e8b", "#ff684e", "#efb85b"
    fonts = {}

    def font(size):
        if size not in fonts:
            fonts[size] = ImageFont.truetype(str(OUT / "assets/BarlowSemiCondensed-SemiBold.ttf"), size)
        return fonts[size]

    def text(name, value, x, y, size, color, align="center"):
        bounds = font(size).getbbox(value, anchor="ls")
        baseline = y - (bounds[1] + bounds[3]) / 2
        lid = cmd("layer.newText", {"name": name, "text": value, "font": "Barlow Semi Condensed",
            "style": "SemiBold", "size": size, "fill": color, "position": [x, baseline], "justify": align})["layer"]
        return lid

    def rect(name, x, y, w, h, color):
        return cmd("layer.newShape", {"kind": "rect", "name": name, "size": [w, h],
            "fill": color, "strokeWidth": 0, "position": [x, y]})["layer"]

    def keys(lid, path, values, interpolation="hold"):
        unique = {round(t * fps) / fps: v for t, v in values}
        return session.call("add_keyframe", {"layer": lid, "path": path,
            "keys": [{"time": t, "value": v} for t, v in sorted(unique.items())],
            "interpolation": interpolation})

    main_comp = cmd("comp.new", {"name": "Let the Phone Book Sing — lyric timing draft v001",
        "width": 1280, "height": 720, "frameRate": fps, "duration": frames/fps, "background": ink})["comp"]
    rest_keys = [(0, 100)]
    layout = []
    folder = cmd("project.newFolder", {"name": "Editable lyric pages"})["item"]
    for page in data["pages"]:
        first, last = page["displayStartFrame"], page["displayEndFrameExclusive"]
        length = (last-first)/fps
        rest_keys.extend([(first/fps, 0), (last/fps, 100)])
        rows = []
        for size in [58, 54, 50, 46, 42]:
            rows = []
            for line in page["lines"]:
                row, used = [], 0
                for word in line["words"]:
                    width = font(size).getlength(word["text"])
                    gap = font(size).getlength(" ") + 6
                    if row and used+gap+width > 1110:
                        rows.append(row)
                        row, used = [], 0
                    row.append((word, width))
                    used += width + (gap if len(row)>1 else 0)
                if row:
                    rows.append(row)
            if len(rows)*(size+20) <= 350:
                break
        cid = cmd("comp.new", {"name": page["id"] + " " + page["lines"][0]["text"][:58],
            "width": 1280, "height": 720, "frameRate": fps, "duration": length})["comp"]
        cmd("project.move", {"items": [cid], "folder": folder})
        records = []
        for ri, row in enumerate(rows):
            gap = font(size).getlength(" ") + 6
            total = sum(w for _, w in row)+gap*(len(row)-1)
            x = (1280-total)/2
            y = 320 + (ri-(len(rows)-1)/2)*(size+20)
            for word, width in row:
                on = max(0, word["startFrame"]-first)
                off = min(last-first, max(on+1, word["endFrameExclusive"]-first))
                lid = text("Word " + word["id"], word["text"], x+width/2, y, size, muted)
                cmd("layer.setComment", {"layers": [lid], "comment": f"Acoustic candidate {word['start']:.3f}–{word['end']:.3f}s. Flags: {', '.join(word['flags'])}. No listening approval."})
                cmd("layer.addTextAnimator", {"layer": lid, "properties": ["fillColor"], "name": "Word reached"})
                keys(lid, "text/animators/animator/properties/fillColor", [(0, muted), (on/fps, paper)])
                color = amber if any(f != "text_review" for f in word["flags"]) else red
                underline = rect("Duration " + word["id"], x, y+size*.65, 1, 3, color)
                cmd("prop.set", {"layer": underline, "path": "transform/anchor", "value": [-.5, 0, 0]})
                cmd("layer.timing", {"layers": [underline], "in": on/fps, "out": off/fps})
                keys(underline, "transform/scale", [(on/fps, [100,100,100]),
                    (max(on,off-1)/fps, [width*100,100,100])], "linear")
                records.append({"id": word["id"], "text": word["text"], "layer": lid,
                    "durationLayer": underline, "onFrame": on+first, "offFrame": off+first,
                    "x": x+width/2, "width": width, "y": y})
                x += width + gap
        cmd("layer.select", {"layers": []})
        cmd("comp.open", {"comp": main_comp})
        page_layer = cmd("layer.addItem", {"item": cid, "time": first/fps, "position": [640,360]})["layer"]
        cmd("layer.setComment", {"layers": [page_layer], "comment": "Source lines: " + ", ".join(page["lineIds"])})
        cmd("comp.addMarker", {"time": first/fps, "comment": page["id"] + " / " + page["lines"][0]["section"]})
        layout.append({"page": page["id"], "comp": cid, "mainLayer": page_layer,
            "startFrame": first, "endFrameExclusive": last, "fontSize": size, "rows": len(rows), "words": records})
        cmd("comp.close", {"comp": cid})
        print("Built", page["id"], len(records), "words", flush=True)
    # Main readouts are overlays above all nested lyric pages. This also keeps
    # persistent titles visible with this pinned renderer's precomp bounds.
    rect("Title band", 640, 44, 1280, 88, ink)
    rect("Footer band", 640, 620, 1280, 200, ink)
    rect("Paper top rule", 640, 88, 1152, 2, paper)
    rect("Registration accent", 70, 42, 10, 30, red)
    text("Song title", data["title"], 350, 42, 32, paper)
    text("Pass label", "LYRIC TIMING / 01", 1070, 42, 22, muted)
    text("Review status", "DRAFT / NUMBERS, WORD ATTACKS AND HELD ENDINGS NEED REVIEW", 640, 590, 18, amber)
    text("Waveform label", "MASTER", 80, 610, 15, muted)
    cmd("file.import", {"paths": [str(OUT / "assets/timing-overview.png")], "addToComp": True})
    playhead = rect("Master playhead", 64, 650, 2, 90, red)
    keys(playhead, "transform/position", [(0, [64, 650, 0]), ((frames-1)/fps, [1216, 650, 0])], "linear")
    grid = text("Bar beat readout", "", 350, 548, 22, paper)
    keys(grid, "text/sourceText", [(b["time"], f"BAR {b['bar']:02} / BEAT {b['beat']}") for b in data["beats"]])
    clock = text("Master clock", "0:00", 720, 548, 22, paper)
    keys(clock, "text/sourceText", [(s, f"{s//60}:{s%60:02}") for s in range(math.ceil(data["duration"]))])
    pending = text("Instrumental state", "INSTRUMENTAL / VOCAL REST", 640, 320, 34, muted)
    keys(pending, "transform/opacity", rest_keys)
    cmd("file.import", {"paths": [str(BASE / "generated/source/master.wav")], "addToComp": True})
    audio_layer = next(l for l in session.call("get_comp", {"comp": main_comp})["layers"] if l["name"] == "master.wav")
    cmd("layer.timing", {"layers": [audio_layer["id"]], "in": 0, "out": frames/fps})
    cmd("layer.select", {"layers": []})
    cmd("time.set", {"time": 0})
    session.call("save_project", {"path": str(target)})
    for second in [2.7, 18.5, 72.0, 140.0]:
        session.call("render_frame", {"time": second, "path": str(OUT / f"preview-{second}.png"), "inline": False, "max_side": 1280})
    report = {"nativeProject": target.name, "frames": frames, "fps": fps,
        "duration": frames/fps, "masterDuration": data["duration"], "resolution": [1280,720],
        "pages": len(layout), "displayWords": sum(len(p["words"]) for p in layout),
        "spokenWordCandidates": len(data["spokenWords"]), "buildSeconds": time.monotonic()-started,
        "status": "Editable machine-timed review draft; no listening approval"}
    (OUT / "layout.json").write_text(json.dumps(layout,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT / "build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    session.close()
    # Portable footage links; nothing outside these known asset paths is edited.
    obj = json.loads(target.read_text(encoding="utf-8"))
    def relocate(value):
        if isinstance(value, str):
            for asset in ["master.wav", "timing-overview.png"]:
                if value.replace("\\", "/") == (OUT / "assets" / asset).as_posix():
                    return "assets/" + asset
            return value
        if isinstance(value, list):
            return [relocate(v) for v in value]
        if isinstance(value, dict):
            return {k: relocate(v) for k,v in value.items()}
        return value
    target.write_text(json.dumps(relocate(obj),ensure_ascii=False)+"\n",encoding="utf-8")
    from portable_animatic import make_portable
    make_portable(target)
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
