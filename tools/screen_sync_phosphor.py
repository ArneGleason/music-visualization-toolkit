"""CRT-inspired screen study: beam dwell, accumulated phosphor, optional dual audio.

Blender -b -t 4 -P tools/screen_sync_phosphor.py -- [--preview] [--assemble-only]
All media is local under out/screen_sync_phosphor; no generation service is used.
"""
import argparse
import array
import json
import math
import pathlib
import sys

import bpy
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import screen_sync_pilot as base
import screen_sync_refine as refined

OUT = base.ROOT / "out" / "screen_sync_phosphor"
N = 768
SUBSTEPS = 8
FAST_HALF = .030
SLOW_HALF = .160
PX = np.linspace(-base.RX, base.RX, N, dtype=np.float32)
PY = np.linspace(-base.RY, base.RY, N, dtype=np.float32)[:, None]
RAD = np.sqrt((PX[None, :]/base.RX)**2+(PY/base.RY)**2)
APERTURE = np.clip((.990-RAD)/.018, 0, 1)
APERTURE *= APERTURE*(3-2*APERTURE)
GRAIN = np.clip(1+np.random.default_rng(8025).normal(0, .085, (N, N)), .70, 1.30)


def float_image(name, rgba):
    image = bpy.data.images.new(name, width=N, height=N, alpha=True, float_buffer=True)
    image.colorspace_settings.name = "Non-Color"
    image.pixels.foreach_set(rgba.astype(np.float32).ravel())
    image.update()
    return image


def image_plane(name, image, z, additive=False):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.surface_render_method = "BLENDED"
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Linear"
    emission = nodes.new("ShaderNodeEmission")
    links.new(tex.outputs["Color"], emission.inputs["Color"])
    clear = nodes.new("ShaderNodeBsdfTransparent")
    output = nodes.new("ShaderNodeOutputMaterial")
    if additive:
        add = nodes.new("ShaderNodeAddShader")
        links.new(clear.outputs[0], add.inputs[0])
        links.new(emission.outputs[0], add.inputs[1])
        links.new(add.outputs[0], output.inputs[0])
    else:
        mix = nodes.new("ShaderNodeMixShader")
        links.new(tex.outputs["Alpha"], mix.inputs[0])
        links.new(clear.outputs[0], mix.inputs[1])
        links.new(emission.outputs[0], mix.inputs[2])
        links.new(mix.outputs[0], output.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=2, location=base.point(base.CX, base.CY, z))
    plane = bpy.context.object
    plane.name = name
    plane.scale = (base.RX, base.RY, 1)
    plane.data.materials.append(mat)


def glass_details():
    # Static dirt sits in front of the trace. It is not random flicker.
    rng = np.random.default_rng(8024)
    rgba = np.zeros((N, N, 4), dtype=np.float32)
    rgba[:, :, :3] = (.012, .008, .004)
    alpha = rgba[:, :, 3]
    for _ in range(1100):
        x, y = rng.integers(5, N-5, size=2)
        if RAD[y, x] > .975:
            continue
        radius = float(rng.uniform(.4, 1.3))
        strength = float(rng.uniform(.14, .45))
        if RAD[y, x] < .70:
            strength *= .55
        dx = np.arange(-4, 5)
        blob = np.exp(-(dx[None, :]**2+dx[:, None]**2)/(2*radius*radius))
        alpha[y-4:y+5, x-4:x+5] += strength*blob
    alpha[:] = np.clip(alpha, 0, .45)*APERTURE
    image_plane("Fixed glass dust above phosphor", float_image("Glass dirt", rgba), .28)
    # Sparse real-looking hairline scuffs; no bright central grid.
    dark = base.material("Fine glass scuffs", (.12, .085, .035), .16)
    for x, y, length, angle in [(632, 442, 19, -.6), (905, 142, 13, .5),
                                (680, 188, 9, -.3), (874, 474, 23, .3),
                                (725, 514, 11, -.6)]:
        coords = [(x + k*length/10, y+math.sin(k/10)*length*angle) for k in range(11)]
        base.line("Glass hairline", coords, .35, dark, .29)
    ticks = base.material("Peripheral calibration", (.15, .095, .032), .48)
    for index in range(36):
        theta = index*math.tau/36
        inner = .878 if index % 3 == 0 else .906
        outer = .931
        coords = [(base.CX+base.RX*r*math.cos(theta),
                   base.CY+base.RY*r*math.sin(theta)) for r in [inner, outer]]
        base.line("Rim calibration", coords, .65 if index % 3 == 0 else .4, ticks, .30)
    arc = [(base.CX+base.RX*.947*math.cos(t),
            base.CY+base.RY*.947*math.sin(t)) for t in np.linspace(0, math.tau, 180)]
    base.line("Subtle calibration ring", arc, .3, ticks, .30)


