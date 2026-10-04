# A Right Little Something — music-video workspace

Initial intake: 2026-10-04. Goal: review a full-song animatic with the master,
performed lyrics, word timing and musical/frame indicators before choosing
scenes or generating footage.

## Located and prepared

- Master: `A Right Little Something 2026-10-03 2137.wav`, 219.378 seconds,
  48 kHz stereo, 24-bit. The original exported master is the audio authority.
- Native Bitwig project: `A Right Little Something.bwproject`.
- Original lead and cleaned `Lead Vocal - Renaissance` samples: both
  218.320 seconds, 48 kHz stereo. These are source samples, not verified
  arrangement-aligned exports. The Renaissance file is 32-bit; original is 16-bit.
- [Lyric source: Lyrics - 2026-10-02](https://docs.google.com/document/d/19mydTi8AzFXmam87QFMKWN1E7Zomooo1r1sgITz9588/edit?usp=drivesdk).
  `lyrics/source-google-doc.txt` preserves the fetched document.
  `lyrics/arranged.txt` extracts the rearrangement, with spelling and repeated
  choruses preserved. `lyrics/source.json` records provenance.
- `timeline.json` contains 64 unplaced lyric lines in 11 arranged sections,
  plus separate empty tracks for audible echoes, timing notes and future scenes.
  Source section bar counts and performance directions are document context,
  not measured timing or instructions to this agent.
- Mood image: `generated/refs/orbit-mood.png`.
- Established Harper reference from Monsters Undone:
  `generated/refs/harper-established.png`. Identity continues; wardrobe and
  setting are provisional. Previous local project remains named
  `projects/monsters-loose`.
- Video direction: graphic-novel illustration, same main character, Kling.
  The previous workflow used 24 fps; this workspace provisionally follows it.

## Timing checkpoint needed before the first aligned pass

The user supplied Bitwig loop/export bounds **2.4.1.00–83.1.1.00**.
If the signature is 4/4, these correspond to zero-based quarter-note beats
7–328; the signature and tempo map still need verification.
Master second zero is the export start, not necessarily vocal sample zero.

No DAWproject export was found in the song folder. The stopped Python bridge
broker was restarted and the live connection verified against A Right Little
Something. Both Apollo and Renaissance lead and backing tracks are enabled;
the original Lead Vocal and Backing Vocals tracks are muted. Delay+ returns
are present, so repeats must be checked against the master as well as source
vocals. The bridge exposes no arrangement clips, loop bounds or tempo map.
The observed transport tempo was 85.4579086303711 BPM at its current position;
this is not a verified song-wide tempo. Snapshot/logs are in generated/bridge/.
The native project and mixer were not changed.
Export the current arrangement as DAWproject to:

`generated/source/A Right Little Something.dawproject`

This file should provide tempo/meter, track and clip positions, source offsets,
and any warp information. Resolve vocal source seconds to project seconds,
then subtract the export start. Check loop duration against the 219.378-second
master and record discrepancies without silently stretching audio.
The 1.058-second difference between master and vocal source durations is
**not** evidence of the vocal offset.

The existing timeline compiler uses DAWproject/master-clip placement to derive
its grid. Confirm its resulting origin matches this loop before running sync;
if the master clip is absent, adapt the import deliberately to the loop origin.
Do not create a guessed 88-BPM grid from the lyric document's performance sketch.

## First-pass workflow

1. Confirm DAW timing, source offsets, active vocal clips and warp status.
   If clips are edited/warped, use arrangement-aligned vocal renders or map
   every source interval through the exported arrangement.
2. Run unprompted Whisper on the cleaned Renaissance lead with word timestamps;
   retain raw candidates in source seconds. Compare the original lead and master
   where echoes are ambiguous. The audible recording determines repeat counts.
3. Reconcile candidates against the arranged lyrics. Retain extra performed words,
   echoes and uncertain sounds; do not force them out to match the sheet.
   Record source-word links, confidence, echo/repeat classification and uncertain
   spans. An echo is not automatically a new sung line or an improv.
4. Align the corrected **performed** transcript with the previous workbench
   word-timing tools. Store source and master times, then derive frame positions
   from the verified musical grid. Keep acoustic word edges available; any
   creative rhythmic snapping is a separate editable decision.
5. Review ambiguous words, echo tails, held vowels, overlaps and instrumental
   passages against the master. Preserve raw recognition and correction history.
6. Build the full-song lyric/timing animatic: original master, primary lyrics,
   a distinguishable echo layer, bar/beat, frame and time indicators.
   Review the backbone before adding scene/shot decisions.
7. Use `shots/shotlist.json` as the shot-edit authority once shots are planned.
   Re-plan using `tools/shotplan.py --merge`; keep shared prompt locks identical.
   Review the animatic before paid Kling generation.

## Environment and file policy

Repository Python works at `./.venv/Scripts/python.exe` on this Windows host
(the Windows equivalent of the repository's `./.venv/bin/python3` convention).
It stays dependency-light.

The previous local alignment runtime was verified by importing Whisper,
stable-ts and Torch and detecting the RTX 4080 SUPER with CUDA.
`project.local.json` records the interpreter, cached large-v3-turbo model,
extension path, original sources and unresolved vocal origin.
No package installation or transcription was performed during intake.

Large media, source exports, images, recognition output and renders go under
Git-ignored `generated/`. Machine-specific paths stay in ignored
`project.local.json`. Small project configuration, lyrics, register and
production notes remain reviewable in the repo.

## DAWproject received

The user exported the project and it was copied into generated/source/.
Inspection confirms 4/4, 919 tempo points spanning 85.457912–91.316771 BPM,
and both cleaned lead clips beginning at beat 7.723630905151367.
Their nested source clips start at source second zero and use algorithm raw;
no warp nodes were found. Source-zero offset is recorded provisionally in
project.local.json and intake-status.json.

The supplied loop beats 7–328 integrate to 219.597816 seconds, while the
master is 219.378 seconds: a 0.219816-second discrepancy needing reconciliation.
Do not stretch the master or mark the mapping verified before resolving it.
The earlier missing-export instructions above describe the intake checkpoint;
the export is now present.

Current status: export received; timing discrepancy under review; words are
unplaced, echoes untranscribed, animatic not yet rendered.

## Bitwig UI timing review — 2026-10-04

The audio export panel was inspected without exporting or changing settings.
It shows From 2.4.1.00, To 83.1.1.00, WAVE 24-bit, 48000 Hz.
Real-time, Dither and Pre-fader appear disabled. These range and format values
match the supplied master information; they do not prove the historical export
used every current option.

The opening arrangement tempo point is 1.1.1.00, 88.83 BPM, Hold disabled.
The DAWproject opening point has value 88.833073. However, a later group of
seven points restarts at time zero after the point at beat 279.25. The importer
sorts these local times into the beginning of the arrangement, replacing four
same-time points and creating an incorrect early tempo curve.

Bitwig contains a separate tempo automation clip at 71.1.1.00 (beat 280),
length 12.0.0.00 (48 beats), offset 1.1.1.00 (zero). Its seven points show
Hold enabled as a group. Individually inspected points: local 1.1.1.00,
86.93 BPM, Hold enabled; local 9.2.1.00 (beat 33), 86.14 BPM, Hold enabled.
These match the exported values 86.931702 at local beat 0 and 86.139074 at
local beat 33. The export incorrectly presents this group at local beats
0, 23, 24, 32, 33, 36, 37 in the global TempoAutomation and labels them linear.
Its final point at beat 328 is outside that local group and was retained.

A diagnostic reconstruction adds 280 beats to those seven local times and
uses hold interpolation for them, retaining the earlier linear ramps. The
calculated export interval becomes 219.380196 seconds, versus the master's
219.378 seconds: residual 0.002196 seconds, reduced from 0.219816 seconds.
This explains approximately 0.217620 seconds of the discrepancy. The small
residual and the transition into the automation clip still need verification;
no duration fitting or stretching was applied. The source DAWproject and
generic importer remain unchanged. Do not use the uncorrected map for alignment.

Only UI selection, zoom and playback-start position were changed during review;
no tempo points, audio clips, mixer parameters or export settings were edited.

## First lyric/timing animatic — 2026-10-04

The user accepted the 2.196 ms residual for this animatic. `timing-repairs.json`
records the seven UI-verified corrections with exact expected source points;
the importer rejects them if a later export differs. `project.json` supplies
the export origin, beat 7. The corrected Renaissance/source vocal origin is
master second 0.488757766. Timing is not fitted to the master's duration.

Local unprompted large-v3-turbo Whisper ran on the Renaissance lead, original
lead and master. The Renaissance pass hallucinated many orbit repetitions;
these are retained in raw output and not copied into the performed register.
The original lead/master cross-check recovered the missing verse. Stable-ts
aligned a lyric-sheet-based phrase plan against the Renaissance source;
agreement between original-lead and master word edges supersedes forced
alignment edges when both independent passes agree. Remaining wording and
syllable edges are provisional. Original source lyrics are preserved.

First pass: 63 primary lyric lines placed, two separately marked repeated
phrases, 278 aligned word candidates and six short/zero-edge review flags.
`lyr-024` (sheet text “Loose it.”) remains unplaced rather than forcing an
unrecognized line into the song. Echo/repeat/new-delivery classification and
the repeated “in” words around 120 seconds require listening review. Outro
“Thank you” recognition candidates disagree across passes and are excluded
from the lyric display pending review. Full acoustic/source timestamps,
recognition results, phrase plan and issues remain in generated/transcription/.

The editable Blender VSE rig and full-song H.264/AAC preview are in
`generated/animatic/A-Right-Little-Something-lyric-timing-v01.blend` and `.mp4`.
The video contains 5265 frames at 24 fps (219.375 seconds); the 3 ms difference
from the WAV length is frame rounding. The master audio is placed at frame 1.
The video displays the primary line, active word, separate repeat candidates,
project bar/beat, BPM and stable lyric IDs. No scene/shot decisions were added.

Revision 02 restores the arranged sheet's exact lyric spelling and punctuation,
including typos. It expands both additional “Out here in orbit.” deliveries
with visible active words, using original-lead Whisper edges. The zoom line
keeps the arranged three “in”s; collapsed repetition edges now have interpolated
spans and explicit review flags. The performed reference in `lyrics/performed.txt`
was appended as a separate “Lyrics as performed” section in the source Google
Doc; all earlier sections were preserved. The standalone “Loose it.” line is
still unconfirmed. `lyrics/performed-adjustments.json` records the timing changes.
There are now 279 displayed word tokens, including the separate “Every thing”
spelling. Render filenames and review URLs remain stable across this revision.

Revision 03 uses the songwriter's performed wording: “Hit zoom. Zoom in, in,
in, in, in, in, in, in, in to see far”. `lyrics/zoom-cues.json` records nine
individually measured vocal-energy attacks, source/master clocks, musical
positions, frames and the processed-vocal cross-check. They are acoustic cue
candidates, not equally spaced interpolation or sample-exact confirmed word
boundaries; the first and fifth attacks differ by about 50 ms across stems.
The animatic displays an active 1/9 through 9/9 counter and Blender markers.
`shots/shotlist.json` captures the sphere-telescope point-of-view shot and its
nine internal zoom cues. Frame counts come from the corrected timing grid.
Normal and half-speed vocal/click checks are in generated/animatic/zoom-nine-cues*.wav.
The Google Doc's performed section was corrected; its arranged section remains
unchanged. Listen to the click check before locking the zoom animation.

Review in Chrome:

- Listening, phrase selection, range notes and local Whisper dictation:
  http://127.0.0.1:8768/ . The First-pass review queue links to flagged words.
- Exact frame stepping/jumping and frame notes: http://127.0.0.1:8767/ .
  Frame numbers are one-based. Use `?frame=1000` for a direct reference.

Listening notes persist under `generated/review/listening-notes.json` with
bar/beat labels, seconds and frame anchors. Dictation pauses playback, freezes
the note's anchor, transcribes locally, and lets the user review text before
saving. Microphone access is requested only after Record dictation is clicked.
The audio endpoint was tested with generated speech, not the user's microphone.
Frame notes persist separately in `generated/review/frame-notes.json`.
`generated/review/current-render.json` is the stable frame-review media pointer.

To restart the local review tools from this repository:

```powershell
& ./.venv/Scripts/python.exe tools/listening_review.py projects/a-right-little-something/project.json
& ./.venv/Scripts/python.exe tools/frame_review.py --video projects/a-right-little-something/generated/animatic/A-Right-Little-Something-lyric-timing-v01.mp4 --notes projects/a-right-little-something/generated/review/frame-notes.json --state projects/a-right-little-something/generated/review/current-render.json --port 8767
```

Run those servers in separate terminals. The first-pass scripts in tools/
preserve raw recognition and keep generated media out of Git. Review edits
belong in the existing register and Blender rig; do not rerun first-pass intake
over reviewed data. `prepare_lyric_animatic.py` rejects a changed register when
its import snapshot exists. Next step: listen and collect lyric/timing notes,
then apply corrections and render the next preview at the same review URLs.


The current nine-cue movie is `generated/animatic/A-Right-Little-Something-lyric-timing-v03.mp4`. Both review URLs remain stable. `current-media.json` and the frame-review pointer select the latest completed render; a Windows file lock produces a fresh media filename instead of leaving the viewer on an older movie.

Restored the performed tail 'things big now.' at master 122.34–123.39 seconds (frames 2937–2961), immediately before the next phrase. All nine user-approved zoom cue times and frames are unchanged. The performed Google Doc section and current review render include this correction.

Performed entrance corrected to 'All, all calling.': first All at master 108.094 s/frame 2595, second all at 109.524 s/frame 2630, calling at 110.254 s/frame 2647. Both raw Whisper passes captured the double word as 'Oh, oh'; songwriter confirms All. The arranged sheet remains unchanged, and the performed reference/Google Doc and animatic now include both words.
