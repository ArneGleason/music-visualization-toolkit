"""Refine the accepted replacement: photographic grain, variable beam, 2x render."""
import json
import math
import pathlib
import sys

import bpy

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import screen_sync_pilot as base

OUT = base.ROOT / "out" / "screen_sync_refined"


def textured_glass():
    mat = base.material("Photographic screen grain", (1, 1, 1), .40)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    coords = nodes.new("ShaderNodeTexCoord")
    repeat = nodes.new("ShaderNodeVectorMath")
    repeat.operation = "MULTIPLY"
    repeat.inputs[1].default_value = (5, 6, 0)
    links.new(coords.outputs["Generated"], repeat.inputs[0])
    split = nodes.new("ShaderNodeSeparateXYZ")
    links.new(repeat.outputs[0], split.inputs[0])
    mirrored = nodes.new("ShaderNodeCombineXYZ")
    for axis in ["X", "Y"]:
        fold = nodes.new("ShaderNodeMath")
        fold.operation = "PINGPONG"
        fold.inputs[1].default_value = 1
        links.new(split.outputs[axis], fold.inputs[0])
        links.new(fold.outputs[0], mirrored.inputs[axis])
    scale = nodes.new("ShaderNodeVectorMath")
    scale.operation = "MULTIPLY"
    scale.inputs[1].default_value = (100/base.W, 80/base.H, 0)
    links.new(mirrored.outputs[0], scale.inputs[0])
    offset = nodes.new("ShaderNodeVectorMath")
    offset.operation = "ADD"
    offset.inputs[1].default_value = (645/base.W, 1-485/base.H, 0)
    links.new(scale.outputs[0], offset.inputs[0])
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(base.ROOT / "codex/out/obs_console_macro_b.jpg"),
                                         check_existing=True)
    links.new(offset.outputs[0], texture.inputs["Vector"])
    emission = next(n for n in nodes if n.type == "EMISSION")
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    base.disk("Trace-free photographic glass texture", mat, .985, .085)


def beam(name, coords, width, mat, z, frame, organic=True):
    smooth = []
    for j in range(len(coords)-1):
        y0 = coords[max(0, j-1)][1]
        y1, y2 = coords[j][1], coords[j+1][1]
        y3 = coords[min(len(coords)-1, j+2)][1]
        for k in range(4):
            t = k/4
            y = .5*((2*y1)+(-y0+y2)*t+(2*y0-5*y1+4*y2-y3)*t*t
                    +(-y0+3*y1-3*y2+y3)*t*t*t)
            smooth.append((coords[j][0]+t*(coords[j+1][0]-coords[j][0]), y))
    coords = smooth + [coords[-1]]
    obj = base.line(name, coords, width, mat, z)
    if organic:
        for i, p in enumerate(obj.data.splines[0].points):
            # Smooth, deterministic variations: thicker at slower vertical travel,
            # plus mild phosphor irregularity. No frame-to-frame random noise.
            left = coords[max(0, i-1)][1]
            right = coords[min(len(coords)-1, i+1)][1]
            slope = abs(right-left)/.9140625
            dwell = 1/math.sqrt(1+slope*slope)
            ripple = .13*math.sin(i*.065/4+frame*.10) + .08*math.sin(i*.19/4-frame*.035)
            p.radius = .70 + .55*dwell + ripple
    return obj


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    samples, offset, norm = base.read_bass()
    scene, camera = base.setup("replacement")
    scene.render.resolution_x = 2560
    scene.render.resolution_y = 1440
    textured_glass()
    for obj in scene.objects:
        if obj.type == "FONT":
            obj.data.body = "REFINED — textured glass / organic amber trace"
    gold = (1, .48, .075)
    mats = [base.material("Wide soft halo", gold, .035),
            base.material("Soft halo", gold, .075),
            base.material("Beam edge", gold, .18),
            base.material("Amber beam", gold),
            base.material("Hot filament", (1, .84, .43))]
    trails = [base.material("Older persistence", gold, .065),
              base.material("Recent persistence", gold, .13)]
    objects = []
    preview = "--preview" in sys.argv
    frames = [45] if preview else range(base.END-base.FIRST)
    for i in frames:
        for obj in objects:
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.curves.remove(data)
        objects.clear()
        for lag, mat in zip([2, 1], trails):
            coords = base.waveform(samples, offset, norm, base.FIRST+i-lag)
            objects.append(beam("Persistence", coords, 1, mat, .15, i-lag))
        coords = base.waveform(samples, offset, norm, base.FIRST+i)
        for width, mat in zip([9, 5.5, 2.7, 1.15, .40], mats):
            objects.append(beam("Live bass", coords, width, mat, .20+.01/width, i))
        progress = i/(base.END-base.FIRST-1)
        camera.data.ortho_scale = base.W/(1.012+.018*progress)
        camera.location.x = progress*5
        camera.location.y = -progress*2
        scene.render.filepath = str(OUT / f"{i:04d}.png")
        bpy.ops.render.render(write_still=True)
    if not preview:
        base.command(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-i",
                      str(OUT / "%04d.png"), "-ss", str(base.FIRST/24), "-i",
                      str(base.ROOT / "audio/song.wav"), "-t", str(69/24),
                      "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264",
                      "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                      "-movflags", "+faststart", str(OUT / "refined.mp4")])
        # Old/new/old/new with identical master audio and no encoder-padding joins.
        filters = [
            "[0:v]setpts=PTS-STARTPTS,split=2[o0][o1]",
            "[1:v]setpts=PTS-STARTPTS,split=2[n0][n1]",
            "[o0][n0][o1][n1]concat=n=4:v=1:a=0[v]",
            f"[2:a]atrim=start={base.FIRST/24}:end={base.END/24},asetpts=PTS-STARTPTS,"
            "asplit=4[a0][a1][a2][a3]",
            "[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]"]
        base.command(["ffmpeg", "-y", "-v", "error", "-i",
                      str(base.OUT / "replacement.mp4"), "-i", str(OUT / "refined.mp4"),
                      "-i", str(base.ROOT / "audio/song.wav"), "-filter_complex",
                      ";".join(filters), "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                      "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                      "-movflags", "+faststart", str(OUT / "comparison.mp4")])
        (OUT / "parameters.json").write_text(json.dumps({
            "source_frames": [86, 155], "fps":24, "render_size":[2560,1440],
            "delivery_size":[1280,720], "texture_source_region":[645,405,745,485],
            "texture_method":"mirror-repeat trace-free original screen patch, alpha 0.40",
            "beam":"slope-dependent radius plus slowly varying deterministic modulation",
            "audio_mapping":"identical to screen_sync_pilot",
        }, indent=2))
    print("REFINED SCOPE COMPLETE")


if __name__ == "__main__":
    main()
