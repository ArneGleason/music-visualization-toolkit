"""Render a bass-driven oscilloscope comparison in Blender from the approved still.

Run with Blender -b -P tools/screen_sync_pilot.py -- [--preview].
Outputs remain under out/screen_sync_pilot/. No generated-media API is used.
"""
import argparse
import array
import json
import math
import pathlib
import subprocess
import sys

import bpy

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "screen_sync_pilot"
FPS, FIRST, END = 24, 86, 155
W, H = 1536, 864
CX, CY, RX, RY = 780, 314, 254, 257
RATE = 8000


def command(args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def material(name, color, alpha=1):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = (*color, 1)
    if alpha < 1:
        mat.surface_render_method = "BLENDED"
        transparent = nodes.new("ShaderNodeBsdfTransparent")
        mix = nodes.new("ShaderNodeMixShader")
        mix.inputs[0].default_value = alpha
        mat.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
        mat.node_tree.links.new(emit.outputs[0], mix.inputs[2])
        mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    else:
        mat.node_tree.links.new(emit.outputs[0], output.inputs[0])
    return mat


def point(x, y, z):
    return (x - W / 2, H / 2 - y, z)


def line(name, coords, width, mat, z):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = width
    curve.bevel_resolution = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(coords) - 1)
    for p, (x, y) in zip(spline.points, coords):
        p.co = (*point(x, y, z), 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def disk(name, mat, scale=1, z=.03):
    vertices = [point(CX, CY, z)]
    vertices += [point(CX + RX * scale * math.cos(i * math.tau / 128),
                       CY + RY * scale * math.sin(i * math.tau / 128), z)
                 for i in range(128)]
    faces = [(0, 1 + i, 1 + (i + 1) % 128) for i in range(128)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)


def setup(mode):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.compression = 15
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.world = bpy.data.worlds.new("Black world")
    scene.world.color = (0, 0, 0)
    bpy.ops.object.camera_add(location=(0, 0, 1000))
    camera = bpy.context.object
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = W
    scene.camera = camera
    bpy.ops.mesh.primitive_plane_add(size=2)
    plane = bpy.context.object
    plane.scale = (W / 2, H / 2, 1)
    mat = material("Approved photographic plate", (1, 1, 1))
    texture = mat.node_tree.nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(ROOT / "codex/out/obs_console_macro_b.jpg"))
    emission = next(n for n in mat.node_tree.nodes if n.type == "EMISSION")
    mat.node_tree.links.new(texture.outputs["Color"], emission.inputs["Color"])
    plane.data.materials.append(mat)

    if mode == "replacement":
        # Nested disks soften the boundary and recreate dark curved glass.
        disk("Edge of clean display", material("Glass edge", (.016, .014, .008)), 1)
        for i in range(24):
            s = .99 - i * .012
            a = .018 + i * .00042
            disk("Glass shading", material("Glass shading", (a, a * .83, a * .48)), s, .04+i*.001)
        grid = material("Subdued amber graticule", (.052, .035, .013))
        line("Horizontal grid", [(CX-244, CY), (CX+244, CY)], .45, grid, .10)
        line("Vertical grid", [(CX, CY-245), (CX, CY+245)], .45, grid, .10)
        for d in range(-220, 221, 20):
            line("Grid tick", [(CX+d, CY-3), (CX+d, CY+3)], .4, grid, .10)
            line("Grid tick", [(CX-3, CY+d), (CX+3, CY+d)], .4, grid, .10)
    elif mode == "layered":
        disk("Dim original display", material("Original at reduced strength", (0, 0, 0), .55))
    labels = {"original": "ORIGINAL — generated still pattern",
              "replacement": "A — bass replaces the original trace",
              "layered": "B — bass over the dimmed original"}
    bpy.ops.object.text_add(location=(-725, 386, .5))
    label = bpy.context.object
    label.data.body = labels[mode]
    label.data.size = 23
    label.data.materials.append(material("Label", (.9, .85, .7)))
    return scene, camera


def read_bass():
    local = json.loads((ROOT / "projects/rivers-of-mars/project.local.json").read_text())
    stems = pathlib.Path(local["sources"]["stems"])
    files = list(stems.glob("*Bass*restored.wav"))
    if len(files) != 1:
        raise ValueError(f"Expected one restored bass stem, got {len(files)}")
    raw = command(["ffmpeg", "-v", "error", "-i", str(files[0]), "-ac", "1",
                   "-af", f"highpass=f=25,lowpass=f=180,aresample={RATE}",
                   "-f", "f32le", "-"])
    samples = array.array("f")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    data = json.loads((ROOT / "projects/rivers-of-mars/generated/waveforms.json").read_text())
    offset = next(t["offsetSec"] for t in data["tracks"] if t["id"] == "bass")
    excerpt = sorted(abs(x) for x in samples[int((FIRST/FPS-offset)*RATE):
                                            int((END/FPS-offset)*RATE)])
    norm = max(excerpt[int(len(excerpt)*.985)], .0001)
    return samples, offset, norm


