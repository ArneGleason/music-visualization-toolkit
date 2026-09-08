# RECEIPT: outro_A1_kling_v1

Status: DONE - one Kling Lip Sync on the approved A1 v3 picture (silent remux, video stream md5-identical to
out/outro_A1_v3/base.mp4) with the supplied continuous-context guide at 0:00, no offset. Downloaded untouched and inspected
every native frame across both visible cuts. Result is USABLE: "You still there?", "Never mind" and "La-la-la, low light"
are all articulated on the guide with clear vowel shapes and consonant closures, the listening gap is closed-mouth, the other
speaker's context lines fall outside her cuts, and her warmth/TV response remain as owner-accepted. Caveats: a small
pre-question mouth opening at 0.3-0.47 s (inside the 12-frame lead, before the cut), and Kling's re-render delays the TV's
static flash by ~0.1 s relative to the base. No Flow, no retry, no assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: aa40341df7e079630de9c7c39bed6a077bfcb060962c1b509388ce24ee8578ba (1280x720, 24/1, 192 frames, 8.000 s, no audio; video md5 identical to
  out/outro_A1_v3/base.mp4, which matches its recorded hash). Not a previously synced file.
- guide `guide.wav`: aec7fa16b9b240410a96b1363db4453bc24cfc355fc5b18c328c8fe7f3bff4f4 (48 kHz mono PCM16, 8.000 s = 384000 samples), uploaded unchanged at 0:00; no
  offset, trim, silence removal, normalization or old-guide substitution. Guide energy (RMS per 0.25 s): silent 0-0.5;
  "You still there?" 0.5-1.75; silent 1.75-2.75; other speaker "Define there" quiet 2.75-4.0; "Never mind" 4.0-4.5;
  "La-la-la, low light" 4.5-6.75 (loud 4.5-5.5); silent 6.75-7.0; other speaker from 7.0.

## Kling (times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded; one face detected, Character 1 =
  the astronomer (sole woman). Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead at 0:00 -> Add Speech -> block
  spans 0:00-0:08 on the Character 1 lane with all gaps intact. Sound from Video OFF (verified by zoom). Generate quoted 10
  credits.
- Submitted 14:42:48; "Task submitted / 0/1 Generating" 14:42:53, balance 381 -> 371. Checks 14:43:18, 14:43:49, 14:44:09,
  14:44:29, 14:45:00, 14:45:20, 14:45:40 (creating); 14:46:12 "1/1 Generated". Download (Video, MP4, Without Watermark ON,
  existing entitlement) clicked 14:47:11; file present and copied 14:47:56. About 3 min 24 s. No reloads, no resubmission.
- Job id 5804 (download name kling_20260907_Lip_Sync__5804_0.mp4). Files: `original_5804.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 4878c1a15925030d58bdc44ce2120b8906fd1e5f99de40e39716a13b0202cf48
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 decoded frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start
  0.000. Not converted to 24 fps, cropped, trimmed or retimed; Codex conforms by timestamps. Source origin stays song 4165.
- Audio: normalized cross-correlation of returned audio vs guide.wav = 0.993 at lag 0 (best lag 0 within +-0.1 s).
- Picture integrity vs base (per native frame): whole frame mean 3.0; desk/specimens mean 2.9; hands mean 3.0 / max 5.0
  (hands unchanged); mouth box mean 11.0 / max 23.9. TV region mean 4.0 but max 58.9 at 2.43 s: checked with
  tv_base_vs_synced_1.8-2.8s_every3.jpg - the static burst is the same content and geometry, but in the synced file it
  begins and ends about 3 native frames (~0.1 s) LATER than in the base (onset ~2.0 vs ~1.9 s; end ~2.6 vs ~2.5 s). A
  Kling re-render timing artefact, not a new effect; bezel/glass stable, screen unobstructed.

## Articulation (mouth_synced_cut1_src0.3-3.0s_native30_everyframe.jpg = native frames 9-89; mouth_synced_cut2_src3.8-7.1s_
   native30_everyframe.jpg = native frames 114-213; mouth_base_every6.jpg vs mouth_synced_every6.jpg; motion trace)
Cut 1 (source 12..67 = 0.5-2.79 s):
- 0.30-0.47 s (f9-14): small open-mouth shapes with teeth BEFORE the guide's onset - a residue of the base's early scratch
  speech that Kling did not fully close. This sits in the 12-frame lead (before source 12), so it is not in the visible cut.
- 0.50-0.67 (f15-20): lips settle, then open on the guide onset.
- 0.70-1.47 (f21-44): "You still" -> "there?" - open vowels with upper teeth and mouth interior, changing every few frames
  (motion 10-24), face frontal then beginning the turn at ~1.3 s.
- 1.50-1.87 (f45-56): tail of "there?" carried in 3/4 profile as the head turns; mouth closes by ~1.85 s (guide ends 1.75).
- 1.90-2.67 (f57-80): closed mouth, listening, head turned (base behaviour) - clean gap matching the guide silence.
- 2.70-2.97 (f81-89): slight lip parting starts on the other speaker's quiet "Define there" - at/after source 67, i.e.
  outside her cut. Codex must not select A1 here (as the guard says).
Cut 2 (source 97..166 = 4.04-6.92 s):
- 3.80-4.17 (f114-125): open with teeth - "Never" begins slightly early (~3.85 s vs 4.0), inside the lead before source 97.
- 4.20-4.57 (f126-137): rounded/narrower shapes - "mind".
- 4.60-5.37 (f138-161): wide open vowels with teeth - "La-la-la"; strongest shapes coincide with the guide's 4.5-5.5 peak.
- 5.40-6.17 (f162-185): open shapes with the moderate smile - "low light".
- 6.20-6.57 (f186-197): smaller open/closing shapes on the "light" tail (guide moderate to 6.75).
- 6.60-6.97 (f198-209): mouth closes into the composed half-smile - clean end of her cut at 6.92 s.
- 7.00-7.10 (f210-213): mouth opens again on the other speaker's line - outside her cut.
- No frozen intervals inside the phrases, no puppet lips, no new teeth artefacts, no identity change; the head turn does not
  break the sync (mouth keeps articulating through it).

## Defects (summary)
- Pre-question mouth motion 0.3-0.47 s (lead only); "Never" starts ~0.15 s early (lead only).
- TV static burst delayed ~0.1 s vs base (Kling re-render timing).
- Other-speaker context animates her mouth at 2.7-3.0 s and 7.0-7.1 s - outside her cuts by design.

## Not done
- No Flow, no retry, no B1/A2, no assembly, no production edits, no TV FX, no commit, no purchase, no owner approval claimed.
