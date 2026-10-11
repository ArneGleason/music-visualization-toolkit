# Orbit flight and camera revision — October 10

## V25 — orbital speed, motion blur and a comet-like wake

`orbit-blender-v03.json` replaces uniform arc-distance timing with
distance-dependent vis-viva speed on the two looping passes. Eccentricity is
0.24: the planet is the ellipse's focus, so closer sections are faster and the
far sections slower. Semimajor axes retain the previous 1.55/1.6 radius ratios.
Curvature-matched connectors retain the broad approaches and flowing transfer.
Approach/transfer timing is authored, and one global time scale fits the
existing 108 travel frames inside the 138-frame song shot. These are fictional
worlds and an illustrated itinerary, not a full gravitational simulation.
[NASA's explanation](https://science.nasa.gov/mission/cassini/gravity-assists/)
distinguishes planet-relative approach/departure speed from the net assist
due to the planet's own motion. A circular orbit itself has constant speed;
the eccentricity gives the requested speed variation a geometric basis.

Native Cycles motion blur uses a centered 0.65-frame shutter. Ship and core
transform keys are sampled eight times per output frame, with 16 motion
intervals per mesh and 32 ray samples. Euler heading is unwrapped across
revolutions to prevent artificial spins during shutter interpolation.
The output remains 24fps. The illustrated background is retained without
adding a global blur. Sparks use elapsed-time positions at the same variable
flight speed. This is native transform blur; it does not integrate animated
material emission separately at every shutter instant.

The ship has a strong white-cyan tracking core. Filament power is reduced to
one quarter of v23, with fewer and dimmer sparks. Trail UVs store normalized
passage time, so decay follows elapsed time even while speed changes. The
new brightness envelope is 92% fast exponential falloff (2-frame scale) plus
8% slow exponential tail (12-frame scale), tapered to zero over 48 frames.
It reaches about 11.4% brightness at age 5 frames and 0.54% at 24 frames.
The result is a short bright wake with an extended faint tail, rather than
orbit rings competing with the ship. Color, planetary occlusion and the
illustrated bloom treatment are retained.

Checks: the relative speed spans 0.620–1.277 (2.06× peak/slow), passage times
are strictly increasing, and sampled angular momentum varies by only about
0.031% within each loop. The connector timing is intentionally separate from
that Kepler check. Native scene, path/speed plots and look proofs live under
`generated/storyboard/orbit-blender-v03/hybrid/`; movie recipe is
`revision-chorus-v05.json`. Prior v24 media is retained. No paid generation.

Review: http://127.0.0.1:8768/storyboard/chorus-revision-v05/ .

## V24 — animated scale reveal

V24 retained the orbital flight and fade direction described below, and filled
the scale placeholder with `scale-reveal-motion-v01` Kling footage beneath
the same editorial camera reveal. Its 48-credit upload was explicitly approved
and the completed take is in the current animatic. Review:
http://127.0.0.1:8768/storyboard/chorus-revision-v04/ .

## V23 — fade language and continuous trajectories

User direction: fades are the default within this coverage/chorus sequence.
Reserve zoom blur for a motivated zoom between connected locations. Do not use
it as a repeated decorative transition. Fades overlap source handles and are
centered on the existing timing-grid boundaries, including the portrait and
scale cuts; the chorus still enters at frame 1046 / 43.54s.

`orbit-blender-v02.json` replaces the abrupt-looking orbit entries with broad
approaches and a transfer that match the position, tangent and curvature of
each loop. Each planet gets a continuous full revolution. The light colors,
layered filaments, sparks, illustrated bloom and painted background are retained.
The geometry is inspired by the smooth bending in
[NASA's gravity-assist diagrams](https://science.nasa.gov/learn/basics-of-space-flight/primer/).
These full loops are an authored visual interpretation; a gravity-assist flyby
does not itself capture a spacecraft into a full circular orbit. This is not a
numerical orbital-mechanics simulation.

Trajectory tube UVs record distance along the path. An animated head distance
gives every point an age, so both the amber orbital trace and the colored wake
fade behind the ship rather than remaining as permanent rings. Amber decays
over 30 frames; the bright filaments over 22. Flight begins at source frame 25
and lasts 108 frames, placing the approaches, both loops, departure and the
decay within the existing 138-frame edit. The source retains 24-frame handles.

Editable scene: `generated/storyboard/orbit-blender-v02/hybrid/orbit-hybrid.blend`.
The complete path study and six composite proof frames are beside the scene.
The path study deliberately displays the whole route for inspection; the final
motion shows only emitted, decaying trails, with planetary depth occlusion.
Recipe: `revision-chorus-v03.json`. Review:
http://127.0.0.1:8768/storyboard/chorus-revision-v03/ .
At v23, the scale-reveal illustration still needed its animation pass. No new
paid generation is part of this revision.

The camera reference is Ken Burns: a continuous, purposeful movement through
the composition. No noise, camera shake, oscillating motion or repeated zoom
pulses within a shot. Start on a subject and travel toward the consequence.
The recipe uses smoothstep pans, bounded crops and two-times oversampling.

The scale insertion stays at frame 854 / 35.54s. A fresh exterior illustration
replaces the recycled opening footage. The camera opens from the ship toward
the immense horizon. The mission at frame 1046 / 43.54s travels from Harper
toward the ecosystems. The creature-level view tracks along the bank; the
key wide at 1263 / 52.58s opens from Harper onto the larger branching response.
All original phrase boundaries and the quiet arms-wide camera are retained.

Two six-second Kling requests were explicitly approved for 96 estimated
credits after automatic review required approval for that paid image upload.
The actual submissions charged 48 credits each. Prompts are in
`kling-ecology-motion-v01.json`. The creature request specifies alternating
planted steps, body travel relative to stones, weight shifts and water-contact
ripples. The wide request asks flowing channels, successive frond responses
and active walking. These are generation targets, not guarantees of the result.

## Blender experiment

`orbit-blender-v01.json` and `tools/build_orbit_flight.py` describe actual 3D
flight curves, two tilted looping flybys, smooth tangent connections, the
existing native spherical ship geometry, cyan/white/violet/amber filament
wakes, deterministic drifting sparks and two bloom scales. The ship turns
along the path. Planet spheres occlude the trail portions behind the worlds.
The flight occurs over 193 source frames; the song uses 138 frames with a
24-frame lead-in and at least 24 tail frames.

The hybrid uses the clean Kling background with hand-matched world silhouettes
and assumed depths. It preserves the painted terrain, clouds and illustrated
star rays while Blender supplies the ship and effects. Depth assignment and
world matching are art-directed, not a recovered physical camera. Blend the
effects in RGB; applying Screen directly to YUV chroma introduces a magenta
cast. The earlier single 2D vector line remains available in v21.

The separate native look study contains displaced sphere terrain, colored
water, a procedural cloud shell, atmospheric limb shading, a seeded starfield,
procedural nebula and authored radiating star rays. It uses no visible Kling
background. Its simpler terrain/cloud appearance does not yet match the
detailed painted reference; it is not a finished substitute for the shot.
The study is rendered at 1280×720; hybrid motion is rendered at 1920×1080.

Matching the complete world in 3D needs dedicated passes for terrain silhouettes,
painted surface detail, cloud shapes, atmospheric color and light composition.
Matching one constrained view is easier than building a scene that remains
convincing from new angles. Camera-projected artwork could preserve the look
for a bounded move, but would retain baked lighting and require new information
for newly exposed surfaces. The hybrid is the closer immediate visual match.
These effort assessments follow the local prototypes; no exact reconstruction
or fixed completion time is promised.

Look review: http://127.0.0.1:8768/storyboard/orbit-blender-v01/review-board.html .
Editable Blender scenes and renders are under `generated/storyboard/orbit-blender-v01/`.
The full revision recipe is `revision-chorus-v02.json`, registered as a versioned
proposal in `shots/shotlist.json`. Large media and native scenes stay out of Git.
