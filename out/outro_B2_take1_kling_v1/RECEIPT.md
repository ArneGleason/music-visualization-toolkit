# RECEIPT: outro_B2_take1_kling_v1 (ONE Kling on the archived FIRST B2 take) - DONE

Status: claude_done_ready_for_codex_verification. One Kling Lip Sync on THIS folder's base.mp4 (byte-identical to
out/outro_B2_v2/take1/base.mp4, Flow media 474079fc) with the unchanged continuous guide at 0:00. Owner override of the
earlier base gate acknowledged; no Flow, no retry. Result filed as synced.mp4 (job 160). Comparison verdict per cut is
below; take 2 (out/outro_B2_v2/synced.mp4, job 86) and its B3 anchor were not touched.

## Inputs verified (SHA-256 match handoff.json)
- base.mp4 ed5f2e2fe7872b682bf1d0b50f8997887e654746a9de53935f5e14fc842f63be (= out/outro_B2_v2/take1/base.mp4; 1280x720, 24 fps, 192 frames, 8.000 s; take 1 = Codex prompt)
- guide.wav ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004 (= out/outro_B2_v2/guide.wav; 48 kHz mono PCM16, 8.000 s, 384000 samples; continuous
  context incl. the other speaker). RMS per 0.25 s: 0.0 1099, 0.25 229, her "No, go on" 0.5-1.75 (2341/514/1288/1732/
  772), other speaker 1.75-3.25, her "You did" 3.5-4.5 (2246/1567/1183/849), other speaker 4.5-5.75, "Da-da-dum"
  5.75-6.75 (44/209/463/500), "Could've" 6.75-7.25 (1295/1240/473), "been" 7.5-8.0 (2113/1711).

## Kling (times UTC)
- Lip Sync editor: base.mp4 uploaded as-is; one face detected, Character 1 = the exobiologist. Upload Local Dubbing ->
  guide.wav (0:00-0:08, gaps intact) -> playhead 0:00 -> Add Speech (first click landed before the audio finished
  loading and did nothing; second click placed the block) -> block spans 0:00-0:08 on the Character 1 lane; Sound from
  Video OFF (zoom verified); Generate quoted 10 credits. Single submission.
- Submitted 16:39:57; "Task submitted / 0/1 Generating" 16:40:02, balance 351 -> 341. Checks 16:40:27, 16:40:47,
  16:41:07, 16:41:38, 16:41:58, 16:42:18, 16:42:38 (creating); 16:43:08 "1/1 Generated". Download (Video, MP4, Without
  Watermark ON) clicked 16:44:24; filed 16:44:52. About 3 min 10 s. No reloads, no resubmission.
- Job id 160 (download name kling_20260908_Lip_Sync__160_0.mp4). Files: `original_kling_160.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 744f1789b92e1de8e4df72a6fc6d88c61cb602deb0109a076b96df934e8edf3d
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}]}
  => 1280x720, NATIVE 30/1 fps, 239 decoded frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both start 0.000.
  Not converted/cropped/trimmed/retimed; no remux made. Cost 10 credits.
- Audio: normalized cross-correlation of the returned audio vs guide.wav = 1.00 at lag 0 (search +-0.1 s).
- Picture integrity vs base (per native frame, base viewed at 30 fps for comparison only): whole frame mean 2.5 / max
  3.0; mouth box mean 3.4 / max 8.2; artifact+hands mean 2.4 / max 6.6 (0.37 s, base motion); chest mean 2.5; window
  mean 3.5. Only the mouth region was re-rendered; artifact, hands, suit, room, identity and teeth preserved. Frames
  alternate duplicate/new (24 -> 30 pull-up) as in every Kling return.

## Sync observations (mouth_synced_cut1/2/3_*.jpg = every 2nd native frame; contact_synced_every10_native.jpg;
   seconds = source frame / 24)
- Cut 1 "No, go on." (source 11..42 = 0.46-1.75 s): rounded open "No" with mouth interior and teeth 0.27-0.75 s,
  closure ~0.85 s, "go on" 1.1-1.5 s as open-then-smiling shapes with teeth, narrowing 1.5-1.7 s, smile 1.8 s. Eyes on
  camera throughout. USABLE - on par with take 2 (job 86); "No" is slightly stronger here.
- Cut 2 "You did." (source 80..111 = 3.33-4.63 s) - PRIMARY TARGET: eyes on camera 3.27-4.0 s with open shapes and
  upper teeth 3.27-3.4 s (strongest mouth motion 3.1-3.3 s, a touch ahead of the guide's 3.5 s onset), lips partly
  closed 3.47-3.6 s, teeth-visible shapes 3.67-3.93 s ("did"), open teeth smile 4.0-4.13 s; from 4.0 s the eyes drop to
  the specimen and from 4.2 s a closed smile looking down to 4.7 s. BETTER than take 2 for the words themselves (take 2
  stays a closed smile), at the cost of the downward gaze in the last 0.6 s of the cut. A cut ending near source 96
  (4.0 s) would avoid the gaze.
- Cut 3 "Da-da-dum / Could've been." (source 141..184 = 5.875-7.67 s): open shapes with teeth 5.8-6.1 s, smile with
  teeth 6.13-6.5 s, closing smile 6.53-6.93 s; head tilts down from ~6.93 s and Kling articulates "Could've" 7.0-7.2 s
  (motion 10-12) ON THE DOWNTURNED FACE; closed, looking down 7.3-7.7 s ("been" absent). WORSE than take 2, which keeps
  the eyes up and articulates "Could've" frontally; both close before the final "been".
- Outside her cuts: open shapes 1.9-2.3 s (other speaker context) and 4.5-5.8 s (early "Da-da-dum" plus context) -
  must not be selected.
- No puppet lips, no teeth artefacts, no face change.

## Suggested per-cut pick (for Codex/owner, not applied)
- Cut 1: either take; take 1 marginally stronger "No".
- Cut 2: take 1 (job 160), ideally trimmed to end by source ~96 to avoid the downward gaze.
- Cut 3: take 2 (job 86).

## Not done
- No Flow, no retry, no assembly, no FX, no edits to take 2 or historical manifests, no commit, no purchase.
