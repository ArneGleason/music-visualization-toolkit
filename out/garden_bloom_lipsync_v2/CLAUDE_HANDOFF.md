# Garden pollen bloom: fresh lip sync at the approved later picture timing

Read handoff.json. Work in its project_root. Owner now wants lip sync on the
later blooming selection, without changing that selection. This authorizes
ONE new Kling Lip Sync. NO Flow, no new stills, no automatic retries.

## Inputs and settings

Use ONLY this folder's base.mp4 and guide.wav, after verifying their hashes.
Base is the original unsynced eight-second garden footage, silently remuxed;
decoded video frames are unchanged. The guide is NEW. Do not reuse the prior
garden_begin_lipsync_v1 guide or its synced output. Do not upload the bloom
preview, any composited clean.mp4, green guide, lyrics or master soundtrack.

Kling Lip Sync, sole woman/Character1. Upload guide at0:00..0:08, Sound from
Video OFF. No additional offset, trimming silence, normalization, TTS or speed
change. Lyrics below are verification notes, not an unsupported text input.
Historical cost10 credits: verify and stop above10. Existing no-watermark
entitlement only; no purchases. If face detection fails, stop and report,
do not crop/zoom or regenerate. Prior test's quiet small face gave weak
articulation; assess this test honestly rather than assuming success.

## Exact clock: source0 = song1720, NOT1774

All frame references below are24fps, zero-based/end-exclusive, regardless of
the returned native frame rate. Full base starts at original source0, not66.

Visible song1786..1854 uses original source66..134, or2.750000..5.583333sec.
The main pollen burst at original source108 (4.5sec) lands on begin at song1828.
Do not move the picture to fit the old guide. The new guide already fits it.

| Word | Song frames | Uploaded-source seconds |
| --- | --- | --- |
| for | 1786..1797 | 2.750000..3.208333 |
| the | 1797..1807 | 3.208333..3.625000 |
| song | 1807..1819 | 3.625000..4.125000 |
| to | 1819..1828 | 4.125000..4.500000 |
| begin | 1828..1841 | 4.500000..5.041667 |
| settling tail | 1841..1854 | 5.041667..5.583333 |

Uninterrupted vocal context before/after the visible shot stays in the guide.
Do not remove it, but do not approve those other words as coverage for this
character. Check the settling tail for inappropriate continuing mouth motion.
Full take has genuine lead and exit footage, not duplicate-frame padding.
The previously rendered later bloom placement must remain exactly as above.

## Monitoring and delivery

First check after30seconds, then every20; at90%+ every10. Tool latency counts.
Percent-based estimates can shorten intervals to10..20seconds. No progressive
backoff or repeated reloads. Respect rate limits. At15minutes report state.
Download promptly once ready, before lengthy inspection. Do not resubmit for
an uncertain download.

Save untouched original_<job-id>.mp4 and byte-identical synced.mp4 here.
No trimming, retiming, crop, stabilization, interpolation or audio replacement.
Preserve returned native fps/timestamps; Codex performs time-preserving conform.
Verify all five words, especially for/song/begin, and the settling tail.
Report missing words, small mouth amplitude, puppet jaw, face changes, and any
change to framing or pollen animation. Minimum coverage5.583333seconds.

Write RECEIPT.md: job/settings/actual cost, input hashes, submit/progress/ready/
download times, file hashes, native fps/frame count/duration/stream starts,
word-level observations and defects. Preserve manifest fields; add
claude_result and set status claude_done_ready_for_codex_verification only
when media and receipt exist. Otherwise record the failure honestly.

Write only under out/garden_bloom_lipsync_v2/. No production/assembly/FX edits,
commits, purchases, other generations, or retries. Keep prior test untouched.
Codex will separately move the dancing green guide above her head and reapply
the accepted musical lighting over this returned plate. Do not do that in Kling.
