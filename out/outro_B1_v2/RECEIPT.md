# RECEIPT: outro_B1_v2 (Flow base + gated Kling)

Status: BOTH STAGES DONE. One Flow base generated from first_frame.png, reviewed against the base gate (passed: same face,
plain suit with no chest hardware, artifact and hands stable, real open articulation on "Define there", locked camera, no
cut), then ONE Kling Lip Sync with the full continuous-context guide at 0:00. Both originals downloaded untouched with
byte-identical copies. Kling result is PARTIAL: inside her cut (source 67..97 = 2.79-4.04 s) "Define there" is carried with
only small jaw/lip movement over a toothy smile, because the guide's level for that line is low (RMS ~150 vs 1000-4000 for
the astronomer's lines) and the base holds a broad smile there. Reported for owner review; no retry. No B2/A2, no assembly,
no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: 96988adbea0a3da9f60dcf098077445a543976cc02d5a854475fe2594fc003b9 (1280x720; uploaded fresh via Add media > Upload; selected by its
  exobiologist preview; thumbnail id 98a6e2e3; generated first frame matches, mean diff 1.0 at 64x36). Approved anchor
  `out/outro_anchors_v2/exobiologist.png` (ea5bc2eb64dabc0601e33769876f3b035e594ae345ede604bc694833f04c5f0b) verified, not uploaded. End slot
  verified empty; no audio upload to Flow.
- prompt `flow_prompt.txt`: 1afbdc838a70a8e99872209e9eb05afe7fec608965ce644a0e118e90e59dcd64 (4504 chars) pasted once with execCommand insertText; editor text compared
  to the file with whitespace removed = identical; lock included verbatim.
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide `guide.wav`: aec7fa16b9b240410a96b1363db4453bc24cfc355fc5b18c328c8fe7f3bff4f4 (48 kHz mono PCM16, 8.000 s; same continuous-context guide as A1; other-speaker lines
  present by design). Energy (RMS per 0.25 s): silent 0-0.5; astronomer "You still there?" 0.5-1.75; silent 1.75-2.75;
  HER "Define there" 2.75-4.0 at only ~80-200; astronomer "Never mind / La-la-la, low light" 4.0-6.75 loud; silent 6.75-7.0;
  her "No, go on" from 7.0 (2400 then 1484/1683).

## Stage 1 - Flow (times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". Flow's "high demand" banner was showing. NOTE: the Chrome extension disconnected once mid-setup (after the
  prompt paste); on reconnect the composer state was re-verified (slot 98a6e2e3, prompt identical, End empty, settings ok)
  before the single send. No duplicate submission.
- Submitted 15:08:59. Progress 15:09:29 21%; 15:09:49 37%; rendered by 15:10:39. Tile URL read 15:11:01; download 15:11:29.
  About 100 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id ed4e7604-e0ef-423c-88aa-47fc7a852316 (Flow caption "Woman holding specimen in room"). Files: `original_ed4e7604-e0ef-423c-88aa-47fc7a852316.mp4` (untouched)
  and `base.mp4` (byte-identical), SHA-256 2ed1a1b84dafd68a77b7141768ae580661a4039b83552fad54a1cdc1493c92b7
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio (AAC 48 kHz stereo). No
  watermark. 100 credits.

### Base review (crop_face_every2.jpg = 1 s per row; crop_artifact_hands_every8.jpg; crop_chest_every24.jpg; contact_every6.jpg;
    keyframes_0_24_67_97_155_191.jpg; traces)
- Identity/suit: same face, red bob and fringe, plain smooth silver high-neck suit for all 8 s - no dials, hoses, patches
  (chest crop). Room, window, lamps unchanged. Camera locked (difference vs frame 0 grows only 0 -> 17 from her own slow
  motion; no cut or reset).
- Artifact/hands: the single fluted shell with golden spiral stays in her hands, same shape/size, hands still and low for
  the whole take (artifact crop every 8 frames); no morph, no duplicate, no handling.
