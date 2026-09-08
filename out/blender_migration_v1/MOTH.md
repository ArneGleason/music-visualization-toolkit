# Psychedelic moth, shot19

Native migration rendered, technically checked and owner-approved.

[Numbered preview, shots18..19](C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/blender_migration_v1/moth_context.mp4)

All55 clean frames and89 review frames decoded and counted at24fps. Six1080
samples passed; largest diagnostic downsample mean difference1.876/255. Largest
per-frame mean against the old uncompressed reference1.981/255. Saved-scene
frames24/40 reproduce sequential output pixel-for-pixel. Source hash, controls
and source-only image dependencies passed. Native peak frames, the1080 peak
and final numbered context contact sequence were visually inspected.

A quiet-frame border clamp was caught and corrected before delivery: when the
optical envelope is zero, sampling is identity, not clamped six pixels inward.
Frames1..7 and48..55 were rerendered, both scenes saved, preview rebuilt and all
checks rerun. run_moth.py --repair reproduces that bounded correction.

Song[1514,1569),55frames
at24fps, raw forest_fauna_moth_v6.mp4 source[0,55). Native preview includes
the preceding migrated walk, starting1480 and ending1569 exclusive.

Preserved: voice-driven warm wing light; eased central optical displacement
and red/blue fringe on psychedelic; limited edge iridescence; three spectral
ghost-wing echoes rooted around the thorax. Colors, trajectory, sparkle and
phrase envelopes are taken from the accepted garden_ghost_wings_v3 recipe.

prepare_moth.py reads the original footage to extract numeric contours. It
does not export FX masks, particle raster layers or distorted pictures.
moth_native.py renders the contour points as native colored disc geometry,
separates geometry from optical AOVs, and uses native masks, blur, displacement,
edge detection and additive composites. Saved scenes retain all frame animation.

Intentional native-renderer differences: subpixel discs replace integer-rounded
circles; Blender sampling replaces OpenCV antialiasing; native Laplace filtering
replaces the old small convolution kernel. Edge strength compensates for render
pixel scale. This is appearance preservation, not a bit-identical raster clone.
Reference coordinates are camera-normalized; displacement and blur scale with
render width. Optical image sampling uses Blender's bilinear displacement.

run_moth.py reuses the validated walk review pipeline with explicit55-frame
shot and89-frame context counts. It extends walk_shotlist.json as an isolated
moth_shotlist.json, preserving shared source-selection decisions. No canonical
shotlist changes, generation, upscaling, mastering or Git operations.

Required checks: all55 native frames against accepted uncompressed reference,
six1080 samples, saved-scene random access24/40, source hash and controls,
source-only image dependencies, complete decode/frame counts. Check moth/qa.json,
blend_audit.json and receipts.json after completion. Waking-eye shot20 remains.
