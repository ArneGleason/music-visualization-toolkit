# Claude execution: one new overhead specimen take

Project: C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit-video-generation

## Scope

The owner authorizes ONE replacement Flow take for s004, not a batch.
Expected cost: 100 Flow credits, no Kling. Verify the UI quote and stop if
higher or if the requested model/settings are unavailable. Do not auto-retry.
The earlier inspection handoff is blocked/finished; this is a separate version.

Read handoff.json, verify the first-frame hash, and paste flow_prompt.txt
verbatim. It already contains the same expressive style lock as v3; do not
append another lock or rewrite it. Use the approved still in Start ONLY.
Leave End EMPTY. Identical start/end is deliberately excluded: we want the
object arrangement to advance rather than reset.

## Flow

Veo 3.1 Quality; Frames-to-Video; 16:9; 720p; eight seconds; x1.
One continuous locked overhead shot, no angle change, morph or midpoint
transition. Keep the pieces flat/parallel to the tabletop to reduce the
opportunity for the generator to invent an underside or different specimen.
Use only the supplied first frame. No new image generation or other references.
The prompt describes ONE simple attempt and a changed end state, not an
"again and again" loop. Do not invent stronger camera motion for interest.

Download the full original result and retain it untouched. Copy byte-for-byte
to out/opening_specimen_v2/base.mp4; do not overwrite a different existing file.
If a normal download fails, record the job and blocker; do not regenerate to
solve a download problem. Do not disable security protections.

## Inspect before calling it ready

Watch the full take, inspect a contact sheet at least every 6 frames at 24 fps
(every quarter-second if another fps), and inspect suspicious transitions more
closely. Check:
- fixed overhead framing for the whole take, especially the old failure region
  around source 3.5-4.5 seconds;
- persistent piece silhouettes/holes/helix patterns and credible hands;
- no new scene, radial blur, dissolve, shape change or loop/reset;
- deliberate action, with a different but stable end arrangement.

Required editorial source interval is [12,154) on a 24 fps timeline:
0.5 through 6.416667 seconds, 142 frames, 5.916667 seconds.
Do not certify eight seconds of coverage from a first-frame match alone.
Retain even a flawed output and report actual usable intervals. Set blocked
status if this required interval is not continuously usable. No automatic retry.
Do not discard an otherwise usable shot solely for imperfect beat alignment;
84 BPM here is a movement character, not proven audio synchronization.

Describe the end object state for a later continuation. Preserve one labelled
end-state reference under this folder if useful; record its source timestamp.
Do not generate a continuation, assign later returns, or reuse this take as a
fresh restart on s006/s008 without further planning.

## Exact timing and assembly division of responsibility

All timeline frames are zero-based, end-exclusive, 24 fps, speed 1.
- Accepted singing s003: [155,334), source origin 143, source interval [12,191).
  This contains "It's important", lyric end 332, within the returned coverage.
- New specimen s004: [334,476), source origin 322, source interval [12,154).
  This contains "More than that sounds", lyric [387,464), plus 12 frames after.
- Source zero for this new prop take maps to song 322/24 = 13.416667 seconds.
  This is editorial placement, not a lip-sync guide origin.
- The half-second lead-in is real source footage. Save it; Codex trims at assembly.
- Eight seconds nominally provides 38 exit frames beyond source frame 154.
  Report actual returned frame count and usable coverage; do not assume handles.

Do NOT apply the 0.178348-second vocal offset to this prop shot. No audio guide
upload, no Kling, no TTS. Codex uses the master music once, ignoring scratch audio.
Preserve native fps; Codex timestamp-conforms if required, never slows footage
by interpreting 30 fps frames as 24 fps.

Claude does NOT assemble, modify production shotlist or change cues. Codex must
update BOTH shotlist and overlay cues for an isolated review ending at frame 476.
The old s005 start at 430 must not cut off s004's phrase. This is a planned
revised opening, not a blind clip swap against old timing.
Do not shift any later shot or protected FX to work around old overlapping cuts.

## Receipt and handshake

Only repository writes under out/opening_specimen_v2/. No commit or push.
Write RECEIPT.md: actual settings, credit quote/charge, job/asset link or ID,
original filename, output path/hash, ffprobe fps/dimensions/frame count/stream
start times/durations, watermark status, inspection sheets, actual usable
intervals, end state and weaknesses. Unknown means unknown, not requested value.

Add claude_result to handoff.json, preserving its clock and proposed cuts.
Status after successful generation/download/QA:
claude_done_ready_for_codex_verification.
If required continuity fails: claude_blocked_unusable_generation, with the
downloaded file pointers and reason. Codex verifies and previews; owner decides
acceptance. No new paid work is implied by either status.