def read_drums():
    local = json.loads((base.ROOT / "projects/rivers-of-mars/project.local.json").read_text())
    files = list(pathlib.Path(local["sources"]["stems"]).glob("*Drum Kit*restored.wav"))
    if len(files) != 1:
        raise ValueError("Expected one restored Drum Kit stem")
    raw = base.command(["ffmpeg", "-v", "error", "-i", str(files[0]), "-ac", "1",
                        "-af", "highpass=f=25,lowpass=f=240,aresample=8000",
                        "-f", "f32le", "-"])
    samples = array.array("f")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    data = json.loads((base.ROOT / "projects/rivers-of-mars/generated/waveforms.json").read_text())
    offset = next(t["offsetSec"] for t in data["tracks"] if t["id"] == "drums")
    excerpt = np.abs(np.asarray(samples)[int((base.FIRST/24-offset)*8000):
                                       int((base.END/24-offset)*8000)])
    return samples, offset, max(float(np.quantile(excerpt, .985)), .0001)


class Phosphor:
    def __init__(self, source, channel, dual):
        self.samples, self.offset, self.norm = source
        self.channel, self.dual = channel, dual
        self.fast = np.zeros((N, N), np.float32)
        self.slow = self.fast.copy()
        self.instant = self.fast.copy()
        self.df = math.exp(-math.log(2)/(24*SUBSTEPS*FAST_HALF))
        self.ds = math.exp(-math.log(2)/(24*SUBSTEPS*SLOW_HALF))
        self.samples = np.asarray(self.samples)

    def deposit(self, sec):
        center = (sec-self.offset)*8000
        start = int(center-256)
        lo, hi = max(1, start-48), min(len(self.samples)-513, start+49)
        crossings = np.flatnonzero((self.samples[lo-1:hi-1] <= 0) &
                                  (self.samples[lo:hi] > 0))+lo
        if len(crossings):
            start = int(crossings[np.argmin(np.abs(crossings-start))])
        sample_indices = start+(PX+base.RX)/(2*base.RX)*512
        left = np.clip(np.floor(sample_indices).astype(int), 0, len(self.samples)-2)
        fraction = np.clip(sample_indices-left, 0, 1)
        signal = (self.samples[left]*(1-fraction)+self.samples[left+1]*fraction)/self.norm
        # Soft compression prevents bright, artificially flat clipped peaks.
        signal = 1.25*np.tanh(signal/1.25)
        amplitude = 88 if self.channel == 0 else 59
        # No rapid independent animation: slowly diverging axes, both horizontal.
        if self.dual:
            rel = sec-base.FIRST/24
            shift = (-7+3*math.sin(rel*.8)) if self.channel == 0 else (13+4*math.sin(rel*.7+.8))
            angle = (.6*math.sin(rel*.6)) if self.channel == 0 else (-1.1*math.sin(rel*.55+.6))
        else:
            shift, angle = 0, 0
        y = signal*amplitude+shift+PX*math.tan(math.radians(angle))
        slope = np.gradient(y, PX)
        speed = np.sqrt(1+slope*slope)
        dwell = 1/speed
        # Distance normal to the trace, rather than vertical stroke thickness.
        distance = (PY-y[None, :])/speed[None, :]
        sigma = .50+1.08*dwell
        intensity = .08+.92*dwell
        core = np.exp(-.5*(distance/sigma[None, :])**2)*intensity[None, :]
        bloom = (.21*np.exp(-.5*(distance/(2.8+2.4*dwell)[None, :])**2)
                 + .045*np.exp(-.5*(distance/9)**2))*(dwell[None, :]**1.5)
        self.instant = ((core+bloom)*APERTURE).astype(np.float32)
        self.fast *= self.df
        self.fast += self.instant*(1-self.df)
        self.slow *= self.ds
        self.slow += self.instant*(1-self.ds)

    def energy(self):
        return .70*self.instant + .95*self.fast + .30*self.slow


def setup(mode):
    scene, camera = base.setup("replacement")
    # Remove the old central grid, leaving only peripheral calibration.
    for obj in list(scene.objects):
        if obj.name.startswith(("Horizontal grid", "Vertical grid", "Grid tick")):
            bpy.data.objects.remove(obj, do_unlink=True)
    refined.textured_glass()
    glass_details()
    scene.render.resolution_x, scene.render.resolution_y = 2560, 1440
    for obj in scene.objects:
        if obj.type == "FONT":
            obj.data.body = ("PHOSPHOR — amber bass / speed-weighted beam" if mode == "single"
                             else "TWO CHANNELS — amber bass + cyan drum body")
            obj.data.size = 20
    rgba = np.zeros((N, N, 4), dtype=np.float32)
    rgba[:, :, 3] = 1
    image = float_image("Accumulated phosphor energy", rgba)
    image_plane("Light behind the glass", image, .18, additive=True)
    return scene, camera, image, rgba


