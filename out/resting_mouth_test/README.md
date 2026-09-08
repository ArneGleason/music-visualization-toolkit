# Resting-mouth lip-sync experiment

Single controlled A1-outro experiment, 2026-09-05. Production assignments remain unchanged.

## Hypothesis

A non-speaking performance plate may yield a more convincing resting mouth in Kling's silent intervals than the existing actively mouthing plate. This tests observed behavior, not a claim about model internals.

## Inputs and clock

- Approved frame: `codex/out/duet_lamplight_astronomer_sync_b.jpg`.
- One Flow Veo 3.1 Quality, Frames, 16:9, 720p, eight seconds, x1. UI quote: 100 credits. Submitted via the owner's signed-in Chrome session.
- New plate direction: relaxed closed lips after the initial quarter-second closure, no talking or singing throughout; alert, cool, self-possessed listening with restrained head/shoulder acting. Same character and room, locked camera. Full unchanged style lock appended.
- Song origin: frame 4165 / 24 = 173.541666667 seconds.
- Existing speaker-gated guide `clips/inbox/guide_A1.wav` is shifted later by 0.178348 seconds to repair the measured stem/master offset. Round to the nearest audio sample, retain exactly eight seconds. The original guide's silent tail allows this without cutting the selected phrases.
- This preserves the prior speaker isolation while correcting its clock. It does not establish that the old phrase gates are creatively optimal.
- Main silent listening check: approximately 2.08 to 3.68 seconds in the corrected guide. Check actual samples before interpreting the result.
- Beginning contains genuine generated movement, not held-head frames. The approved still starts with parted lips, so judge whether it settles before the first vocal onset.

## Acceptance

Inspect base and synced versions at entry, within voiced words, internal listening silence and end. Verify downloaded guide alignment, preserve video duration when converting frame rate, and use the same song origin for the master-mux preview. Never shift a correctly aligned take merely to disguise unwanted mouth motion in silence.

## Result and resume point

- First Flow attempt failed audio generation; UI explicitly said no charge. Enabled Return silent videos and retried once. Returned the preference to its original OFF state after success.
- Successful Flow asset: `27f78d02-d4c8-45bd-aae2-486e0fafb6a8`, titled Woman listening in 1950s room. Full prompt remains in its details.
- Download `Woman_listening_in_1950s_room_202609052147.mp4` copied to `base.mp4`. Verified 192 frames, 24 fps, eight seconds; also contains an audio stream, so discard that scratch audio for any master preview.
- `base_contact.jpg` samples the eight seconds. The mouth remains parted substantially longer than the requested quarter second, then settles closed around the middle and stays closed in later sampled frames. Do not call this a fully compliant neutral-mouth plate. It can still test whether Kling animates the later words from a closed pose and returns to rest afterward, but the opening remains a confound.
- `guide_A1_aligned.wav`: exactly 384000 mono samples at 48 kHz. Verified sample equality to the original guide after a delay of 8561 samples (0.178354167 s); 2.1..3.6 seconds is exactly zero. No stretching.
- Kling file-chooser upload returned Not allowed. No Kling job submitted and no Kling credits spent. Browser troubleshooting requires the owner to enable Allow access to file URLs in the ChatGPT Chrome extension details before resuming upload.
- Resume by uploading `base.mp4` and `guide_A1_aligned.wav` to Kling Lip Sync. Check current quoted credit cost. Download and compare base/synced silent intervals; retain song origin 4165/24 for master preview. Do not regenerate the base automatically.

## Upload permission resolved

Owner enabled file-URL access. Both files uploaded successfully. Audio upload works through the exact visible `Click / Drop / Paste` label, not the surrounding description or hidden input. Full guide placed at clip time zero, eight seconds, original video sound OFF. Submitted one Kling Lip Sync job at the final quoted cost of 10 credits. Awaiting result; no duplicate submission.

## Kling result

Kling showed 1/1 Generated. Balance changed from 516 to 506, confirming the 10-credit charge. Latest result thumbnail matches the uploaded astronomer/television plate. The download control navigated to Kling's CDN (`v15-kling.klingai.com`), where Chrome displayed: This page has been blocked by Chrome, ERR_BLOCKED_BY_CLIENT. No new local download appeared. Do not generate again or claim audio/visual QA completed.

Resume: obtain the completed latest Kling result through the normal browser download once the owner resolves the Chrome block, save as `out/resting_mouth_test/synced.mp4`, then run `python out/resting_mouth_test/review.py`. That script checks embedded-guide alignment and renders side-by-side, master and shared-assembler previews without changing production assignments. It has not yet run against a result.

## Completed review delivery

Owner downloaded `kling_20260906_Lip_Sync__2520_0.mp4`; copied unchanged to `synced.mp4`. This download has a visible Kling watermark, so it is a test asset, not a clean final.

`review.py` completed. Embedded audio correlates 0.998901 with the uploaded guide at zero lag; the best lag in the +/-50 ms check is zero. Embedded samples at 2.1..3.6 s are exactly silent. The downloaded audio ends at 7.8948 s, earlier than the eight-second guide; do not count the absent tail as complete coverage. Picture is timestamp-conformed to 24 fps, not slowed down.

- `comparison_guide.mp4`: base left, Kling right, isolated guide audio. Use this to judge speech/rest behavior across the whole take.
- `master_preview.mp4`: continuous new take with master music at song origin 4165/24. Other-speaker vocals remain in the master while this character listens.
- `assembly_preview.mp4`: actual shared Blender assembler, shots o02/o03/o04, 154 frames at 24 fps, with existing lyrics and master. New A1 used for o02/o04; existing B1 for o03 retains the previously tested stem-clock correction. No production EDL edits.
- Both principal previews decode cleanly. Assembly audio and video start at zero; duration 6.4167 seconds. Production EDL hash remained unchanged.

Sampled visual evidence: later voiced portions show mouth changes against the base's closed pose, and the last sampled frames return to closed lips. Internal listening silence still contains partly open mouth poses also present in the base. This supports separating source-performance quality from timeline placement, but does not prove model internals or establish perceptually perfect phoneme sync. Owner playback review is still required. A truly closed/resting starting reference remains a candidate for a later entrance test; no further paid generation authorized or launched by this review.

Status: test and review previews delivered; awaiting owner judgment. Production unchanged.
