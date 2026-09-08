# Returning reply: clean receiver plate only

Read handoff.json first. Paths are relative to its project_root.

The owner approved trying a return to the familiar receiver for "Don't clean it up first. I'll work on it now." No singer, hands or sorting. This supersedes the proposed next lip-sync performance. The reference does not establish a wide room: do not invent one.

1. Verify the first-frame SHA-256 and the supplied prompt/lock. Attach ONLY codex/out/receiver_dial_macro_b.jpg as FIRST frame, no end frame. Use flow_prompt.txt verbatim, including the unchanged lock. Do not use a frame extracted from another video or redraw/crop the still.
2. Make ONE Flow Veo 3.1 Quality, Frames, 16:9, 720p, 8-second, x1 take. Expected 100 credits, not a live price guarantee. Check the displayed quote; stop above 100 or if unavailable. No automatic retry. NO Kling submission or guide upload.
3. Download promptly when ready. Preserve untouched original under this folder and a byte-identical base.mp4. Do not crop, trim, retime, upscale, add effects/audio or assemble.
4. Inspect the entire take. Receiver layout and background must remain recognizable and stable. No people, hands, new props, rosettes, floating lights, cuts, dramatic meter pulses or camera reveal. Note any morphs, abrupt movements or freezes with source timestamps. Do not claim success just because generation completed. If unsuitable, preserve it and report; do not spend on a retry.
5. Write RECEIPT.md with original/base paths and hashes, job ID, settings, credits, native dimensions/fps/frame count/durations/stream starts, usable interval, continuity weaknesses, and submission/check/ready/download times plus displayed progress.
6. Add claude_result to handoff.json without removing other fields; set status claude_done_ready_for_codex_verification only after saving the files. If blocked, record stage and reason. Never resubmit because download status is uncertain.

## Prompt checks, without progressive backoff

First check after 30 seconds, then every 20 seconds. At 90% or higher, every 10 seconds. With rising percentages, estimate remaining from recent progress and check halfway to that estimate, clamped to 10..20 seconds. If percent stalls/disappears, keep 20 seconds; do not escalate to minute-long waits. Tool latency counts toward interval. No overlapping checks or repeated page reloads. Honor explicit service rate limits/retry-after. At 15 minutes pending, report and continue bounded checks if possible. No background services or automations.

## Exact editorial contract

Timeline is 24 fps; ranges are zero-based, end-exclusive. Proposed picture cut is song1082..1201. Source zero maps to song1070, so use source12..131 after timestamp conform, not native frame-number reinterpretation. That supplies 12 frames of real pre-roll. Requested 192-frame take would leave 61 exit frames; report actual usable handles rather than assuming them.

"Don't clean it up first" is song1090..1137, source20..67.
"I'll work on it now" is song1137..1201, source67..131.
This is a silent editorial plate, so Flow does not need to act out exact phrase timing. Any generated audio will be discarded.

Codex owns rosette continuity, fresh voice-driven receiver light, tracking and the next same-clock preview. Do not synthesize those effects in Flow. Do not touch the accepted duet or prior takes.

Write ONLY under out/receiver_reply_arrival_v1/. No other project changes, commits, paid retries or later shots. Tell the owner this folder is ready for Codex verification.

