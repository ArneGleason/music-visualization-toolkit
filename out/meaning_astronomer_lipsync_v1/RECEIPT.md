# RECEIPT: meaning_astronomer_lipsync_v1

Status: DONE - one Kling Lip Sync on the astronomer push-in plate (owner-authorized audition: the astronomer sings "Words leave
words"), downloaded untouched and inspected every native frame over source 1.5-4.7 s plus lead and tail. Result is PARTIAL:
the first "Words" (1.6-2.6 s) and the final "words" (4.17-4.7 s) are articulated; "leave" (2.75-3.3 s) is NOT visibly
articulated - the lips stay closed while the base performance looks down at the desk. Camera push, gaze, hand move, costume,
empty suit and background are preserved. No Flow, no retry, no assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: 355e271a0dc845cfe8ab3f9a3920f894abfe635363f6fe0c9464e8954f193d0d (1280x720, 24/1, 192 frames, 8.000 s, no audio; video stream md5-identical to
  out/meaning_exchange_handoff_v1/astronomer/base.mp4, which also matches its recorded hash)
- guide `guide.wav`: 121b19471d809c28c1f0cdcb13ad6b9981462c11a5f5bbd4b385ba62a715ca8c (48 kHz mono PCM16, 8.000 s), uploaded unchanged at 0:00; no offset, trim, gain, TTS.
  Guide energy (RMS per 0.25 s): context 0-0.75 s (loud at 0.5-0.75), "Words" 1.75-2.5 s moderate, "leave" 2.75-3.25 s loud
  (1973/2348), 3.25-3.5 s 920, quiet 3.5-4.25 s, "words" 4.25-4.75 s (669 then 1560 at 4.5-4.75), quiet 4.75-6.5 s, context
  6.5-7.0 s.

## Kling (times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded from a fresh editor page (upload took
  ~35 s). Kling detected ONE face: Character 1 = the astronomer; the empty spacesuit on its stand was not detected as a
  character, so nothing could be assigned to it. Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead 0:00 -> Add Speech
  -> block spans 0:00-0:08 on the Character 1 lane. Sound from Video OFF (verified by zoom). Generate quoted 10 credits.
- Submitted 01:26:10; "Task submitted / 0/1 Generating" 01:26:15, balance 411 -> 401. Checks 01:26:40, 01:27:11, 01:27:31,
  01:27:51, 01:28:22, 01:28:42, 01:29:02 (creating); 01:29:34 "1/1 Generated". Download (Video, MP4, Without Watermark ON,
  existing entitlement) clicked 01:30:36; file present and copied 01:31:22. About 3.4 min. No reloads, no resubmission.
- Job id 2403 (download name kling_20260907_Lip_Sync__2403_0.mp4). Files: `original_2403.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 42472161ce8a468658146540ff5f3404bce03fe3f51fb578f7172af04fafb3e2
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not trimmed/cropped/retimed. Covers source 38..107 (1.583-4.458 s) and the whole plate. Codex conforms 30 -> 24 fps.
- Audio: normalized cross-correlation of returned audio vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base (per native frame, luminance): whole frame mean 3.0 / max 4.4; empty-suit region mean 2.7 / max 3.3
  (noise; the suit stays empty and inert); desk-left mean 3.0; hands region mean 3.3 with one brief peak 11.6 at ~2.97 s
  (re-render jitter around the hand, no changed action); mouth box mean 8.6 / max 18.8. The gentle push-in, the gaze pattern
  (screen right -> down-left -> up) and the hand slide onto the desk at 3.3-4.5 s are all preserved (contact sheet identical in
  layout to the base). Identity, hair, pencil, jacket unchanged.

## Word-level inspection (mouth_synced_src1.5-4.7s_native30_everyframe.jpg = native frames 45-140, every frame, 12 per row;
   mouth_base_src1.5-4.7s_every6.jpg = base (mouth closed throughout this window); mouth_synced_src0-1.6s_every3.jpg;
   mouth_synced_src4.6-8s_every6.jpg; frame-to-frame mouth-motion trace)
- Lead 0.1-0.8 s: the mouth opens and moves on the guide's preceding context (the other speaker's "thread"). This sits inside
  the listening section that Codex keeps from the original (source 12..38), so it must be excluded, as planned.
- 0.9-1.55 s: mouth closed (guide quiet) - clean hand-over point at source 38.
- Words (1.583-~2.6 s, f48-78): OK. Rounded "O" opens at f48 (1.60 s), held/varied through 2.27 s while the gaze goes to screen
  right, narrowing 2.3-2.55 s, closing by ~2.65 s. Readable sung vowel with mouth interior visible; no teeth-heavy grimace.
- leave (2.75-3.3 s, f83-99): MISSING. Guide is loud here but the lips stay closed or barely parted while she looks down-left
  (the base's "considering" beat); frame-to-frame mouth motion 1-3. The word does not read.
- 3.3-4.1 s: closed lips, head down (guide quiet 3.5-4.25 s) - fine.
- words (4.17-4.7 s, f125-141): OK/moderate. Lips part at f125 (4.17 s), the head lifts and the mouth opens moderately
  4.33-4.67 s, closing ~4.9-5.0 s. Note the guide's energy for this word peaks at 4.5-4.75 s, i.e. partly AFTER the phrase's
  out-point at source 4.458 s (frame 107); the mouth is still open at frames 107-113 (24 fps) - Codex should check whether the
  cut at 2881 clips the last word.
- Tail: closed by ~5.0 s; small lip motion 6.6-7.4 s on the guide's later context (outside approved use); eyes lower to the desk
  as in the base.
- No puppet jaw, no clamped-lip artifact, no distorted teeth, no face/costume change.

## Defects (summary)
- "leave" not articulated (2.75-3.3 s) - lips closed during a loud part of the guide.
- Final "words" runs to ~4.7 s, past the source 107 out-point (guide places it late).
- Guide-context mouth motion 0.1-0.8 s (listening section; excluded by the planned keep of original 12..38).

## Not done
- No Flow, no retry, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.
