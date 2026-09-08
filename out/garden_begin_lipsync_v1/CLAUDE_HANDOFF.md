# Garden finale: one lip-sync test, NO Flow

Read handoff.json first. Work inside its project_root. Owner approved using the
existing garden footage. This task authorizes ONE Kling Lip Sync, not a new
Flow performance, not new stills, and not an automatic retry.

1. Verify base.mp4 and guide.wav hashes against handoff.json. Base is the entire
existing8second take with its generated audio removed, no changed video frames.
It has no Codex garden-light, green-guide or lyric overlays. Do NOT upload
garden_begin_guide_v2/clean.mp4 or any preview movie.
2. Kling Lip Sync, sole woman/Character1, supplied guide.wav at0:00..0:08,
Sound from Video OFF. No TTS, replacement vocal, transcript synthesis, pitch or
speed changes, silence trimming, normalization or extra offsets. The words in
the manifest are inspection references, not an unsupported script input.
3. Historical quote is10credits. Verify actual cost and stop above10 or if
the required feature/settings are unavailable. Use existing no-watermark
entitlement only, no purchase. If face detection fails, report; no crop or zoom
workaround without permission. A small, quiet face is a known test risk.
4. Check after30seconds, then every20seconds; every10seconds at90%+. Rising
percent can inform a next check clamped10..20seconds. Tool latency counts.
No progressive backoff, repeated reloads, overlapping checks or resubmission
for an uncertain download. Honor rate limits/retry-after. At15minutes report
actual state. Download promptly when ready before lengthy inspection.
5. Save the untouched download under an original_<job-id>.mp4 name and a
byte-identical synced.mp4. Do not trim, crop, stabilize, pad, interpolate or
retime the result. Keep native frame rate and timestamps. Inspection crops may
be separate images only, not replacement source media.

## Exact timing, do not reinterpret

All editorial frames are24fps, zero-based/end-exclusive. Source0 corresponds
to song1774 (73.916666667seconds). Guide already includes the stem placement
correction exactly once. Upload it at zero with NO additional shift.

Visible song1786..1841 uses source12..67, source0.5..2.791666667seconds.
That is55frames, containing the whole phrase "for the song to begin."

| Word | Source seconds |
| --- | --- |
| for | 0.500000..0.958333 |
| the | 0.958333..1.375000 |
| song | 1.375000..1.875000 |
| to | 1.875000..2.250000 |
| begin | 2.250000..2.791667 |

There are12 genuine lead frames, not a held frame or duplicated padding.
The uninterrupted guide contains preceding/following vocal context; do not
delete it. Following dialogue is NOT approved use of this face or a new shot.
Retain the entire returned take and report actual duration. At minimum the
result must cover source2.791667seconds. Do not infer clean tail from duration.

The earlier accepted FX preview used source0..55. This deliberate new in-point
uses12..67 so the synchronizer has lead-in. Codex will inspect the slightly
later picture, conform timestamps if Kling returns30fps, and REBUILD the
accepted garden-light response and excited green guide over the synced result.
Do not simply move the old baked FX clip by12frames, upload it, or overwrite it.

## Verify, receipt, handshake

Inspect the five words individually, especially the first "for" and sustained
"begin." Report any missing articulation, frozen-mouth interval, puppet-like
teeth/jaw, identity changes, altered body/set/framing or residual mouth motion
after singing. Sync on a few syllables alone is not success. This is a quieter
base than the expressive opening takes; do not hide that risk or automatically
spend on a fresh performance. A poor result is useful test information.

Write RECEIPT.md with job ID, actual settings/cost, input hashes, submission/
progress/ready/download times, original and synced paths/hashes, native fps,
frame counts, dimensions, durations and stream starts. List actual mouth
coverage/defects with source timestamps. Preserve manifest fields, add
claude_result and set claude_done_ready_for_codex_verification only once files
and receipt exist. On failure record the stage and reason instead.

Write ONLY under out/garden_begin_lipsync_v1/. No production edits, assembly,
FX edits, commits, purchases, other generations or retries. Tell the owner
when Codex can verify the manifest and make the same-clock preview.
