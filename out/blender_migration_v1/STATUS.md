# Blender migration, full-review assembly

All 70 selected cut dependency records now pass preflight. All 35 native effect
families have 720p renders and 1080p samples; 70 saved scene files were inspected,
with no unexplained image-buffer dependencies. Source-only cuts stay in native
Blender sequencing. This is an isolated review migration, not a production
manifest promotion or a 1080p master.

The full numbered 720p review is COMPLETE: `full_native_context.mp4`.
All 4854 frames at 24 fps decode; master audio alignment, all 70 midpoint
pictures and all 140 first/last cut pictures pass. Full-film contact sheets
were visually inspected. See `full_delivery_check.json` and
`full_cut_edges_check.json`. The initial extra AgX transform at the assembly
boundary was corrected to Standard / None in both the saved assembly and
reproducible builder before this final render. The exceptional previews
are `world_context.mp4`, `orb_context.mp4`, `meaning_context.mp4`,
`scope_context.mp4`, and `outro_native_context.mp4`.

Next: owner review of the full numbered movie, then selected-source upscaling
and native 1080p FX rendering when the edit is settled. No routine migration
approval queue remains. The canonical production manifest has not been promoted.

See `AUTONOMOUS_PASS.md`, `verified_native_shots.json`,
`full_selection_check.json`, `full_resolution_check.json`,
`autonomous_blend_audit.json`, and `resolution_delivery_plan.json`.
The1080stage rerenders native FX before relinking them in Blender; it must NOT
merely upscale the720composite. No paid generation/upscale or mastering occurred.

## Historical progress notes below

The pending-work descriptions below are retained history and superseded by
the status above. Do not restart these completed migrations or ask for routine
per-shot approval. Owner authorized autonomous self-review and completion.

## Latest continuation

Owner explicitly accepted the shop optics proof and authorized self-review of
the world reveal followed by the remaining migrations without approval stops.
Do not ask for another routine shot approval. The two shop hoops were deliberately
absent only from the optical proof; keep them at final integration. Owner asked
not to rerender that proof now.

Current autonomous pass: world26 is rendered at720, eight1080 samples checked,
context at world_context.mp4. Native silhouette/lantern, planet and messages;
procedural nebula detail differs while preserving palette/composition. Self-review
passed. Orb28 also has128native frames and six1080 samples, orb_context.mp4.
Meaning33/34 is rendering223frames after correcting a moving-compositor-domain
issue using a fixed-domain native picture plane. TV55/57 and night69 native
recipes are in progress. These are isolated candidates, NOT full-film completion.
See each family's qa.json and logs rather than assuming a recipe is a delivery.

Workflow changed to technique-first, then autonomous repeated-technique batches.
See TECHNIQUE_FIRST_PLAN.md. Do not resume one-by-one approval requests for
ordinary shots. World cutout and shop snap zoom lead the exceptional queue;
frame exchange, outro projection/TV, reflection/iris and scope dependencies
also need explicit checks. No full-film completion or mastering is implied.

First isolated exceptional-technique proof completed: shop snap-zoom optics,
85 frames plus eight 1080 checks and exact saved-scene random-access repeat.
See SHOP_OPTICS_PROOF.md. Decorative signal intentionally excluded from this
diagnostic proof, so cut 29 is NOT marked fully migrated. World reveal is next.

The owner accepted the native message/receiver look (shots14 tail and15) and
screen-to-garden shot16. See MESSAGE.md, SCREEN.md and owner_approvals.json.
Green-light walk shot18 is rendered and technically checked in walk_context.mp4.
The owner requested continuation without changes. Moth19 was explicitly accepted.
Waking20 is rendered, technically checked and owner accepted in waking_context.mp4.
WAKING.md records exact clocks, source-only inputs, native3D
airflow and remaining texture approximations. Full release remains closed.

## Owner acceptance of first batch

The owner watched `aerial_context.mp4` and `probe_context.mp4` and accepted both native looks. See `owner_approvals.json`. Aerial color-parity refinement is closed: subtle differences detectable mainly through A/B comparison are not a reason to keep adjusting an otherwise successful appearance. Preserve musical timing, effect intent and visual quality; still check for missing elements, broken tracking and resolution-dependent changes. This accepts the migrated looks for cuts4,11and13, not the migration of adjacent footage or the whole film. Candidate receipts remain historical technical records; owner_approvals.json records the later creative acceptance.

## Scope and frozen clocks

Owner correction after batch3: the TUNNEL (not the title) is different and
preferred. Its native look is accepted. See owner_approvals.json; do not keep
tuning the tunnel toward its old raster rendering. This is not full-film sign-off.


