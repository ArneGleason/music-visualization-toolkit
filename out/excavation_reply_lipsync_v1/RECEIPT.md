# RECEIPT: excavation_reply_lipsync_v1

Status: DONE - one Kling Lip Sync on the owner-approved excavation close-up, downloaded untouched and inspected every native
frame over source 0.0-4.8 s plus the tail. Result is USABLE: the guide is embedded at zero lag, every word gets real
articulation including through the grin (1.4-3.1 s), consonant closures are present, the question completes on time and the
mouth settles at ~4.6 s. Caveats: reduced mouth motion 2.4-3.05 s (tail of "stupid" and "Can"), and the base's early mouth
opening before 0.875 s remains. No Flow, no acting change, no retry, no assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: 2fe46beb1d0cf338e677aa7a1bb621c79758209fdf1102f1279ff420d7275426 (1280x720, 24/1, 192 frames, 8.000 s, no audio; silent remux of excavation_reply_v1/base)
- guide `guide.wav`: 95a97c5381e72760c5dfbfbaf0ba53d0a5793a9530ce860c24651d69940d6534 (48 kHz mono PCM16, 8.000 s). Uploaded unchanged at 0:00; no offset, trim, gain, TTS.
  Only these two files were uploaded.

## Kling (actual, times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded; one face detected, Character 1 = the
  woman (sole character). Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead at 0:00 -> Add Speech -> block spans
  0:00-0:08 on the Character 1 lane. Sound from Video OFF. Generate quoted 10 credits.
- Submitted at approximately 19:54:05 (the Generate click was the first action of a polling batch that then hit a tool
  timeout, so the exact click timestamp was not captured; the batch started ~19:54:00). Balance 436 -> 426 (10 credits) and
  "0/1 Generating" confirmed at 19:56:55; 19:57:27 "1/1 Generated"; card playable when brought to top at 19:57:55. Download
  (Video, MP4, Without Watermark ON, existing entitlement) clicked 19:58:06; file present and copied 19:58:48. About 3.4 min
  submit -> generated. No reloads, no resubmission.
- Job id 983 (download name kling_20260907_Lip_Sync__983_0.mp4). Files: `original_983.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 ecaf2acd7e15cb485e19ec799043c93d66bce40fc1429ae39c75b6c938849fe8
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not trimmed/retimed/cropped. Coverage 7.967 s >= required 4.417 s. Codex conforms 30 -> 24 fps by timestamps.
- Audio check: normalized cross-correlation of returned audio vs guide.wav = 0.999 at lag 0 (best lag 0 within +-0.1 s).
- Picture integrity vs base (per native frame, luminance mean abs diff): whole frame mean 3.2 / max 5.5; right background
  mean 2.5 / max 3.1 (noise level); collar mean 3.9 / max 7.9; eyes band mean 4.7 / max 14.6 at 3.77 s (Kling re-renders the
  lower face and the jaw motion shifts the region, the eyes themselves read the same); mouth box mean 8.8 / max 17.0.
  Framing, background, hair, collar unchanged; identity consistent; teeth natural.

## Word-level inspection (mouth_synced_src0.8-4.8s_native30_everyframe.jpg = native frames 24-143, every frame, 12 per row;
   mouth_synced_src0-0.8s_every2.jpg; mouth_base_src0.8-4.8s_every4.jpg; mouth_synced_src4.7-8s_every6.jpg; frame-to-frame
   mouth-motion trace)
Native frame = source seconds x 30. The base already opens the mouth at 0.25 s and holds a grin 1.4-3.1 s.
- 0.00-0.875 (pre-phrase): lips closed to ~0.25 s, then open shapes 0.27-0.75 s (base opening plus guide context). Not clean
  silence before "Especially"; it is inside the 0.5 s in-point lead.
- Especially (0.875-1.792 s, f26-54): OK. Open vowel with teeth f24-27 (0.80-0.90), closure f28-35 while the eyes are squeezed
  (0.93-1.17), re-opening with teeth f40-47 (1.33-1.57), open f48-51 (1.60-1.70). Syllables read through the wince.
- stupid (1.792-2.833 s, f54-85): OK through the grin. The grin is no longer frozen: f52-59 wide toothy open (1.73-1.97 "stu"),
  f60-63 narrower, f64-67 rounded lips (2.13-2.23 "-pi-"), f68-77 open with teeth (2.27-2.57 "-d"), then a held small open
  f78-85 (2.6-2.83). Mouth shapes change across the grin; not a static smile. Caveat: frame-to-frame motion drops to 2-3 for
  f72-92 (2.4-3.07 s), so the word's tail is a held shape rather than a moving one.
- Can (2.833-3.083 s, f85-92): WEAK. Held small open/teeth-visible shape with little motion; reads as a soft "Can".
- you (3.083-3.292 s, f92-99): OK. Clear open vowel f94-99 (motion 11-14).
- hear (3.292-3.542 s, f99-106): OK. Open, changing shapes (motion 17 at f100, 13-18 at f104-106).
- what (3.542-3.792 s, f106-114): OK. Open f108-111, lip closure f112-115 (3.73-3.83) for the consonant.
- I (3.792-3.958 s, f114-119): OK. Rounded open "O/I" f116-119.
- meant (3.958-4.417 s, f119-132): OK. Wide open vowel f120-127 (4.0-4.23), closing f128-131 (4.27-4.37) for "-nt".
  Phrase completes at ~4.4 s, on time.
- 4.4-4.7 s: mouth relaxes to a slight open smile; SETTLES ~4.6-4.7 s.
- Tail 4.7-8.0 s: closed 4.7-5.2 s, then the mouth opens again 5.3-5.7 s and 5.9-6.3 s and lightly to 7.7 s, following the
  guide's later vocal context (the other speaker's line). Not approved coverage; Codex cuts at source 106 (4.42 s).
- No puppet jaw, no distorted teeth, no face change, no timing drift: loud guide moments (2.0-2.5 s "stupid", 4.0-4.3 s
  "meant") coincide with the widest mouth shapes.

## Defects (summary)
- Held/low-motion mouth 2.4-3.05 s: tail of "stupid" and "Can" under-articulated.
- Mouth already open 0.27-0.75 s before the phrase (base performance plus guide context).
- Guide-context mouth motion after 5.3 s (outside approved use).

## Not done
- No Flow, no acting revision, no retry, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.
