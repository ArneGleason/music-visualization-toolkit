# Timing repair auditions

These are isolated experiments, not a revised production edit. No new images,
motion or lip sync were generated. Production shotlist checksum is unchanged.
Render snapshots and source hashes are recorded in `manifest.json`.

## Watch in this order

1. **01_opening_comparison.mp4**, 13.5 seconds. A is current source mapping;
   B corrects the measured stem-to-song origin. Listen to the words after “Hey”:
   does the mouth track them more convincingly through the whole shot?
   The correction lacks five source frames at the entrance. Those are explicitly
   held for the diagnostic, not genuine pre-roll or a repaired missing syllable.
2. **02_cut43_comparison.mp4**, 11.5 seconds. A uses the old 2.84-second trim.
   B removes only that stale trim. C also corrects the stem-clock origin.
   This should make the difference between a large placement error and the
   smaller constant offset easy to judge. C holds four missing entrance frames.
3. **03_outro_comparison.mp4**, about 8.08 seconds. A is current mapping; B moves
   both actors consistently according to the measured guide origin. There is
   enough existing head coverage here, so no held frames are needed. The acting
   and smiling remain unchanged: this test cannot repair those creative issues.

Each comparison plays A then B (and C for cut 43), with the same passage of
master music repeated. Labels identify the variant. Separate A/B/C files are
also available. Context before/after the tested cut is retained where specified.

## What stayed fixed

Editorial cut points, adjacent shots, flat lyric choreography, local effects,
source performances, 24 fps playback and the master soundtrack. No global flash.
No guessed phoneme-level offsets. B/C source origins use the measured
0.178348-second stem placement, rounded to the nearest output frame.

Both control and treatment exports explicitly normalize video and audio start
timestamps to zero. This removes the old container's roughly one-frame offset
equally in all variants. Thus A is a control of the old source mapping, not a
byte-identical extract of the v04 container.

Held entrance frames are ONLY a diagnostic substitute for unavailable source
coverage. Do not promote them as final performance fixes. Genuine missing “Hey”
or clipped onset material still needs earlier performance/guide context or a
deliberate alternate shot, not a fictitious negative in-point.

## Verification

- The same `tools/blender_comp.py` path creates the previews and the movie:
  protected source resolver, time-preserving CFR conversion, global song frames,
  and the existing lyric renderer. No separate picture-timing implementation.
- Added an explicit `--shotlist` argument to both the Blender assembler and the
  full lyrical render wrapper. An approved snapshot can be passed to both.
  Production defaults remain unchanged. Always use a new output/segment name.
- All three finished comparisons decode without errors. Counts are exactly
  324, 276 and 194 frames. Both streams begin at zero.
- Every individual variant's audio matches the same master excerpt to within
  the 0.5 ms diagnostic sample resolution. Master excerpt origins are
  143/24, 3290/24 and 4165/24 seconds respectively.
- Source-image checks confirm the intended mapping changes. Opening at song
  frame 227 changes from source frame 90 to 84. Cut 43 at song frame 3332 changes
  from source frame 123 to approximately 39 (trim-only) and 33 (both corrections).
  Outro at song frame 4190 changes from source frame 25 to 21. Matches are within
  two original-source frames of quantized expectations; similar adjacent frames
  limit this image-matching measurement. These are not phoneme-quality scores.
- A separately rendered single frame at song frame 227 matches that frame in
  the longer opening-B audition: correlation 0.99945, mean pixel difference 2.40
  on a 0-255 scale after video encoding. Audition range does not reset source time.
- Fifteen existing source-selection/timebase tests pass. Also corrected integer
  versus decimal fps spelling so 24 and 24.0 use the same conversion cache.

## Decision after watching

Do not conclude “all lip sync is solved” from a better source mapping. Evaluate:
does a correction help consistently at beginning/middle/end; is the first word
still missing; is the speaker assignment correct; does the acting suit the line?

If the corrections help, preserve their source/guide-clock provenance and apply
the same mapping method, not a universal guessed delay. If an accurately placed
clip still looks wrong, investigate its original guide-versus-mouth performance
before spending on a replacement.

Then prepare a phrase-led opening section, starting at the beginning and moving
forward. Approve that section's timing and acting before extending the pattern.
Use about half a second of real pre-roll per generated performance take, more
where the vocal phrase needs context, and record the actual take origin. Returning
cuts advance through the same take. Re-timed music FX must use the new song range.

Shared handoff per take: stable take ID, source and guide hashes, master version,
stem placement, guide song origin, fps conversion, available head/tail frames,
all cut in/out frames, and approved preview snapshot. Final assembly must use
that snapshot or explicitly reviewed changes. No silent re-slicing from a new
cut start and no reuse of an old trim after replacing its underlying guide.

The next full reconstruction is intentionally waiting for review of these tests.
