# Version-two investigation and review translation

Investigation only, 2026-09-05. No edit, source assignment, guide, prompt, media,
or production configuration changed. No generation or replacement render.
Review reference: `rough_v04_numbered_720p.mp4`, 71 cuts. The owner's pasted
feedback is the creative brief; spelling and approximate lyric quotations are
interpreted by meaning, not treated as changes to the actual lyrics.

## Verdict

The assessment is supported by evidence. This is not simply a taste difference,
nor one global shift that requires moving the whole soundtrack. There are at
least four separate problems:

1. A consistent missing stem-to-song offset in lip-sync guides, including the
   newer outro. The earlier 30-to-24 playback correction did not fix this.
2. A stale source in-point on cut 43 after a new lip-sync guide replaced the old
   one. This creates an error of about three seconds, not a subtle onset issue.
3. A beat/bar-first edit whose picture intervals often do not contain the
   intended lyrical thought. Better lip sync alone will not fix that structure.
4. Repeated source intervals and posed performance direction. Timing alone
   cannot repair an unsuitable expression, wrong action, clone, or source restart.

Recommendation: do a phrase-led version-two edit and a small verified sync test
before spending on widespread replacements. Preserve good material. Some requested
acting/still changes genuinely warrant new generation, but do not regenerate all
clips merely to conceal pipeline errors.

## Timing evidence

### The master has not drifted

Decoded review audio at 5, 70, 140 and 180 seconds matches the same positions
in `audio/song.wav`. Band-limited waveform correlations: 0.99987, 0.99964,
0.99948 and 0.99984 respectively. No measurable accumulated soundtrack drift
at the 0.5 ms analysis resolution. This checks audio placement, not mouth motion.

The v04 frame-rate fix was independently verified against actual source images
in the earlier audit: real-time source progression is restored. It was a real
defect, but the previous investigation stopped too early to explain all the
remaining symptoms. In particular, coverage and correct playback speed do not
establish that a clip was given the right song-time guide.

The container's video stream starts about 0.041 seconds after its audio stream.
That deserves explicit timestamp normalization in a later controlled export test,
but is too small to explain multi-second discrepancies or the phrase edit.
It also means final visible lead/lag is not exactly the nominal guide offset.

### Lip-sync guides used the stem clock as though it were the song clock

`projects/rivers-of-mars/generated/waveforms.json` records the lead-vocal stem
at song offset **+0.178348 seconds**. For example, stem sample-time 6.4758 is
heard near song-time 6.6541, not 6.4758.

The guide files were correlated against both the restored vocal and the actual
master. All eight tested early guides match the stem at the nominal cut start
and the master about 0.178 seconds later:

| Shot / review cut | Nominal guide origin | Measured matching master origin |
| --- | ---: | ---: |
| s003 / 3 | 6.4758 | 6.6540 |
| s005 / 5 | 17.9243 | 18.1025 |
| s007 / 7 | 23.6664 | 23.8450 |
| s012 / 12 | 37.9796 | 38.1580 |
| s014 / 14 | 49.3328 | 49.5110 |
| s026 / 26 | 91.9656 | 92.1440 |
| s031 / 31 | 106.1423 | 106.3205 |
| s033 / 33-34 | 111.8191 | 111.9975 |

The downloaded clips' embedded audio matches their corresponding uploaded guide
at zero lag, correlation 0.9999 or better. This strongly supports correct file
identity and audio transfer. It does NOT prove Kling correctly animated every
phoneme. The error exists before evaluating the generated mouths.

The same pattern appears in the chorus and all six newer outro takes:
chorus guide 146.0556 -> master 146.2340;
A1/B1 173.5417 -> 173.7200;
A2/B2 180.0000 -> 180.1785;
A3/B3 187.5000 -> 187.6785.
Speaker-gated outro correlations are lower, as expected from silenced portions,
but agree on the same lag. The scope/contour tools, by contrast, explicitly read
and subtract their stem offsets when sampling the music.

If a face followed its guide perfectly, this mapping would tend to show a future
phoneme too early in the edit, before accounting for model error, rounding and
container timing. It is not evidence that all faces should receive an arbitrary
global delay. Guides starting inside a word may have omitted material that cannot
be recovered by shifting their result.

### Cut 43 contains a stale 2.84-second trim

