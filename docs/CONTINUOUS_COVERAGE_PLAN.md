# Continuous coverage and whole-film refinement

Owner direction recorded 2026-09-05. The production strategy below is adopted;
the exact outro cut proposal is for review in a free animatic before generation.
The current approved picture remains v04. DAW visualization experiments follow
this coverage discussion.

## Production unit: a continuous take

Generate enough continuous performance to cover an exchange, including the
time when that performer is off screen. Cut between independently running
views. On returning to a view, advance to the source moment corresponding to
the song's current time. The actor should have continued breathing, listening,
and moving while the audience was looking elsewhere.

A setup defines the recurring composition. A take is continuous source footage.
An editorial cut selects a portion of a take. Several cuts can use the same
take at different in-points; several takes can cover one setup over a long
scene. These are different units and should have separate records.

For example, when A returns at song frame 4262, take A1 starts at its local
frame 97, not at its beginning. The gap while B spoke has elapsed in both
performances. Source clips need not run simultaneously during export; their
time mappings preserve the same result.

The owner's ten-second example captures the approach. The recent local motion
tests used eight-second clips, so the concrete plan below uses that known
working length. Confirm the generator's actual duration choices before placing
an order. The existing eight-second maximum *editorial shot* rule does not
limit source-take duration, and a longer source should not lengthen the edit.

## Why the outro needs a different cut

The current s054–s057 pictures are two-bar blocks: astronomer, astronaut,
telescope tunnel, astronomer. They cover many shorter alternating replies.
Consequently “Define there” appears over the astronomer, most of “Never mind /
La-la-la, low light” appears over the astronaut, and the tunnel covers several
exchanges. The recorded speakers and picture choices have become disconnected.

Use the dialogue's actual speaker changes to drive this passage. Hold the same
view over adjacent phrases from the same speaker. Occasional listening
reactions remain welcome; they should be deliberate choices. The tunnel can
introduce the conversation, and the colony/iris can receive the final goodbye.

A = Them 1, the astronomer beside the period-futurist television:
`duet_lamplight_astronomer_sync`.

B = Them 2, the astronaut in the dark bunk interior:
`duet_lamplight_astronaut_sync`.

## Proposed outro edit

All ranges are zero-based 24 fps frames, with the end frame excluded.
Milliseconds are for reading only. Cue positions come from
`shots/lyric_motion_full.json`; the lead-in and closing insert boundaries come
from the current shot list. This is a proposal, not a second active edit source.
On acceptance, promote it into `shots/plan.json` and `shots/shotlist.json`
through the merge workflow, and regenerate downstream cues.

| Song frames | Cut time | View | Phrase / purpose | Take @ source frame |
|---|---|---|---|---|
| 4120–4177 | 2:51.667 | Tunnel | Lead-in; finish the previous answer and approach the exchange | Insert |
| 4177–4232 | 2:54.042 | A | You still there? | A1 @ 12 |
| 4232–4262 | 2:56.333 | B | Define there. | B1 @ 67 |
| 4262–4331 | 2:57.583 | A | Never mind. / La-la-la, low light. | A1 @ 97 |
| 4331–4362 | 3:00.458 | B | No, go on. | B2 @ 11 |
| 4362–4400 | 3:01.750 | A | Thought I heard something. | A2 @ 42 |
| 4400–4431 | 3:03.333 | B | You did. | B2 @ 80 |
| 4431–4461 | 3:04.625 | A | Was it you? | A2 @ 111 |
| 4461–4504 | 3:05.875 | B | Da-da-dum. / Could've been. | B2 @ 141 |
| 4504–4557 | 3:07.667 | A | Say goodnight. / hold for the unassigned Who? | A3 @ 4 |
| 4557–4574 | 3:09.875 | B | To who? | B3 @ 57 |
| 4574–4622 | 3:10.583 | A | La-la-la—la-la | A3 @ 74 |
| 4622–4644 | 3:12.583 | B | You first. | B3 @ 122 |
| 4644–4671 | 3:13.500 | A | Night. | A3 @ 144 |
| 4671–4689 | 3:14.625 | B | Night. | B3 @ 171 |
| 4689–4747 | 3:15.375 | Colony | Lights settle; final unassigned Night stays off screen | Insert |
| 4747–4782 | 3:17.792 | Iris | Final aperture / end of the actual master | Insert |

This gives fourteen performance views, with thirteen A/B switches during the
exchange. Same-speaker phrases remain together. The two shortest replies are
deliberately quick; if the free animatic feels too busy, hold a listening view
through one of them instead of generating another angle. Start with hard
picture cuts and continuous master audio. Preserve the approved lyric
choreography and its intentional vocal overlaps.

Speaker metadata is missing for “Who?” at frame 4530 and the final “Night” at
4742. The proposal holds A through the first as a possible listening reaction
and keeps the last voice over the colony. These picture choices do not assign
the voices. Confirm attribution by ear before preparing sync audio.
“You first” and the following “Night” overlap slightly in the lyric data;
switching picture at 4644 must not truncate either audible phrase.

