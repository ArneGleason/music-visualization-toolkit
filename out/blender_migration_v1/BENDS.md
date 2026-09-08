# Bends Your Mind native migration

Status: rendered, technically checked and owner-approved. Owner prefers the
native look. Production promotion and full-film integration remain pending.

[Numbered contextual preview](C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/blender_migration_v1/bends_context.mp4)

Review spans song [3438,3710), 272 frames, shots44..47. Shots45/46 use the new
native treatment. Adjacent swimmer treatments use the prior native batch.
Native lyrics appear once and master audio is trimmed from the same song clock.

All137 clean frames and272 review frames decoded and counted at24fps. Both saved
Blender scenes passed dependency checks. Six1080 samples were compared with720;
the largest per-frame mean difference after diagnostic downsampling was1.31
levels on an8-bit scale. Random-access frame100 from the saved720blend matched
the sequential render pixel-for-pixel (PNG metadata differs).

Compared all137 frames against the encoded old look reference. Maximum per-frame
mean difference7.33/255, with the largest differences near the strong trailing
loops. Viewed buildup, peak, worst-difference frame and contextual contact frames.
Native lines are cleaner and their bloom differs somewhat from the old raster
polylines. These are visual candidates, not a pixel-identity or owner-approval claim.

Scope: shots 45 and 46, s045/s046, song frames [3505,3642), 137 frames at24fps.
One continuous effect clock covers both cuts. The original resolved performances
are unchanged, including source [0,69) followed by [68,136). The one-frame reuse
at the boundary is inherited from the accepted edit, not a new timing correction.

Native Blender now builds the radial distortion, RGB dispersion, three looping
spirographs, 320 deterministic mote seeds, phosphor persistence and two bloom
scales. The face-protection field and lower-frame fade are retained. No externally
drawn effect images are inputs. Only the untreated conformed video is extracted
into a source image sequence.

The full animation is stored in each saved .blend. Each trace has a keyed decay
and visibility interval. Thirty-two frames of 0.78-decay history are retained;
the discarded older tail is below0.04% per trace. Blender can render a later
frame directly without executing a frame-by-frame simulation beforehand.

Both sizes use the same reference-coordinate geometry and requested-width
scaling for displacement and bloom. Rebuild the recipe at the requested width,
as specified in NATIVE_CONTRACT.md. This is not a claim that changing only one
resolution field in an arbitrary old scene fixes all its dependent settings.

The native rasterization of ribbons differs slightly from the old OpenCV
polylines. Treat numerical differences as diagnostics. Preserve the approved
choreography and intended strength, not exact compressed pixel identity.

An initial test revealed the opposite sign convention between cv2 remap and
Blender displacement. Corrected before the full render. Reflected edge sampling
is expressed analytically because Blender's displacement extension enum does
not include the old reflection mode. The rejected test is not a delivery.

Reproduction: prepare_bends.py, bends_native.py with arguments bends and width,
run_bends.py for the complete render/review queue, check_bends.py for full-frame
and resolution diagnostics, audit_bends.py for saved-scene dependencies and
random-access rerender. All files and logs stay under out/blender_migration_v1.

The full film is still not native. NEXT_ROSETTA.md records the next stateful
message/receiver family, including the previously hidden assembly replacement.
