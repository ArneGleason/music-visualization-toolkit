"""CRT-inspired screen study: beam dwell, accumulated phosphor, optional dual audio.

Blender -b -t 4 -P tools/screen_sync_phosphor.py -- [--profile depth] [--preview]
Media is local under out/screen_sync_phosphor or out/screen_sync_depth.
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
CLASSIC_OUT = OUT
PROFILE = "classic"
ANALOG = False
CRACKLE = False
GUITAR = None
GUITAR_GAIN = .15
PUSH_IN = False
RAIL = False
CLEAN = False
N = 1024 if "--push-in" in sys.argv else 768
SUBSTEPS = 8
FAST_HALF = .030
SLOW_HALF = .160
PX = np.linspace(-base.RX, base.RX, N, dtype=np.float32)
PY = np.linspace(-base.RY, base.RY, N, dtype=np.float32)[:, None]
RAD = np.sqrt((PX[None, :]/base.RX)**2+(PY/base.RY)**2)
APERTURE = np.clip((.990-RAD)/.018, 0, 1)
APERTURE *= APERTURE*(3-2*APERTURE)
GRAIN = np.clip(1+np.random.default_rng(8025).normal(0, .085, (N, N)), .70, 1.30)


def signal_noise(phase, sec):
    """Small deterministic, band-limited pickup; continuous across frames."""
    noise = sum(a*np.sin(math.tau*(k*phase+hz*sec)+offset)
               for a, k, hz, offset in [(.42, 17, 2.3, .7), (.28, 31, -3.7, 1.9),
                                        (.18, 53, 5.1, 2.7), (.12, 79, -6.7, .2)])
    if not CRACKLE:
        return noise
    t = sec-base.FIRST/24
    # A wandering pickup floor, plus sparse bipolar disturbances. These change
    # geometry, never soundtrack or global exposure. Keep time continuous.
    envelope = 1.55*(1+.25*math.sin(t*3.1+.4)+.12*math.sin(t*7.3+1.7))
    noise *= envelope
    for when, position, strength, duration, width in [
            (.19, .26, 1.8, .045, .027), (.64, .73, -2.2, .060, .035),
            (1.09, .43, 1.3, .035, .016), (1.73, .61, 2.0, .055, .023),
            (2.38, .18, -1.6, .045, .030)]:
        temporal = math.exp(-.5*((t-when)/duration)**2)
        distance = np.mod(phase-position+.5, 1)-.5
        x = distance/width
        noise += strength*temporal*(1-x*x)*np.exp(-.5*x*x)
    return noise


def sweep_weight(phase, sec, circular=False):
    """A slow camera-beat impression, not literal high-frequency scan aliasing."""
    head = (.27+sec*(.23 if circular else .31)) % 1
    age = np.mod(head-phase, 1)
    tail = np.exp(-age/.24)
    # Soften the wrap into the next head; never extinguish the previous sweep.
    ramp = np.clip((1-age)/.035, 0, 1)
    tail += (1-tail)*(1-ramp*ramp*(3-2*ramp))
    return .95+.05*tail


def rail_motion(t):
    """Small continuous mechanical sway in view fractions, degrees and scale."""
    ramp = 1-math.exp(-4*t)
    x = .0016*math.sin(2.7*t+.4)+.0007*math.sin(7.1*t+1.8)+.00020*math.sin(19.3*t)
    y = .0011*math.sin(3.3*t+2.1)+.0005*math.sin(8.3*t+.2)+.00015*math.sin(17.7*t)
    roll = .11*math.sin(2.3*t+.8)+.045*math.sin(6.7*t+1.2)
    travel = .0018*math.sin(4.1*t+.3)+.0005*math.sin(10.3*t)
    return tuple(ramp*v for v in (x, y, roll, travel))


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


def read_stem(stem="Drum Kit", track_id="drums", low=25, high=240):
    local = json.loads((base.ROOT / "projects/rivers-of-mars/project.local.json").read_text())
    files = list(pathlib.Path(local["sources"]["stems"]).glob(f"*{stem}*restored.wav"))
    if len(files) != 1:
        raise ValueError(f"Expected one restored {stem} stem")
    raw = base.command(["ffmpeg", "-v", "error", "-i", str(files[0]), "-ac", "1",
                        "-af", f"highpass=f={low},lowpass=f={high},aresample=8000",
                        "-f", "f32le", "-"])
    samples = array.array("f")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    data = json.loads((base.ROOT / "projects/rivers-of-mars/generated/waveforms.json").read_text())
    offset = next(t["offsetSec"] for t in data["tracks"] if t["id"] == track_id)
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
        if GUITAR is not None and self.channel == 0:
            guitar_samples, guitar_offset, guitar_norm = GUITAR
            # Same song-time window and bass trigger; no independent phase reset.
            guitar_indices = np.clip(sample_indices+(self.offset-guitar_offset)*8000,
                                     0, len(guitar_samples)-2)
            guitar_left = guitar_indices.astype(int)
            guitar_fraction = guitar_indices-guitar_left
            guitar = (guitar_samples[guitar_left]*(1-guitar_fraction)
                      +guitar_samples[guitar_left+1]*guitar_fraction)/guitar_norm
            signal += GUITAR_GAIN*1.25*np.tanh(guitar/1.25)
        amplitude = 88 if self.channel == 0 else 59
        # No rapid independent animation: slowly diverging axes, both horizontal.
        if self.dual:
            rel = sec-base.FIRST/24
            shift = (-7+3*math.sin(rel*.8)) if self.channel == 0 else (13+4*math.sin(rel*.7+.8))
            angle = (.6*math.sin(rel*.6)) if self.channel == 0 else (-1.1*math.sin(rel*.55+.6))
        else:
            shift, angle = 0, 0
        magnification = 1
        if PROFILE in ("depth", "rosette"):
            amplitude = 96 if self.channel == 0 else 112
            rel = sec-base.FIRST/24
            shift = -7 if self.channel == 0 else 10
            angle = 0 if self.channel == 0 else 12+16*math.sin(rel*1.25+.55)
            # Magnify deflection around its own axis, not the fixed screen/grid.
            magnification = 1+.20*(1-(PX/base.RX)**2)**2
            if ANALOG:
                magnification = 1+.55*(1-(PX/base.RX)**2)**2
        y = signal*amplitude*magnification+shift+PX*math.tan(math.radians(angle))
        if ANALOG:
            y += .85*signal_noise((PX+base.RX)/(2*base.RX), sec)
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
        if ANALOG:
            self.instant *= sweep_weight((PX+base.RX)/(2*base.RX), sec)[None, :]
        self.fast *= self.df
        self.fast += self.instant*(1-self.df)
        self.slow *= self.ds
        self.slow += self.instant*(1-self.ds)

    def energy(self):
        return .70*self.instant + .95*self.fast + .30*self.slow


class Rosette(Phosphor):
    """Rectified bass, three phase-folded cycles per revolution; not an XY scope."""
    def __init__(self, source):
        super().__init__(source, 1, True)
        self.period = None
        self.radius = np.sqrt(PX[None, :]**2+PY**2)
        self.theta = np.arctan2(PY, PX[None, :])

    def deposit(self, sec):
        center = int((sec-self.offset)*8000)
        chunk = self.samples[max(0, center-1024):center+1024].astype(float)
        chunk -= chunk.mean()
        # Autocorrelation over the bass range, with slow period changes to avoid
        # turning noisy pitch estimates into visual jumps. Silence holds pitch.
        if np.sqrt(np.mean(chunk**2)) > self.norm*.04:
            corr = np.correlate(chunk, chunk, mode="full")[len(chunk)-1:]
            candidates = np.arange(45, 201)
            scores = corr[candidates]/(len(chunk)-candidates)
            peaks = np.flatnonzero((scores[1:-1] > scores[:-2]) &
                                   (scores[1:-1] >= scores[2:]))+1
            if len(peaks):
                best = scores[peaks].max()
                lag = float(candidates[peaks[scores[peaks] >= best*.92][0]])
                self.period = lag if self.period is None else .96*self.period+.04*lag
        period = self.period if self.period is not None else 100.
        lo, hi = max(1, center-int(period)), min(len(self.samples)-1, center+int(period))
        crossings = np.flatnonzero((self.samples[lo-1:hi-1] <= 0) &
                                  (self.samples[lo:hi] > 0))+lo
        origin = float(crossings[np.argmin(abs(crossings-center))]) if len(crossings) else center
        phase = np.arange(512)/512
        # Fold three neighboring periods; preserve level, rather than normalize
        # every frame. Rectification maps both polarities outward.
        wave = np.zeros(512)
        for k in [-1, 0, 1]:
            indices = np.clip(origin+(phase+k)*period, 0, len(self.samples)-2)
            left = indices.astype(int)
            fraction = indices-left
            wave += self.samples[left]*(1-fraction)+self.samples[left+1]*fraction
        wave /= 3*self.norm
        wave = np.abs(wave)
        # Close the cycle gently across its seam before repeating it.
        wave = (wave+np.roll(wave, 1)+np.roll(wave, -1))/3
        radial = 42+153*np.tanh(wave*1.65)
        if ANALOG:
            radial *= 1+.45*(1-radial/base.RX)**2
            radial += 1.1*signal_noise(phase, sec)
        angle = (self.theta+.10*(sec-base.FIRST/24))*3/math.tau
        phase_grid = np.mod(angle, 1)*512
        target = np.interp(phase_grid, np.arange(513), np.r_[radial, radial[0]])
        derivative = (np.roll(radial, -1)-np.roll(radial, 1))*512*3/(2*math.tau)
        dr = np.interp(phase_grid, np.arange(513), np.r_[derivative, derivative[0]])
        speed = np.sqrt(1+(dr/np.maximum(target, 1))**2)
        dwell = 1/speed
        distance = (self.radius-target)/speed
        sigma = .50+1.08*dwell
        core = np.exp(-.5*(distance/sigma)**2)*(.08+.92*dwell)
        bloom = (.21*np.exp(-.5*(distance/(2.8+2.4*dwell))**2)
                 +.045*np.exp(-.5*(distance/9)**2))*dwell**1.5
        self.instant = ((core+bloom)*APERTURE).astype(np.float32)
        if ANALOG:
            self.instant *= sweep_weight(np.mod(self.theta/math.tau, 1), sec, True)
        self.fast = self.df*self.fast+(1-self.df)*self.instant
        self.slow = self.ds*self.slow+(1-self.ds)*self.instant


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
            if PROFILE == "depth":
                obj.data.body = "DEPTH — fixed amber / larger, defocused cyan"
            if PROFILE == "rosette":
                obj.data.body = "ROSETTE — horizontal bass / soft circular bass"
                if ANALOG:
                    obj.data.body = "ROSETTE ANALOG — centre lens / noise / gentle sweep"
                    if CRACKLE:
                        obj.data.body = "ROSETTE ANALOG 2 — wandering noise / soft crackle"
                    if GUITAR is not None:
                        obj.data.body = f"GUITAR BLEND — amber bass + {GUITAR_GAIN:.0%} guitar / cyan bass"
                    if PUSH_IN:
                        obj.data.body = "SCOPE PUSH-IN — 30% guitar / gentle light build"
                        if RAIL:
                            obj.data.body = "SCOPE RAIL — subtle sway / imperfect push-in"
    rgba = np.zeros((N, N, 4), dtype=np.float32)
    rgba[:, :, 3] = 1
    image = float_image("Accumulated phosphor energy", rgba)
    image_plane("Light behind the glass", image, .18, additive=True)
    return scene, camera, image, rgba


def encode(mode):
    if CLEAN:
        base.command(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                      "-i", str(OUT/mode/"%04d.png"), "-frames:v", "69",
                      "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264",
                      "-crf", "17", "-pix_fmt", "yuv420p", "-an",
                      "-movflags", "+faststart", str(OUT/f"{mode}.mp4")])
        return
    base.command(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                  "-i", str(OUT/mode/"%04d.png"), "-ss", str(base.FIRST/24),
                  "-i", str(base.ROOT/"audio/song.wav"), "-t", str(69/24),
                  "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-crf", "17",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                  "-movflags", "+faststart", str(OUT/f"{mode}.mp4")])


def defocus(energy, sigma=7.5):
    """Spread radiance with a unit-sum Gaussian, preserving energy away from edges."""
    radius = math.ceil(3*sigma)
    x = np.arange(-radius, radius+1, dtype=np.float32)
    kernel = np.exp(-.5*(x/sigma)**2)
    kernel /= kernel.sum()
    result = energy
    for axis in [0, 1]:
        padding = [(0, 0), (0, 0)]
        padding[axis] = (radius, radius)
        padded = np.pad(result, padding, mode="constant")
        result = np.apply_along_axis(lambda row: np.convolve(row, kernel, mode="valid"),
                                     axis, padded)
    return result


def render(mode, bass, drums, preview):
    folder = OUT/mode
    folder.mkdir(parents=True, exist_ok=True)
    scene, camera, image, rgba = setup(mode)
    if CLEAN:
        for obj in list(scene.objects):
            if obj.type == "FONT":
                bpy.data.objects.remove(obj, do_unlink=True)
    channels = [Phosphor(bass, 0, mode == "dual")]
    if mode == "dual":
        channels.append(Rosette(bass) if PROFILE == "rosette" else Phosphor(drums, 1, True))
    # Prime persistence from preceding audio; this is a view into an ongoing tube.
    dt = 1/(24*SUBSTEPS)
    for step in range(64):
        sec = base.FIRST/24-(64-step)*dt
        for channel in channels:
            channel.deposit(sec)
    stop = 46 if preview else 69
    stats = []
    for i in range(stop):
        progress = i/68
        ease = progress*progress*(3-2*progress)
        exposure = [np.zeros((N, N), np.float32) for _ in channels] if ANALOG else None
        for sub in range(SUBSTEPS):
            sec = (base.FIRST+i)/24+(sub+.5)*dt
            for index, channel in enumerate(channels):
                channel.deposit(sec)
                if ANALOG:
                    exposure[index] += channel.energy()/SUBSTEPS
        energy = exposure[0] if ANALOG else channels[0].energy()
        if PUSH_IN:
            # Prefer existing bright cores over adding another broad halo.
            energy = energy*(1+.20*ease*(.35+.65*np.clip(energy/1.2, 0, 1)))
        rgb = energy[:, :, None]*np.array([1.00, .43, .075], dtype=np.float32)
        focus_stats = {}
        if mode == "dual":
            cyan = exposure[1] if ANALOG else channels[1].energy()
            if PROFILE in ("depth", "rosette"):
                spread = defocus(cyan, 7.5*N/768)
                focus_stats = {"cyan_sharp_energy": float(cyan.sum()),
                               "cyan_spread_energy_before_aperture": float(spread.sum()),
                               "cyan_sharp_peak": float(cyan.max()),
                               "cyan_spread_peak": float(spread.max())}
                cyan = spread*APERTURE
            if PUSH_IN:
                cyan *= 1+.20*ease
            rgb += cyan[:, :, None]*np.array([.065, .40, .38], dtype=np.float32)
        # Gentle radiance shoulder keeps color addition from turning into clipping.
        rgb *= GRAIN[:, :, None]
        rgba[:, :, :3] = rgb/(1+rgb*.25)
        image.pixels.foreach_set(rgba.ravel())
        image.update()
        stats.append({"frame": base.FIRST+i, "energy_peak": float(rgb.max()),
                      "energy_sum": float(rgb.sum()), **focus_stats})
        if preview and i != 45:
            continue
        p = i/68
        camera.data.ortho_scale = base.W/(1.012+.018*p)
        camera.location.x, camera.location.y = p*5, -p*2
        if PUSH_IN:
            # Move optically into the display, not into the centre of the plate.
            camera.data.ortho_scale = (base.W/1.012)*(610/(base.W/1.012))**ease
            camera.location.x = (base.CX-base.W/2)*ease
            camera.location.y = (base.H/2-base.CY)*ease
            if RAIL:
                dx, dy, roll, travel = rail_motion(i/24)
                width = camera.data.ortho_scale
                camera.location.x += dx*width
                camera.location.y += dy*width
                camera.rotation_euler.z = math.radians(roll)
                camera.data.ortho_scale *= 1+travel
        scene.render.filepath = str(folder/f"{i:04d}.png")
        bpy.ops.render.render(write_still=True)
    if not preview:
        encode(mode)
        (OUT/f"{mode}_energy.json").write_text(json.dumps(stats, indent=2))


def assemble():
    inputs = [refined.OUT/"refined.mp4", OUT/"single.mp4", OUT/"dual.mp4"]
    if PROFILE == "depth":
        inputs = [CLASSIC_OUT/"dual.mp4", OUT/"dual.mp4"]
    if PROFILE == "rosette":
        inputs = [base.ROOT/"out/screen_sync_depth/dual.mp4", OUT/"dual.mp4"]
        if ANALOG:
            inputs = [base.ROOT/"out/screen_sync_rosette/dual.mp4", OUT/"dual.mp4"]
            if CRACKLE:
                inputs = [base.ROOT/"out/screen_sync_rosette_analog/dual.mp4", OUT/"dual.mp4"]
            if GUITAR is not None:
                inputs = [base.ROOT/"out/screen_sync_rosette_analog2/dual.mp4", OUT/"dual.mp4"]
                if GUITAR_GAIN != .15:
                    inputs = [base.ROOT/"out/screen_sync_guitar_blend/dual.mp4", OUT/"dual.mp4"]
    if PUSH_IN:
        inputs = [base.ROOT/"out/screen_sync_guitar_blend_30pct/dual.mp4", OUT/"dual.mp4"]
        if RAIL:
            inputs = [base.ROOT/"out/screen_sync_scope_pushin/dual.mp4", OUT/"dual.mp4"]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for source in inputs:
        cmd += ["-i", str(source)]
    cmd += ["-i", str(base.ROOT/"audio/song.wav")]
    count = len(inputs)
    filters = [f"[{i}:v]setpts=PTS-STARTPTS,split=2[v{i}a][v{i}b]" for i in range(count)]
    video_labels = "".join(f"[v{i}{repeat}]" for repeat in ["a", "b"] for i in range(count))
    audio_labels = "".join(f"[a{i}]" for i in range(count*2))
    filters += [f"{video_labels}concat=n={count*2}:v=1:a=0[v]",
                f"[{count}:a]atrim=start={base.FIRST/24}:end={base.END/24},"
                f"asetpts=PTS-STARTPTS,asplit={count*2}{audio_labels}",
                f"{audio_labels}concat=n={count*2}:v=0:a=1[a]"]
    base.command(cmd+["-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
                      "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                      str(OUT/"comparison.mp4")])


def main():
    global OUT, PROFILE, ANALOG, CRACKLE, GUITAR, GUITAR_GAIN, PUSH_IN, RAIL, CLEAN
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--assemble-only", action="store_true")
    parser.add_argument("--analog", action="store_true")
    parser.add_argument("--crackle", action="store_true")
    parser.add_argument("--guitar", action="store_true")
    parser.add_argument("--push-in", action="store_true")
    parser.add_argument("--rail", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--guitar-gain", type=float, default=.15)
    parser.add_argument("--profile", choices=["classic", "depth", "rosette"], default="classic")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    PROFILE = args.profile
    PUSH_IN = args.push_in
    RAIL = args.rail
    CLEAN = args.clean
    if RAIL and not PUSH_IN:
        parser.error("--rail requires --push-in")
    if PUSH_IN and (not args.guitar or args.profile != "rosette"):
        parser.error("--push-in requires --profile rosette --guitar")
    GUITAR_GAIN = args.guitar_gain
    if not 0 <= GUITAR_GAIN <= 1:
        parser.error("--guitar-gain must be between 0 and 1")
    CRACKLE = args.crackle or args.guitar
    ANALOG = args.analog or CRACKLE
    if ANALOG and PROFILE != "rosette":
        parser.error("--analog requires --profile rosette")
    if PROFILE == "depth":
        OUT = base.ROOT / "out" / "screen_sync_depth"
    if PROFILE == "rosette":
        OUT = base.ROOT / "out" / ("screen_sync_rosette_analog" if ANALOG else "screen_sync_rosette")
        if CRACKLE:
            OUT = base.ROOT / "out" / "screen_sync_rosette_analog2"
        if args.guitar:
            OUT = base.ROOT / "out" / "screen_sync_guitar_blend"
            if GUITAR_GAIN != .15:
                OUT = base.ROOT / "out" / f"screen_sync_guitar_blend_{GUITAR_GAIN*100:g}pct"
    if args.guitar:
        samples, offset, norm = read_stem("Guitar", "guitar", 90, 900)
        GUITAR = np.asarray(samples), offset, norm
    if PUSH_IN:
        OUT = base.ROOT / "out" / "screen_sync_scope_pushin"
        if RAIL:
            OUT = base.ROOT / "out" / "screen_sync_scope_rail"
    if CLEAN:
        OUT = OUT.with_name(OUT.name+"_clean")
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.assemble_only:
        bass, drums = base.read_bass(), read_stem()
        for mode in (["dual"] if PROFILE != "classic" else ["single", "dual"]):
            render(mode, bass, drums, args.preview)
    if not args.preview:
        if not CLEAN:
            assemble()
        (OUT/"parameters.json").write_text(json.dumps({
            "song_frames": [86,155], "fps":24, "substeps":SUBSTEPS,
            "phosphor_half_lives_sec":[FAST_HALF,SLOW_HALF],
            "phosphor_texture_size":[N,N], "render_size":[2560,1440],
            "dwell_model":"1/sqrt(1+(dy/dx)^2), art-directed width and bloom",
            "aperture":"elliptical soft clipping; trace reaches beyond useful glass",
            "channels":{"amber":(f"bass 25-180 Hz + {GUITAR_GAIN:.0%} guitar 90-900 Hz" if GUITAR is not None
                                   else "bass 25-180 Hz"),"cyan":("rectified bass 25-180 Hz"
                        if PROFILE == "rosette" else "drum body 25-240 Hz")},
            "dual_axes":("fixed amber; cyan begins near 20 degrees and swings widely"
                         if PROFILE == "depth" else "fixed amber; radial cyan" if PROFILE == "rosette" else
                         "two near-horizontal axes with slow <=1.1 degree drift"),
            "scope":"CRT-inspired composite, not a calibrated tube simulation",
            "profile": PROFILE,
            "rail_settings": ({"model":"continuous multi-frequency mechanical sway",
                               "max_x_view_fraction":.0025,"max_y_view_fraction":.00175,
                               "max_roll_degrees":.155,"max_scale_fraction":.0023,
                               "soundtrack_and_signal":"unchanged",
                               "motion_blur":"none; low-amplitude camera movement at 24 fps"}
                              if RAIL else None),
            "push_in_settings": ({"end_view_width_plate_px":610,
                                  "target_plate_xy":[base.CX,base.CY],
                                  "ease":"smoothstep with exponential zoom",
                                  "max_beam_gain_at_end":1.20,
                                  "amber":"core-weighted intensity, no new blur",
                                  "cyan":"uniform intensity lift retaining defocus",
                                  "amplitude":"unchanged","handles_rendered":0}
                                 if PUSH_IN else None),
            "guitar_settings": ({"gain":GUITAR_GAIN,"filter_hz":[90,900],
                                 "normalization":"fixed excerpt absolute 98.5th percentile",
                                 "normalization_value":GUITAR[2],"offset_sec":GUITAR[1],
                                 "trigger":"shared bass-triggered song-time window"}
                                if GUITAR is not None else None),
            "analog_settings": ({"amber_center_gain":1.55,"cyan_radial_center_gain":1.45,
                                 "noise_scale_px":{"amber":.85,"cyan":1.1},
                                 "crackle":CRACKLE,
                                 "noise_floor_gain":("1.55*(1+.25*sin(t*3.1+.4)+.12*sin(t*7.3+1.7))"
                                                     if CRACKLE else 1),
                                 "crackle_event_times_sec":([.19,.64,1.09,1.73,2.38] if CRACKLE else []),
                                 "sweep_brightness_range":[.95,1.0],
                                 "sweep_cycles_sec":{"amber":.31,"cyan":.23},
                                 "temporal_exposure_samples":SUBSTEPS}
                                if ANALOG else None),
            "rosette_settings": ({"cycles_per_revolution":3,"base_radius":42,
                                  "outward_gain":153,"compression_drive":1.65,
                                  "rotation_rad_sec":-.10,"period_range_samples":[45,200],
                                  "driver":"three-period folded rectified bass, no frame normalization",
                                  "cyan_defocus_sigma_texture_px":7.5}
                                 if PROFILE == "rosette" else None),
            "depth_settings": ({"amber_axis_deg":0, "amber_amplitude":96,
                                "cyan_amplitude":112, "cyan_axis_deg":"12+16*sin(t*1.25+.55)",
                                "center_deflection_gain":1.20, "edge_deflection_gain":1,
                                "cyan_defocus_sigma_texture_px":7.5,
                                "cyan_exposure":"unchanged; normalized Gaussian spreads energy"}
                               if PROFILE == "depth" else None),
        }, indent=2))
    print("PHOSPHOR STUDY COMPLETE")


if __name__ == "__main__":
    main()
