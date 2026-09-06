# RECEIPT: pieces_performance_v1

Status: DONE. One Flow take, one Kling pass; both files on disk. Writes only under out/pieces_performance_v1/.
No production, cue, shotlist, assembly or Git changes. No retries, no specimen generation.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/astronomer_close_sync_b.jpg`: BEB0A3EA59495CFC33935C9520BA1B8C6D4796318A00D2A6D44B4C680B6F5FD3
- guide `out/pieces_performance_v1/guide.wav`: DEBC0DA4CAD19239DEE67B27F7E4A9426B20205B95037C929D84A4BDB187B037 (48 kHz mono, 8.000 s; used exactly as supplied, no offset, no trim, no speed change)
- lock `style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496; prompt `flow_prompt.txt` (4073 chars incl. the lock) pasted verbatim once.

## Flow (actual)
- Project "Rivers of Mars - AI video". Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1,
  "Generating will use 100 credits"; composer chip 720p. Start slot = `astronomer_close_sync_b.jpg` (slot id 5e9ffd61); End slot verified EMPTY.
- Submitted once at 2026-09-06T03:54:09Z (2026-09-05 23:54:09 local); rendered by 03:56:21Z. Cost 100 Flow credits as quoted.
- Result media id f912fbd2-467a-4780-94fd-5355d8ef6679 (Flow caption "Woman singing performance on Mars"); downloaded via the tile's
  signed flow-content video URL. Files: `original_f912fbd2-467a-4780-94fd-5355d8ef6679.mp4` (untouched) and `base.mp4` (byte-identical),
  SHA-256 434FA54AF26FE808ED355833540CA895B30BB0EE02002F65B71F4B377A58A86C
- ffprobe base.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; disposable Veo audio present. No watermark.
- First frame vs approved still: mean pixel difference 0.9 (64x36). Per-6-frame difference against frame 0 stays 2-7 for the whole
  take (no scene change; the earlier O1 take from this still had gone to 30+ when it dissolved).

## Base inspection (base_contact_every6.jpg; base_mouth_1.0-4.9s_every4.jpg and base_mouth_5.25-7.4s_every3.jpg are face crops)
- Identity, freckles, updo, tweed/vest, warm plain backdrop, close framing: held for all 192 frames; locked camera; no cut, no new set.
- Lead-in 0.00-1.0 s: real motion (breath, small settle), mouth already moving by 0.25 s.
- Phrase 1 window (1.17-4.75 s): visible singing with changing vowels and upper teeth 1.0-3.2 s and 3.8-4.9 s; one brief closed-lip
  moment 3.3-3.8 s (~0.5 s). Gaze drops downward ~3.8-4.5 s (reads as the "pleasure at the discovery" beat, eyes off lens).
- Breath 4.75-5.50 s: mouth softens, then a wide open vowel arrives ~5.25 s (slightly early).
- Phrase 2 window (5.50-7.08 s): active singing 5.25-6.75 s with a small brow lift around 6.0-6.4 s ("almost"); from ~6.9 s she
  closes and lowers her gaze into the listening breath, about 0.2 s before the written 7.08.
- 7.08-8.0 s: thoughtful stillness, eyes down, no extra words.
- Movement character: grounded, no bobbing, one slow shoulder/head settle; frontal enough for sync throughout; mouth never obstructed.
- Verdict: suitable; sent to Kling.

## Kling (actual)
- Lip Sync, Standard plan. Balance 486 before, 476 after (10 credits, as quoted).
- base.mp4 uploaded unchanged; this folder's guide.wav via "Upload Local Dubbing"; Character 1 (only detected face); speech placed
  at 0:00 covering 0:00-0:08; "Sound from Video" OFF (verified); no TTS. Submitted once at 2026-09-06T03:59:36Z (23:59:36 local).
  Task id 3048 (from the download filename).
- Download via the normal card control (Video > MP4); the account's "Without Watermark" plan switch was already ON (existing option,
  no purchase) and was not touched; corner crop shows no watermark. No protections disabled.
- Files: `original_kling_20260906_Lip_Sync__3048_0.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256 020381A7D4CBA87F9D9295F7DBDB6EAB3469584B950C77488E2841E56764C48B
- ffprobe synced.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, 30/1, 239 video frames, video 7.9667 s, audio 7.895 s, start 0.000. Shorter than 8.000 s (reported, not padded);
  30 fps retained for Codex's timestamp conform. Required picture end 7.5833 s is covered; exit handle ~0.38 s.
- Audio clock: normalized cross-correlation of synced.mp4 audio vs guide.wav = 1.005 at lag 0 (best over +/-0.1 s is 0.0000 s).

## Synced inspection (synced_contact.jpg)
- Mouth articulates through both phrase windows including the base's 3.3-3.8 s closure; listening stillness after ~7.0 s; identity,
  backdrop and the base's grounded body motion preserved. Not judged: phoneme accuracy and beat feel; owner review.

## Weaknesses
- Eyes drop off the lens twice (~3.8-4.5 s and from ~6.9 s); the second is the intended thoughtful tail, the first may read as shy.
- Phrase 2 vowel arrives ~0.25 s before the guide's 5.50 s; harmless after sync.
- Not done: no continuation, no assembly, no cue/shotlist edits, no commit.
