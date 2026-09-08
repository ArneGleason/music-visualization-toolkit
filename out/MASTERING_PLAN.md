# Finishing / 1080p planning notes

## Owner direction

Target1920x1080 at24fps. First test and tune a short representative section, not a full-film mastering run. Desired finish is coherent exposure, color, contrast, highlight handling and restrained film-like texture. No actual film transfer. Do not bake a filmic grade/grain into individual source elements and then apply it again globally. No paid upscaling service or full render authorized by this planning note.

## Recommended order

### Approved scope for upscaling

The owner approved source-range upscaling after the picture edit is settled. Quality takes priority over choosing a free tool; a paid upscaler is acceptable in principle, but no provider or purchase has been selected. Test a representative sample and establish cost before a paid production run.

Create an exact source-frame usage list from the locked assembly. Process only ranges contributing to the final picture, including frames actually used in transitions. Keep additional context/handles only where technically required by the chosen upscaler or explicitly retained for an edit need; do not routinely pay to process entire unused clip tails. Merge overlapping ranges from reused takes to avoid duplicate processing. Use higher-resolution originals where available. Preserve the source-frame mapping, frame count and24fps timing, and validate returned clips before substitution.

Render Blender graphics and lyrics natively at delivery resolution over the prepared plates. Do not upscale the flattened720preview as the principal master. Apply the cohesive finishing treatment once after compositing. This decision does not start upscaling now; migration and edit settlement come first.

1. Resolve edit/timing and keep best original downloads plus exact source-frame mappings. Inventory actual dimensions first; do not upscale a720proxy if a higher-resolution original exists.
2. Upscale only needed generated plates and available edit handles to1080, with conservative cleanup if necessary. Preserve duration and timestamps; no invented frame-rate interpolation. This is source preparation, not a creative master. Compare a conventional resample against one temporal AI upscale on a short test; watch faces, teeth, hands, texture flicker, artificial detail and lip sync.
3. Re-render lyrics, vectors, particles, masks and other graphics at1080 or higher, retaining independent emission/alpha layers where practical. Normalize coordinates and scale pixel-valued tracking points, line widths, blur radii, particle sizes and displacement. Recheck registration after upscaling, especially if enhancement changes edges.
4. Composite in a consistent scene-linear working space. Light emission adds; opaque objects use appropriate alpha. Keep HDR core energy until the output transform. Match the underlying generated plates without assuming they contain raw camera dynamic range. OpenEXR/float intermediates for emission/composites where practical, not repeatedly encoded8bit previews.
5. Balance shots and apply one restrained finishing look across the combined image. Shot-level exposure/white-balance/saturation corrections, highlight rolloff and contrast are analogous to balancing a mix; grain, halation and subtle lens texture belong near the end at delivery scale. Avoid double bloom where creative emission already has bloom. Preserve intentional night/day and psychedelic contrasts rather than equalizing every shot.
6. Export a high-quality1080p24 master plus viewing copy, with audio unchanged and present once. Check cuts, sync, gradients, dark detail, text and fine motion. Archive an unmastered composite as well.

## Alternative: upscale flattened720 assembly

Fast and useful as a comparison or low-effort fallback. However, it scales baked lyric edges, particles, masks, compression and blur together. An enhancement model may alter invented lines/text/particles, and controls are no longer independent. Not recommended as the principal final workflow for this graphics-heavy piece.

## Supersampling

Spatial: begin tests with overlays rendered at2x delivery dimensions (3840x2160) then downsample to1080. This is internal oversampling, not a4K delivery commitment. Temporal: motion blur/subframe samples for fast vectors/particles while output remains24fps. More render samples reduce noise but are not a substitute for either higher raster resolution or shutter sampling. Test shutter length for readability of beat accents; avoid smearing lyrics. Procedural compositors also need subframe evaluation; Blender settings alone do not affect existing Python/OpenCV overlays.

Current scripts are not all resolution-independent: several use fixed1280x720 coordinates and some previews have already flattened the effects. Plan a controlled source/layer rebuild, not an automatic upsize switch. Shot8's new overlay uses normalized coordinates and2x spatial/four temporal samples as a preview implementation, not proof that the full toolkit is ready.

## First test, not whole-film processing

Choose brief samples including a face/lip-sync shot, fine TV vectors, colorful particles, and dark water/reflection. Compare A: flattened720 upscale; B: upscale plate + freshly rendered graphics. Then review two restrained finishing strengths on the preferred pipeline. Select process and look before doing the rest. No provider chosen or purchases made.

Technical references: Blender scene-linear color management https://docs.blender.org/manual/en/5.0/render/color_management/color_spaces.html and compositing https://docs.blender.org/manual/en/5.0/compositing/index.html . Pipeline recommendation is project-specific judgment, not a claim that upscaling recovers original detail.
