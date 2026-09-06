# Next close-up: pieces / almost fit

Read handoff.json first. All paths are relative to its project_root. This is one bounded generation experiment, not a request to batch-generate later shots.

## Execute

1. Verify first-frame and guide hashes in the manifest. Use the approved close-up B still, not a newly edited quiet-mouth portrait. The accepted opening_performance_v3 is the acting benchmark, not the input video.
2. Submit ONE Flow Veo 3.1 Quality, Frames, 16:9, 720p, eight-second output. Attach only the specified first frame, no end frame. Paste flow_prompt.txt verbatim including its unchanged lock block. Expected cost 100 Flow credits; stop if unavailable or more expensive.
3. Download and preserve the untouched original plus base.mp4. Inspect the full clip before Kling: stable identity, real lead-in, unobstructed mouth and active singing especially source1.17..4.75 and5.50..7.08. If it turns into silent posing or has large closed-mouth gaps, record the problem and STOP, no automatic regeneration or wasted lip-sync submission.
4. Submit ONE Kling Lip Sync on the full base. Select Character1. Upload this folder's guide.wav exactly as supplied, from0:00 through0:08. Sound from Video OFF. Do not remove leading silence, apply another offset, crop the audio, reuse an older guide, change speed or substitute scratch audio. Expected cost10 Kling credits; stop if more expensive. Use the existing no-watermark option when available without extra purchase.
5. Download the untouched original plus synced.mp4. No trimming, frame-rate reinterpretation, padding, freezing, music muxing or assembly. If a download is uncertain, resolve the existing job, never resubmit to obtain another download.
6. Write RECEIPT.md and add claude_result to handoff.json. Include actual filenames and SHA-256 hashes, native fps/frame counts, stream start times and durations, actual costs, job IDs, observed mouth coverage and any problems. Preserve all other manifest fields. Set status to claude_done_ready_for_codex_verification ONLY when both files are on disk. If blocked, record the precise stage and keep it clearly blocked.

## Clock and proposed edit

The guide is already aligned. Source time0 maps to song frame488 (20.333333s). The planned visible close-up starts at song frame500 (20.833333s), using source frame12: exactly half a second of real generated pre-roll. It ends at song frame670 (27.916667s), source frame182 exclusive. Both complete phrases fit. Speed stays1.0.

The current opening preview ends at476. Codex will test extending the existing overhead specimen shot one second to500, using its real source frames through177, including the late hand movement. Do not extend the singer backwards to476: that would invalidate this guide mapping. The old production cuts s005/s006/s007 are not the new instructions.

"I've got pieces" is song516..602; "Things that almost fit" is620..658. Cut back to future specimen progression at670, ahead of "Then they don't quite match" at680..719. That later prop take is NOT part of this order. Do not replay the old specimen action or manufacture its coverage.

Kling previously returned slightly less than eight seconds. Measure actual coverage, do not assume it. The required picture ends at source7.583333s, leaving a modest exit handle if the usual7.966667s returns. Codex handles timestamp-based24fps conversion and master-audio assembly, never30fps footage played frame-for-frame at24fps.

## Scope

Write only inside out/pieces_performance_v1/. No production shotlist, cue, source assignment, global document, Git or other project changes. No commits. No specimen generation. No retries without owner approval. This is a review candidate, not an accepted final.

When finished, tell the owner to ask Codex to read this folder's handoff.json and RECEIPT.md, verify the downloads and extend the same-clock opening preview.
