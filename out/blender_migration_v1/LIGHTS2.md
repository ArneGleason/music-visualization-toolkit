# Native lighting batch2: receiver and held specimen

Owner review pending. No production or canonical shotlist changes. Earlier aerial/probe approvals remain in force.

## Receiver, whole-film cut12

Song frames805..856, source0..51, raw `clips/raw/receiver_dial_macro_v6.mp4`. Uses the existing checked homographies and the actual lead-vocal response from `out/receiver_voice_review/fx/tracking.json`. No return to the earlier drum-driven treatment. Native inverse-homography aperture selection, warm-color qualification, multiplicative core reinforcement, two-scale additive bloom. Analytic aperture coordinates are normalized through the reference1280x720 coordinate system; no fixed-size FX mask is imported. Boundary feathering is reconstructed in Blender and need not be pixel-identical to OpenCV.

## Held specimen, whole-film cut25

Song frames2016..2122. Untreated plate is source12..118 of `out/lipsync_followup_review_v1/specimen_combined.mp4`, which preserves the original listening lead-in and accepted later lip sync. Do not substitute the older un-synced performance.

Native source-color mask, local prop-region restriction, neutral glove exclusion, circulating centroid-based accent, vocal envelope, acquisition2062..2070, stronger2087 punctuation, and final settling. Blur and emission compositing are Blender nodes. Existing screen-like response is deliberately reconstructed as its accepted appearance, not replaced with an arbitrary new glow. The glove-edge softening is approximate, not hand roto or a solved3D object. No new acting, camera or lyric timing changes.

Preparation extracts untreated footage and computes tracking/control numbers only. No externally generated FX masks, glow images or deformation layers feed the render. Both saved Blender files contain native animated image-sequence inputs and can render their full frame range. The specimen confinement output uses Blender5.2's explicit AOV name; a missing connection discovered in the initial test was fixed before final batch rendering.

## Reproduce

Run `prepare_lights2.py` with ordinary Python, then Blender with `lights2_native.py -- receiver 1280` and `lights2_native.py -- specimen 1280`. Width1920 rebuilds all dependent render dimensions and blur widths for1080output. Optional final argument is a comma-separated list of1-based sample frames. `native_nodes.py` provides procedural math-node helpers shared by these recipes.

`finish_lights2.py` checks reference differences, encodes silent native candidates, validates counts, and prepares isolated review mappings. `lights2_preview.py` uses the existing Blender assembler and native lyric renderer, with the same small whole-film numbers. `mux_lights2.py` supplies the master audio once at the exact song origin. No comparison panels or full-frame diagnostic labels.

The receiver context includes the previously accepted native probe effects on both sides; the specimen context includes the preceding table shot. Adjacent footage is retained, not claimed as newly migrated. No mastering or paid upscaling performed.
