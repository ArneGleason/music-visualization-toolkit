# RECEIPT: opening_performance_v2_s003

Status: DONE. One Flow take, one Kling pass. Nothing outside out/opening_performance_v2/ was changed;
no shotlist, style, FX, timing or audio-master edits; no commit.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/astronomer_desk_sync_b.jpg`: 24D2794A65E01BA10526249C190A5B576B459D2D7B654BB2CDD3ACA59F503FCB
- guide `out/opening_sync_test/guide.wav`: 63B9B6C2F67F83581ECC43764696EB798018BA65BF7FAD16B15FBBE2A418C41B (48 kHz mono 8.000 s; used as-is, no re-extraction, no offset)
- prompt `flow_prompt.txt` pasted verbatim, once (includes style_lock_v2; the old lock and the old listening prompt were NOT appended)

## Flow (actual)
- Project "Rivers of Mars - AI video". Settings read from the Settings panel before submit: Video, Frames, 16:9,
  "Veo 3.1 - Quality", 8s, x1, "Generating will use 100 credits"; composer chip 720p. No End frame, no second reference.
- Start frame: asset `astronomer_desk_sync_b.jpg` (slot thumbnail id df5e41be = the earlier upload of the approved still).
- Submitted once at 2026-09-06T02:40:27Z (2026-09-05 22:40:27 local). Flow showed a "high demand" banner; the take completed normally.
- Result media id c3f5bc0e-6ec8-45fc-ae4b-537c278cfe87 (Flow caption "Astronomer singing to camera").
  Downloaded via the tile's own signed flow-content video URL (labs.google media.getMediaUrlRedirect answered "Internal Error" at the time).
- Files: `original_c3f5bc0e-6ec8-45fc-ae4b-537c278cfe87.mp4` (untouched) and `base.mp4` (byte-identical copy),
  SHA-256 CB489EAC672A135A98DA720D10AA656C530B17BE2BD3C23CA8392F430AD938E1
- ffprobe base.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; a Veo audio track is present (disposable).
- First frame vs approved still: mean pixel difference 1.0 (64x36 downscale), i.e. the approved composition.
- Cost: 100 Flow credits (matches quote).

## Base inspection (base_contact.jpg, 18 frames)
- Lead-in 0.00-0.50 s is generated motion (breath and pickup); mouth active by 0.25 s.
- 1.0-3.0 s: continuous singing, changing vowel shapes, jaw movement, no closed-mouth hold.
- Expression: brow lifts, crooked smile (~1.5-2.5 s, ~5.5-6.5 s), cheeks active, assured lean; head predominantly frontal.
- Hands: rhythmic shoulder motion, small accents below face level, one raised finger ~6.0-6.5 s; mouth never obstructed.
- Identity, updo, wardrobe, desk, telescope, empty silver suit, Mars backdrop held throughout; no cut, no new characters, no dissolve.
- Verdict: suitable; sent to Kling.

## Kling (actual)
- Lip Sync tool, Standard plan. Balance before 506, after 496 (10 credits, matches quote).
- Video: base.mp4 uploaded unchanged. Audio: existing guide.wav via "Upload Local Dubbing", Character 1 (the only detected face),
  speech block placed at 0:00 covering 0:00-0:08. "Sound from Video" switch OFF (default; verified visually). No TTS, no speed change.
- Submitted once at 2026-09-06T02:50:57Z (22:50:57 local). Job/task id 2765 (from the download filename); no separate share link captured.
- Download: normal card download control, Video > MP4. The account's "Without Watermark" (plan feature) switch in that menu was already ON
  and was not touched; the result carries no visible watermark (corner crop inspected). No other protection was disabled.
- Files: `original_kling_20260906_Lip_Sync__2765_0.mp4` (untouched) and `synced.mp4` (byte-identical copy),
  SHA-256 532A5B6724FD1E5CC01EF8170808F870C148F277F7A52F65AEA9F09E0F4969CA
- ffprobe synced.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, 30/1, 239 video frames, video 7.9667 s, audio 7.895 s, start 0.000. SHORTER THAN 8.000 s (reported, not padded;
  Kling returned 30 fps as with every earlier job; Codex to timestamp-conform to 24 fps).
- Audio clock check: normalized cross-correlation of synced.mp4 audio vs guide.wav = 1.006 at lag 0 samples (best over +/-0.1 s is lag 0),
  so the guide sits at source time zero with no shift.

## Synced inspection (synced_contact.jpg, 17 frames)
- Mouth articulates through 0.5-3.0 s and again 3.5-5.5 s and 6.5-7.5 s; between-phrase moments read as breaths, not a frozen face.
- The base take's expression, hand accents and identity survive the sync; no new artifacts seen at contact-sheet scale.
- Not judged here: perceptual phoneme accuracy and the exact entry/tail; owner review.

## Not done / notes
- No retries, no regeneration, no second take, no assembly. Production assignment of s003 unchanged (still the earlier Kling clip).
- The extra Veo audio in base.mp4 is left in place (disposable, per prompt); synced.mp4 audio is the guide as Kling embedded it.