def encode(mode):
    base.command(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                  "-i", str(OUT/mode/"%04d.png"), "-ss", str(base.FIRST/24),
                  "-i", str(base.ROOT/"audio/song.wav"), "-t", str(69/24),
                  "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-crf", "17",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                  "-movflags", "+faststart", str(OUT/f"{mode}.mp4")])


def render(mode, bass, drums, preview):
    folder = OUT/mode
    folder.mkdir(parents=True, exist_ok=True)
    scene, camera, image, rgba = setup(mode)
    channels = [Phosphor(bass, 0, mode == "dual")]
    if mode == "dual":
        channels.append(Phosphor(drums, 1, True))
    # Prime persistence from preceding audio; this is a view into an ongoing tube.
    dt = 1/(24*SUBSTEPS)
    for step in range(64):
        sec = base.FIRST/24-(64-step)*dt
        for channel in channels:
            channel.deposit(sec)
    stop = 46 if preview else 69
    stats = []
    for i in range(stop):
        for sub in range(SUBSTEPS):
            sec = (base.FIRST+i)/24+(sub+.5)*dt
            for channel in channels:
                channel.deposit(sec)
        energy = channels[0].energy()
        rgb = energy[:, :, None]*np.array([1.00, .43, .075], dtype=np.float32)
        if mode == "dual":
            rgb += channels[1].energy()[:, :, None]*np.array([.065, .40, .38], dtype=np.float32)
        # Gentle radiance shoulder keeps color addition from turning into clipping.
        rgb *= GRAIN[:, :, None]
        rgba[:, :, :3] = rgb/(1+rgb*.25)
        image.pixels.foreach_set(rgba.ravel())
        image.update()
        stats.append({"frame": base.FIRST+i, "energy_peak": float(rgb.max()),
                      "energy_sum": float(rgb.sum())})
        if preview and i != 45:
            continue
        p = i/68
        camera.data.ortho_scale = base.W/(1.012+.018*p)
        camera.location.x, camera.location.y = p*5, -p*2
        scene.render.filepath = str(folder/f"{i:04d}.png")
        bpy.ops.render.render(write_still=True)
    if not preview:
        encode(mode)
        (OUT/f"{mode}_energy.json").write_text(json.dumps(stats, indent=2))


def assemble():
    inputs = [refined.OUT/"refined.mp4", OUT/"single.mp4", OUT/"dual.mp4"]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for source in inputs:
        cmd += ["-i", str(source)]
    cmd += ["-i", str(base.ROOT/"audio/song.wav")]
    filters = [f"[{i}:v]setpts=PTS-STARTPTS,split=2[v{i}a][v{i}b]" for i in range(3)]
    filters += ["[v0a][v1a][v2a][v0b][v1b][v2b]concat=n=6:v=1:a=0[v]",
                f"[3:a]atrim=start={base.FIRST/24}:end={base.END/24},"
                "asetpts=PTS-STARTPTS,asplit=6[a0][a1][a2][a3][a4][a5]",
                "[a0][a1][a2][a3][a4][a5]concat=n=6:v=0:a=1[a]"]
    base.command(cmd+["-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
                      "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                      str(OUT/"comparison.mp4")])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--assemble-only", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.assemble_only:
        bass, drums = base.read_bass(), read_drums()
        for mode in ["single", "dual"]:
            render(mode, bass, drums, args.preview)
    if not args.preview:
        assemble()
        (OUT/"parameters.json").write_text(json.dumps({
            "song_frames": [86,155], "fps":24, "substeps":SUBSTEPS,
            "phosphor_half_lives_sec":[FAST_HALF,SLOW_HALF],
            "phosphor_texture_size":[N,N], "render_size":[2560,1440],
            "dwell_model":"1/sqrt(1+(dy/dx)^2), art-directed width and bloom",
            "aperture":"elliptical soft clipping; trace reaches beyond useful glass",
            "channels":{"amber":"bass 25-180 Hz","cyan":"drum body 25-240 Hz"},
            "dual_axes":"two near-horizontal axes with slow <=1.1 degree drift",
            "scope":"CRT-inspired composite, not a calibrated tube simulation",
        }, indent=2))
    print("PHOSPHOR STUDY COMPLETE")


if __name__ == "__main__":
    main()
