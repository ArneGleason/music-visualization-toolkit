# RECEIPT: outro_B2_v2 (Flow base done; Kling WITHHELD for owner review)

Status: base_needs_owner_review. ONE Flow continuation generated from the supplied first_frame.png (= B1 base frame 155,
pixel-identical, mean diff 0.0). Downloaded untouched with a byte-identical base.mp4. Bounded review: face, plain suit,
artifact, hands, room and locked camera all PASS; passages 1 and 2 articulate; passage 3 ("Da-da-dum / Could've been",
source 141..184 = 5.875-7.67 s) does NOT: she articulates "Da-da-dum" EARLY at 5.0-6.0 s (mostly before the cut opens),
then holds a closed-lip smile and from ~6.85 s tilts her head and looks DOWN at the specimen through the whole
"Could've been" window (6.9-7.67 s) - no mouth motion, extended downward gaze during speech. That is a missing-articulation
failure on an assigned passage per base_gate.must_pass, so per the handoff Kling was skipped and no retry was made. The
owner may still accept this base for Kling (Kling re-renders the mouth; the downward gaze would remain) or order one retry.

## Inputs verified (SHA-256 match handoff.json)
- first_frame.png 8f7641bb6332a8291ce778fa75a9addd60bf636179955c3cbc6379185eadb4d5 (1280x720; equals ../outro_B1_v2/base.mp4 frame 155 exactly)
- continuation_base ../outro_B1_v2/base.mp4 2ed1a1b84dafd68a77b7141768ae580661a4039b83552fad54a1cdc1493c92b7 (not uploaded)
- approved_anchor ../outro_anchors_v2/exobiologist.png ea5bc2eb64dabc0601e33769876f3b035e594ae345ede604bc694833f04c5f0b (comparison only, not uploaded)
- flow_prompt.txt 674315f4caf44a47c9e832240feb560608012156647ec6d8ebf4a765b5fc5184 (4079 chars; pasted once via execCommand insertText; editor text vs file with
  whitespace removed = identical, 3505 chars; lock included verbatim)
- lock ../astronaut_reply_v1/style_lock_v2.txt 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide.wav ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004 (48 kHz mono PCM16, 8.000 s, 384000 samples; NOT used - Kling withheld). Energy (RMS per
  0.25 s): 0.0 1099 (tail of previous line), 0.25 229, 0.5-1.75 her "No, go on" (2341/514/1288/1732/772), 1.75-3.25 other
  speaker "Thought I heard something" (473/204/376/398/555/309), 3.25 silent, 3.5-4.5 her "You did" (2246/1567/1183/849),
  4.5-5.75 other speaker "Was it you?" (83/640/672/1017/2016), 5.75-6.75 her "Da-da-dum" (44/209/463/500), 6.75-7.25 "Could've"
  (1295/1240/473), 7.5-8.0 "been" + next line (2113/1711).

## Flow (times UTC)
- Fresh upload of first_frame.png via Add media > Upload (hooked file input), selected as START by real click on the
  top "first_frame.png" entry in the picker (preview verified: open-mouth exobiologist, bunk room); End empty; no audio
  upload. Settings panel read before send: Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100
  credits". Flow's "high demand" banner was showing. Single send via the Start generation button; no duplicate.
- Submitted 16:06:26. 16:07:05 28%; 16:07:25 44%; 16:07:45 no progress text (rendered). Tile URL read 16:07:53; curl
  download 16:08:13. About 80 s. No reloads.
- Media id 474079fc-bade-4422-9162-b409ce12c676. Files: `original_474079fc-bade-4422-9162-b409ce12c676.mp4` (untouched) and `base.mp4` (byte-identical), SHA-256 ed5f2e2fe7872b682bf1d0b50f8997887e654746a9de53935f5e14fc842f63be.
  Cost 100 credits.
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, video 8.000 s; disposable Veo audio AAC 48 kHz stereo 8.000 s.
  First generated frame vs first_frame.png: mean diff 1.1 (64x36).

## Base review (sheets: contact_every6.jpg, crop_face_every2.jpg [1 s per row], crop_face_cut2_every2.jpg [frames 78-112],
   crop_face_cut3_every2.jpg [frames 138-184], crop_artifact_hands_every8.jpg, crop_chest_every24.jpg,
   keyframes_0_11_41_80_110_141_180_183.jpg; traces below)
- Identity/suit: same face, red bob and fringe; plain smooth silver high-neck suit for all 8 s, no dials/hoses/patches.
  Room, window, lamps unchanged. Camera locked: whole-frame drift vs frame 0 rises only 0 -> 10 through her own motion,
  prev-3 diffs 0-1; no cut or reset.
- Artifact/hands: the single fluted shell with golden spiral stays low in both hands, same size/shape/spiral for the whole
  take; hands settled; no stroking, lifting or morph.
- Mouth motion trace (frame-to-frame mean abs diff in the mouth box, 24 fps): active 0.0-0.8 s (4-7), fading to ~2 by
  1.0 s; small 1.0-1.5 (2-4); quiet 2.0-3.0 (0.2-2.9); ACTIVE 3.05-3.35 s (3.9-8.7); quiet 3.4-4.6 (1-2); rising 4.7-5.0
  (3-4); ACTIVE 5.1-5.6 (5-9) and 5.6-6.1 (3-5); quiet 6.1-6.6 (0.5-2); 6.7-7.3 s values 3-10 are the HEAD TILT DOWN, not
  lip motion (closed lips in the strip); 7.4-8.0 quiet.
- Passage 1 "No, go on." (cut 11..42 = 0.46-1.75 s): open vowel shapes with mouth interior 0.0-0.9 s (starts before the
  cut, from the anchor's open mouth), then a warm closed smile with small lip motion and a brief teeth-visible smile
  ~1.7 s. Readable articulation inside the cut for 0.46-0.9 s; the "on" ending is a smile. PASS (early, warm).
- Passage 2 "You did." (cut 80..111 = 3.33-4.63 s): eyes on camera, open articulation with upper teeth 3.05-3.9 s, small
  knowing smile; from 4.0 s the eyes drop to the specimen with a closed smile until 5.0 s (inside the cut's second half).
  PASS with note (articulation early in the cut, downward glance after).
- Passage 3 "Da-da-dum / Could've been." (cut 141..184 = 5.875-7.67 s): "Da-da-dum" is articulated 5.0-6.0 s with teeth
  (mostly BEFORE the cut opens at 5.875); 6.0-6.85 s closed-lip smile, no motion; 6.85-7.67 s head tilts down and she
  gazes at the specimen with a closed smile - NO articulation for "Could've been" and none for the final "been". FAIL
  (missing articulation on an assigned passage + extended downward gaze during her line).
- Warmth: closed-lip smiles between lines, one brief toothy smile at 1.7 s; not a fixed grin - within tolerance.
- Frame 180 (7.5 s, future B3 anchor at song 4500): hands/artifact stable, suit plain, but head tilted down, eyes on the
  specimen, mouth closed - a continuation from it would start looking down.
- Gate result: face/suit PASS, artifact/hands PASS, no cut PASS, articulation on all three passages FAIL (passage 3).

## Kling
- NOT submitted (gate failure). No credits spent; balance remains 361.

## Not done
- No retry, no Kling, no A2/B3, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.
