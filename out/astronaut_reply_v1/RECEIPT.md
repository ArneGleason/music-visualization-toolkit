# RECEIPT: astronaut_reply_v1

Status: DONE. One Flow take, one Kling pass; both files on disk. Writes only under out/astronaut_reply_v1/.
No production, cue, shotlist, assembly or Git changes. No retries, no later shots.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/astronaut_close_sync_a.jpg`: 85C55DC768EC12BF041AB194749412A25F127926C68B64F80C9D8E38BBA7BF34 (approved still, unedited; Start slot only, End empty)
- guide `guide.wav`: 49DDFA2494EC1ADFAFCD12C5303623CFFB742386E8957C79D9A1B5C276051E5C (48 kHz mono 8.000 s; used exactly as supplied, no offset/trim/gate/speed change)
- prompt `flow_prompt.txt`: 255D81717C834629F204A9F3CB4E788E82FDF465F7B113552CB1B541654E1EB7 (4274 chars incl. the lock) pasted verbatim once; lock: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496

## Flow (actual, times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, "Generating will use 100 credits"; chip 720p.
  Start = `astronaut_close_sync_a.jpg` (slot id bc55d662).
- Submitted 12:59:58. Displayed progress: 13:00:08 3%; 13:00:42 33%; 13:01:00 48%; 13:01:18 no percentage (complete); confirmed
  ready 13:01:53 (tile video URL available); download 13:02:14. Generation about 80 s. Checks at 10 s, 44 s, then every ~18-20 s.
- Result media id a2494344-5854-41c5-ba4a-45a4f77647ca (Flow caption "Astronaut singing on Mars settle..."); downloaded via the
  tile's signed flow-content video URL. Files: `original_a2494344-5854-41c5-ba4a-45a4f77647ca.mp4` (untouched) and `base.mp4`
  (byte-identical), SHA-256 A9B4CB462212AE39E789FFD1E85EAEAF4B7D4931E2308A6085155B75BA0E6FFB
- ffprobe base.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; disposable Veo audio present. No watermark. Cost 100 credits as quoted.
- First frame vs approved still: mean pixel difference 0.8 (64x36).

## Base inspection (base_contact_every6.jpg; face crops base_mouth_0.75-3.2s_every3.jpg, base_mouth_3.0-5.6s_every3.jpg, base_mouth_5.5-8s_every4.jpg)
- Identity (red curls, freckles), silver suit with collar ring, Mars river settlement and planets: held for all 192 frames. No helmet,
  no extra characters, no set change, no cut or dissolve. Camera locked; she leans slightly toward the lens over the take (face a
  little larger by 7 s), which is performance movement, not a camera move. Mouth unobstructed throughout.
- Lead-in 0.00-0.88 s: real motion, mouth already forming a vowel by 0.25 s (she starts early, no frozen pickup).
- "I don't see anything" (0.88-3.00): articulated vowels 0.75-1.4 s and 2.5-3.1 s; 1.5-2.4 s is a held toothy smile (lips parted,
  teeth showing, little jaw change; eyes close briefly at 2.25 s). Not a closed-mouth gap, but ~0.9 s without articulation.
- "Think you forgot to attach it" (3.00-5.46): articulated 3.0-4.1 s; 4.25-5.25 s another held grin (~1.0 s); open vowel 5.25-5.5 s.
- Spare tail "If you've got it, give it" (5.46-7.63): articulated 5.5-6.4 s; grin hold 6.5-6.8 s; small mouth motion 7.0-7.3 s;
  closed smile 7.5-8.0 s (natural breath).
- Expression: eyebrow lift and smiling eyes present; the smile is more constant than the prompt asked ("no constant smile").
- Verdict: suitable; the two grin holds are open-mouth, so Kling had a visible mouth to drive. Sent to Kling.

## Kling (actual, UTC)
- Lip Sync, Standard plan. Balance 476 before, 466 after (10 credits, as quoted). base.mp4 uploaded unchanged (editor ready 13:03:56);
  this folder's guide.wav via "Upload Local Dubbing"; Character 1 (only detected face); speech placed at 0:00 covering 0:00-0:08;
  "Sound from Video" OFF (verified); no TTS.
- Submitted ~13:04:53 (Generate click; the "Task submitted" toast had cleared by the 13:04:59 read; credit drop confirmed 13:06:39).
  Status "Queueing" at 13:05:23, :41, :59, 13:06:39, :57, 13:07:15, :33, :51; result present at 13:08:29 (about 3.6 min).
  Checks every ~18-20 s as instructed; no reloads, no resubmission. Download clicked 13:09:44; file landed by 13:10:05.
- Task id 5392 (download filename). Download via the normal card control (Video > MP4); the account's existing "Without Watermark"
  switch was already ON and untouched; corner crop shows no watermark. No protections disabled.
- Files: `original_kling_20260906_Lip_Sync__5392_0.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256 DA5A90AAA59B6FFA94C26517C34AD9F3EEB3A0EC8BF66A9C4D59968D7D2EE3EF
- ffprobe synced.mp4: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, 30/1, 239 video frames, video 7.9667 s, audio 7.895 s, start 0.000. Shorter than 8.000 s (reported, not padded);
  30 fps retained for Codex's timestamp conform. Required picture end 5.4583 s is covered with ~2.5 s of real tail.
- Audio clock: normalized cross-correlation of synced.mp4 audio vs guide.wav = 0.997 at lag 0 (best over +/-0.1 s is 0.0000 s).

## Synced inspection (synced_mouth_contact.jpg, face crop every 0.5 s)
- Kling articulates through both visible phrases including the base's grin holds (frames at 1.5-2.5 s and 4.5-5.5 s now show
  changing mouth shapes) and through the spare tail to ~7.0 s; closed smile after ~7.3 s. Identity and background preserved.
- Not judged: phoneme accuracy and feel; owner review.

## Weaknesses
- Smiles more than directed; two ~1 s grin holds in the base (Kling covers them, but the cheeks stay in smile position).
- Slight lean-in growth of the face over the take.
- Not done: no assembly, no cue/shotlist edits, no later shots, no commit.
