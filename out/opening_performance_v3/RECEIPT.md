# RECEIPT: opening_performance_v3_s003

Status: DONE. One Flow take, one Kling pass. Only out/opening_performance_v3/ was written; v1 and v2 untouched;
no shotlist, style, FX, timing or audio-master edits; no commit.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/astronomer_desk_sync_b.jpg`: 24D2794A65E01BA10526249C190A5B576B459D2D7B654BB2CDD3ACA59F503FCB
- guide `out/opening_sync_test/guide.wav`: 63B9B6C2F67F83581ECC43764696EB798018BA65BF7FAD16B15FBBE2A418C41B (48 kHz mono 8.000 s; used as-is, no re-extraction, no offset, no speed change)
- prompt `flow_prompt.txt` (4447 chars, includes style_lock_v2) pasted verbatim, once; no old lock, no listening prompt, no second reference.

## Flow (actual)
- Project "Rivers of Mars - AI video". Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1,
  "Generating will use 100 credits"; composer chip 720p. Start frame only (asset `astronomer_desk_sync_b.jpg`, slot id df5e41be).
- Submitted once at 2026-09-06T03:10:47Z (2026-09-05 23:10:47 local). Rendered by 03:12:40Z. No retry.
- Result media id 674ecc19-6b11-4f25-8865-cc4210eda681 (Flow caption begins "Astronomer singing in re..."). Downloaded through the
  tile's signed flow-content video URL (the labs.google redirect endpoint was still failing tonight).
- Files: `original_674ecc19-6b11-4f25-8865-cc4210eda681.mp4` (untouched) and `base.mp4` (byte-identical), SHA-256 225E9FBA2276A20E6BB8ECCE3E760D4D4D4B41C20660F648EA910D2C4386EA99
- ffprobe base.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; disposable Veo audio track present.
- First frame vs approved still: mean pixel difference 1.0 (64x36 downscale).
- Cost: 100 Flow credits (as quoted).

## Base inspection (base_contact.jpg at 0.5 s steps; base_interior_2.6-5.4.jpg at 0.2 s steps, face crop)
- Tempo/movement: grounded. No head-bobbing or double-time bounce; one measured forward inclination begins ~3.2 s and settles by
  ~4.4 s (the requested ~3.39 s anchor); hands stay on the desk below the face; a low hand accent ~6.0-6.5 s; eyes drop at ~7.9 s.
- Lead-in 0.00-0.50 s: real generated motion; mouth active by 0.25 s; a direct open "Hey"-shaped vowel at ~0.5 s.
- Singing coverage: active with changing vowel shapes 0.25-3.0 s (the stretch v1 missed) and 4.6-7.5 s.
  GAP: 3.2-4.4 s the lean is played as a closed-lipped smile (about 1.2 s inside "I need you for something"), so the base does
  not sing through that interior. Reported as a limitation; judged not "silent/stiff" overall, so Kling was run.
- Expression: brow and cheek activity, fleeting smile ~3.0 s, firmer gaze ~5.0-6.0 s; no mugging, no perpetual grin.
- Identity, updo, wardrobe, desk, telescope, empty suit, Mars backdrop held for 8 s; locked frame; no cut, no dissolve, no new characters; mouth never obstructed.
- Verdict: suitable with the noted 3.2-4.4 s gap.

## Kling (actual)
- Lip Sync, Standard plan. Balance 496 before, 486 after (10 credits, as quoted).
- base.mp4 uploaded unchanged; existing guide.wav via "Upload Local Dubbing"; Character 1 (only detected face); speech placed at
  0:00 covering 0:00-0:08; "Sound from Video" OFF (verified); no TTS; one submit at 2026-09-06T03:15:35Z (23:15:35 local). Task id 2872.
- Download via the normal card control (Video > MP4). The account's "Without Watermark" plan switch was already ON and was not touched;
  corner crop of the result shows no watermark. No protections disabled, no upgrades.
- Files: `original_kling_20260906_Lip_Sync__2872_0.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256 971BA8734AF38414B91BFEAF9909F2A257F57AFA4596850BC7D7FF95901DA26D
- ffprobe synced.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, 30/1, 239 video frames, video 7.9667 s, audio 7.895 s, start 0.000. SHORTER than 8.000 s (reported, not padded);
  30 fps retained for Codex's timestamp conform.
- Audio clock: normalized cross-correlation of synced.mp4 audio vs guide.wav = 1.006 at lag 0 (best over +/-0.1 s is 0.0000 s).

## Synced inspection (synced_contact.jpg)
- Kling supplies mouth articulation through the whole voiced span including the base's 3.2-4.4 s closed-lip lean
  (frames at 3.5 and 4.0 s now show open vowel shapes); the grounded body motion and expression of the base are preserved.
- Not judged: perceptual phoneme accuracy, entry/tail feel; owner review.

## Not done
- No retries, no second take, no assembly, no production assignment change (s003 still on the earlier Kling clip), no commit.
