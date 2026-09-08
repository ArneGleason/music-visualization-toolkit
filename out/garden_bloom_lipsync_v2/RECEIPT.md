# RECEIPT: garden_bloom_lipsync_v2

Status: DONE - one Kling Lip Sync on this folder's base.mp4 with this folder's NEW guide.wav, downloaded and inspected frame by
frame over original-source 2.60-5.60 s plus the tail. Result is PARTIAL, much like garden_begin_lipsync_v1: the guide is
embedded at zero lag and the mouth events land inside the phrase, but articulation on this ~50 px quiet face is small. Only
the "for"->"the" transition opens clearly; "song", "to" and "begin" stay essentially closed. No Flow, no retry, no assembly,
no FX/production edits, no commit, no purchase. Prior test folder untouched. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: BA2641F5DA2A88B230FC3BA5A490274094A68DC82B9150294B99583AD3E9EB86 (1280x720, 24/1, 192 frames, 8.000 s, no audio track; same plate as v1, source0 = song1720 here)
- guide `guide.wav`: B38441740658BA5908E2189AB6B964874B1400A9A9F13315740D2D0A901EA4F6 (48 kHz mono PCM16, 8.000 s). NEW guide: its correlation with the old v1 guide is 0.005,
  i.e. a different slice. Uploaded unchanged at 0:00; no offset, trim, gain, TTS or speed change. The old synced.mp4, bloom
  preview, clean.mp4, green guide, lyrics or master were NOT uploaded.

## Kling (actual, times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): fresh editor page; base.mp4 uploaded; face auto-detected
  as Character 1 (sole woman). Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead at 0:00 -> Add Speech -> speech block
  spans 0:00-0:08 on the Character 1 lane. Sound from Video OFF. Generate quoted 10 credits.
- Submitted 16:12:33. Balance 456 -> 446 (10 credits charged). Checks: 16:13:03 queueing/creating; 16:13:23; 16:13:55; 16:14:15;
  16:14:35; 16:14:55; 16:15:28 (creating); 16:15:48 "1/1 Generated"; card playable when brought to top at 16:17:03.
  Download (Video, MP4, "Without Watermark" ON, existing entitlement) clicked 16:17:13; file in Downloads by 16:17:50; copied
  into this folder 16:18:12. About 3 min 15 s submit -> generated. No reloads, no resubmission.
- Job id 57 (download name kling_20260907_Lip_Sync__57_0.mp4; Kling's date rolled to 09-07 in its time zone). Files:
  `original_57.mp4` (untouched download) and `synced.mp4` (byte-identical), SHA-256 EE4935D09EA824BE44A61E6416C3C154072ED87E5C3176D361FEB9A113E1E371
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not retimed/trimmed/cropped. Coverage 7.967 s > required 5.583 s. No watermark. Codex conforms 30 -> 24 fps.
- Audio check: normalized cross-correlation of the returned audio vs guide.wav = 0.999 at lag 0 (best lag 0 within +-0.1 s).
- Picture check: full-frame diff vs base every 0.5 s stays 2.0-2.8 over the whole take; the pollen bloom develops identically
  to base (mouth_base sheet vs synced sheet show the same brightening), framing/set/costume/hair unchanged; only the mouth
  region is altered.

## Word-by-word inspection (mouth_synced_src2.6-5.6s_native30_everyframe.jpg = native frames 78-168, every frame, 13 per row;
   mouth_base_src2.6-5.6s_every3.jpg for the closed-mouth base; mouth_synced_src5.0-8s_every3.jpg for the tail)
Native 30 fps frame = original-source seconds x 30. Base mouth is closed throughout.
- for   (2.750-3.208 s, f83-96): WEAK. Closed through ~2.93 s (f88); lips part slightly f88-95; the clear opening only arrives at
        f96 (3.20 s), i.e. at the very end of the word. No "f" lip contact readable.
- the   (3.208-3.625 s, f96-109): OK. Clear open mouth f96-103 (3.20-3.43 s), narrowing f104-108, closed by ~3.6 s. Strongest
        articulation of the take.
- song  (3.625-4.125 s, f109-124): MISSING/near-closed. Lips stay closed with only faint lip-line motion; the sustained vowel
        is not shown open at any frame.
- to    (4.125-4.500 s, f124-135): WEAK. Closed with faint parting around f128-134 (4.27-4.47 s).
- begin (4.500-5.042 s, f135-151): WEAK. Slight parting f138-142 (4.60-4.73 s) and f147-151, never a real open vowel; the
        sustained "-gin" on the pollen burst at 4.5 s is not visibly sung.
- settling tail (5.042-5.583 s, f151-167): CLEAN. Mouth closed with only faint lip motion; no inappropriate talking. The next
        clear opening starts at ~f171 (5.70 s), just after the visible out-point, following the guide's later vocal context
        (5.7-6.3 s and 7.4-7.9 s); that is expected but not approved coverage.
- No frozen interval within the phrase (tiny motion every few frames), no puppet jaw, no teeth artifacts, no identity change.
- Test verdict: timing aligned, amplitude insufficient; "song", "to" and "begin" do not read as sung. Same limitation as v1 on
  this small quiet face. Useful test information; no retry spent.

## Not done
- No Flow, no retry, no assembly, no FX edits, no production/cue edits, no commit, no purchase, no owner approval claimed.
