# Message sprites and receiver: native migration

Status: native look accepted by the owner. Technical checks complete. Not
promoted to production; whole-film integration remains pending.

[Numbered preview: sprites into receiver](C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/blender_migration_v1/message_context.mp4)

All230 native frames and230 numbered review frames decoded and counted at24fps.
The171-frame performance cache is silent and frame-count checked as well.
Both saved Blender scenes pass source-image dependency checks. Seven1080 samples
pass the resolution comparison, with maximum per-frame mean difference1.43/255
after diagnostic downsampling. Saved-scene frames70 and211 match the corrected
sequential renders pixel-for-pixel. Original receiver file hash matches its
handoff receipt. See message/qa.json, blend_audit.json and receipts.json.

Visual review covered entrance, knob binding, the peak burst, seven-resolution
diagnostics and the numbered context contact sequence. The final encoded burst
was checked explicitly because the eight-frame contact sheet stops before it.
Old encoded-look comparisons are diagnostic only: maximum mean difference6.72
levels/255, including old display treatment and differing native line/blur
sampling. Do not mistake technical checks for owner look acceptance.

Song [971,1201), 230 frames at24fps. Covers the end of shot14 (s012) and
shot15 (receiver_reply_arrival). Accepted performances and receiver camera move
are unchanged. Screen transition after1201 is not part of this delivery.

## Native implementation

The old phase-folding algorithm provides numerical curves at two ordered
subsamples per frame. Cyan is gated to1030..1060; amber to1060..1082. Each keeps
its captured shape after its phrase. Knob acquisition starts1110, screen/bezel
traces1137, small meters1150, and the cabinet/control burst1175.

Native Blender ribbon meshes, separate sprite/hardware/burst view layers,
native Gaussian bloom, masks and additive compositing create the picture.
Only untreated source frames are image inputs. No old FX preview, painted
effect buffer or title-bearing movie is the substrate.

The sprite geometry retains12 frames of trail history, with0.55 decay per
subsample. Two-subsample weights preserve the original accumulated energy.
The much smaller omitted tail is below0.0001% per historical contribution.
Subsample light is averaged before clipping in the native version; the old
renderer clipped each subsample before averaging. This can slightly change
bright cores, along with the different ribbon rasterization and native blur.
It is a controlled migration, not pixel-identical arithmetic.

Receiver tracks and vocal levels are copied from the accepted tracking record,
not retracked or retimed. Numerical centre positions during the singing shot
match the old choreography to floating-point precision.

## Source clocks and cache packaging

Singing span971..1082 uses source72..183 from the same conformed synced take.
Receiver1082..1201 uses source12..131 from receiver_reply_arrival_v1/base.mp4.
The clean native cache has230 frames. A171-frame performance cache simply
joins the preceding60 untreated source frames to the native111-frame tail so
the original s012 in-point can stay unchanged in the review resolver.
That join is media packaging, not an effects compositor. Final native assembly
must retain the source mapping rather than assume this cache is a reusable
source take or that the first60 frames contain new effects.

All masks, geometry and blur scale from the single target-width argument.
Saved scenes contain full keyed animation and can render out of sequence.
The render queue keeps all view layers enabled. An attempted optimization that
disabled initially empty layers left their animation unevaluated, so later
outlines disappeared. Random-access and1080 checks caught this before delivery.
The optimization was removed and affected frames167..230 rerendered. Direct
saved-scene rendering must produce matching pixels; check_message.py enforces it.

## Lessons and continuation

Two complementary cabinet paths initially lay on precisely the same surface,
and one suppressed the other during ray intersection. Small separate depth
offsets corrected this without changing the orthographic projected placement.
The failed test is not a delivery.

Native continuation after1201 should use continuation_state.json and the
geometric trail history in paths.json.gz. Screen-garden applies a later fade to
the sprite/hardware glow, so do not simply splice a freshly restarted oscillator.
Full-film migration and mastering remain unfinished. No paid generation used.
