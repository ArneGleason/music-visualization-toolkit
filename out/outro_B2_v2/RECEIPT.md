# RECEIPT: outro_B2_v2 (two Flow takes, Kling on take 2) - BOTH STAGES DONE

Status: claude_done_ready_for_codex_verification. Take 1 (Codex prompt) failed the base gate on passage 3 (looked down,
closed mouth through "Could've been"); the OWNER authorized ONE Flow retry with a prompt change made in this session
(flow_prompt_take2.txt, lock byte-identical). Take 2 keeps eyes up and level for all 8 s and articulates passages 1 and 3
inside their cuts; passage 2 "You did." is a closed-lip knowing smile in the base. Reported to the owner, who ACCEPTED
take 2 and authorized the single Kling pass (chat, 2026-09-07). Kling job 86 is filed as synced.mp4. Kling result is
PARTIAL: cut 1 and the "Could've" half of cut 3 read well; cut 2 "You did" stays mostly a closed smile with the lips
parting only briefly; the final "been" lands on a mouth that closes at ~7.4 s. No further retries. Current base.mp4 =
TAKE 2; take 1 preserved unchanged in take1/.

## Inputs verified (SHA-256 match handoff.json)
- first_frame.png 8f7641bb6332a8291ce778fa75a9addd60bf636179955c3cbc6379185eadb4d5 (1280x720; equals ../outro_B1_v2/base.mp4 frame 155 exactly, mean diff 0.0)
- continuation_base ../outro_B1_v2/base.mp4 2ed1a1b84dafd68a77b7141768ae580661a4039b83552fad54a1cdc1493c92b7 (not uploaded)
- approved_anchor ../outro_anchors_v2/exobiologist.png ea5bc2eb64dabc0601e33769876f3b035e594ae345ede604bc694833f04c5f0b (comparison only)
- flow_prompt.txt 674315f4caf44a47c9e832240feb560608012156647ec6d8ebf4a765b5fc5184 (take 1, Codex prompt, 4079 chars)
- flow_prompt_take2.txt ece36dc093bdb7cc4477a430a22f7af696b2b045645410097120494782f59b91 (take 2, owner-authorized edit, 4488 chars; lock suffix byte-identical to style_lock_v2.txt)
- lock ../astronaut_reply_v1/style_lock_v2.txt 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide.wav ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004 (48 kHz mono PCM16, 8.000 s, 384000 samples; not yet used). RMS per 0.25 s: 0.0 1099,
  0.25 229, her "No, go on" 0.5-1.75 (2341/514/1288/1732/772), other speaker 1.75-3.25 (473/204/376/398/555/309), 3.25 6,
  her "You did" 3.5-4.5 (2246/1567/1183/849), other speaker 4.5-5.75 (83/640/672/1017/2016), "Da-da-dum" 5.75-6.75
  (44/209/463/500), "Could've" 6.75-7.25 (1295/1240/473), "been" 7.5-8.0 (2113/1711).

## Prompt change for take 2 (three edits, everything else verbatim)
1. Listening window 4.69-5.81 s now reads: still closed mouth, head level, eyes up, no early singing; from 5.81 s
   "Da-da-dum" runs straight into "Could've been" (6.90-7.73) with lips forming every syllable and eyes on the colleague
   through the end of "been"; must NOT look down, close the mouth or drift into a silent smile before 7.75 s; only after
   7.75 s settle into a level listening pose facing camera.
2. "A tiny glance at the artifact is possible only while listening" replaced by: she never looks down at the specimen in
   this take; head level, eyes toward the colleague the whole time.
3. The 7.5 s pose note adds: head level, eyes up, mouth mid-phrase is fine.

## Take 1 - Flow (Codex prompt) - see take1/RECEIPT.md
- Media 474079fc-bade-4422-9162-b409ce12c676, submitted 16:06:26Z, rendered by 16:07:45Z, downloaded 16:08:13Z, 100
  credits, 24 fps/192 frames, SHA-256 ed5f2e2fe7872b682bf1d0b50f8997887e654746a9de53935f5e14fc842f63be. Gate: face/suit/artifact/camera PASS; passage 1 PASS (early), passage 2
  PASS (3.05-3.9 s, then eyes down), passage 3 FAIL (Da-da-dum early at 5.0-6.0 s, then closed smile and head down
  6.85-7.67 s). Frame 180: looking down.

