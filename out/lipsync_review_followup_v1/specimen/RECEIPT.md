# RECEIPT: lipsync_review_followup_v1 / specimen

Status: DONE - one Kling Lip Sync on the specimen_discovery_v1 base (silent remux; video stream bit-identical to the source),
downloaded untouched and inspected every native frame over source 2.2-5.0 s plus the listening lead and the tail.
Result is PARTIAL / MIXED: "I'm sure it's there" (2.29-3.33 s) is articulated; "Hard to find, right?" (3.33-4.92 s) has real
mouth motion but it sits awkwardly on a guide that is near-silent for "Hard" and only moderate afterwards, and Kling clamps
the base's open "oh" into a tense pressed-lip mouth at ~3.7-4.0 s that reads puppet-like. Also the guide's loud context
before 2.25 s (the other speaker's line) makes her mouth move during the listening section, which Codex must discard as
planned (replace only source 55..118). No Flow, no retry, no assembly, no FX, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: 80265cbe654db4049e46920a39ff6270813ab02728021cf4af243f2efb385746 (1280x720, 24/1, 192 frames, 8.000 s, no audio; video md5 identical to
  out/specimen_discovery_v1/base.mp4)
- guide `guide.wav`: 62f4d93ccfc1a65b222c5daf741b8e59998937d2784f432e564073efbd3399e0 (48 kHz mono PCM16, 8.000 s), uploaded unchanged at 0:00. Guide energy (RMS per
  0.25 s): loud 0-2.5 s (offscreen speaker's line + "I'm sure"), then quiet: 2.5-3.25 s 595/337/240, 3.25-3.5 s 26,
  3.5-4.25 s 251/367/254, 4.25-4.75 s 708/884, 4.75-5.0 s 243, then loud again from 5.25 s (following context).

## Kling (times UTC; local = UTC-4)
- Kling Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded from a fresh editor page; one
  face detected (Character 1 = the woman, sole character). Upload Local Dubbing -> guide.wav (shown 0:00-0:08) -> playhead at
  0:00 -> Add Speech -> speech block spans 0:00-0:08 on the Character 1 lane. Sound from Video OFF. Generate quoted 10 credits.
  No offset, trim, TTS, normalization or crop. Download: Video, MP4, "Without Watermark" ON (existing entitlement).
- Submitted 20:56:42; "Task submitted / 0/1 Generating" at 20:56:47; balance 416 -> 406 confirmed 20:57:38 ("0/2 Generating").
  Checks 20:57:58, 20:58:28 ("1/2 Generating" = opening done, this one still creating), 20:58:49, 20:59:09 (creating,
  "Estimated wait 30 s"); done by 20:59:49 (no generating badge). Card time 4:56:46 PM local. Download clicked 21:00:54;
  file present and copied 21:01:50. About 3 min. No reloads/resubmits.
- Job id 1259 (download name kling_20260907_Lip_Sync__1259_0.mp4). Files: `original_1259.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 995aff0397d7b3e56670c86707de40a4bc76b6b04d841d3b9549942596d26b4e
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Coverage covers source 55..118 (2.29-4.92 s). Codex conforms 30 -> 24 fps by timestamps.
- Audio: normalized cross-correlation vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base: background corner mean 2.6 / max 2.8 (noise), face region mean 5.2 / max 11.7, mouth box
  mean 7.9 / max 21.1 - only the lower face re-rendered; hands, specimen, set, framing unchanged; identity consistent.

## Word-level inspection (mouth_synced_src2.2-5.0s_native30_everyframe.jpg = native frames 66-150, every frame, 11 per row;
   mouth_synced_src0-2.3s_every3.jpg; mouth_base_src2.2-5.0s_every4.jpg; mouth_synced_src5-8s_every6.jpg; motion trace)
- 0.3-2.2 s (listening section, to be discarded): the mouth sings the OFFSCREEN speaker's line because the guide carries it.
  Codex's plan keeps original source 12..55 for listening, so this is expected but must not leak into the cut.
- I'm sure (2.29-2.6 s, f69-78): OK. Open/rounded shapes 2.2-2.45 s, closing 2.45-2.55.
- it's there (2.6-3.33 s, f78-100): OK but small. Parted-lip shapes 2.6-2.9 s, mostly closed/slight 2.95-3.27 s (guide is quiet
  here, so the small motion matches).
- Hard (3.33-3.6 s, f100-108): mouth opens WIDE (dark interior) 3.3-3.63 s although the guide is near-silent (RMS 26) - this
  is the base's own open-mouth "oh" (3.5-4.5 s in the base) that Kling partly retains. Visually it reads as a loud syllable
  where the audio has almost nothing.
- to find (3.6-4.25 s, f108-127): DEFECT. Kling forces the mouth shut over the base's open jaw: 3.7-4.0 s (f112-120) shows
  tightly pressed lips with a bulging lower face - tense, puppet-like. Then a wide open "O" 4.03-4.3 s with raised brows
  (guide 254-708) - reads as "find".
- right? (4.25-4.92 s, f127-148): OK. Open with teeth 4.4-4.73 s (guide 884), easing to a toothy smile and closing by ~5.0 s
  (the base's wry smile arrives here).
- 5.0-8.0 s (tail): closed-mouth smile with a brief opening ~5.5-5.7 s and small motion later, following the guide's later
  context; not approved coverage.
- No timing drift on the audible parts (the 4.25-4.75 s guide peak coincides with the widest 4.03-4.73 s shapes); no teeth
  distortion; no face or framing change.

## Defects (summary)
- Tense pressed-lip mouth 3.7-4.0 s (Kling closing the base's open "oh") - puppet-like.
- Wide open mouth 3.3-3.63 s on a near-silent part of the guide ("Hard" has almost no audio energy in this guide).
- "it's there" small; overall amplitude on 2.6-3.3 s modest.
- Mouth motion during the listening section 0.3-2.2 s (offscreen speaker's line in the guide) - must be excluded by the cut.

## Not done
- No Flow, no retry, no assembly, no FX (specimen_signal_v1 glow not applied), no cut changes, no production edits, no commit,
  no purchase, no owner approval claimed.
