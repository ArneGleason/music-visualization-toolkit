# Kling generation order — October 10 recommendation

The user approved all five chorus stills, then authorized proceeding in this
order. The earlier coast cut at frame 1046 is confirmed. The prepared sequence
is `kling-chorus1-motion-v01.json`, followed by the revised
`kling-window-coast-v01.json`; submissions and results are saved by take ID.
Do not repeat a submission with an existing `request.json`; collect its task.
The eight planned takes were estimated at 432 credits using the last observed
eight-credit/second rate. Actual charges are recorded on submission.

Generate by continuity dependency, then assemble by song time. Start with
the fresh chorus's highest-risk action and review it before generating the
dependent response. The stills remain the visual authority; reject motion
that loses their character, ecology or illustrated finish.

1. **48.71s / chorus1-02:** water-channel intervention. First motion test:
   a small deliberate hand action, readable water response, living fauna.
   Use the approved still plus the existing gray-outfit Harper Element.
2. **51.12s / chorus1-03:** creatures repurpose the intervention. Capture a
   clean accepted state from the first take, and use it to reconcile this
   shot's starting reference. The approved response still sets composition
   and intended result; avoid resetting the water or creature layout.
3. **43.54s / chorus1-01:** mission projections. Match the turquoise globe
   to the accepted living coast; the other two worlds retain their approved
   ochre and indigo motifs. Keep one deliberate selection action and quiet
   ecological motion; no automatic multi-shot edit.
4. **53.79s / chorus1-04:** orbital expansion. Carry the coast's branching
   motif into sparse orbital light arcs. Use the approved cosmic still for
   appearance rather than inheriting a literal-scale shoreline mistake.
5. **58.79s / chorus1-05:** echoes between worlds. Use accepted orbital
   motion/frame cues to preserve path color, pulse behavior and direction.
6. **37.96s / space-011:** earlier arms/tide coast. Backfill using the same
   approved coast vocabulary and accepted motion references where useful.
   Its new edit span is 912–1045, 134 frames, because chorus1-01 now begins
   at 1046. Revise the prepared 12-second plan before submission; do not
   generate the old coast hold through frame 1169.
7. **32.83s portrait and 30.67s inlet:** fill the remaining preceding still
   placeholders. These have fewer direct motion dependencies; retain the
   approved portrait and world palette.

The first two takes form a review gate: if literal creature engineering is
unconvincing, simplify the response to creatures redirecting/occupying an
existing branching flow before committing to the remaining family.

Observed first tests: water-channel v01 produced a usable gesture/flow response
(40 credits). Creature-response v01 (40 credits), using a captured predecessor
frame and the differently composed approved response still as tail, inserted
an internal cut near source frame 39. Do not use it as continuity authority.
Response v02 uses the approved response still alone, a locked camera, existing
water gaps and simpler creature/pebble interaction (40 credits). This one retry
raises the run estimate to 472 credits. Retain the first attempt for comparison.
Lesson: different camera/geography start and tail frames can invite a cut even
when multi-shot is disabled; use a reconciled next starting still for coverage.

Mission v01 (64 credits) produced expressive motion but switched attention to
the blue reef world and added background globe/ring graphics. Mission v02
(64 credits) restricts the action to the turquoise globe and the three original
projections. Both attempts are retained. With this second correction, the
interim generation run totaled 536 credits across ten takes (eight planned
shots and two comparison attempts). Independent renders overlap only after
the causal shore pair has been reviewed; submission follows the proposed order.

The initial inlet and arms/tide coast generations introduced unwanted ship
and celestial subjects despite ship-free starting images. Each was corrected
once using scene-only motion language, with the unchanged canonical identity
block retained in metadata rather than adding off-screen subjects to the
active generation prompt. Inlet v02 and coast v02 retain the intended scene.
The completed run totals **640 credits across 12 tasks**, with eight working
motion choices and four rejected comparisons. All tasks are collected.
The eight working choices are review drafts in full animatic v20, not
user-approved motion. Prompt/Element/task/source-frame receipts and all
comparisons are retained under `generated/kling-tests/` and in the shotlist.
The overall recorded Kling spend is 1,576 credits including the earlier 936.

## Continuity capture

For every accepted take retain the original clean file, generation ID,
model/settings, prompt/lock, Element bindings, source/edit frame mapping and
review rationale. Extract sharp representative frames of character, ecology,
water state and a usable boundary pose; record their exact source frames.
Only accepted frames become reusable references. Keep the original approved
still alongside them so successive generations do not compound drift.

Use the exact boundary frame as the next start only when continuing the same
camera/shot. For a new angle, adapt the approved next still against the accepted
state instead of forcing an awkward last-frame composition. Optional tail
frames are useful when the result must arrive at a particular state; check
that the start and end describe physically compatible motion.

The repository's current image-to-video runner passes starting images,
optional tail images and Element bindings. Official Kling 3.0 documentation
also describes video-derived Elements, but that creation route is not wired
into this runner. Do not assume video upload is available through the current
plan format or that repeated requests remember previous generations.

## Edit and timing

Reserve one second / 24 frames at each end for new chorus footage. Handles are
extra source material, not an instruction to freeze at the head/tail and not
a one-second transition requirement. Natural action must continue through
them. Frame lengths come from the existing timing grid. Keep master audio,
small word-timed lyrics and original spelling.

Generate clean single-shot action without baked lyrics, music or inter-scene
zoom blurs. Try the jump cut, zoom-out blur or dissolve in the animatic edit,
using the handles. This preserves timing control and lets transitions change
without buying new footage. Review the assembled run before further batches.

Official references checked October 10:
- https://kling.ai/quickstart/klingai-video-3-model-user-guide
- https://kling.ai/quickstart/klingai-element-library-3-user-guide
