# RECEIPT: swimmer_shore_lipsync_v1

Status: DONE - one Kling Lip Sync on the ORIGINAL silent shore performance (basin_edge_sync_v6, silent remux) with the supplied
aligned guide, downloaded untouched and inspected every native frame over source 2.7-5.8 s plus lead and tail. Result is
USABLE: "go" and "swimming" land at their anchors with wide open singing shapes and visible teeth, "in" is articulated at
5.13 s, no blank gaps inside the visible window, no puppet lips or warping, and the chrome swimmers, water, rocks, lantern and
camera are unchanged. No Flow, no retry, no assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- base `base.mp4`: 8a6aceaab1689ec333f1b5f868346bb798d334b3a3d47df544effa4bb98b5b68 (1280x720, 24/1, 192 frames, 8.000 s, no audio; video stream md5-identical to
  clips/raw/basin_edge_sync_v6.mp4, which matches its recorded hash). This is the original Flow performance, not the old Kling.
- guide `guide.wav`: cefde169c755ce5ce04a4ab5cc597e438b99e308e1950c14e442da2fbe79847b (48 kHz mono PCM16, 8.000 s), uploaded unchanged at 0:00; no silence removal, trim,
  shift, offset or pre-roll. Guide energy (RMS per 0.25 s): loud 0-1.0 s, moderate 1.25-1.75, quiet 2.0-3.0 (~400-800),
  loud 3.0-5.5 s (2100-3200), quiet 5.5-6.25, moderate 6.25-8.0 (context).

## Kling (times UTC; local = UTC-4)
- Lip Sync editor (kling.ai/app/ai-human/video/new?trackName=lipsync): base.mp4 uploaded. Kling detected ONE face:
  Character 1 = the red-haired woman kneeling in the foreground (thumbnail confirmed by zoom). None of the chrome swimmers was
  detected as a character, so nothing could be assigned to them. Upload Local Dubbing -> guide.wav (0:00-0:08) -> playhead at
  0:00 -> Add Speech -> block spans 0:00-0:08 on the Character 1 lane. Sound from Video OFF (verified by zoom). Generate
  quoted 10 credits.
- Submitted 03:09:06; "Task submitted / 0/1 Generating" 03:09:11, balance 391 -> 381. Checks 03:09:36, 03:10:11, 03:10:31,
  03:10:51, 03:11:30, 03:11:50 (creating); 03:12:10 "1/1 Generated". Download (Video, MP4, Without Watermark ON, existing
  entitlement) clicked 03:12:29; file present and copied 03:13:12. About 3 min. No reloads, no resubmission.
- Job id 2850 (download name kling_20260907_Lip_Sync__2850_0.mp4). Files: `original_2850.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 ba892d705834c66de39fe7cf6aca76f62a0a3996b96b4ae537d934b9876c3628
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not trimmed/cropped/retimed; native timebase preserved for Codex's 30 -> 24 fps timestamp conform. The visible in-point
  2.84 s sits inside the take with 2.84 s of context before it, as supplied.
- Audio: normalized cross-correlation of returned audio vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base (per native frame, luminance): whole frame mean 3.6 / max 6.8; left swimmer group mean 5.0 /
  max 14.3 and right group mean 4.8 / max 14.3 (both at 0.83 s) - checked visually with swimmers_base_vs_synced_0.5-1.5s.jpg:
  the swimmers' poses, count and chrome are identical frame for frame; the residual comes from the base's own fast arm motion
  under re-encoding, not from Kling animating them. Rocks/lantern/water mean 3.4. Mouth box mean 9.7 / max 22.9. Camera,
  costume, hair, lantern, reflections unchanged; identity consistent.

## Articulation (mouth_synced_src2.7-5.8s_native30_everyframe.jpg = native frames 81-174, every frame, 12 per row;
   mouth_base_src2.7-5.8s_every6.jpg; mouth_synced_src0-2.8s_every4.jpg; mouth_synced_src5.8-8s_every6.jpg; motion trace)
Anchors: cut in 2.84 s; go 2.882 s; swimming 3.673 s; in 5.132 s; cut out 5.673 s.
- Lead 0-2.8 s (not visible): active singing shapes on the guide's "Chrome-plated bodies" context - expected, outside the cut.
- 2.70-2.93 s (f81-88): wide open "O" - the "go" onset lands right at the in-point/anchor (2.84-2.88 s), mouth already open
  and held through 2.93, narrowing 2.97-3.07.
- 3.10-3.47 s (f93-104): open shapes with upper teeth, changing every few frames (moving into "swim-").
- 3.50-3.87 s (f105-116): big open vowel with mouth interior - "swim-" at 3.67 s reads strongly.
- 3.90-4.27 s (f117-128): rounded shapes then a lip closure into a smile - the "m" of "-ming".
- 4.30-4.67 s (f129-140): near-closed lips with small motion over the sustained "-ing" (guide still loud). Reads as a held
  note with a closed-ish mouth; the weakest stretch, not a blank freeze (motion 8-30).
- 4.70-5.07 s (f141-152): open shapes with teeth resume.
- 5.10-5.47 s (f153-164): "in" at 5.13 s - open shapes with teeth, narrowing toward 5.47.
- 5.50-5.80 s (f165-174): open "O" shapes to the cut-out (guide quieter here; slight over-articulation).
- Tail 5.8-8.0 s: open then relaxed, opens again ~7-8 s on the context (outside the cut).
- No missing-word gaps inside 2.84-5.673 s, no puppet lips, no facial warping, teeth natural.

## Defects (summary)
- Sustained "-ing" 4.3-4.67 s carried with near-closed lips (weakest stretch).
- Slight open-mouth activity 5.5-5.8 s where the guide is quieter.
- Otherwise clean; swimmers and FX regions untouched.

## Not done
- No Flow, no retry, no assembly, no FX/shotlist/production edits, no commit, no purchase, no owner approval claimed.
