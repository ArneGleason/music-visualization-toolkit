# Match the orbital rockets to the accepted landing

Read `out/orbital_continuity_v1/handoff.json` first. Execute this bounded handoff only.

The owner approved the new landing in `out/message_into_rockets_v3/preview.mp4`. They now explicitly request that the preceding orbital rockets match it. This supersedes the old landing task's restriction against replacing orbital. Leave the approved landing and its lip sync/FX untouched.

1. Verify the input hashes. Inspect `first_frame.png` and compare its rocket designs with `landing_design_reference.jpg`. The new start frame was created using the built-in OpenAI image tool, editing the old orbital composition with the approved landing frame as the design reference.
2. Submit ONE Flow Veo 3.1 Quality, Frames, 16:9, 720p, 8-second, x1 generation. Historical cost 100 credits; verify the UI and stop if higher or unavailable. Upload `first_frame.png` as the START frame only. No end frame. Paste `flow_prompt.txt` verbatim including its style lock. No Kling, no audio guide, no purchases.
3. First progress check at 30 seconds, then roughly every 20 seconds, or 10 seconds above 90%. Count tool time toward the interval; respect service limits. No progressive backoff that leaves a finished generation waiting minutes.
4. Inspect the full result, especially source 0.5 through 2.458 seconds. Check matching rocket silhouettes and hardware, controlled tail-first descent, and no explosions or morphing. Record minor defects rather than silently retrying. A material failure requires saving the result and stopping for owner review.
5. Download without watermark, preserve the original and a byte-identical `base.mp4`. No trim, retiming, interpolation or crop. Write `RECEIPT.md` with hashes, settings, actual credits, media ID, dimensions, native fps, frame count/duration and visual findings. Add `claude_result` and update manifest status to `claude_done_ready_for_codex_verification` when complete.

Codex will make the comparison preview. The intended cut remains song frames [2881,2928), taken from source [12,59) on a 24 fps clock. No assembly or production-file edits by Claude, and no commit.