The actual movie ends at frame 4782. The planning row for the final iris extends
beyond the master, so source orders and reviews must use the actual movie end.

## Six source takes, not fourteen separate generations

Each row represents two independent takes, one for A and one for B.

| Pair | Song-frame coverage | Song-time coverage | Length per take | Next reference frame |
|---|---|---|---|---|
| A1 / B1 | 4165–4357 | 2:53.542–3:01.542 | 192 frames / 8 s | Pair 2 starts from local frame 155 of pair 1 |
| A2 / B2 | 4320–4512 | 3:00.000–3:08.000 | 192 frames / 8 s | Pair 3 starts from local frame 180 of pair 2 |
| A3 / B3 | 4500–4692 | 3:07.500–3:15.500 | 192 frames / 8 s | End of coverage |

The first overlap is 37 frames; the second is 12. A1 stays on screen through
4330 while B2 enters at 4331. A2 first becomes visible at 4362. Similarly A3
enters at 4504 while B3 need not appear until 4557. Every source-take change
therefore occurs while that view is off screen, not midway through a visible
gesture or syllable.

This is six motion generations and up to six full-take sync jobs, producing
48 seconds of source coverage for a 21.33-second dialogue. It is an editorial
flexibility choice, not a promise of lower cost than short clips. Start with
one candidate per take. Insert footage can use an adequate existing test or
the approved still in the rough pass.

Handles vary: A3 has only four frames before its first selected moment, and
B3 has three frames after its final selected moment. Those are enough for
this exact proposal, not generous retiming room. If the review changes those
edges materially, revise the source windows or use an available longer
duration before generation; never stretch a synced mouth to manufacture room.

The same initial board image should not be used to restart all three takes.
For each sister, use the approved image for her first take; for a continuation,
prefer the preceding base-motion take's frame at the next window's exact song
position, plus the same identity/style references when the tool supports them.
At the planned overlaps those are frames 155 and 180, not automatically the
last frame. Check for accumulated identity or wardrobe drift before carrying
an anchor forward. A fresh reference-anchored take hidden under the reverse
shot is an acceptable alternative when continuation drifts.

Longer generation cannot guarantee continuity. It reduces repeated beginnings;
the overlap, reference choice, take review, and hidden join finish the job.

## Performance prompts for coverage

Compose a coverage prompt from the approved setup and cast descriptions,
reference image, the take's local behavior, and the exact existing lock block
from `shots/style.md`. Copy that lock verbatim. The prose below is a direction
layer, not a complete ready-to-submit prompt and not a replacement for the
lock.

For A: a continuous quiet end-of-day performance beside the television, its
warm screen light already settled. She listens with tired fondness, breathes,
makes an occasional small eye or shoulder response, and returns to the shared
eyeline. Maintain the established hair, clothes, hand position, light, and
framing. Let the take remain usable at any point, including between lines.

For B: a continuous quiet listening performance in the dim bunk, with cool
night outside and small warm practical lights inside. A subtle, dryly amused
reply, a breath, and a settling posture belong to one ongoing exchange. Keep
the face available for sync and the body comfortably alive.

Across both views: choose a stable framing and eyeline; keep hands and props
away from the mouth; use restrained, relaxed mouth activity in the base take.
The audio pass supplies the actual phrases. A television switch, setting down
an object, or a final settling gesture should happen once at an assigned
moment, not once at the start of every generation. Later takes continue from
the resulting state. Do not ask the image-to-video model to perform the edit
or reliably hit exact lyric times.

The approved still may depict a moment within an action. If it is an awkward
literal start frame, create a calmer coverage anchor using the same approved
identity, wardrobe, set, and lighting, then review that anchor before animation.
A beautiful storyboard composition does not require replaying its entrance
action on every return.

## Lip-sync and source timing

1. Give every source take a song start frame, length, setup, performer, version,
   base-motion file, and eventual synced file.
2. Prepare a vocal guide for the entire take window. For A, include A's lines
   at their original positions and leave B's turns as silence. Prepare B's
   guide the other way around. Do not concatenate a speaker's phrases.
3. The project uses the same recorded singer for both roles. The lead-vocal
   stem is not automatically a separate A or B stem. Use verified speaker
   metadata and listen to the guides. If voices overlap in one stem, gating
   cannot separate simultaneous voices: resolve from available separated
   material, a reviewed edit, or a listening/insert shot.
4. Keep every gap and any leading silence. Use short fades outside phonemes
   to avoid clicks, without shaving consonants or changing line onsets.
5. Sync a usable full take once, then select its visible pieces. Inspect the
   silent/listening intervals too: silence in the guide does not by itself
   guarantee that the generated mouth will stay still.
6. Use source time at normal playback speed. For normalized 24 fps media:
   `source_in_frame = cut_start_frame - take_song_start_frame`.
   Select exactly the cut's frame count and check source bounds.
7. After sync, measure the returned duration, frame rate, and audio/video
   offset. If a service trims lead silence or changes timing, record the
   measured mapping explicitly; do not assume its frame zero still matches
   the input's frame zero.
