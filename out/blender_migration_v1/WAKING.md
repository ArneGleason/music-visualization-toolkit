# Waking garden, shot20

Native migration rendered and technically checked, owner review pending.

[Numbered preview, shots19..20](C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/blender_migration_v1/waking_context.mp4)

All81 native frames and136 review frames decoded and counted at24fps. Six1080
samples passed, largest diagnostic downsample mean difference0.816/255.
Largest per-frame mean difference from the accepted uncompressed reference is
1.404/255. Saved-scene frames38/61 match sequential output pixel-for-pixel.
Original eye centers/openings and all81 airflow diagnostics match exactly.
Source hash and both saved scenes' original-image-only dependencies pass.
Closed, partly open and late opening frames,1080 late opening, and the numbered
context contact sequence were visually inspected. See waking/qa.json,
blend_audit.json and receipts.json. Technical checks are not owner approval.

Song[1569,1650),81frames
at24fps. Source out/garden_eyes_motion_v1/base.mp4 frames[0,81). Context
preview[1514,1650),136frames, starts with the owner-approved native moth.

The nine creature groups/17 eyes retain exact accepted tracked centers and
aperture cues, including one-frame asymmetry within pairs. Native shader masks
cover the existing source-eye halo until the soft aperture opens. Blender's
Inpaint compositor fills the closed region from the original image, replacing
the prior Telea fill. Full opening restores the original eye and halo.

Shadow-detail lift retains the original luminance gating, eye exclusion and
gamma0.86 response. Fine contour shimmer is now native Sobel plus4D noise,
advected by the broad camera fit, rather than the old pixel noise grid advected
by dense optical flow. This is an intentional texture approximation; local
leaf deformation is not claimed to have the original exact noise trajectory.
Foliage detail, approximate green phosphor strength and waking accent remain.

Airflow reuses the accepted deterministic3D simulation:3600 motes,100 wisps,
three depth bands,8 simulation substeps, seed19031, drum emission envelope,
bass-modulated velocity, helical forward eddies and proxy foliage deflection.
The original camera fit, motes, velocity-stretched quads and two Gaussian halo
bands are retained. Eye-clearance data are used only to derive numerical
per-particle visibility, not as a final image/AOV dependency.

capture_waking_air.py captures numerical mesh/color state from that simulation
without rendering external FX images. waking_native.py stores each frame's
mesh state and visibility natively, animates the perspective camera, renders
air separately and combines it with the raw source before the waking layers.
Saved blends need only original source plates, no .npy masks, geometry.npz
loaders, frame handlers or old rendered composites. Numerical caches are build
inputs, not external compositing layers. Camera projection and shader UVs scale
with render resolution; inpaint reach, edge strength and blur scale accordingly.

The isolated waking_shotlist.json extends the moth snapshot. Shared assembler
source resolution remains active, native lyrics once, master audio once,
small review numbers19/20. No canonical promotion, paid generation, upscaling,
mastering or Git changes. Full-film migration remains incomplete.

Checks planned: exact eye tracks/openings, exact airflow diagnostics, original
source hash,81-frame comparison, six1080 samples, saved-scene random access,
source-only image dependencies, full decode and frame counts.
