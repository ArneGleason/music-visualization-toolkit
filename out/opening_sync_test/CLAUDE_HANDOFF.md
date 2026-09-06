# Claude handoff: opening lip-sync timing test

## Current status: download task completed by owner

The owner supplied kling_20260906_Lip_Sync__2622_0.mp4. Codex copied it
unchanged to synced.mp4, verified embedded-guide alignment, and rendered
the review previews. The download-only task below is now historical. Do not
download again, regenerate, or start a batch. Await a new explicit task.

## Immediate task: download only

Work in `C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation`, not the sibling toolkit repository.
Read this file and `handoff.json` in this directory before acting.
The owner has delegated the browser/download work to Claude. This opening test
has ALREADY been generated in Flow and lip-synced in Kling. Do not submit
either again, spend more credits, or start a batch.

Use the owner's existing signed-in Kling session to download the completed
opening astronomer-at-desk Lip Sync result. It shows the woman with an updo,
mustard vest and tweed jacket, seated at a desk; telescope left, empty silver
spacesuit right, Mars landscape behind. It is NOT the earlier dim television
outro result. Do not identify it solely by being the newest card if more jobs
have appeared. Compare with `base_contact.jpg` and `base.mp4`.

Flow base title: Astronomer at desk listening.
Flow source page:
https://flow.google.com/project/a703a463-e6e5-41e6-9bec-49d2d2930ba0/edit/83089134-9699-4e40-bd45-9450f8f8d287
Original base download: Astronomer_at_desk_listening_202609052213.mp4.
Kling job: eight-second Character 1 Lip Sync, 10 credits, submitted after that
base download; observed balance 516 to 506. No durable Kling job ID was captured.
The attempted download address was
https://v15-kling.klingai.com/klingai-stream-sgp/kling/download/MzIwNjMyNDQwMzA0MDE1MTY2ODUxMDcwMQ==?x-kcdn-pid=112372
This is an identification clue, not a guaranteed durable URL. Prefer the normal
Kling download interface. Codex's attempt encountered ERR_BLOCKED_BY_CLIENT.
Do not disable security controls to force a download. If your normal workflow
also fails, report the blocker without regenerating.

Retain the original downloaded file unchanged, then copy it to:
`C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation/out/opening_sync_test/synced.mp4`
If that target already exists, verify identity and report it; do not overwrite
a different file. Report a watermark if present; do not remove it or upgrade
the account. Download is not acceptance of a candidate final.

## Timing contract, no implicit offsets

All song-frame numbers are zero-based on a 24 fps timeline. Intervals are
start-inclusive and end-exclusive. Native source fps may differ.

| Item | Exact value |
| --- | --- |
| Song origin of source time zero | song frame 143 = 5.958333333333 s |
| Full requested source coverage | 192 timeline frames = 8 s |
| Existing s003 cut interval | song frames [155,293), 138 frames |
| Source in-point for s003 | 12 timeline frames = 0.5 s |
| Source out-point for s003 | 150 timeline frames = 6.25 s, exclusive |
| First lyric onset reference | song frame 156 |
| Guide upload placement | source time 0, full eight seconds |
| Additional guide shift in Kling | ZERO |
| Playback speed | 1.0, no stretch |

The supplied `guide.wav` is already aligned. Upload it unchanged if a FUTURE
explicitly authorized retry is needed. Never add the 0.178348-second offset
again. Never trim its leading quiet section or normalize the first syllable to
time zero. The existing guide was extracted from the raw lead stem starting at
5.779985333333 s, because raw stem time + 0.178348 s = master song time.
This extraction rule is provenance, NOT another action to apply to the guide.

The half-second lead-in consists of genuine generated frames. It is not silence
to prepend to a finished video, repeated first frames, or a reason to discard
the first half-second of the downloaded source. Codex applies the source
in-point at assembly. Preserve the entire returned take and its actual duration.

For any future approved continuous take:
source in-point seconds = (cut start song frame - take origin song frame) / 24.
It is not the cut's absolute song time and is not a native 30 fps frame count.
Changing frame rate must preserve elapsed time, never interpret 30 fps footage
as 24 fps playback. Codex's shared timebase converter handles this after receipt.

## Recorded Kling settings, already submitted

- Input video: `base.mp4`, SHA-256 recorded in `handoff.json`.
- Audio: `guide.wav`, mono 48 kHz, 384000 samples, hash recorded.
- Character 1; guide spans source time 0 through 8 seconds.
- Sound from Video OFF. No generated speech, added music or speed adjustment.
- The full master soundtrack is used only for the review/assembly, not as the
  lip-sync driver for this test.

## Receipt and ownership

Write `CLAUDE_RECEIPT.md` alongside this file. Include:
- result identification and original download filename;
- exact saved path, byte size and SHA-256;
- actual width/height, fps, picture frame count, video/audio duration and start
  timestamps, using ffprobe if available (otherwise mark unverified);
- whether the output includes embedded guide audio and a visible watermark;
- any trimming, conversion, substitutions or settings changes (expected: none);
- blockers or ambiguity. Never fill unknown values with the requested values.

Write only under `out/` in the repository. Leave prompts, production shotlist,
assembly rules, protected FX selections and original media untouched. No commit,
push, additional generation, production ingest or full-film render in this task.

Codex owns receipt verification, audio alignment checks, frame-rate conversion,
and the standalone/same-assembler previews. The owner then reviews perceptual
sync before any production adoption or further batch generation.
`review.py` is prepared here for Codex; Claude need not run or modify it.

Embedded audio matching the guide checks clock preservation, not whether the
mouth convincingly matches each phoneme. Check entrance, phrase interior and
ending separately. Do not shift the whole take to disguise unwanted motion in
silence. This base has unsolicited mouth movement around 6.5-7 s, a known source
limitation. Keep it visible in the comparison.

The current edit cuts away during "It's important" (lyric frames [284,332)).
The full-take review shows her through that phrase; the assembly review keeps
the current cutaway. This is intentional and not a request to move a cut.

## Before future generation batches

This is a worked single-take contract, NOT authorization for 60 generations.
Codex will issue one versioned manifest row per approved take with exact inputs,
hashes, speaker, song origin, requested coverage, cut mappings, generation
settings and output paths. Claude must report actual delivered coverage.
A changed guide, cut plan or origin requires a new contract/version, not an
unrecorded local adjustment. Ambiguity or contradictory instructions means stop
that item and report it. Test one returned take end-to-end in the assembler
before scaling up.
