# RECEIPT: garden_walk_return_v1

Status: DONE - one Flow take generated from the supplied extracted frame, downloaded and inspected across all 192 frames.
Proposed window source [12,72) is usable with one defect (foreground frond crossing the face, see below). No Kling, no audio,
no retry, no assembly, no production/cue edits, no commit. Writes only under this folder.

Note for the owner/Codex: the start frame is a frame extracted from a Veo-rendered clip (clips/raw/forest_walk_track_v6.mp4
frame 144), used deliberately per CLAUDE_HANDOFF.md. This departs from the owner's 2026-09-05 rule that only ChatGPT/Codex
stills feed Flow; it was executed as instructed and is flagged here rather than silently.

## Inputs verified (SHA-256 match handoff.json)
- first frame `out/garden_walk_return_v1/first_frame.png`: 31DD376C573D3E26C532D491ECC84907E6586853EA51474123C3182E5C23BA77 (1280x720 PNG; Start slot only, End verified empty; no other upload)
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496 (contained verbatim in the prompt)
- prompt `flow_prompt.txt` (3657 chars) pasted once with execCommand insertText; SHA-256 4DFBCB0C01109568DE9D9190832F5A8E1E42CFD7D5A0DFAD40C8745A5505B831.
  `codex/out/forest_walk_track_b.jpg` was NOT uploaded (continuity reference only).

## Flow (actual, times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
  Start = first_frame.png (uploaded via Add media > Upload; asset thumbnail id 006f6c1b).
- Submitted 15:19:06. Progress: 15:19:36 21%; 15:20:04 45%; 15:20:24 no percentage (complete). Tile video URL read 15:20:39;
  download finished 15:20:58. Generation about 78 s. Checks at 30 s, then ~28 s and ~20 s; no reloads, no resubmission.
- Result media id a136a80f-ca0c-4e24-959f-631264d09077 (Flow caption "Woman walking in alien garden"); downloaded via the
  tile's signed flow-content URL. Files: `original_a136a80f-ca0c-4e24-959f-631264d09077.mp4` (untouched) and `base.mp4` (byte-identical), SHA-256 834C5CAC6D8DDC7E8140DC3B44EBCE95A4400D20B30C9C3FB5B0514C62EADCA2
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 video frames, start 0.000, 8.000 s; disposable Veo audio track present (no audio uploaded).
  No watermark. Cost 100 credits. No crop/trim/retime/stabilize/effects.
- First frame vs first_frame.png: mean pixel difference 1.7 (64x36) = matches.

## Inspection (contact_every6.jpg full take; contact_0.5-3.0s_every4.jpg window; crop_window_f12-72_every3.jpg and
   crop_exit_f72-192_every8.jpg are 560px-wide figure crops; per-3-frame difference trace)
- Motion starts immediately: she is mid-stride at frame 0 and keeps walking screen-right for the entire take, feet planting on the
  path with believable weight transfer, no stops, no posing, lips at rest, gaze along the path with a small glance ahead.
- Likeness/costume/prop: copper curls, plain silver suit, brass lantern in the near (left) hand with a modest natural swing, all
  stable across 192 frames. No extra limbs, no hand weirdness, no costume changes, no talking. The forward arm swings naturally.
- Camera: smooth lateral track with her, gradually easing wider from ~1 s onward (physical widening, no zoom snap, no angle
  change, no cut). Per-3-frame difference is large (12-26) throughout because the whole frame tracks; the trace is smooth with no
  spike, i.e. no cut or morph.
- Green distant light stays a small background dot.
- DEFECT inside the proposed window, ~1.1-2.8 s (frames ~27-66): a soft foreground fern frond enters from the right and sweeps
  across her; its blades cross her legs at frames ~30-45, then her torso and face at frames ~45-66 (head largely covered around
  frames 57-63). She remains visible and walking behind it, but the face is obscured for roughly 0.7 s. Frames 12-27 and 66-72 are
  clear. Whether this is acceptable "foliage drift" or a defect is Codex/owner's call; I flag it.
- Exit handle, 3.0-8.0 s (frames 72-192): walking, likeness and lantern remain clean. From ~4.0 s (frame ~96) the widening
  reveals a NEW large pale teardrop hanging lamp at top right, which grows to a dominant bright element and sits behind her head
  around frames 128-144; from ~6.3 s (frame ~152) a pale blue misty depth and further round lanterns appear, so the panorama
  drifts from the start frame's garden. Frames 72-96 are clean (frond clears by ~frame 78); frames 96-192 usable for walking
  continuity but carry the invented big lamp / wider garden.
- Useful intervals: [0,27) clean; [27,66) frond crossing (face obscured ~57-63); [66,96) clean; [96,192) clean performance with
  changed composition (new large lamp, wider panorama). Requested exit handle of 120 frames exists but is not defect-free.

## Not done
- No Kling, no audio, no retry, no assembly, no cue/shotlist/plan edits, no commit, no owner approval claimed.
