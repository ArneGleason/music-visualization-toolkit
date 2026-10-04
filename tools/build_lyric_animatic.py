"""Blender VSE rig for a lyric/timing review; all text remains editable."""
import json
import math
import pathlib
import sys
import textwrap
import time

import bpy


def main():
    project_file = pathlib.Path(sys.argv[sys.argv.index("--") + 1]).resolve()
    base = project_file.parent
    project = json.loads(project_file.read_text(encoding="utf-8"))
    local = json.loads(project_file.with_name("project.local.json").read_text(encoding="utf-8"))
    data = json.loads((base / "generated/animatic/animatic-data.json").read_text(encoding="utf-8"))
    out = base / "generated/animatic"
    fps = data["fps"]
    count = data["frames"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = project["title"] + " / lyric timing revision 03"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 6
    scene.frame_start = 1
    scene.frame_end = count
    scene.render.use_sequencer = True
    scene.view_settings.view_transform = "Standard"
    strips = scene.sequence_editor_create().strips
    font = bpy.data.fonts.load("C:/Windows/Fonts/arial.ttf")
    mono = bpy.data.fonts.load("C:/Windows/Fonts/consola.ttf")

    def text(name, body, y, size, color, channel, start, end, use_mono=False):
        start, end = max(1, start), min(count + 1, end)
        if end <= start:
            return
        strip = strips.new_effect(name=name, type="TEXT", channel=channel,
                                   frame_start=start, length=end-start)
        strip.text = body
        strip.font = mono if use_mono else font
        strip.font_size = size
        strip.color = color
        strip.blend_type = "ALPHA_OVER"
        strip.location = (.5, .5)
        strip.anchor_x = "CENTER"
        strip.anchor_y = "CENTER"
        strip.alignment_x = "CENTER"
        strip.transform.offset_y = y - 360
        return strip

    bg = strips.new_effect(name="Timing slate", type="COLOR", channel=1,
                            frame_start=1, length=count)
    bg.color = (.018, .026, .035)
    strips.new_sound("Original exported master", local["sources"]["audio"],
                      channel=2, frame_start=1)
    text("Title", project["title"], 650, 30, (.94, .91, .83, 1), 3, 1, count+1)
    text("Pass", "LYRIC TIMING / 03    •    NINE TELESCOPE ZOOM CUES",
         605, 19, (.52, .65, .69, 1), 4, 1, count+1)
    text("Guide", "Primary lyrics: ivory    •    active word: amber    •    performed repeats: cyan",
         135, 19, (.52, .65, .69, 1), 5, 1, count+1)
    text("Review", "24 fps  |  frame numbers and correction notes in the review viewer",
         75, 20, (.60, .65, .70, 1), 6, 1, count+1, True)
    primary = sorted((p for p in data["phrases"] if p["role"] == "primary"), key=lambda p:p["start"])
    for i, phrase in enumerate(primary):
        a = phrase["startFrame"]
        b = max(a+1, phrase["endFrameExclusive"])
        # Separate channels preserve genuinely overlapping phrase windows.
        channel = 10 + i % 3
        body = "\n".join(textwrap.wrap(phrase["text"], 46))
        text(phrase["id"], body, 425 + (i % 3)*0, 40,
             (.94,.91,.83,1), channel, a, b)
        text(phrase["id"]+" reference", phrase["id"]+"  /  "+phrase["section"],
             525, 20, (.57,.68,.71,1), 15+i%3, a, b, True)
        scene.timeline_markers.new(phrase["id"]+" "+phrase["text"][:40], frame=a)
        for j, word in enumerate(phrase["words"]):
            wa, wb = word["startFrame"], word["endFrameExclusive"]
            active = f"in  {word['zoomCue']}/9" if word.get("zoomCue") else word["text"]
            st = text(phrase["id"]+f" word {j+1}", active, 320, 48,
                       (1,.68,.23,1), 20+i%3, wa, max(wa+1,wb))
            if st:
                st["source_start_seconds"] = word["sourceStart"]
                st["source_end_seconds"] = word["sourceEnd"]
                st["master_start_seconds"] = word["start"]
                st["master_end_seconds"] = word["end"]
            if word.get("zoomCue"):
                scene.timeline_markers.new(f"TELESCOPE ZOOM {word['zoomCue']}/9",frame=wa)
    for phrase in data["phrases"]:
        if phrase["role"] == "primary":
            continue
        text(phrase["id"], phrase["text"], 425, 40,
             (.3,.84,.88,1), 25, phrase["startFrame"], phrase["endFrameExclusive"])
        for i, word in enumerate(phrase["words"]):
            text(phrase["id"]+f" repeat word {i+1}", word["text"], 320, 48,
                 (1,.68,.23,1), 26, word["startFrame"], word["endFrameExclusive"])
        scene.timeline_markers.new(phrase["id"], frame=phrase["startFrame"])
    for i, beat in enumerate(data["beats"]):
        a = beat["frame"]
        b = data["beats"][i+1]["frame"] if i+1<len(data["beats"]) else count+1
        text(f"Beat {beat['bar']}.{beat['beat']}",
             f"BAR {beat['bar']:02d}  •  BEAT {beat['beat']}    |    {beat['bpm']:.2f} BPM",
             570, 23, (.7,.8,.8,1), 30, a, b, True)
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    for frame in [1, 265, 1310, 1580, 2830, 3520, 4200, count]:
        scene.frame_set(frame)
        scene.render.filepath = str(out / f"preview-{frame}.png")
        bpy.ops.render.render(write_still=True)
    scene.render.image_settings.media_type = "VIDEO"
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.audio_codec = "AAC"
    scene.render.ffmpeg.audio_bitrate = 256
    scene.render.filepath = str(out / "A-Right-Little-Something-lyric-timing-v03.mp4")
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "A-Right-Little-Something-lyric-timing-v01.blend"))
    if "--render" in sys.argv:
        final = pathlib.Path(scene.render.filepath)
        pending = final.with_name(final.stem+".rendering.mp4")
        scene.render.filepath = str(pending)
        bpy.ops.render.render(animation=True)
        try:
            pending.replace(final)
        except PermissionError:
            # Windows may keep the previous movie open in a review browser.
            final = final.with_name(final.stem+f"-{time.time_ns()}.mp4")
            pending.replace(final)
        scene.render.filepath = str(final)
        (out / "current-media.json").write_text(json.dumps({"video":final.name+f"?v={final.stat().st_mtime_ns}"}), encoding="utf-8")
        pointer = base / "generated/review/current-render.json"
        pointer.parent.mkdir(parents=True, exist_ok=True)
        temp = pointer.with_suffix(".tmp")
        temp.write_text(json.dumps({"video":str(final),"master_start":1}), encoding="utf-8")
        temp.replace(pointer)
        bpy.ops.wm.save_as_mainfile(filepath=str(out / "A-Right-Little-Something-lyric-timing-v01.blend"))


main()
