# B1 afterglow v4: organic projector patterns

Owner liked v3 strength and room motion, but requested larger-scale fractal imperfection rather than perfect smooth color shapes.

V4 keeps the same depth proxy, palette, nominal intensity, artifact effect, practical-light animation, and performance. Three seeded coherent noise octaves distort projector coordinates and contour shapes, with gentle uneven brightness. Noise drifts continuously in projector space, not random frame-to-frame grain. The largest shapes dominate; smaller octaves add soft irregularity rather than sparkle.

Status: OWNER APPROVED. V3 retained as comparison. V4 is the selected B1 treatment for the next assembly; global production shot assignment remains pending the outro merge. Approved selection and exact source range recorded in docs/OUTRO_REVISION_V2.md.

## Assembly contract

- `clean.mp4`: silent 1280x720, 24 fps, 191 frames. Source zero = song 4165; end exclusive 4356.
- B1 uses source 67..97, song 4232..4262.
- `preview.mp4`: 154 frames, song 4177..4331, approved A TV / revised B / approved A TV, master audio once.
- Blender combines v1 optical and artifact-light sequences with only the v4 room layer. Do not stack another afterglow clean or duplicate artifact effects.
- Existing face, window exclusions and right-hand practical light positions preserved. No new generation, lip sync or mastering.
- Delivery script validates full decode, frame counts and frame rates.