## Take 2 - Flow (owner-authorized prompt) (times UTC)
- Same first_frame.png selected as START from the picker (top "first_frame.png" entry; preview verified); End empty; no
  audio. Settings read before send: Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100
  credits". Editor text vs flow_prompt_take2.txt with whitespace removed = identical (3839 chars). Single send.
- Submitted 16:15:42. 16:16:12 22%; 16:16:32 37%; 16:16:52 55%; 16:17:22 rendered. URL read 16:17:54; download 16:18:16.
  About 100 s. No reloads, no duplicate.
- Media id e8170422-751d-4940-890b-f885a63368c6 (Flow caption "Woman holding specimen and singing"). Files: `original_e8170422-751d-4940-890b-f885a63368c6.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 9a7056b689a77dd50fcc262540d04033c77bb6f271a899b131135ae6cca556f0. Cost 100 credits (200 total for this handoff).
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, video 8.000 s; disposable Veo audio AAC 48 kHz stereo 8.000 s.
  First generated frame vs first_frame.png: mean diff 1.08.

### Take 2 base review (contact_every6.jpg, crop_face_every2.jpg [1 s/row], crop_face_cut1/2/3_every2.jpg [frames 8-44,
    78-112, 138-184], crop_artifact_hands_every8.jpg, crop_chest_every24.jpg, keyframes_0_11_41_80_110_141_180_183.jpg)
- Identity/suit: same face, red bob; plain smooth silver high-neck suit throughout, no dials/hoses. Room unchanged.
  Camera locked (drift vs frame 0 only 0 -> 10 from her own motion, prev-3 diffs 0-1). No cut or reset.
- Artifact/hands: single fluted shell with spiral, same size/shape, low in both settled hands for all 8 s; no morph.
- Gaze: eyes up on the colleague for the whole take; never looks down. Head tilts to her side 2.4-4.4 s, level otherwise.
- Passage 1 "No, go on." (0.46-1.75 s): open vowel articulation 0.0-0.75 s (from the anchor's open mouth), then a BROAD
  toothy grin 1.0-1.7 s, opening again at 1.8 s. PASS (early; grin stronger than "modest").
- Listening 1.8-3.3 s: open-mouth toothy singing/laughing shapes 1.7-2.6 s (invented, prompt asked for no words here),
  then a smile with head tilt. Outside her cuts.
- Passage 2 "You did." (3.33-4.63 s): closed-lip knowing smile, head tilted, eyes up, one blink; lips part only at
  4.45-4.7 s. Mouth motion 1-4 per frame (small). FAIL on articulation, PASS on posture/gaze.
- Listening 4.7-5.8 s: mouth opens 4.5-5.0, singing shapes 5.0-5.8 s (early "Da-da-dum", invented before the cut).
- Passage 3 "Da-da-dum / Could've been." (5.875-7.67 s): open singing shapes with teeth 5.875-6.2 s, toothy smile
  6.2-6.7 s, open articulation again 6.75-7.3 s ("Could've been"), closing to a calm closed smile by 7.4 s; eyes up,
  frontal. PASS (the final "been" at 7.5-7.75 s in the guide lands on a closed mouth - Kling territory).
- Frame 180 (7.5 s, future B3 anchor): frontal, head level, eyes up, calm closed smile, hands/artifact stable. Good anchor.
- Warmth: broad toothy grin 1.0-1.7 s and open laughing shapes 1.7-2.6 s exceed "a little" warmth - report only.
- Gate: face/suit PASS, artifact/hands PASS, no cut PASS, articulation on all three passages FAIL (passage 2).

## Kling (times UTC) - job 86 on take 2 base
- Owner acceptance of take 2 given in chat ("use take two in a single clean pass"). Lip Sync editor: base.mp4 (take 2)
  uploaded as-is; one face detected, Character 1 = the exobiologist; Upload Local Dubbing -> guide.wav (0:00-0:08, gaps
  intact) -> playhead 0:00 -> Add Speech -> block spans 0:00-0:08 on the Character 1 lane; Sound from Video OFF (zoom
  verified); Generate quoted 10 credits.
- Submitted 16:22:23; "Task submitted / 0/1 Generating" 16:22:28, balance 361 -> 351. Checks 16:22:54, 16:23:14, 16:23:44,
  16:24:04, 16:24:24, 16:24:44, 16:25:15, 16:25:35, 16:25:55, 16:26:15, 16:26:47, 16:27:07, 16:27:27, 16:27:47, 16:28:17
  (creating); 16:28:37 "1/1 Generated". Download (Video, MP4, Without Watermark ON) clicked 16:29:37; filed 16:29:53.
  About 6 min 15 s. No reloads, no resubmission.
- Job id 86 (download name kling_20260908_Lip_Sync__86_0.mp4). Files: `original_kling_86.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 26ed64c2dec16db98ccb15877a24e57d826a290ffd58ecd199e597e393ef494f
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}]}
  => 1280x720, NATIVE 30/1 fps, 239 decoded frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both start 0.000.
  Not converted/cropped/trimmed/retimed; no separate remux made.
