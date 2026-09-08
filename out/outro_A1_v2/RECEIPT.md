# RECEIPT: outro_A1_v2 (BASE ONLY)

Status: FLOW BASE DONE - one take generated from first_frame.png, downloaded untouched and inspected across all 192 frames.
Returned for review with defects: the performance is alive and articulated (real singing/speech on the voiced intervals,
quiet listening gaps, locked camera, identity and outfit intact, hands low), BUT (1) the TV screen flashes to bright white
static from ~1.75 s to ~2.5 s, which the prompt explicitly forbade, and (2) the singing is delivered with a wide toothy smile
rather than a restrained half-smile. Also the "glance toward the TV" becomes a 2-second head turn. No Kling, no B1/A2, no
retry, no assembly, no production edits, no commit. STOPPED after the base as instructed.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: 242b884af3a06ae3410ba695e87dc47786269303ceb7b744fb21b7a50e6c089c (1280x720; uploaded fresh via Add media > Upload; chosen from the
  library files named first_frame.png by its astronomer-study preview; thumbnail id 96a0762e; generated first frame matches,
  mean diff 0.8 at 64x36). Approved anchor `out/outro_anchors_v2/astronomer.png` (bb733e52548540403d7b4f3a5d4303999d65a8af71e7ff3317acb9565de1ebab)
  verified, not uploaded. End slot verified empty; no audio upload. Old A1 media/prompt not used.
- prompt `flow_prompt.txt`: f45a4e5bf5ebd16922a0ebd0be30a6379b005842c5affc6c5e5c66e701ee3ed9 (4249 chars) pasted once with execCommand insertText; editor text compared
  to the file with whitespace removed = identical; lock included verbatim and unedited.
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC; local = UTC-4)
- Flow's "high demand" banner was showing; the single submission succeeded, no retry.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
- Submitted 13:48:28. Progress 13:48:58 21%; 13:49:18 38%; 13:49:38 55%; rendered by 13:49:58. Tile URL read 13:50:00;
  download 13:50:27. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id 55959967-d030-4f7a-97f9-906e72fa01b6 (Flow caption "Astronomer performing musical sc..."). Files: `original_55959967-d030-4f7a-97f9-906e72fa01b6.mp4`
  (untouched, download filename kept) and `base.mp4` (byte-identical), SHA-256 5783b45cf3d16997d62b59bd5418291fe3ec3a9dcb5021fb871106d3817eb8d3
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720 16:9, 24/1 native, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio (AAC 48 kHz stereo) kept.
  No watermark, no crop/trim/retime. 100 credits.

## Inspection (crop_face_every2.jpg = every 2nd frame, 12 per row = 1 s per row; crop_tv_every8.jpg; contact_every6.jpg;
   keyframes_0_24_48_96_155_191.jpg; TV-luma, mouth-motion and hand-motion traces)
- Identity/outfit/room: same face, red updo, tweed coat, checked shirt, mustard cardigan, desk, lamp, orrery, specimens, chart
  and TV; no spacesuit; no extra people; no captions. Camera locked (difference vs frame 0 stays 1-3 except the TV flash).
- Mouth activity vs the choreography (source seconds):
  * 0.05-1.20: speech shapes with open vowels - "You still there?" (starts a little early vs 0.44, ends ~1.2 vs 1.81).
  * 1.20-3.25: LISTENING gap - mouth closed. But the "brief glance toward the TV" becomes a full head turn to screen right held
    from ~1.2 s to ~3.2 s (3/4 profile, face less readable); she returns frontal at ~3.3 s.
  * 3.3-4.0: frontal, a broad smile with teeth builds; small mouth motion ~2.9-3.3 then articulation resumes ~3.9.
  * 3.9-7.3: continuous voiced articulation - "Never mind" then the "La-la-la, low light" run: wide open vowels with mouth
    interior and teeth visible, eyebrows lifting, head gently swaying on a slow pulse (no per-syllable bobbing). Articulation
    is generous and real - a good Kling base - but delivered with a WIDE TOOTHY SMILE through 4-7 s (prompt asked for at most
    a fleeting half-smile, no teeth display).
  * 7.3-8.0: mouth closes, she smiles and looks down; hands begin to lift/gesture at ~7.7 s (f186+), otherwise hands stay low
    and still for the whole take, no specimen fiddling, nothing crosses the face or TV.
- TV screen: dark amber-gray and stable 0-1.5 s; DEFECT - from ~1.75 s (f42) it lights up to bright white static/noise
  (screen luma 32 -> 200), peaking ~1.9-2.3 s, then fades back by ~2.6 s (f62); thereafter dim and stable but slightly
  brighter than the start (luma ~43 vs 32), still unobstructed with bezel and curved glass intact. The flash sits inside the
  first visible cut (source 12..67).
- Frame 155 (6.46 s): frontal, mid-phrase open mouth with smile, hands low, TV dim - continuity is fine for a later A2 anchor,
  but it is mid-word; Codex should pick a closed-mouth neighbour if a static anchor is wanted.
- No cuts, no gesture reset, no prop/hand morphing, no scope graphics, no text.

## Defects (summary)
- TV screen flashes to bright white static 1.75-2.6 s (forbidden; inside visible cut 12..67).
- Wide toothy smile during the sung run 4-7 s and at 3.5-4.0 s (prompt: no big smile/teeth display).
- Head turned to the TV for ~2 s (1.2-3.2 s) instead of a brief glance; face 3/4 profile in part of the first visible cut.
- Hands start moving at 7.7 s (last ~7 frames).
- Voiced phrase 1 runs 0.05-1.2 s (earlier/shorter than 0.44-1.81).

## Not done
- No Kling, no B1/A2, no retry, no assembly, no production edits, no commit, no purchase, no owner approval claimed.
