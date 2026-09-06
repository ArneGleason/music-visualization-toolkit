# Garden dust pilot: the air wakes up

Status: owner accepted the bloom/depth version as the full-strength reusable
FX-01 look. Reassess strength over motion footage. Latest preview is flattened;
separate production layers are still needed. Not approved for assembly.
See `FX_TYPES.md` for the reusable type and delivery requirements.

## Drum-led light pulse — latest review

### Follow-up: bloom and three depth bands

Owner requested substantially brighter, camera-overload-like bloom and layered
depth extending to the periphery. Latest preview:
**`out/garden_airflow_bloom_depth/garden_airflow.mp4`**.
Run Blender `-b -t 4 --python-exit-code 1 -P tools/garden_airflow.py -- --bloom-depth`.

Same 3600 motes, now distributed in three depth bands: distant fine/slower,
middle-sized/active, and nearer larger/faster. Peripheral fades extend beyond
the image edges instead of leaving a broad quiet border. Eye exclusions and
approximate foliage masks remain. No camera tracking or recovered geometry.
Drum-driven emission gain is now 3–10 before layer weighting and envelope
smoothing. Two Gaussian halo shells (3x and 8x core dimensions) approximate
optical bloom around dust only; this is an artistic sprite bloom approximation,
not physical scattering or an image-wide glare filter. Wisps receive less gain
to avoid washing out the scene. No new assembly substitution. Prior versions
remain intact. Owner accepted this as the full-strength reference; adjust its
compositing strength in context when motion footage and separate layers exist.

Preview: **`out/garden_airflow_pulse/garden_airflow.mp4`**. Reproduce with Blender
`-b -t 4 --python-exit-code 1 -P tools/garden_airflow.py -- --pulse-light`.

Keep the accepted airflow, but raise emission across the dust on selected drum
attacks: 22 ms attack and 200 ms release. Bass still controls flow strength.
Emission gain is `1.15 + 1.35 * envelope`; the rendered excerpt ranges from
1.355 to 2.161 times the previous emission. This is a shader-input gain, not a
claim of proportional perceived brightness. Particle count, size, opacity and
motion are unchanged; the original version remains available for comparison.

Verified 68 frames at 24 fps, 1280x720, same song interval [1527,1595). Diagnostic
speeds and visible counts match the original airflow pass. Strongest-pulse frame
visually checked: eyes and foliage remain readable. Review against moving footage
is still needed; no assembly selection or generated footage changed.

## Space-filling airflow — latest alternative

Owner rejected the concentrated, crawling native-particle clusters as the wrong
spatial behaviour. Wants finer, faster, gaseous material throughout the scene,
acting collectively and interacting with its surroundings. Latest short test:
**`out/garden_airflow/garden_airflow.mp4`**. Reproduce with Blender
`-b -t 4 --python-exit-code 1 -P tools/garden_airflow.py`.

This deliberately switches methods: a scripted 3D curl-field advection model,
rendered with Blender billboard meshes. It is NOT a native gas bake or a
pressure-solving/incompressible fluid solver. 3600 small motes and 100 very faint
elongated wisps occupy a continuous reservoir, rather than two point emitters.
Velocities respond quickly (55 ms relaxation), using eight simulation substeps
per 24 fps output frame. Short velocity-aligned streaks suggest motion; these
are geometric streaks, not shutter-sampled physical motion blur.

Bass changes overall flow strength; actual selected drum attacks launch broad
localized disturbances that decay over about 170 ms. Existing event timing is
reused, not guessed from a beat grid. Continuous trigonometric curl supplies
coherent eddies without a central attracting sink. No added soundtrack noise.

Use an approximate perspective volume (50 mm / 36 mm sensor, static camera),
with the original photograph placed to fill the same frame. The garden does
not provide enough evidence for a unique calibrated camera or reconstructed
3D scene. Three broad ellipsoid foliage proxies deflect motion; approximate
foreground visibility regions occlude more distant particles. Eye exclusions
preserve the photographed eyes. Near motes can cross in front of the leaves.
These are authored depth cues, not inferred true geometry or tracking.

One second of simulation warm-up precedes the same [1527,1595) output. Periodic
reservoir replenishment is softened near boundaries; inspect for any visible
re-entry if the view or length changes. No delivery handles and no assembly
selection change. This pass saves composite PNGs, preview MP4, and control/
diagnostic JSON; no transparent pass or portable simulation cache yet.

