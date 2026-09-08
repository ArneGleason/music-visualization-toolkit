# Astronaut reply: one performance, then review

Read handoff.json first. All paths are relative to project_root. Owner authorized
one fresh Flow take and one Kling lip-sync, not reuse of the old s012 result.

1. Verify input hashes. Use approved astronaut_close_sync_a.jpg as sole FIRST
   frame, no end frame. Do not edit it into a quiet-mouth pose or use a generated
   video frame. Paste flow_prompt.txt VERBATIM with its identical lock block.
2. Flow: Veo3.1 Quality, Frames,16:9,720p,8seconds,x1. Expected100 credits.
   Stop if settings/model unavailable or quote exceeds100. No automatic retries.
3. Monitor BOTH Flow and Kling using the schedule below. Download promptly.
4. Preserve untouched Flow original plus byte-identical base.mp4. Inspect full
   take: identity/set/costume stability, mouth unobstructed, active singing through
   source0.875..5.458 and real moving lead-in. Check each phrase for blank mouth
   gaps, not merely whether some mouth movement exists. If clearly unsuitable,
   report and stop before spending on Kling. Do not substitute an older base.
5. Kling: one Lip Sync, Character1, full base, supplied guide.wav at0:00..0:08,
   Sound from Video OFF. Expected10 credits; stop if more. No shifted guide,
   silence trimming, gating, TTS, scratch vocal or speed changes. Existing
   no-watermark option only, no extra purchase. No retries without owner approval.
6. Save untouched original plus synced.mp4. Do not crop, trim, retime, pad,
   add master audio or assemble. Inspection crops are separate JPGs only.
7. Write RECEIPT.md and add claude_result to manifest, preserving other fields.
   Include paths/SHA-256, native fps/frame count, actual durations/stream starts,
   job IDs, actual costs, input identity, usable mouth coverage and weaknesses.
   Record submission/check/ready/download times and displayed percentages, so
   we can distinguish generation time from waiting and inspection time.
   Set status claude_done_ready_for_codex_verification when downloads are saved.
   If blocked, state stage and reason; never resubmit to solve uncertain download.

## Prompt completion checks, no progressive backoff

For BOTH services: check after30seconds, then every20seconds. At90% or higher,
check every10seconds. If consecutive percentages rise, estimate remaining time
from recent progress and check halfway to that estimate, clamped to10..20seconds.
Percent is only a hint, not a reliable completion promise. If percentage stalls
or disappears, keep20second checks; do NOT extend to60/120/240second waits.
Do not repeatedly reload the page; inspect the existing job's displayed status.
Do not overlap checks. Tool-call time counts toward the interval, so do not add
a full extra sleep after a slow response. Respect explicit rate limits/retry-after.
Use short waits rather than a long blocking sleep. This is a foreground job
workflow, not permission to install background polling services or automations.
When ready, download before doing lengthy inspection. At15minutes pending,
report progress to the owner; keep bounded20..30second checks if possible.

## Exact clock and edit

Source zero is song899/24=37.458333s. Visible cut starts911/24=37.958333s at
source0.5s, giving genuine12-frame pre-roll. Cut ends1030/24=42.916667s,
source131/24=5.458333s. Never use old912..1047 boundaries or the old audio slice.
The raw vocal extraction offset was already applied once by Codex; no more shifts.

The eight-second guide includes a third phrase, "If you've got it, give it",
after the visible cut. Keep it intact and perform it as continuation; it is a
real spare tail, not dead air. This does NOT authorize generating the next scene
or moving that phrase into the current shot. Final edit stays with Codex.

Whole phrases visible: "I don't see anything"920..971, "Think you forgot to
attach it"971..1030. Timing markers are editorial references; report what the
actual mouth does rather than assuming correct articulation from audio correlation.
Kling may return less than8seconds. Report actual coverage, never assume it.

Write only under out/astronaut_reply_v1/. No production edits, commits, additional
shots or paid retries. Tell the owner when the manifest/receipt are ready for
Codex to verify and make a short same-clock assembly preview.