- Face/timing (source seconds): 0.4-0.7 small lip movement while listening; 0.5-1.3 glance down at the specimen; 1.3-1.9
  eyes back up with a small smile and slight lip motion; 2.0-2.6 "DEFINE THERE" - open vowels with upper teeth and mouth
  interior, clearly articulated but EARLY (window 2.73-4.10) and delivered with a bright, delighted open-mouth look rather
  than dry wit; 2.6-5.5 listening with a broad closed-lip smile (warmth stronger than "a little"); 5.5-6.4 invented speech
  shapes (the "No, go on" pickup arriving early; window 6.86+); 6.4-7.3 smile; 7.3-7.6 more speech shapes; 7.5-8.0 looks
  down at the specimen with a smile. Frame 155 (6.46 s): frontal, mouth slightly open mid-shape, hands/artifact stable -
  usable as the B2 anchor though mid-word.
- Gate: face/plain suit PASS; artifact/hands PASS; readable active articulation on "Define there" PASS (early, delighted);
  no cut/reset PASS. Tolerated and reported: broad smile, early timing, invented mouth motion at 0.4-0.7, 1.3-1.9, 5.5-6.4
  and 7.3-7.6 s. => Kling authorized.

## Stage 2 - Kling (times UTC)
- Lip Sync editor: `base.mp4` uploaded as-is (Sound from Video OFF, verified by zoom, so its Veo audio is ignored). One face
  detected, Character 1 = the exobiologist. Upload Local Dubbing -> guide.wav (0:00-0:08, gaps intact) -> playhead 0:00 ->
  Add Speech -> block spans 0:00-0:08 on the Character 1 lane. Generate quoted 10 credits.
- Submitted 15:13:50; "Task submitted / 0/1 Generating" 15:13:55, balance 371 -> 361. Checks 15:14:20, 15:14:52, 15:15:12,
  15:15:32, 15:16:03, 15:16:23, 15:16:43 (creating); 15:17:15 "1/1 Generated". Download (Video, MP4, Without Watermark ON)
  clicked 15:18:16; file present and copied 15:18:59. About 3 min 25 s. No reloads, no resubmission.
- Job id 5949 (download name kling_20260907_Lip_Sync__5949_0.mp4). Files: `original_kling_5949.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 7055e5d5037286e56692ddc33343f551e4d5aa212f14802e2ca181756ddf7ea6
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 decoded frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start
  0.000. Not converted/cropped/trimmed/retimed; no separate remux was made.
- Audio: normalized cross-correlation of returned audio vs guide.wav = 0.993 at lag 0.
- Picture integrity vs base (per native frame): whole frame mean 2.6 / max 3.5; artifact+hands mean 2.7 / max 9.7 (last
  frames only); chest mean 2.7; window mean 3.2; mouth box mean 11.5 / max 29.6. Only the mouth region was re-rendered;
  artifact, hands, suit and room preserved; identity and teeth intact.

### Kling articulation (mouth_synced_cut_src2.4-4.4s_native30_everyframe.jpg = native frames 72-131; mouth_base_every6.jpg
    vs mouth_synced_every6.jpg; motion trace)
- 2.13-2.5 s (before her cut): Kling reshapes the base's early "Define there" (motion 20-26) into an open toothy smile that
  narrows - residue in the lead before source 67.
- Her cut 2.79-4.04 s (source 67..97): the face holds a toothy smile; "Define" (2.8-3.2 s) shows only small jaw/lip changes
  (motion 2-10) and "there" (3.2-3.6 s) small shape changes (motion 3-16); 3.6-4.04 s closed-lip smile, static. The initial
  "D" closure and the "-ere" ending are barely readable. Cause: the guide carries her line at ~150 RMS while the base is
  smiling with teeth, so Kling produces little motion. Weak, not frozen.
- 4.5-6.4 s: strong open singing shapes on the astronomer's loud "La-la-la, low light" context - outside her cut, must not be
  selected (assembly guard).
- 6.75-7.0 s: closed; 7.3-7.7 s: open shapes on "No, go on" (B2 territory; continuation context only).
- No puppet lips, no new teeth artefacts, no face change; artifact preserved throughout.

## Defects (summary)
- Kling: "Define there" under-articulated over the toothy smile (2.8-3.6 s); D onset and word ending barely read.
- Base: delighted open-mouth look and broad smile (warmth beyond "a little"); phrases early; invented mouth motion outside
  the spoken windows (0.4-0.7, 1.3-1.9, 5.5-6.4, 7.3-7.6 s).
- Other-speaker context animates her mouth at 4.5-6.4 s (outside her cut by design).

## Not done
- No retry, no B2/A2, no assembly, no production edits, no artifact/TV graphics, no commit, no purchase, no owner approval
  claimed.
