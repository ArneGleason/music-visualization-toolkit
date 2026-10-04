# Ship and distant-world experiments

Review: http://127.0.0.1:8768/storyboard/depth-field-experiments-v01/

These candidates do not replace the shotlist's current motion selections or
the full animatic. Original listening notes and their frame positions remain
unchanged.

## Native ship hybrid

`tools/build_hybrid_ship.py` derives a separate scene from the opening-v02
Blender file. Shot 4 supplies its camera and 122-frame span: 98 edit frames
plus 12 frames at each end, at 24 fps. Render size is native 1920 × 1080.
Preview animation uses eight Cycles samples with denoising; the still uses 24.

The ship is native geometry: continuous metal annulus, two circular platforms,
engine ring, panel seams, sparse rectangular cyan lamps, amber rims and the
thin geodesic field. Satin material and platform details are an initial look
development pass, not an exact reconstruction of the approved ImageGen finish.

Planet, volcanic moon, ice moon and stars are one ImageGen illustration on an
unparented plane 50,000 model units away. This eliminates nearby moon meshes
and their excessive translation parallax for this modest camera move. It is
not a spherical environment or a physical orbital model.

Harper is a separately generated RGBA card, packed into the Blender file,
with a small vertical float. She has no articulated animation or changing
viewpoint. Large camera orbits, changing poses and close acting shots require
a separate actor animation/compositing approach. Emissive illustrated layers
also do not yet provide fully integrated scene lighting or shadows.

Generated assets live in `generated/storyboard/hybrid-ship-v01/` and stay out
of Git. Rebuild with the installed Blender executable and:

    --background --python tools/build_hybrid_ship.py -- projects/a-right-little-something

## Kling shot 2 comparisons

Plan and identical prompt lock: `kling-depth-field-experiments.json`.
Three 7-second 1080p generations cost 56 credits each, 168 total. They use
one starting image, no ending image, and the same fixed-camera depth guidance.
Exact review edits contain 136 frames after a 12-frame lead-in. Master audio
starts at authoritative shot frame 228; no time stretching is applied.

- Lines: distant background is more stable in the fixed-camera test.
- Dots: subtle dots can resemble stars; Harper unexpectedly turns away,
  confounding a pure comparison of display styles.
- Rotating dots: Kling restores prominent hexagonal lines. The requested
  five-degree rotation of only the display is not reliably demonstrated.

These are visual observations, not measured moon tracking or proof that the
same instructions solve a moving camera. No further generation was submitted
for the native ship experiment.

`tools/review_ship_experiments.py` assembles separate 1080p review clips with
master audio and verifies their frame counts. It does not update the current
animatic pointer. Image editing prompts are preserved in
`depth-field-imagegen-log.json` and `hybrid-actor-prompt.txt`.

## Native energy field revision

Review: http://127.0.0.1:8768/storyboard/energy-field-v01/

The requested direction is connected dots and lines, rather than isolated
dots. Junctions stay consistent; line brightness varies as though external
disturbances require more energy from different parts of the field. Keep the
camera locked and the motion restrained. This is an artistic effect, not a
solar-wind simulation.

`tools/build_energy_field.py` derives a separate scene from the native hybrid.
It uses the same geodesic edge coordinates and 320 unique junctions, with
steady dots and a traveling, smooth brightness wave on the connecting lines.
Only the display rotates: six degrees over 122 frames. Camera transforms are
held at the shot 4 edit-in view. Ship and distant plate do not rotate with it.
Harper retains the prototype's tiny float on her illustrated card.

The earlier requested rotating-dot test and the locked-camera lines clip are
Kling animations, not Blender motion graphics. The new energy field is actual
Blender geometry and material animation, with no additional paid generation.

`tools/review_energy_field.py` renders review movies using the authoritative
98-frame shot 4 edit and 12-frame handles on each side, native 1920 × 1080 at
24 fps. Matching master audio is sliced at the shotlist frame positions.
The preview uses eight Cycles samples and denoising, so fine transparent lines
can show sampling noise. This candidate does not replace the current animatic.