The current `basin_edge_sync_kling.mp4` embedded audio matches the restored vocal
at **137.578 seconds**, correlation 0.9997. It matches the newer
`basin_edge_vocal8_retimed.wav`, not the older guide beginning at 134.7357.
Its corresponding master origin is about **137.7565**.

The cut s042 still starts at song 137.578 with `in_sec: 2.84`. Thus the mouth
content selected at entry corresponds to song about 140.5965, roughly 3.02
seconds ahead. The old trim was reasonable for the old guide, but not the new
file. Merely resetting to zero would fix the large stale trim while leaving
the smaller stem-clock error and possible first-word truncation.

This is direct evidence for the owner's suspicion that a good earlier preview
could become a bad assembly. Source identity, guide origin and source in-point
must be versioned together; a familiar filename is not sufficient.

## Why the picture cuts feel wrong even where text is good

`tools/shotplan.py` defaults to snapping sections back to bars and cutting on a
bar/beat grid. `shots/plan.json` cycles setup lists over those cuts. Lyrics are
then attached by onset; this does not make the picture contain a whole phrase.
Only a few explicit boundaries and the recent outro depart from that pattern.
The lyric animation has its own finer phrase/word timings, explaining why it can
feel more accurate than the picture edit. Use it as a working reference, then
verify against the actual vocal, not as unquestionable forced alignment.

| Cut | Evidence from existing lyric timings | Consequence |
| --- | --- | --- |
| 3 | Picture [155,293); first thought [156,284), next phrase ends 332 | Almost no entry context; cut away during the following thought |
| 8 | Picture ends 706; “don't quite match” ends 719 | Cuts away about 0.54 s before phrase ends |
| 9 | Picture [706,774); “Can I send…” [719,805) | Enters 0.54 s early and leaves 1.29 s early |
| 10 | Picture [774,843); “Tell me…” [826,852) | Enters 2.17 s early and leaves 0.38 s early |
| 13 | Picture [1047,1184); desired group [1030,1201) | Misses about 0.71 s at both ends |
| 16 | Picture [1321,1391); phrase [1304,1412) | Starts late and ends before the phrase completes |
| 19 | Picture starts 1527; “through…” starts 1514 | Enters about 0.54 s late |
| 22 | Picture [1731,1799); desired group [1710,1841) | Starts 0.88 s late and leaves 1.75 s early |
| 26 | Picture starts 2207; desired group starts 2122 | Misses roughly 3.54 s of the requested thought |
| 31 | Picture starts 2547; “Especially stupid” starts 2573 | Enters about 1.08 s before the intended punchline |

All frame intervals above are at 24 fps, end-exclusive. These differing signs
and magnitudes rule out one edit-wide offset as the explanation. They need an
editorial re-plan. “Enclose the phrase” should mean entry, delivery, and reaction
with purposeful exceptions, not a mechanical cut at every lyric onset.

Moving a music-reactive shot requires re-sampling its actual song-time drivers.
Do not slide the existing baked scope, receiver, garden, pressure or tunnel
effect along the timeline and assume it remains synchronized.

## Source continuity and acting

- Map: cut 4 consumes source 0 to about 5.72 s. Cut 6 returns to source 2.5 s.
  Cut 8 returns to 5.1 s. These are different in-points but overlapping action,
  not a long progressing scene. The owner's repetition impression is supported.
- Specimen table: cut 23 consumes about source 0..5.67; cut 25 begins at 2.3.
  That replays several seconds of the same activity.
- Rockets: cut 40 explicitly returns to source zero after cuts 37-39 progress
  through the landing take. This is an actual restart, not just a similar angle.
- Split duet: notes confirm one full mixed-speaker guide was supplied to Character
  1. Timing correction cannot make both characters own the right lines.
- Performance brief for version two: cool, groovy, assertive, intentional and
  conversational. Small rhythmic weight shifts, knowing looks, precise gestures,
  and changes of thought. No persistent promotional smile or default lens gaze.
  Direct each phrase as an action: challenge, request, tease, dismiss, inspect,
  listen, reconsider. Preserve room for stillness and contrasts, not constant mugging.
- “Especially stupid”: dry, pointed emphasis; “No”: a clean interruption;
  “bends your mind”: a purposeful extreme close-up and larger expression;
  outro: speaker-call eyelines, listening and uncertainty rather than posing.

