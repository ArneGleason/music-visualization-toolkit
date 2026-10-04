# Stable moon identities

- `moon-a`: larger volcanic moon, charcoal basalt, branching orange-red lava fissures and localized glowing basins. Leftmost moon in the current exterior camera.
- `moon-b`: smaller ice world, pale cyan/white frozen plates with dark blue branching fractures. To the right of Moon A in the current camera.

These IDs and descriptions are stored in `blockout.json` and native Blender object custom properties. Screen positions may change between shots; identities must follow the objects. Procedural material coordinates stay attached to the geometry. Surface patterns in generated illustrations are approximate, not exact texture matches.

Model: `generated/blockout-moon-identities/sphere-ship-blockout.blend`.
Selected illustration: `generated/blockout-moon-identities/starting-frame-volcanic-ice-v01.png`.
Both retain the shared upper-right sunlight; the volcanic lava also emits its own light.

## Approved ship appearance reference

On 2026-10-04 the user approved this illustration as a reference for the ship's
details, lighting arrangement and finish. A stable copy is registered in
`project.json` as `ship-finish-lighting-approved-v01`, at
`generated/refs/ship-finish-lighting-approved-v01.png`.
Carry forward the dark grey satin metal, panel seams, layered platform rims,
continuous amber edge lights, sparse cyan rectangular band lights, cyan inner
engine-ring arc, and clear glass with restrained reflective highlights.
Use this alongside the original geometry and character references when making
future ship frames. Camera composition and planet scale remain art directed.

## Built-in Image Gen edit prompt

Use case: precise-object-edit. Image 1 is the finished illustration edit target. Image 2 is the Blender moon-identity reference only. Change ONLY the surface appearance of the two moons in Image 1. Preserve the spaceship, woman, planet, starfield, camera composition, lighting and every other element as closely as possible. Preserve the exact two moon silhouettes, screen positions and apparent sizes.
Stable identity moon-a: the LARGER moon at upper LEFT becomes a volcanically active world: dark charcoal basalt crust with irregular branching orange-red lava fissures, a few glowing lava basins, rugged black volcanic terrain. It must read as a dark rocky world with localized glowing magma, not a sun or an entirely molten orange ball. Reflected sunlight comes from upper right; lava itself glows even on its night side.
Stable identity moon-b: the SMALLER moon to its RIGHT becomes an ice world: pale cyan and white frozen plates, distinctive deep blue branching fractures, some frosty bright ridges, clearly icy rather than ordinary grey cratered rock. Reflected sunlight also comes from upper right, dark lower-left limb; no lava on this moon.
Image 2 indicates the contrasting charcoal/orange and pale blue identities; make the natural irregular surface detail match Image 1's polished cinematic painterly illustration, not the coarse procedural cell pattern. Exactly two moons. No added objects, no labels, text or watermark.
