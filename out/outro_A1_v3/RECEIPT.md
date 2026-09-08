# RECEIPT: outro_A1_v3 (single authorized retry, BASE ONLY)

Status: FLOW BASE DONE - one take generated from the same approved first frame as v2, downloaded untouched and inspected
across all 192 frames. v2 media and receipt untouched. Result is a clear improvement toward "mission accomplished": relaxed
mouth corners through the question and "Never mind", real open articulation, a composed acknowledging settle with a small
nod, the TV's single brief static response with reflected light on her face (now allowed), locked camera, identity intact.
Remaining notes for review: a moderate smile with visible teeth creeps in during the sung run (~4.6-6.0 s, milder than v2's
grin), the TV glance is still a ~1.5 s head turn, all phrases run ~0.5-1 s ahead of the approximate windows, and in the last
0.4 s she looks down and a hand rises toward the table. No Kling, no B1/A2, no retry, no assembly, no production edits,
no commit. STOPPED after the base.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: 242b884af3a06ae3410ba695e87dc47786269303ceb7b744fb21b7a50e6c089c (1280x720; byte-identical to out/outro_A1_v2/first_frame.png, so the
  existing Flow library copy - thumbnail id 96a0762e - was selected by a real click; generated first frame matches, mean diff
  0.8 at 64x36). Approved anchor `out/outro_anchors_v2/astronomer.png` (bb733e52548540403d7b4f3a5d4303999d65a8af71e7ff3317acb9565de1ebab) verified,
  not uploaded. End slot verified empty; no audio upload.
- prompt `flow_prompt.txt` (v3): a446ee8ecba1ce34fd794dd134ad2f137bc3c86e74b1437024fd236996f5ab12 (4704 chars) pasted once with execCommand insertText; editor text
  compared to the file with whitespace removed = identical; lock included verbatim and unedited. v2 prompt not used.
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC; local = UTC-4)
- Flow's "high demand" banner was showing; the single submission succeeded, no retry.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
- Submitted 14:22:09. Progress 14:22:39 20%; 14:22:59 38%; 14:23:19 54%; 14:23:39 71%; 14:24:04 93%; rendered by 14:24:14.
  Tile URL read 14:24:26; download 14:24:50. About 2 min 5 s. Checks at 30 s, then 20 s, 10 s near completion; no reloads,
  no resubmission.
- Media id 5a714c7e-042e-4fdf-9b9e-921e60f2a4ae. Files: `original_5a714c7e-042e-4fdf-9b9e-921e60f2a4ae.mp4` (untouched, download filename kept) and `base.mp4`
  (byte-identical), SHA-256 99124a5780cd629cb086e9d362db2e1d78bb5afa2a9d89ca41fc09a428c13767
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720 16:9, 24/1 native, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio (AAC 48 kHz stereo) kept.
  No watermark, no crop/trim/retime. 100 credits.

## Inspection (crop_face_every2.jpg = every 2nd frame, 12 per row = 1 s per row; crop_tv_every8.jpg; contact_every6.jpg;
   keyframes_0_24_48_96_155_191.jpg; TV-luma, face-luma, mouth-motion and hand-motion traces)
- Identity/outfit/props: same face, red updo, tweed coat, checked shirt, mustard cardigan, desk, lamp, orrery, chart,
  specimens, TV; no spacesuit; no extra people; no captions. Camera locked (difference vs frame 0 stays 1-4 apart from the
  TV response; no cut, zoom or reset).
- 0.05-1.0 s: "You still there?" - open vowels and consonant closures, face near-frontal, mouth corners relaxed, gaze
  focused. Reads as a calm check, not alarm and not a smile. (Runs earlier/shorter than the 0.44-1.81 window.)
- 1.0-1.3 s: closed lips, a faint private half-smile, then the eyes and head shift toward the TV.
- 1.3-2.9 s: head turned toward the TV (3/4 profile) - still a ~1.5 s turn rather than an eye-shift, but shorter than v2's;
  mouth closed; the TV's static response lands here (see below) and reflected light lifts her face (face luma 55 -> 64 at
  2.0-2.3 s) - plausible and useful.
- 2.9-3.9 s: back to frontal; "Never mind" with dry understatement - open shapes, relaxed corners, no apologetic smile.
- 4.0-6.0 s: "La-la-la, low light" - generous open vowels with upper teeth/mouth interior; from ~4.6 s a moderate smile
  builds (raised cheeks, teeth visible in a few frames 5.0-5.6 s). It is a smiling sung phrase, noticeably milder than v2's
  broad grin, but not fully the "relaxed corners" asked for. Flag for owner judgement.
- 6.0-7.4 s: settles into a closed-lip, composed small smile with a slight acknowledging nod - the intended "mission
  accomplished" beat; eyes alert. Frame 155 (6.46 s) is frontal, closed-mouth, hands low, TV dim: a clean A2 anchor.
- 7.4-8.0 s: she looks down toward the table and a hand rises into the lower frame reaching toward the specimens
  (f182-191) - an end-of-take reach the prompt excluded; hands are low and still for the rest of the take.
- TV: dark amber-gray 0-1.9 s; single brief phosphor/static response ~2.0-2.5 s (luma 32 -> 207), fading back to dim by
  ~2.7 s; thereafter dim and stable (luma 38-39 vs 32 at start), curved glass and bezel intact, never occluded. This matches
  the "welcome brief response" and is not counted as a defect. No text, symbols or programme content.
- No prop/hand morphing, no gesture repeat, no reset.

## Defects (summary)
- Moderate smile with visible teeth during the sung run ~4.6-6.0 s (milder than v2, not fully relaxed corners).
- TV glance is a ~1.5 s head turn (1.3-2.9 s) rather than a brief eye shift; face 3/4 for part of the first visible cut.
- Phrases run ~0.5-1 s ahead of the approximate windows (question 0.05-1.0; Never mind 2.9-3.9; la-la-la 4.0-6.0).
- Looks down and reaches a hand toward the table 7.4-8.0 s (last visible cut ends at source 166 = 6.9 s, so outside it).

## Not done
- No Kling, no B1/A2, no retry, no assembly, no production edits, no commit, no purchase, no owner approval claimed.