The reconciled review register contains70 cuts, frames0..4854 at24fps, with no gaps/overlaps. Music ends4782; closing titles occupy72silent frames. Numbering is whole-film1..70. Prior outro-local1..12 correspond to whole-film59..70. Final review should show only a small top-right number, not the old diagnostic header.

`shots/shotlist.json` remains canonical. `migration_register.json` records the later owner-approved review snapshot plus subsequent outro changes for a proposed merge. It is not a silent overwrite or production promotion. Protected source resolver checks pass. Raw source versus baked effects, wrapper-added effects, and reused crops still need per-shot reconciliation. In particular the opening startup and receiver/rosetta treatments are not necessarily visible in the selected clip filename.

## First native implementation

`aerial_native.py`: converts the aerial garden glimmer from77 externally drawn light images to a native Blender shader scene. Three tracked anchors, exact pulse/envelope data, analytic Gaussian core/spill, and native sequence-editor additive compositing over the original movie. No external FX raster inputs. Saved `.blend` contains the full animation and original movie strip, not one manually swapped still. External preparation extracts reference images and computes audio/track data only.

Existing tracking is retained, including the third anchor fading out when tracking becomes invalid at source59. Effect clock remains song205..282. Reference-coordinate numbers1280/720 express normalized image geometry; no light texture grid is allocated. Rebuild using the single width argument1280or1920 to set every dependent scene and plate scale consistently.

The77-frame720render and four1080samples exist. First implementation exposed an image/movie and output-transform difference. Original movie source and sequence-editor color path are retained rather than introducing an unnoticed regrade. Remaining whole-image difference from the encoded reference is2.41..3.53 levels on an8-bit scale; this is a candidate, not an exact visual-parity certification. Quantitative results alone do not certify the rest of the film.

## Probe implementation

`probe_native.py`: native gold/luminance selection of the original beam, tracked corridor mask, vocal envelope, narrow/core light reinforcement and two Gaussian bloom scales. Shader and compositor nodes do all effects. Extracted original PNGs are untreated footage, not generated effect layers; the compositor sequence animates natively in the saved blend. Movie source is also read for the native mask. Both follow sourceframe1..192, with songorigin719. Source0..86 and137..192 cover s009 and s011 respectively; the intervening receiver cut is not replaced.

All192720reference frames were checked. The largest per-frame mean difference is0.2171 on an8-bit scale from the old uncompressed effect; maximum per-frame99th-percentile difference is2levels. Seven corresponding1080renders, reduced to720for diagnosis, differ by0.89..1.21levels including original-plate resampling. These numbers are not zero-error equivalence claims. Full motion render and clean encoding are tracked in `native_candidates.json`. Both77-frame aerial and192-frame probe candidates were decoded and frame-count checked. No production promotion performed.

## Coverage and release gates

`coverage.json` checks all70 selected references:24fps, sufficient source coverage, valid in/out frames. All70 pass. This confirms temporal coverage, not native FX completeness. `preflight.py` deliberately refuses a full-native release until every selected shot has an explicit verified dependency record. No such global sign-off has been made. Existing native scope/lyrics/particles also require dependency checks, not blind exemptions.

Rendering size is currently selected once through each recipe's width argument, which sets all dependent scenes and resolution-derived blur sizes. Merely changing a parent scene's output size without rebuilding child-scene controls is not the supported contract. Final orchestration must pass the same target size everywhere and verify it before assembly.

Color transforms are part of each accepted look: the aerial's existing sequence-editor path usesAgX; probe's linear-light effect outputsStandard. Do not apply an extra globalAgX transform blindly to already transformed deliveries. Resolve and test this at the final native assembly boundary before mastering.

## Remaining batches

### Message entrance and receiver interaction ready for review

message_context.mp4 covers song971..1201,230frames, the end of shot14 and
shot15. New native sprite geometry, phase-gated voices, persistence, tracked
dial lighting, knob acquisition, hardware outlines and NOW burst. Source
performances and camera move retained. MESSAGE.md holds checks and limitations.
Seven1080 checks and two saved-scene dependency audits pass; random-access
frames70/211 match corrected sequence pixels exactly. Source receiver hash
verified. All clean/review movie frame counts and decodes pass.

An empty-layer render optimization failed: later objects remained unevaluated.
Saved-scene/1080 checks caught the missing outlines before owner delivery.
Removed optimization, rerendered affected167..230, rebuilt caches and preview,
then reran verification. Do not disable view layers using unevaluated object
visibility as an optimization. All layers now remain enabled by default.

Screen-to-garden after1201 remains next. Oscillator state and geometric trail
history are saved for that continuation. Message look approval and production
promotion remain pending. No full-film or mastering-ready claim.

### Bends Your Mind follow-up complete for review

