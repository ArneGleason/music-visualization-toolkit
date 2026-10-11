# Headquarters ark — editable 3D development

Current decision: the user shelved this model and the ImageGen pose-transfer
experiment on October 10, preferring the original graphite robot laboratory ship.
See `ROBOT-SHIP-SO-BRIGHT.md`. Assets below remain available as development history.

The user accepted the balanced lab2-06 illustration and rejected the distorted
three alternative generated angles. On October 10 they requested a real Blender
ship, beginning with simple geometry and then refining its geometry and textures.

## Review assets

First blockout: `generated/design/ark-blender-v01/headquarters-ark-v01.blend`.
Current illustrated working model: `generated/design/ark-blender-v04/headquarters-ark-v04.blend`.
Previous geometry/material model: `generated/design/ark-blender-v02/headquarters-ark-v02.blend`.
Build source: `generated/design/ark-blender-v02/build_ark.py`.

Current look review: http://127.0.0.1:8768/storyboard/ark-illustrated-v01/review-board.html
Previous geometry review: http://127.0.0.1:8768/storyboard/ark-blender-v02/review-board.html
Previous V02 camera sweep: http://127.0.0.1:8768/storyboard/ark-blender-v02/camera-sweep.mp4

Every ship surface in these renders is actual 3D geometry. The illustration is
a proportion guide; no projected artwork or ImageGen angle reinterpretation is
used. The full original illustration remains the target for later detail work.

## Structure and controls

Forward is -X, port is +Y. All six pod roots share Z=0; every structural base
uses the same height. The three physical pairs are centred at X=-6, 0, +6, with
Y offsets +/-4.7, +/-7.2, +/-4.7. Equal canopy radii are 2.8 design units. The
middle pair is farther outboard. Units are arbitrary; these are authored
proportions inferred from one illustration, not recovered physical dimensions.

`ARK_ROOT / animate this transform` moves the entire ship. Each named POD root
owns its canopy, base, terrain, water, colonies and internal illumination. The
spine, twelve broad curved supports and the single vertical aft field ring are
separate editable objects. The renderer verifies pod count, mirrored pair
centres and common structural level. The six physical biome assignments remain
fixed in the model, regardless of camera angle.

The second pass adds procedural hull microtexture, graphite joins, amber trim,
cyan culture galleries, glass thickness, terrain ridges and river channels,
small alien colony placeholders and separate habitat service lighting. Dome
normals face outward. Broad studio lights are hidden from transmission rays;
internal lights illuminate habitats without large reflected/refracted white discs.

Four named review cameras give forward, aft, top and low side views.
`CAMERA_ORBIT / optional yaw animation` carries the main camera through a
60-degree arc over 120 frames at 24 fps. The model itself does not deform.
The five-second review sweep is a design test, outside the song edit.

## Illustrated lighting and surface pass — V04

The user accepted the V02 direction and requested a closer match to the film's
painted graphic-novel look. V03 adds fitted spine armour, fine fasteners, layered
pod bases, smaller varied alien colony meshes, terrain shading and habitat haze.
V04 replaces the opaque cyan window inserts with twelve real hull openings,
dark recessed galleries, transparent lenses, culture vessels and service structure.
The physical six-pod positions remain identical to V02.

Warm key light, cool fill and aft rim lighting separate ivory alloy from graphite
recesses. Procedural surface variation, denser small vegetation, blue-violet space
clouds, faint field filaments and restrained amber/cyan glow develop the style.
The final compositor adds a subtle anisotropic brush finish: 3-pixel radius,
35% blend. Original edges and small details remain dominant. This is a native
Blender compositor, applied to live Render Layers in the saved model.

Proof settings: Cycles/OptiX, 96 samples with denoising, 1600x900, AgX Medium High
Contrast, exposure +0.25. Fog Glow uses threshold 1.25, size 0.14 and strength 0.55.
All materials are procedural. The saved scene has no external texture files or
cached-image compositor dependencies. EXRs in the development folder are only
comparison caches; the working .blend renders its own geometry.

Forward, aft and detail proofs use the same model and lighting. The review also
includes the approved illustration, V02 render and the new render before the
subtle brush finish. Saved-model inspection verifies six unchanged pod centres,
live renderer input, the filter settings and no external image textures.

Sources, applied sequentially after the V02 builder:

- `generated/design/ark-blender-v03/style_ark.py`
- `generated/design/ark-blender-v04/polish_ark.py`
- `generated/design/ark-blender-v04/finish_look.py`

Verification: `generated/design/ark-blender-v04/saved-model-verification.json`.
Creative Production board: `ea37232e-e258-4176-b1b9-1d38747fc88e`; completed items
`ark-blender-v04-hero`, `ark-blender-v04-aft`, `ark-blender-v04-detail` (revision 64).

## Further refinement

The subsequent ImageGen pose experiment combines native V04 camera renders with
the approved illustration. Forward and aft output images preserve the broad
six-pod layout and improve painted detail substantially, with some local silhouette
and panel drift. Review:
http://127.0.0.1:8768/storyboard/ark-pose-transfer-v01/review-board.html .
Exact prompts, input ordering, provenance and actual QA are in
`generated/storyboard/ark-pose-transfer-v01/experiment.json`. These are unselected
starter-frame experiments; the .blend remains the pose guide.

The updated materials and lighting are closer to the illustration, while the
spine silhouette, support arms and habitat ecology remain simpler. Gallery
interiors now have physical depth, but their culture vessels are simple meshes.
The six habitats still share underlying terrain structure, despite fixed biome
identities and different small colony meshes. The brush finish has been reviewed
in stills; its temporal stability needs checking in the next animated render.

Next priorities after proportion review:

1. Refine the spine silhouette and arm joins after review of the new look.
2. Give each physical habitat more distinctive terrain and detailed ecology.
3. Refine canopy reflection and the field-ring housing.
4. Check the illustrated compositor in motion at final delivery resolution.
5. Render the four replacement lyric shots from this same model, using the
   existing canonical frame grid and editorial fades.

All meshes and shader networks are in the .blend. Current materials use
procedural nodes; no external texture maps are needed. Rebuild with Blender
5.2 in background mode and the saved build source. Rendered images and models
remain under ignored `generated/`. No paid Kling generation occurred, and the
V33 animatic timing and soundtrack remain unchanged.