def waveform(samples, offset, norm, song_frame):
    center = (song_frame / FPS - offset) * RATE
    start = int(center - .032 * RATE)
    # Select the closest rising crossing in +/- 6 ms; preserve bounded timing.
    crossings = [i for i in range(max(1, start-48), min(len(samples)-513, start+49))
                 if samples[i-1] <= 0 < samples[i]]
    if crossings:
        start = min(crossings, key=lambda i: abs(i-start))
    coords = []
    for i in range(257):
        idx = max(0, min(len(samples)-1, start+i*2))
        value = max(-1.15, min(1.15, samples[idx]/norm))
        coords.append((CX-234+i*468/256, CY-value*96))
    return coords


def render(mode, samples, offset, norm, preview):
    folder = OUT / mode
    folder.mkdir(parents=True, exist_ok=True)
    scene, camera = setup(mode)
    trace_objects = []
    gold = (1, .48, .075)
    cyan = (.18, .85, .73)
    color = gold if mode == "replacement" else cyan
    mats = [material("Trace glow", color, .10),
            material("Trace soft edge", color, .25),
            material("Trace", color),
            material("Trace bright core", (.95, .98, .82))]
    frames = [30] if preview else range(END-FIRST)
    for i in frames:
        for obj in trace_objects:
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.curves.remove(data)
        trace_objects.clear()
        if mode != "original":
            for lag, alpha in [(2, .10), (1, .20)]:
                trail = material(f"Phosphor persistence {i} {lag}", color, alpha)
                trace_objects.append(line("Persistence", waveform(samples, offset, norm, FIRST+i-lag),
                                          1.2, trail, .15))
            coords = waveform(samples, offset, norm, FIRST+i)
            for width, mat in zip([7, 3.4, 1.35, .45], mats):
                trace_objects.append(line("Live bass", coords, width, mat, .20+(.01/width)))
        progress = i / (END-FIRST-1)
        camera.data.ortho_scale = W / (1.012 + .018*progress)
        camera.location.x = progress*5
        camera.location.y = -progress*2
        scene.render.filepath = str(folder / f"{i:04d}.png")
        bpy.ops.render.render(write_still=True)
    if not preview:
        command(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i",
                 str(folder / "%04d.png"), "-ss", str(FIRST/FPS), "-i",
                 str(ROOT / "audio/song.wav"), "-t", str((END-FIRST)/FPS),
                 "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "17",
                 "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                 "-movflags", "+faststart", str(OUT / f"{mode}.mp4")])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--assemble-only", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    OUT.mkdir(parents=True, exist_ok=True)
    samples, offset, norm = read_bass()
    if not args.assemble_only:
        for mode in ["original", "replacement", "layered"]:
            render(mode, samples, offset, norm, args.preview)
    if not args.preview:
        # Take audio directly from the master to avoid accumulated AAC padding
        # at comparison joins. All six excerpts are exactly 69 frames long.
        args_ff = ["ffmpeg", "-y", "-v", "error"]
        for mode in ["original", "replacement", "layered"]:
            args_ff += ["-i", str(OUT / f"{mode}.mp4")]
        args_ff += ["-i", str(ROOT / "audio/song.wav")]
        filters = [f"[{i}:v]setpts=PTS-STARTPTS,split=2[v{i}a][v{i}b]" for i in range(3)]
        filters += ["[v0a][v1a][v2a][v0b][v1b][v2b]concat=n=6:v=1:a=0[v]",
                    f"[3:a]atrim=start={FIRST/FPS}:end={END/FPS},asetpts=PTS-STARTPTS,"
                    "asplit=6[a0][a1][a2][a3][a4][a5]",
                    "[a0][a1][a2][a3][a4][a5]concat=n=6:v=0:a=1[a]"]
        command(args_ff + ["-filter_complex", ";".join(filters), "-map", "[v]",
                 "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                 str(OUT / "comparison.mp4")])
        (OUT / "parameters.json").write_text(json.dumps({
            "fps": FPS, "song_frames": [FIRST, END], "stem_offset_sec": offset,
            "signal_rate": RATE, "band_hz": [25, 180], "window_ms": 64,
            "trigger_search_ms": 6, "normalization": norm,
            "plate": "codex/out/obs_console_macro_b.jpg",
            "screen_ellipse_px": [CX, CY, RX, RY],
            "scope": "still plate with shared camera transform; no motion tracking",
        }, indent=2))
    print("SCREEN TEST COMPLETE", OUT)


if __name__ == "__main__":
    main()
