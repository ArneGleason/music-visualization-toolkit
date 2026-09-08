# RECEIPT: shop_wide_lipsync_v1

Status: DONE - one Kling Lip Sync on the wide shop take, downloaded untouched and inspected frame by frame over source 0.3-2.3 s
plus the tail. Result is USABLE for the approved wide window: "No" opens clearly at ~0.57 s and "Don't make it better" gets
distinct openings through 2.17 s; reflection, alien head, identity and camera are unchanged. Articulation is moderate on this
~110 px face (details below). No Flow, no close-up processing, no retry, no assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: 9db1c6c112424d0f301fce9b900fc7ae2403e19d8c7297be3fdb4b5819cde7ef (1280x720, 24/1, 192 frames, 8.000 s, no audio; remux of shop_performance_v1/wide)
- guide `guide.wav`: f497d6e98e9f5283b4e815338cf3fffcea73a6c87308590d85de5efa96174439 (48 kHz mono PCM16, 8.000 s). Uploaded unchanged at 0:00; no offset, trim, gain, TTS.
  The close-up take was NOT uploaded or touched.

## Kling (actual, times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded. Kling detected TWO faces:
  Character 1 = the real woman (thumbnail of her face), Character 2 = the alien souvenir head. Character 1 was the selected
  character (green outline) and the only lane that received speech; Character 2 received nothing.
- Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead at 0:00 -> Add Speech -> block spans 0:00-0:08 on the Character 1
  lane. Sound from Video OFF. Generate quoted 10 credits.
- Submitted 19:02:24. Balance 446 -> 436 (10 credits). Checks: 19:02:54 queueing/creating; 19:03:14; 19:03:34; 19:04:10;
  19:04:30; 19:04:50; 19:05:10 (creating); 19:05:30 "1/1 Generated". Download (Video, MP4, Without Watermark ON, existing
  entitlement) clicked 19:06:10; file present and copied 19:06:54. About 3 min 6 s submit -> generated. No reloads/resubmits.
- Job id 774 (download name kling_20260907_Lip_Sync__774_0.mp4). Files: `original_774.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 1b0c12830a3196c9f3e13a1f40dbb521296e4b2bb9ab21f090b53f07e84cea45
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not trimmed/retimed/cropped. Coverage 7.967 s >= required 2.083 s (target phrase) and 1.833 s (visible wide). Codex conforms
  30 -> 24 fps by timestamps.
- Audio check: normalized cross-correlation of returned audio vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base (per native frame, luminance mean abs diff): whole frame mean 3.0 / max 5.4; window reflection
  region mean 2.9 / max 5.1; alien head region mean 3.1 / max 5.5; lower display mean 3.2 / max 6.4 - all at encoder-noise level,
  so the reflection and the souvenir head were NOT animated and the camera/framing is unchanged. Her face region: mean 5.2,
  max 14.1 at 2.17 s; mouth box max 17.4 - the only region Kling altered.

## Word-level inspection (mouth_synced_src0.3-2.3s_native30_everyframe.jpg = native frames 9-68, every frame, 12 per row;
   mouth_base_src0.3-2.3s_every3.jpg = base, closed mouth throughout; mouth_synced_src2.2-8s_every6.jpg = tail)
Native frame = source seconds x 30. Base lips are closed for the whole take, so every opening below is Kling's.
- 0.1-0.3 s (f3-9): lips part/open briefly - this follows the guide's preceding vocal context (guide has energy 0-0.25 s); it
  is BEFORE the visible in-point at source 12 (0.5 s) and therefore not shown.
- 0.33-0.53 s (f10-16): mouth closed while her eyes close for the base head dip.
- No. (0.500-1.000 s, f15-30): OK. Mouth opens at f17 (~0.57 s) into a clear rounded "O", held open through f20-32
  (0.67-1.07 s), then closes. Onset lands ~2 frames after the word start; readable as a sung "No".
- Don't make it better (1.000-2.083 s, f30-62): OK/moderate. Mouth closes ~1.07 s; small opening at f36-37 (1.20-1.23 s,
  "Don't"); opening f40-44 (1.33-1.47 s, "make"); closed f45; open f46-49 (1.53-1.63 s, "it"); closed f50-55; open f56-60
  (1.87-2.00 s, "bet-"); open with teeth f61-65 (2.03-2.17 s, "-ter"); closing f66-68 (2.20-2.27 s). Consonant closures are
  present; amplitude is moderate, never a wide jaw drop, no teeth-heavy grimace. The head turn toward the viewer at 1.3-1.6 s
  from the base is preserved under the mouth motion.
- Through source frame 50 (2.08 s, native f62): the last syllable of "better" is still open at 2.03-2.17 s, so the phrase
  completes just past the target end; the visible wide window [12,44) (0.5-1.83 s) covers "No" and "Don't make it" fully and
  "bet-" begins at 1.87 s (frame 45), i.e. on the close-up side of the switch. Consistent with the handoff's guard.
- Tail (2.2-8.0 s): mouth opens again 2.2-2.4 s and lightly around 4.2-5.0 s and 6.0-6.7 s, following the guide's later vocal
  context (guide energy 4.0-5.5 s). Not approved coverage; the wide is not to be extended.
- Identity/teeth: same face, natural warm teeth on "-ter", no puppet jaw, no frozen interval inside the phrase.

## Not done
- No Flow, no close-up Kling pass, no retry, no assembly, no FX baking, no production/cue edits, no commit, no purchase,
  no owner approval claimed.