## Proposed version-two workflow

1. Freeze v04 and its numbered lookup as the review reference. Normalize the notes
   to stable shot IDs, including the ambiguities below. Do not re-number the notes
   opportunistically while changing the edit.
2. Make a phrase-led paper edit over the unchanged master. Specify speaker,
   phrase group, first/last word, picture entry, exit/reaction, dramatic action,
   and intended insert. Verify lyric landmarks by listening. Use beats for motion,
   punctuation and selected cuts, not as the sole boundary rule.
3. Audit every retained performance asset's guide origin against the master.
   Correct metadata/in-points where possible. Preserve originals and document
   missing head coverage. Never fabricate a negative source in-point.
4. Run three diagnostic auditions before broad generation: cut 3 for guide-clock
   and first-word behavior; cut 43 for stale trim; an outro exchange for correct
   clock plus expressive listening. Compare against the master, not merely the
   uploaded guide. No further automatic offset based only on mouth-energy peaks.
5. Plan longer source takes across returns. Use continuous forward-progressing
   sections or state-matched continuations; don't reset at every cut. If using an
   old still as an end target, explicitly direct the action leading into it.
6. Build the split-screen, if still wanted, from separately generated and synced
   single-person takes. Composite two panels afterward. Alternatively use
   alternating singles/reaction inserts, which is likely clearer and more flexible.
7. Generate selectively for missing coverage, revised acting, unsuitable stills,
   clones, incorrect digging, and rocket smoke. Keep approved visual treatments and
   usable clips; no blanket regeneration decision yet.
8. Review a phrase-timed low-cost animatic before paid replacement work, then
   assemble a full broad pass. Reapply/retrack local FX to changed plates. Refine
   across the film, not repeatedly on one tiny section.

### Half-second pre-roll: useful default, not a substitute for a correct clock

Use **12 frames / 0.5 s of real context before the earliest visible entrance of
each generated performance take**, not an extra half-second added to every
return cut within an existing take. Include actual preceding audio and visual
performance, not silence or a held portrait. Prefer longer context when a phrase
is already in progress. Add an explicit exit handle where possible.

Keep three clocks explicit. If E is the picture cut's song time, H is its intended
pre-roll, T = E-H is take origin, and O = 0.178348 s is the stem placement:

- extract the stem guide from **T-O**;
- align guide time zero and synced picture time zero to **song time T**;
- use source in-point **E-T** for the cut;
- for a later return at E2, use **E2-T**, not a restarted 0.5 seconds.

Record master version/hash, stem placement, guide range, take origin, source fps,
time-preserving proxy, verified sync adjustment, available head/tail coverage and
cut in/out frames. Bake no hidden padding or unrecorded audio offset into delivery.

Some new outro takes already had roughly half a second before their first visible
entry. They still have the stem-clock discrepancy and the wrong acting attitude,
which demonstrates why pre-roll alone is not the cure. It may help missing “Hey”
and other abrupt entrances, but cannot guarantee Kling's performance quality.

Long phrase groups plus handles may exceed an eight-second take. For example the
cut-13 group is about 7.13 s before handles, and the opening two phrases about
7.33 s. Use a longer supported take or a purposeful continuation/insert rather
than trimming off words to satisfy a fixed generation duration.

## Normalized owner feedback, keyed to this numbered version

“Enclose” below refers to the owner's requested phrase framing, not a timing edit
already implemented. Approximate quotes should be resolved against actual lyrics.

