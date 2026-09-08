# Green-light garden walk, shot18

Native migration rendered and technically checked, owner review pending.
Preserve song[1412,1514), source[0,102),24fps.

[Numbered preview, shots17..18](C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/blender_migration_v1/walk_context.mp4)

All102 clean frames and140 review frames decoded and counted. The largest
per-frame average difference from the old uncompressed reference is0.187/255.
Six1080 samples passed; diagnostic downsample differences average at most
1.219/255. Two saved-scene renders match sequential output pixel-for-pixel.
Source hash, tracking and source-only image dependency checks passed. Native
frames, higher-resolution accent and the numbered contact sequence inspected.
These checks do not substitute for owner playback approval.
The original footage is clips/raw/forest_walk_track_v6.mp4. Its generated light
remains in the picture, with only the approved minor tracked reinforcement.
The separate green guide uses the accepted Catmull-Rom swoop, two motion samples,
six tapered wake samples, bright core and broad additive bloom. Lead-vocal
amplitude and the accent on green light retain the original timing and strength.

prepare_walk.py extracts only original footage and numerical controls. No FX
pixel buffers feed the native recipe. walk_native.py builds analytic shader
light fields and native compositor addition, preserving the old display-referred
light sum through an explicit sRGB conversion. Coordinates are normalized to
the camera frame; the width argument rebuilds at720 or1080 without shifting
the light, changing the path or changing the glow's relative size.

This retains a peripheral authored overlay, not a new physical relighting or
camera-tracked3D simulation. It intentionally preserves the accepted appearance
and does not invent occlusion or cast light onto the performer.

run_walk.py produces102 clean frames and140 numbered review frames[1374,1514),
including the preceding raw garden entrance. The native lyrics and master audio
are added once by the shared-resolver Blender assembler. walk_shotlist.json
extends the screen candidate snapshot without editing production assignments.

Validation: all-frame old-uncompressed comparison, six1080 samples, two
saved-scene random-access checks, original-source hash and tracking equality,
native source-only dependency audit, full decode and exact frame counts.
See walk/qa.json, blend_audit.json and receipts.json after completion.

No paid generation, upscale, mastering, commit or production promotion.
Moth shot19 and waking-eye shot20 remain separate pending migrations.
