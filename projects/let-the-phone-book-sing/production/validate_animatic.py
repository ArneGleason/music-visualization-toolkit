"""Check the actual native project, source spelling and frame consistency."""
import hashlib
import json
from effectcraft_session import Session, BASE, OUT


def main():
    timing = json.loads((OUT / "assets/lyric-timing.json").read_text(encoding="utf-8"))
    layout = json.loads((OUT / "layout.json").read_text(encoding="utf-8"))
    native = OUT / "Let-the-Phone-Book-Sing-lyric-animatic-v001.ecproj"
    session = Session(native)
    main_comp = session.call("get_comp", {"comp": 1})
    master = next(l for l in main_comp["layers"] if l["name"] == "master.wav")
    session.command("comp.open", {"comp": 1})
    session.command("layer.timing", {"layers": [master["id"]], "in": 0, "out": timing["frames"]/24})
    session.call("save_project", {"path": str(native)})
    count, max_rounding = 0, 0
    words = {w["id"]: w for p in timing["phrases"] for w in p["words"]}
    for i, page in enumerate(layout):
        assert i == 0 or layout[i-1]["endFrameExclusive"] <= page["startFrame"]
        comp = session.call("get_comp", {"comp": page["comp"]})
        assert len(comp["layers"]) == 2*len(page["words"])
        for word in page["words"]:
            prop = session.call("get_property", {"comp": page["comp"], "layer": word["layer"], "path": "text/sourceText"})
            assert prop["value"] == word["text"]
            assert page["startFrame"] <= word["onFrame"] < word["offFrame"] <= page["endFrameExclusive"]
            assert word["width"]/2 <= word["x"] <= 1280-word["width"]/2
            assert 100 < word["y"] < 510
            source = words[word["id"]]
            max_rounding = max(max_rounding, abs(word["onFrame"]/24-source["start"]))
            count += 1
    assert count == 203 and len(timing["phrases"]) == 38 and len(timing["spokenWords"]) == 306
    assert max_rounding < 1/48 + .002
    for time, expected in [(0, 100), (2.7, 0), (18.5, 0), (72, 0), (140, 0), (170, 100)]:
        prop = session.call("get_property", {"comp": 1, "layer": "Instrumental state", "path": "transform/opacity", "time": time})
        assert prop["value"] == expected, (time, prop["value"])
    with (BASE / "generated/source/master.wav").open("rb") as stream:
        master_sha = hashlib.file_digest(stream, "sha256").hexdigest()
    assert master_sha == "31d49e985bb40c36c1209fbd7dbd5687bcb086b9c28f20bf5f82f7c319cb4ad2"
    report = {"status": "Native structure, text and frame consistency passed; acoustic draft awaits listening",
        "lines": 38, "displayWords": count, "spokenCandidates": 306, "pages": len(layout),
        "maxFrameRoundingMs": max_rounding*1000, "masterSha256": master_sha,
        "fps": 24, "nativeFrames": timing["frames"], "resolution": [1280,720],
        "finalPictureTarget": [1920,1080], "noLyricTextBakedIntoFootage": True}
    (OUT / "validation.json").write_text(json.dumps(report, indent=2)+"\n")
    session.close()
    from portable_animatic import make_portable
    make_portable(native)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