| Review cut / stable ID | Recorded direction |
| --- | --- |
| 1 / s001 | Keep; consider an attention-grabbing, musically integrated opening |
| 2 / s002 | Strong keeper: scope |
| 3 / s003 | Investigate guide/assembly sync and missing “Hey”; possible separate close-up |
| 4 / s004 | Keep concept; musical equipment response, longer progressing map action |
| 5 / s005 | Fix sync; retain/rebuild based on corrected test |
| 6 / s006 | Variation/continuation of map activity, not replay |
| 7 / s007 | Fix sync and phrase placement |
| 8 / s008 | Hold through and beyond “don't quite match” |
| 9 / s009 | Enclose “Can I send you my stuff?” |
| 10 / s010 | Enclose “Tell me what you got”; re-time local FX if moved |
| 11 / s011 | Enclose “Right?” |
| 12 / s012 | Enclose “I don't see anything / Think you forgot to attach it” |
| 13 / s013 | Enclose “If you've got it, give it / Don't clean it up first / I'll work on it now”; performance sync needed |
| 14 / s014 | Enclose “We'll see what's your deal” |
| 15 / s015 | Remove: no useful function in this edit |
| 16 / s016 | Enclose “In the garden, meanwhile” |
| 17 / s017 | Enclose “There's a little green light” |
| 18 / s018 | Enclose/emphasize “moving” |
| 19 / s019 | Enclose “through the psychedelic garden”; moving plate with retained/rebuilt separate particle layer |
| 20 / s020 | Enclose “Something with no name is waking” |
| 21 / s021 | Enclose “in the psychedelic garden”; hanging-light music response |
| 22 / s022 | Enclose “And whatever woke is waiting / for the song to begin”; approach into close-up or split the latter phrase |
| 23 / s023 | Enclose “There / You've got it”; progressive specimen work across returns |
| 24 / s024 | Enclose “That should be enough / Just look and tell me / Do you see a pattern”; varied purposeful activity and lip sync |
| 25 / s025 | Enclose “I'm sure it's there / Hard to find, right?” |
| 26 / s026 | Enclose “I see the world plus more” through “Close but no see car” |
| 27 / s027 | Enclose “Subject: Mars / You come back around” |
| 28 / s028 | Enclose “I'll pull it into a shape / and spin your world around / No”; remove clone; possible punctuating “No” close-up |
| 29 / s029 | Keep |
| 30 / s030 | Uncover/excavate, not bury; consider reference as end-state |
| 31 / s031 | Enter on “Especially stupid”; prepare gesture/expression with real pre-roll |
| 32 / s032 | Acceptable weather insert |
| 33-34 / s033-s034 | Replace split-generation approach with separate actor takes/compositing or singles |
| 35 / s034b | Reconsider filler; use its available interval purposefully in phrase-led re-plan |
| 36 / s035 | Keep |
| 37-38 / s036-s037 | No explicit note supplied; do not infer approval or rejection |
| 39 / s038 | Excessive post-landing fire; reported sync concern needs contextual interpretation |
| 40 / s039 | Eliminate restart of preceding rocket action |
| 41 / s040 | Requested “Can't tell you if they're true” entrance; see timing conflict below |
| 42 / s041 | Keep |
| 43 / s042 | Sync wrong: confirmed stale in-point plus guide-clock discrepancy |
| 44-45 / s043-s044 | Keep |
| 46 / s045 | Enclose “Tails wagging to music” |
| 47 / s046 | Enclose “that bends your mind”; extreme close-up and heightened acting |
| 48 / s047 | Enclose “Tiny mouths all agape” |
| 49-54 / s048-s053 | Keep |
| 55 / o01 | Strong keeper: tunnel |
| 56 / o02 | Rework sync and reference; question to someone on speaker call, off-camera eyeline |
| 57 / o03 | Rework sync and reference; confused response, not smiling at lens |
| 58-69 / o04-o15 | Potentially usable timing/concept; act each exchange's emotion, not generic happiness |
| 70-71 / o16-o17 | Likely intended closing pair: one continuous vista/state rather than two different vistas; confirm numbering |

### Ambiguities preserved, not silently decided

- The reviewed movie contains 71 cuts, not 72. The final “71-72” note likely
  refers to the two closing views, numbered 70-71 here. Treat that as provisional.
- Cut 39 maps to rockets_landing_wide, not a designated lip-sync performance.
  Preserve the complaint but don't assign a facial-sync fix to it without checking
  the intended moment. Numbering may be approximate in this region.
- Cut 41 is the spring/canal shot. The new note asks it to enter on “Can't tell
  you if they're true”; the previous approved instruction placed it at “Elsewhere,
  under a smaller moon.” This is a potential creative revision or numbering slip,
  not evidence that the old explicit cut mysteriously moved. Resolve in paper edit.
- Cut 70 is a landscape, so the generic emotional-acting note for “58-70” primarily
  applies to the performance takes through 69.

These do not block the diagnosis. They should be settled before rewriting the
shot plan or ordering replacements. Nothing has been changed on their assumption.