Blender also offers a native gas solver and
[gas-detail turbulence](https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/gas/noise.html).
Defer that heavier workflow until this faster alternative establishes whether
space-filling motion is the right visual direction. Prior tests remain intact.

## Native emitter/effector choreography — latest experiment

Owner requested substantially more collective motion: particles as an actor,
organized by emitters, attraction, dispersion, swirling fields and musical
choreography, rather than merely brighter dots. New-only preview:
**`out/garden_dust_fields/garden_fields.mp4`**. Reproduce with Blender
`-b -t 4 --python-exit-code 1 -P tools/garden_dust_fields.py`.

This version uses actual Blender emitter particle systems, unlike the first
scripted-sprite pass. Two emitters supply up to 1700 particles over the simulation
window, with randomized size/lifetime and modest Brownian motion. Native fields:

- HARMONIC pulls toward a moving centre; smoothed bass strengthens gathering.
- VORTEX supplies angular motion, also strengthened by bass.
- FORCE briefly repels on selected actual drum attacks while attraction relaxes.
- TURBULENCE perturbs the volume more on attacks; particle damping limits motion.

The centre travels with phase interpolated from the saved tempo/beat grid.
This is authored choreography on top of measured drum/bass signals, not a
claim that the musical notes specify an exact path. No DAW MIDI notes added yet.
Emission rate is steady in this pass; density changes through gathering,
dispersion and particle lifetime. Audio-controlled emission rate is a future
control, not something already implemented.

The first internal native render was too dense/solid; reduce sprite size and
opacity, broaden the emitter volume and increase random initial velocity.
Retain the original subdued preview separately. Current method uses two
green/cyan and amber streams to make collective interaction visible.

The native scene, animated emitter/field objects and materials are saved in
`out/garden_dust_fields/garden_fields.blend`; controls in `controls.json`.
Replay simulation from frame 1, not by jumping directly to a later frame.
24 simulation warm-up frames precede the output; these are NOT editorial lead
handles. The actual review still covers only [1527,1595), 68 frames, and has
no delivery handles. No particle cache portability claim: reproduce with script.

Camera/eyes remain static. Original-photo patches protect eyes and the outside
of a broad central window; these are simple holdouts, not depth reconstruction.
No motion tracking, local volumetric relighting or new assembly selection.
This pass saves composite frames and an editable Blender scene; a separate
transparent pass has not yet been exported for the native-field version.

Blender 5.2 emitted dependency-graph RIGIDBODY_REBUILD warnings while evaluating
animated native fields, but completed the particle renders. Keep this recorded
when moving to another Blender version or rebaking; do not suppress a genuine
render failure as if it were an expected warning.