8. Assemble under the untouched continuous song master. Moving a cut within
   available coverage changes the selected view and in-point, not the
   song time or lip-sync timing. Keep `clip.speed = 1` for synced footage.

Known implementation limits: `tools/prompts.py` currently orders duration by
the longest individual cut, so it does not yet produce these coverage orders.
`tools/ingest.py --auto` attaches a common zero in-point to all matching setup
uses; it must not be used blindly on these takes. The Blender path already
reads each cut's `clip.in_sec`, but the planning-to-assignment step must supply
the correct individual values and preserve them through re-planning.
Check the live shot list and persistent overrides together before a merge;
historical in-points may no longer match a newly synced source.

## Other sections that benefit

| Section / current shots | Useful coverage | What it teaches |
|---|---|---|
| Opening, s003–s008, about 0:06–0:29 | One ongoing astronomer performance per composition, with map/console inserts over its elapsed time; use a few overlapping blocks for the long span | Continuing thought and hand/prop state through inserts |
| Receiver reply, s012–s014, about 0:38–0:52 | Astronaut coverage continues beneath the night-wide insert | Natural return after a long cutaway, with sync still on the same song clock |
| Pattern inspection, s023–s025, about 1:15–1:32 | One specimen-handling action with an inspection angle covering the same window | Object positions and task progression, not repeated pickup gestures |
| Call and response, s032–s034, about 1:49–2:00 | Independent sister views spanning the exchange; derive suitable single-person compositions from approved references if needed | Reliable speaker ownership without having a sync service choose between two faces |
| Rocket landing, s036–s039, 2:02–2:11.875 | One continuous landing action for the full 237-frame span | The existing short EDL rows do not mean the landing should restart; eight seconds alone is too short here |
| Garden returns, s017–s020, about 0:58–1:09 | A progressing walk continuing behind the fauna inserts | Advancing position in the forest and hiding a continuation join under an insert |
| Chorus returns, s043/s047 and s045–s046 | Keep the adjacent hero close-ups continuous; treat the two overhead returns as later states of the choreography | Flowing formations without replaying the opening move; an overhead take spanning both returns needs about 14.17 seconds |
| Current/underwater returns, s049–s053, about 2:37–2:52 | Continued travel with inserts covering a new source block | Stable travel direction and water motion across views |

Use continuous source time where the scene represents one ongoing event.
A much later return in a different narrative context can be a new take with
the same visual identity; it need not simulate all elapsed song time.
The existing chorus tests already establish useful motion and sync behavior.
They count as first-pass material, and can remain until a later pass provides
a clear improvement.

## Whole-film passes: learn, advance, return

The owner's rule: rough out the whole timeline strategically, learn from each
new section, and apply the lesson forward. Revisit earlier sections when a
later experiment gives a concrete reason to improve them. Existing animations
and sync tests are replaceable, but keep their files as comparisons.

| Pass | Work across the film | Finish condition |
|---|---|---|
| 1. Coverage and edit | Review this outro proposal with approved stills; map continuous takes, cutaways, speaker ownership, and required source length across the song | Every section has a practical coverage plan; changed edit passages have a free animatic review |
| 2. First motion assembly | Use one candidate per planned take and useful existing tests; move through the remaining sections, recording issues as encountered | The whole timeline plays using rough motion, with explicit still fallbacks where needed |
| 3. Sync and continuity | Sync usable performance takes and check returns, listening gaps, source offsets, and crosscuts throughout the film | The whole song has a reviewed performance pass and a ranked issue list |
| 4. Targeted refinement | Apply lessons learned later to weak earlier sections; replace only the affected takes | Remaining issues are acceptable in a full-context review |
| 5. Effects and finishing | Review the DAW effects plan, test a small passage, then extend the successful treatment; grade and final sound/picture checks | One coherent full-film review |

These are broad passes, not a rigid prohibition on earlier experiments. A
small sync test in a newly encountered situation is useful while making the
first motion assembly. Return to the coverage queue once it answers the
question.

For each section, record: current take, what it taught us, visible problem,
severity, and the hypothesis to try next. Allow one initial attempt and at
most one targeted correction for a clear failure during a first pass. If it
still fails, use the best available take or a still/insert and move on.
A file/download failure is a technical retry; repeated creative variants need
a reason. Do not spend successive rounds polishing one passage merely
because it is familiar.

Review small batches with neighboring shots and music, then periodically watch
the whole film. Judge progress by timeline coverage and coherence, not by
the number of variants accumulated for a favorite shot.

## Next work

1. Review the proposed outro timing in a stills-only excerpt, using the source
   windows here as a planning overlay or accompanying notes.
2. Promote accepted cuts, define the coverage manifest and speaker guides,
   and make the generation work orders reflect take duration.
3. Use the outro as the next new type of section after the chorus tests, then
   proceed to opening/receiver coverage, action/insert continuity, and the
   remaining timeline. Carry a short findings log forward.
4. Review and test the DAW overlay plan after the coverage discussion.