- Audio: normalized cross-correlation of the returned audio vs guide.wav = 1.00 at lag 0 (search +-0.1 s).
- Picture integrity vs base (per native frame, base re-timed to 30 fps for comparison only): whole frame mean 2.4 / max
  2.9; mouth box mean 3.3 / max 8.2; artifact+hands mean 2.3 / max 3.6; chest mean 2.6; window mean 3.5. Only the mouth
  region was re-rendered; artifact, hands, suit and room preserved; identity and teeth intact. Returned frames alternate
  duplicate/new (24 -> 30 fps pull-up), as with every Kling result so far.

### Sync checks (mouth_synced_cut1_src0.27-1.87s_native30.jpg, mouth_synced_cut2_src3.27-4.7s_native30.jpg,
    mouth_synced_cut3_src5.8-7.7s_native30.jpg = every 2nd native frame; contact_synced_every10_native.jpg)
- Cut 1 "No, go on." (source 11..42 = 0.46-1.75 s): open rounded "No" shapes 0.27-0.85 s with mouth interior, a brief
  closure ~0.9 s, then "go on" 1.0-1.5 s carried as open-then-smiling shapes with teeth, narrowing 1.55-1.7 s, opening
  again 1.73-1.87 s (the base's invented shape; guide is quiet there). USABLE: initial "No" reads clearly; "on" is soft.
- Cut 2 "You did." (source 80..111 = 3.33-4.63 s): 3.27-3.7 s closed-lip smile, head tilted (guide loud from 3.5 s);
  lips part slightly 3.73-3.85 s and again ~4.0-4.07 s with teeth; closed smile 4.1-4.4 s; open shapes 4.47-4.7 s (late
  - guide is silent at 4.5 and the other speaker starts 4.75). WEAK: "You" is barely a lip parting over the smile, "did"
  is a small shape; the strongest motion arrives after the word. Kling kept the base's closed smile, as it did on B1.
- Cut 3 "Da-da-dum / Could've been." (source 141..184 = 5.875-7.67 s): open singing shapes with teeth 5.8-6.3 s
  ("Da-da-dum"), smile 6.33-6.6 s, open shapes 6.67-7.2 s ("Could've"), closing 7.27-7.4 s, closed calm 7.47-7.7 s.
  USABLE for Da-da-dum and Could've; the final "been" (guide ~7.3-7.75 s) lands mostly on the closing/closed mouth.
- Outside her cuts: open shapes 1.9-2.3 s and 4.47-5.0 s follow the other speaker's context (must not be selected).
- No puppet lips, no new teeth artefacts, no face change; artifact preserved throughout.

## Defects (summary)
- Kling cut 2 "You did" under-articulated over the base's closed knowing smile.
- Kling cut 3 final "been" on a closing/closed mouth (~7.4 s on).
- Base take 2: broad toothy grin 1.0-1.7 s and open laughing shapes 1.7-2.6 s (listening window); early "Da-da-dum"
  5.0-5.8 s before the cut; head tilt 2.4-4.4 s.
- Take 1 (archived): looks down with closed mouth through "Could've been".

## Not done
- No third Flow, no second Kling, no A2/B3, no assembly, no FX, no production edits, no commit, no purchase. The Flow
  retry, its prompt edit and the Kling go-ahead on take 2 were owner-authorized in chat (2026-09-07). Codex verifies.