Current Blender reference options:
[native force fields](https://docs.blender.org/manual/en/latest/physics/forces/force_fields/introduction.html)
and [Geometry Nodes simulation zones](https://docs.blender.org/manual/en/latest/physics/simulation_nodes.html).
Native fields make this familiar emitter/effector experiment straightforward;
simulation nodes remain an option for more explicit per-particle state, event
births, or designed formations after the basic choreography is reviewed.

## First render

New-only preview: `out/garden_dust_pilot/garden_dust.mp4`, 68 frames, 1280x720,
24 fps, master audio from song frame 1527. Original plate and camera stay fixed.
Reproduce with Blender `-b -t 4 -P tools/garden_dust_pilot.py`.

Implemented as 56 individually controlled emissive particle sprites in Blender,
not the legacy emitter/physics system. This gives deterministic audio timing.
The drum stem (100–2800 Hz) supplies selected rising-energy events at least
0.25 s apart; one of four mote groups responds per event. Smoothed bass changes
drift width. No added eye animation or haze. Conservative corridor and eye
exclusions are a first-pass placement aid, not foliage segmentation or tracking.

Reusable output: `out/garden_dust_pilot/overlay/0000.png` through `0067.png`,
1920x1080 RGBA PNGs, straight alpha for alpha-over compositing (not additive).
Composite PNGs are saved separately at the same resolution. Music controls,
selected event times, seed and frame range: `out/garden_dust_pilot/controls.json`.
No source clip assignments or protected assembly decisions have changed.
No exit handles rendered. First-frame/state initialization is local to this
pilot; a later reusable take should preserve its origin when cuts move.

## Candidate and intention

- Shot s019 / `forest_fauna_eyes`, lyric "Something with no name is waking".
- Approved still: `codex/out/forest_fauna_eyes_a.jpg`.
- Current cue frames [1527,1595) at 24 fps: 68 frames, approximately
  63.625–66.458 seconds. Shotlist remains the timing authority; recheck cues.
- Keep camera and plate static in the first test. No tracking or eye animation.
- Intention: rhythm appears to disturb a living atmosphere between the watching
  creatures. Make the musical texture spatially perceptible without a waveform,
  spectrum display, whole-frame exposure pulse, or constant sparkling confetti.

The approved image has a dark central passage, several depth cues from eye
sizes and foliage, and warm/cool luminous sources. Low-density pollen in the
passage can add life without reconstructing any animal or matching a hard object.

## One dominant behaviour, one supporting driver

**Drums: a small disturbance releases or lights a pocket of dust.** Analyze the
actual saved-offset drum stem in this exact interval. Use selected strong
onsets, not every grid beat or hi-hat; begin with a minimum 0.25-second separation.
Only a subset of motes responds to a hit. Fast 1–2-frame appearance, then roughly
8–14-frame glow decay; motion continues after the light fades. A hit increases
local spread/velocity briefly, not the brightness of the entire frame.

**Bass: slow collective motion.** A smoothed bass envelope gently changes the
width and speed of the drifting pocket, with roughly 150 ms attack / 400 ms
release as starting values. Do not reverse direction on every bass cycle.
Bound its effect so the drum disturbances remain readable.

Maintain a very faint baseline drift between events. No master-envelope or
synth layer in this first pass. Add a phrase-level build later only if actual
audio or DAW evidence supports a crescendo worth communicating here.

## First image treatment

- One loose, asymmetric ribbon through the central negative space, not a
  perfectly circular vortex. Begin around 30–60 visible motes across depth.
- Predominantly muted green-gold / pale cyan drawn from the scene. No rainbow
  cycling; the existing eyes remain the brightest, most legible points.
- Small, comparatively crisp middle-distance motes; sparse larger soft near
  motes; dimmer tiny distant motes. Avoid camera-wide bokeh or snowy coverage.
- A barely visible, broken haze may connect the dust, but must not lift the
  blacks into a milky fog. Start without haze if particles already communicate.
- Avoid the eyes and reserve the lower lyric region. Use conservative broad
  foliage holdouts so dust isn't visibly drawn across foreground leaf faces.
- Don't make eyes blink, track particles, or pulse in unison yet. That would
  introduce object-specific synchronization before the ambient method is tested.

## Implementation and reusable boundary

Use the existing Blender pipeline, but keep this separate from the scope code.
Represent deterministic seeded particles in a shallow depth volume or layered
planes. A bounded drifting vector field supplies baseline movement; timestamped
drum events add local impulses; bass supplies slow spread modulation. Retain
particle state in song time, not time since the latest cut.

Inputs: source plate, song start/end frames, saved stem offsets, selected onset
times/strengths, smoothed bass controls, random seed, spatial region/holdouts,
palette, density and decay parameters. Outputs: composite preview, separate
transparent effect pass, reusable controls/settings, and a short review record.
Use master audio once in the review, with no synthetic sound added.

Export a premultiplied-alpha pass with its compositing convention documented;
if using additive emission, retain that as an explicit separate pass rather
than disguising additive pixels as ordinary opacity. Keep local light spill
optional and masked; don't bake a full-frame glow into the clean plate.

For a later motion clip, reuse event timing, particle behaviour and broad depth
layers; replace the plate and recheck the spatial fit. Ambient movement tolerates
some imprecision, but does not remove camera-motion/occlusion requirements:
a pan/dolly may need approximate camera compensation, while passing foreground
leaves require masks. Do not claim tracking success from the still test.

## Review deliverable and gates

First render one restrained new-only 68-frame preview, plus an optional
unmodified/effected comparison. Show the new-only version first. No assembly
override: s019 remains a candidate; s002's protected selection is unaffected.
No generated footage is discarded or altered.

Check: can we hear why a disturbance happens? Does it feel like atmosphere in
this garden rather than an added screen layer? Can we still read the eyes and
lyrics? Does bass add organic motion rather than distracting pumping? Does it
stay useful at the shot's actual short duration? If too quiet, adjust one
parameter family, then carry the lesson to a different shot rather than grind.

No handles exist until rendered. If this is adopted, follow exit-only handle
policy and record actual source-time coverage in the assembly register.
