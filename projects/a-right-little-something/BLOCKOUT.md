# Sphere spacecraft: small Blender experiment

The working scene is `generated/blockout-moon-identities/sphere-ship-blockout.blend`.
The plain two-moon study remains in `generated/blockout-moons/`.
The initial experiment remains in `generated/blockout/`.
Two matte rocky moons have independent ROOT objects for art-directed placement
and scale. A single distant SUN illuminates the ship, planet and both moons;
its `towards` vector in `blockout.json` points towards the source. In the exterior
camera it lights from above and slightly screen right. The sun is off camera.
Soft world illumination keeps shadow detail readable, and ship trim emits light.
These are composition proxies, not simulated orbital positions or physical sizes.

Stable celestial identities live in `blockout.json` and Blender custom properties:
`moon-a` is the larger volcanic moon (charcoal basalt, branching orange lava
fissures); `moon-b` is the smaller ice world (pale cyan plates, deep blue fracture
networks). ROOT objects carry `id`, `surface`, and `identity`; meshes carry
`celestial_id` and `visual_identity`. Procedural surfaces follow their objects
when moved or rotated. Preserve these identities across camera views and image
prompts; apparent size and placement may be art directed. Lava emits locally;
the shared sun still determines reflected-light direction on both worlds.
It contains a clear spherical cabin, a broad equatorial band, upper/lower
platforms, a vertical rear engine ring, a floating figure proxy, and a separate
globe with latitude/longitude lines and a north-pole marker. The two supplied
reference images are packed into the file in a hidden viewport collection.

The dimensions in `blockout.json` are artistic working assumptions. They are
not recovered measurements or a final spacecraft design. Bow is -Y, engine
is +Y, and up is +Z. A cyan bow chevron and cardinal ticks mark orientation.
The figure is a scale/pose proxy, not Harper's finished character model.

Collections separate ship geometry, figure, globe, orientation marks, cameras,
references and lighting. Move/rotate the SHIP ROOT to place the whole ship.
The PLANET ROOT can be moved/scaled independently for composition. Hide the
orientation collection for clean reference frames. The shell shader keeps its
centre transparent and reflects at the rim; it is a legibility approximation
for this blockout, not physically accurate thick glass.

Four cameras share the same ship: Exterior, Interior, Side layout and Top
layout. A fifth camera, Inspection arc, has an editable three-second move on
frames 1–72. This is a design inspection, not a timed shot in the song edit.
The music timeline and `shots/shotlist.json` have not been replanned.

The camera `planetScale` values in the JSON allow per-view planet-size changes
when rebuilding/rerendering. In interactive Blender, edit PLANET ROOT directly;
camera custom properties are descriptive and do not install automatic handlers.

Rebuild using the existing Blender installation:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 6 --python tools/build_ship_blockout.py -- projects/a-right-little-something/blockout.json --motion
```

This recreates the file from the configuration, so preserve hand-edited Blender
work under another filename before rebuilding. Generated renders and the
packed `.blend` stay out of Git. The construction script and small configuration
retain the reproducible blockout.

## How to judge the experiment

Compare exterior and interior compositions for readable orientation, ring
placement and figure scale. Use the inspection move to see what holds up as the
camera shifts. Prefer changes that improve the image over strict physical scale.

The renders can guide composition and the position of objects in styled
keyframes. Keep the illustrated references as the appearance/character guide.
Blender can retain camera motion and common geometry; a generated-video result
still needs visual review for geometry and continuity. This experiment does not
test a video provider's reference-video support or guarantee that it will preserve
the blockout. No generated footage or paid image generation was used.

A useful next test is one short exterior shot and its related interior shot,
then compare that result with the reference-sheet workflow from Monsters Undone.
Avoid detailing the entire spacecraft before that comparison.
