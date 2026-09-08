# RECEIPT: lipsync_review_followup_v1 / opening

Status: DONE - one fresh Kling Lip Sync on the ORIGINAL slower opening performance (opening_performance_v3 base, silent remux;
its video stream is bit-identical to the source), downloaded untouched and inspected every 2nd native frame across the take.
Result is USABLE and natural: generous, varied articulation with natural teeth on both phrases, no puppet jaw, identity and
framing unchanged. Caveats: the mouth closes into a smile for ~3.4-4.0 s while the guide still carries energy (possible
missed sustain inside "something"), and the base's smiling open mouth persists through the guide's silence at 1.0-1.5 s.
No Flow, no retry, no assembly, no production edits, no commit. The old synced take is untouched.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: f08ace1f47eb9b43064ec280a26c2788be75163a4e5a01cf70b956f2af03edb1 (1280x720, 24/1, 192 frames, 8.000 s, no audio; video md5 identical to
  out/opening_performance_v3/base.mp4)
- guide `guide.wav`: 63b9b6c2f67f83581ecc43764696eb798018ba65bf7fad16b15fbbe2a418c41b (48 kHz mono PCM16, 8.000 s), uploaded unchanged at 0:00.

## Kling (times UTC; local = UTC-4)
- Kling Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded from a fresh editor page; one
  face detected (Character 1 = the woman, sole character). Upload Local Dubbing -> guide.wav (shown 0:00-0:08) -> playhead at
  0:00 -> Add Speech -> speech block spans 0:00-0:08 on the Character 1 lane. Sound from Video OFF. Generate quoted 10 credits.
  No offset, trim, TTS, normalization or crop. Download: Video, MP4, "Without Watermark" ON (existing entitlement).
- Submitted 20:55:08; "Task submitted / 0/1 Generating" and balance 426 -> 416 at 20:55:13. Checks 20:57:07, 20:57:38, 20:57:58
  (creating); 20:58:28 badge "1/2 Generating" = first of the two jobs done (this one; Kling's card time 4:55:12 PM local);
  both done by 20:59:49. Download clicked 21:00:32; file present and copied 21:01:50. About 3 min 20 s. No reloads/resubmits.
- Job id 1235 (download name kling_20260907_Lip_Sync__1235_0.mp4). Files: `original_1235.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 d897149596862338c7de7d66203728be5e3d2d9ab84b7af22f69dfcfa2db6355
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Coverage 7.967 s covers source 12..191 (0.5-7.96 s). Codex conforms 30 -> 24 fps by timestamps.
- Audio: normalized cross-correlation vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base (per native frame): background corner mean 2.5 / max 3.3 (noise), face region mean 5.6 / max 15.3,
  mouth box mean 9.5 / max 24.3 - only the lower face is re-rendered; framing, set, costume, hair unchanged; identity consistent.

## Word-level inspection (mouth_synced_src0.4-7.87s_native30_every2.jpg = native frames 12-234 every 2, 14 per row;
   mouth_base_src0.4-7.87s_every8.jpg; frame-to-frame mouth-motion trace)
Guide energy: silent 0-0.25 s; "Hey" 0.5-1.0 s; near-silent 1.0-1.5 s; continuous vocal 1.5-7.9 s.
- 0.4-1.0 s "Hey": wide open smiling mouth with upper teeth - reads as a sung "Hey" (the base already opens into a smile here).
- 1.0-1.5 s (guide silent): the mouth stays in the base's open smile rather than closing - held smile, not a missed word.
- 1.5-3.4 s "I need you for some-": clearly changing shapes - open, rounded, narrowed, brief closures; motion 5-21 per frame
  pair. Natural jaw opening, teeth warm.
- 3.4-4.0 s: mouth closes into a closed-lip smile while the guide still has energy (RMS ~2800 at 3.5-3.75 s). Possible missed
  sustain / held consonant inside "something". Flag for audition.
- 4.1-5.9 s: open singing resumes with big open vowels 4.5-4.9 s and varied shapes to 5.9 s (phrase 1 ends 5.875).
- 5.9-7.1 s "It's important": open "O" vowels 6.3-6.7 s held open (sustain), narrowing to 7.1 s. Consonant closures present.
- 7.1-7.8 s: mouth mostly closed/small while the guide's tail continues; eyes close and the head dips (base behaviour) 7.5-7.8.
  Reads as the line finishing slightly early.
- No puppet mouth, no distorted or bleached teeth, no face change, no timing drift (loud guide moments coincide with the widest
  shapes). Phrase starts: "Hey" ~0.45 s; phrase 2 onset ~5.9 s.

## Defects (summary)
- Closed-lip smile 3.4-4.0 s during a voiced part of the guide (possible missed sustain).
- Held open smile during the guide's 1.0-1.5 s silence (from the base performance).
- Mouth closes ~7.1 s while the guide tail runs to ~7.8 s.

## Not done
- No Flow, no retry, no assembly, no cut changes, no production edits, no commit, no purchase, no owner approval claimed.
