# Opening phrase sync test

## Current result

Owner downloaded kling_20260906_Lip_Sync__2622_0.mp4. Copied unchanged to
synced.mp4 (14,927,838 bytes), SHA-256
840FE139A49EDC0193BF36FEE4E5AFDD7F456E229078B708139DBA18411466F5.
The Claude download-only task is complete; no new paid job was submitted.

Downloaded picture: 1280x720, 239 frames at 30 fps, 7.966667 seconds.
Embedded audio: 7.895011 seconds. Both streams start at zero. Shorter than
the requested eight seconds; do not assume full requested tail coverage.
Audio correlation to guide: 0.999494 at zero lag, best lag 0 ms in +/-50 ms
search. This verifies the guide clock, NOT complete or convincing lip animation.
Timestamp conversion produced the 24 fps review source without slowdown.

review.py completed, production shotlist hash unchanged. Deliveries:
- comparison_guide.mp4: base left, Kling right, isolated guide.
- master_preview.mp4: uninterrupted face with the master at song frame 143.
- assembly_preview.mp4: current edit, frames [143,335), same Blender assembler
  and lyrics. Protected scope remains selected; cut away at frame 293 remains.

Owner reports some words receive no mouth animation despite aligned movements
elsewhere. Contact-sheet samples likewise show closed poses around source
1.5..3 seconds, with animated poses later. Guide half-second RMS in that
early interval is approximately -20 to -19 dBFS, not missing/silent audio.
There is a very quiet interval at 1.0..1.5 seconds (-81 dBFS RMS).
Energy measurements do not establish vocal intelligibility or the exact missed
words. No blanket offset adjustment is justified by these checks. Review the
side-by-side before choosing a repeat pass or modified guide. No retry yet.

## Historical preparation and generation log

Isolated experiment for s003, "Hey, I need you for something. / It's important."
Production edit remains unchanged. Use a relaxed-mouth reference and real generated lead-in.

Clock: 24 fps. Existing cut rounds to frame 155; take starts at frame 143
(5.958333333 seconds), giving 12 frames of real pre-roll. Eight-second guide
must start at raw lead stem time 5.779985333 seconds, subtracting the verified
0.178348-second stem offset. Preview and assembly use song origin frame 143;
source in-point at the existing cut is frame 12, never a held-head placeholder.

Status: one Flow Veo 3.1 Quality take submitted, 8 seconds, 720p, x1,
quoted 100 credits. Kling subsequently completed (see below). Guide verified as eight
seconds, mono, 48 kHz. Image edited with built-in imagegen to relaxed lips;
original approved still remains unchanged. Exact prompts saved beside this note.

Base downloaded as Astronomer_at_desk_listening_202609052213.mp4.
Verified 1280x720, 24 fps, 192 frames, eight seconds. Contact-sheet review:
closed relaxed mouth at entrance and most of take, but unsolicited mouth
opening around 6.5-7 seconds despite instruction. Keep as a diagnostic limitation;
do not claim all tail mouth behavior is driven by Kling. No second Flow take.

Kling submitted once, quoted 10 credits. Character 1 detected, full guide
placed at 0:00 through 0:08, Sound from Video OFF, no speed change.
Kling finished successfully, account balance changed from 516 to 506.
Download through the visible button was blocked by Chrome with
ERR_BLOCKED_BY_CLIENT. No retry generation and no bypass attempted.
Download now delegated to Claude via CLAUDE_HANDOFF.md and handoff.json.
No new generation authorized by that handoff. Embedded-audio timing check
and review renders remain pending.
Run `python out/opening_sync_test/review.py` after saving `synced.mp4` here.
It produces base-versus-sync with the guide, a full-take master preview,
and an eight-second preview using the actual Blender assembler. Test shotlist
only replaces s003; surrounding cuts and protected scope selection stay intact.

Flow take page: https://flow.google.com/project/a703a463-e6e5-41e6-9bec-49d2d2930ba0/edit/83089134-9699-4e40-bd45-9450f8f8d287
Existing cut s003 ends at frame 293, during 'It's important' (lyric frames
284..332). Full-take preview deliberately retains the face through that phrase;
assembly preview preserves the current cutaway. This test does not re-plan cuts.
