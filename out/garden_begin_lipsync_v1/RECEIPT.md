# RECEIPT: garden_begin_lipsync_v1

Status: DONE - one Kling Lip Sync submitted, downloaded and inspected word by word. Result is PARTIAL: the mouth moves, timing
is aligned to the guide, identity/set/framing unchanged, but articulation on this small quiet face is thin - only "the" reads
clearly; "for", "song", "to" and "begin" are weak or near-closed (details below). No Flow, no retry, no assembly, no FX edits,
no production edits, no commit, no purchase. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: BA2641F5DA2A88B230FC3BA5A490274094A68DC82B9150294B99583AD3E9EB86 (1280x720, 24/1, 192 frames, 8.000 s, no audio track)
- guide `guide.wav`: 839360F3AEC9744482B2ECC765E671746BDDCAF936CC7DE249E6284720B34F5A (48 kHz mono PCM16, 8.000 s). Uploaded unchanged; no TTS, no offset, no trimming.
  Neither garden_begin_guide_v2/clean.mp4 nor any preview movie was uploaded.

## Kling (actual, times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded; face detected automatically as
  Character 1 (sole woman). Upload Local Dubbing tab -> guide.wav (shown 0:00-0:08) -> Add Speech with the playhead at 0:00 ->
  speech block spans 0:00-0:08 on the Character 1 lane. Sound from Video toggle OFF. Generate button quoted 10 credits.
- Submitted 15:53:00. Balance 466 -> 456 (10 credits charged). Checks: 15:53:31 "0/1 Generating"; 15:54:02; 15:54:22; 15:54:53;
  15:55:13; 15:55:33; 15:56:04 (all generating); 15:56:24 badge "1/1 Generated" but the card still showed "Creating..." at
  15:57:17; card playable at 15:57:47 (ready). Download (Video, MP4, "Without Watermark" ON, existing entitlement) clicked
  15:58:43; file present and copied at 15:59:22. About 4 min 47 s from submit to ready. No reloads, no resubmission.
- Job id 6096 (from the download name kling_20260906_Lip_Sync__6096_0.mp4). Files: `original_6096.mp4` (untouched download) and
  `synced.mp4` (byte-identical), SHA-256 9926D0DC18A93CFFDE317E4875917D16A268835716863670E3F75A58644E6EB7
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not retimed/trimmed/cropped; Codex must timestamp-conform 30 fps -> 24 fps. Returned coverage 7.967 s > required 2.792 s.
  No watermark.
- Audio check: normalized cross-correlation of the returned audio against guide.wav (8 kHz mono) = 0.997 at lag 0, best lag 0
  over +-0.1 s, i.e. the guide is embedded with no shift.
- Picture check: first frame vs base 1.9 mean pixel diff (64x36); full-frame diff vs base every 0.5 s stays 2.0-3.1, i.e. no
  framing, set, costume, body or identity change anywhere in the take. Only the mouth/jaw region changes.

## Word-by-word inspection (mouth_synced_src0.4-2.9s_native30fps_everyframe.jpg = native frames 12-86, every frame, 15 per row;
   face_synced_0-3s_every2_24fps.jpg vs face_base_0-3s_every2.jpg; mouth_synced_src2.8-8s_every3_native.jpg for the tail)
The face is ~50 px wide at 1280x720, so all mouth shapes are small and soft. Base mouth is closed throughout.
- for   (0.500-0.958 s, native f15-28): WEAK. Lips stay closed/barely parted until ~0.63 s, then part slightly (f19-26); no
        real jaw drop, no "f" lip-bite readable. The first clearly open mouth arrives at ~0.93 s (f28), i.e. at the tail of "for".
- the   (0.958-1.375 s, f29-41): OK. Clear open mouth f28-35 (0.93-1.17 s), closing f36-41. This is the strongest articulation.
- song  (1.375-1.875 s, f41-56): WEAK. Lips mostly closed with small lip motion; slight parting f53-56 (~1.77-1.87 s). The
        sustained vowel is not shown open.
- to    (1.875-2.250 s, f56-67): WEAK. Small parting f57-58, closed f60-66, slight parting again f67-71.
- begin (2.250-2.792 s, f68-84): WEAK/PARTIAL. Soft half-open mouth f73-79 (2.43-2.63 s), closing f80-86. The sustained "-gin"
        is not held open; reads as a murmur rather than a sung note.
- No frozen-mouth interval inside the phrase (small motion every 2-4 frames), no puppet jaw or exposed teeth, no identity drift.
- After the phrase: mouth is closed 2.8-3.6 s, then opens ~3.7-4.0 s and again around 5.4-5.6 s, 6.4-6.9 s and 7.0-7.9 s. That
  follows the vocal context present in the guide outside the visible cut (guide energy rises at 3.5-4.5 s and 7-8 s), so it is
  expected, but per the handoff it is NOT approved coverage; Codex must cut at source 67/24 s or earlier.
- Test verdict: sync timing is aligned (mouth events land on the guide), but the amplitude is too small on this quiet base for
  the whole phrase to read; "for", "song", "to" and "begin" would need a bigger/closer face or a more expressive base to sell the
  lyric. This is useful test information; no retry spent.

## Not done
- No Flow, no retry, no assembly, no FX edits, no production/cue edits, no commit, no purchase, no owner approval claimed.