Native shots45/46 now cover all137 frames at song3505..3642, with optical
distortion, chromatic split, geometry loops, motes, trails and bloom. Untreated
performance plates and original frame clocks preserved. Six1080 samples and
both saved blend dependency checks pass. Direct saved-scene frame100 reproduces
the sequential pixels exactly. Numbered272-frame context: bends_context.mp4.
See BENDS.md and bends/receipts.json. Owner approval is now recorded; the owner
prefers the native look. Production promotion remains pending. This removes
psychedelic warp from the unimplemented list, not
from the list awaiting final integration. No full-film completion claim.

Next: the stateful message-sprite/receiver/screen family. NEXT_ROSETTA.md traces
the hidden preview-only replacement and numerical state continuity between cuts.

### Batch3 complete as an isolated review package

Twelve native deliveries, 798 clean frames total, plus 41 representative1080
frames. Eight numbered contextual previews are available in REVIEW_BATCH3.md.
All deliveries and previews passed decoding and exact24fps frame-count checks.
All24 saved Blender scenes passed dependency/output-size checks. Their image
inputs are untreated plates, not raster FX layers. Source-preservation checks
kept performances, cut points, source offsets and music controls unchanged.

Completed families: opening CRT acquisition (shot1); native crop inserts (8,32);
walking guide (21); bird/lantern response (22); pollen bloom/conductor (23);
rocket pressure lens (37); swimmers (43,44,47); tunnel contours (54); corrected
closing card (70). The currently visible overhead cut uses source54..116 of
the116-frame native cache; its song interval remains3376..3438.

Visual review covered representative frames, high-resolution samples and
eight contextual contact sequences. Quantitative comparison covered581 frames
where uncompressed references exist. Most families stay below0.58 maximum
per-frame mean difference on an8-bit scale. Tunnel differs more (up to6.67),
with cleaner ribbon edges and different bloom coverage; its geometry, controls
and arrivals are retained and it is explicitly flagged for owner look review.
No claim of pixel identity or full-film completion is made.

The first insert test sampled incorrectly because sequence image dimensions
were not reliable before evaluation. It was corrected to use probed source
dimensions, then rerendered and visually checked before delivery. No bad test
was encoded into the preview. See NATIVE_CONTRACT.md for the reusable lesson.

Remaining work is still material: scope pixel-buffer dependencies, rosette and
message/world exchanges, screen-to-garden, moth/waking, planet/nebula, shop,
psychedelic warp and the layered outro. remaining_dependencies.json provides
static navigation hints, not proof of completeness. Source-only cuts still
need their final integration records. preflight.py now validates record status,
timing, hashes, resolution review and explicit absence of baked FX dependencies,
instead of accepting any existing key. It correctly still refuses full release.

Production manifests and accepted source media remain untouched. No paid
generation/upscaling, mastering, commit or push was performed. These scenes
are technically checked candidates for owner review, not global promotion.

### Batch2 rendered, contextual review pending

Receiver cut12 and held-specimen cut25 now have native Blender recipes and complete silent renders. All51receiver and106specimen frames checked against their old uncompressed effects: largest per-frame average differences0.192and0.178 respectively on an8-bit scale. Three receiver and four specimen1080samples were also rendered. Exact frame counts and decoding pass. See `LIGHTS2.md` and `lights2_receipts.json`. These are not yet owner-approved or globally promoted. Contextual previews preserve native probe approvals around the receiver and the accepted listening/lip-sync source at the artifact.

Shared procedural math helpers now support source-color masks, tracked planar coordinates, animated controls, native blur and light composites. Manual Blender rerender output paths are explicitly inside each family's out/ folder. Prior accepted files remain untouched.

1. Aerial and probe looks accepted. Extend native lighting to receiver, specimen, garden, birds and swimmers using their own masks/tracks, not a generic replacement effect. Keep the final integration contract explicit.
2. Opening phosphor acquisition, probe signals, receiver/meaning/world rosettas, tunnel contour pulses. Preserve geometry, audio clocks, persistence and trajectories.
3. Garden fluid/motes, ghost wings, waking eyes, guide actor, world reveal/nebula, shop transition and psychedelic warps. Explicitly account for optical masks and supersampling.
4. Outro TV maps, room projections, artifact response, native-particle dependencies, green actor/water reflection and iris. Keep accepted particle continuity and face-cut timing.
5. Native title recipe uses the corrected short copy and Arne Gleason credit. Assemble with native lyrics once, no global flash, master audio once, small review numbers. Resolve all pending entries before declaring completion.
6. Compare representative motion at720and1080, then full-film review. No mastering baked into intermediate elements. Keep approved originals as look references.

Each batch must record raw plate, frame mapping, active native recipe, reference movie, resolution test, visual review and remaining limitations. A scene that plays baked FX is explicitly not marked migrated.
