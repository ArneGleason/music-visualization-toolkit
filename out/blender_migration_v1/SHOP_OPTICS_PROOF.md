# Shop optical transition proof

Native compositor test: `shop_optics/preview_optics_only.mp4`.
85 frames, song frames [2399,2484), 24 fps. No change to performances or clocks.
This intentionally omits the alien-head signal and lyrics so the optical join
can be inspected by itself. It is not a replacement for the approved full shot.

The native scene uses the untreated, timestamp-conformed wide performance and
untreated close-up sequence. It averages 17 transform samples for the push,
switches sources at 2431 without dissolving faces, applies 13 radial samples
and brief defocus, then settles into the unchanged close-up at 2436. The
compositor explicitly resamples in display space before returning to linear
output, preserving the original blur character more closely.

All 85 frames render and the preview decodes. Eight representative 1080 frames
include entry, blur peak, source switch and exit. Largest downsampled mean
difference is 1.563/255. Comparison to the prior compressed picture-only render
averages 1.653/255, largest per-frame mean 2.178/255. These are diagnostics, not
pixel-identity claims. Visual contact review shows the intended direction,
blurred switch and clean landing. Reloading the saved scene and rendering frame
33 directly matches the sequential render exactly at the pixel level.

## Reusable lessons

- Keep independent source origins; select sources by song frame, not local shot
  time or a dissolve.
- Scale transform offsets and blur radii with requested render width.
- In Blender 5.2 the compositor Scale mode is a Type input, not the old space
  property. Inspect actual installed node sockets when porting older examples.
- Display-space versus linear-space averaging can change optical appearance.
- Pass absolute output paths to saved-scene render jobs. Blender can change the
  process working directory when loading a saved file. The random-access output
  from this test was moved back into the intended out/ directory after checking.

Next integration step: reconstruct the approved signal as native paths, retaining
its window crop and disappearance at 2433, then review with the preceding globe.
Do not mark cut 29 fully migrated or promote this proof in a production manifest.
