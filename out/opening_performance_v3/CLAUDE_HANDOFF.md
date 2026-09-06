# Opening performance v3: Claude execution handoff

Project: `C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation`.

## Scope and current status

Ready for Claude, NOT submitted. Owner approved one further test: retain v2's active singing, but replace its
fast bopping/scat-like delivery with a grounded 84 BPM groove.
Generate ONE eight-second Flow take, inspect it, then ONE Kling pass if suitable.
No batch, automatic retries, still regeneration or production edit changes.
Expected costs from the previous run: Flow 100 credits, Kling 10 credits.
Verify the actual UI quotes; stop if either exceeds these amounts or the named
model/settings are unavailable. Do not substitute a model silently.

V2 is completed and preserved. This is a new authorized single-take experiment,
not a retry of an unfinished job. Do not overwrite any v1 or v2 files.

## Creative conflict resolved

Use flow_prompt.txt verbatim, which already includes style_lock_v2.txt.
Do not append the old lock or the old listening prompt.
The versioned candidate lock changes ONLY:
"deadpan performance." -> "self-assured, expressive musical performance."
All photographic, cast, wardrobe, world and camera lock wording is preserved.
This same candidate lock must remain identical if reused in later approved tests.
It is not yet a global replacement in shots/style.md.

For this test the owner's expressive singing direction supersedes the older
style-bible line "Deadpan from the neck up" and the prior closed-lips directions.
She is singing, not listening quietly. Stable frontal visibility does not mean
a frozen face. Aim for wit, groove and assertiveness, not stiffness or glamour.

Return to the original approved singing-pose still listed in handoff.json.
Do NOT use opening_sync_test/closed_mouth.png. The still, vocal guide, style lock and timing are identical to v2.
Only the performance choreography prompt changes. Do not alter the audio to
slow the groove; do not slow or time-stretch the video.

## Execute

1. Read handoff.json; verify the existing first-frame and guide SHA-256 hashes.
2. In Flow use the supplied first frame, Frames-to-Video, Veo 3.1 Quality,
   16:9, 720p, eight seconds, x1. Paste flow_prompt.txt exactly once.
   Do not use an old prompt, a second twin reference or a closed-mouth edit.
3. Submit once and download the entire original result to the base output path.
   Record actual settings, cost, asset link/ID and original filename.
4. Inspect the whole base take before Kling. It must have active singing through
   phrase interiors, readable facial expression, the same identity, and an
   unobstructed largely frontal mouth. The half-second lead-in must be actual
   generated motion. Do not demand perfect word timing from Flow.
   If she remains silent/stiff, covers her mouth or drifts in identity, stop and
   report the base for review rather than spending on Kling or regenerating.
5. If suitable, upload that base and the EXISTING opening_sync_test/guide.wav.
   Character 1, full guide at source 0:00 through 0:08, Sound from Video OFF.
   No TTS, no new audio extraction, no speed adjustment. Submit once.
6. Download the entire Kling result to the synced output path, unchanged.
   Preserve original downloads. Do not overwrite an existing different result.
   Use normal permitted download controls; report browser blocks rather than
   disabling protections. No watermark removal or account upgrades.
7. Write RECEIPT.md with paths, SHA-256 hashes, actual model/settings/costs,
   job IDs or links, observed acting quality, watermark status, and ffprobe
   dimensions/fps/frame count/start timestamps/audio and video durations.
   Mark unavailable details unknown, never copy requested values as actuals.

## Non-negotiable clock

The guide is ALREADY aligned. Do not add any offset or delete quiet sections.
Source time zero = song frame 143 / 24 = 5.958333333333 seconds.
Guide upload time zero = source time zero. Extra offset = ZERO.
Requested source length = 192 timeline frames = eight seconds.
Existing s003 cut = song frames [155,293), source interval [12,150) at 24 fps.
Codex applies the 0.5-second source in-point at assembly; Claude must NOT pretrim.
Speed is 1.0. If Kling returns 30 fps, retain it; Codex timestamp-conforms it
to 24 fps without changing speed. A returned duration shorter than eight seconds
must be reported, not silently padded or treated as a full-length handle.

The guide's 0.178348-second stem/master correction has already been applied by
extracting from raw stem time 5.779985333333 seconds. This is provenance only.
Never shift it again. The original guide hash is unchanged in this test.

## Return and acceptance

Write repository files only inside out/opening_performance_v3/.
Do not change shotlist, production style, protected FX, timing, or audio masters.
No commit or push. Codex will verify embedded audio against the guide and render
the same standalone and actual-assembler previews used for v1.
The owner judges personality AND coverage of the sung words, especially the
earlier missing mouth movement around source 1.5-3 seconds, plus entry and tail.
Audio correlation verifies a clock, not perceptual phoneme accuracy.
No further generation is implied if the test is imperfect.



## Completion handshake
Write RECEIPT.md and claude_result (actual paths, hashes, settings and coverage),
then set status to claude_done_ready_for_codex_verification. Do not mark owner
approval or production adoption. Codex verifies and renders the previews.
