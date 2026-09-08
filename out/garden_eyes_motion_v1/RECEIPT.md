# RECEIPT: garden_eyes_motion_v1

Status: DONE - one Flow plate generated, downloaded and inspected across all 192 frames. Usable with a caveat inside the proposed
window and an unusable late handle (details below). No Kling, no audio, no retry, no assembly, no production/cue changes, no commit.
Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/forest_fauna_eyes_a.jpg`: A37ECA9B1095B798E1C9B4591073516680C998E02E5C162BAE88458D8F55CBFE (approved still, unedited; Start slot only, End verified empty)
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496; prompt `flow_prompt.txt` (3793 chars incl. the lock) pasted verbatim once; prompt SHA-256 6B22DAED5099448E6642DE7914C31DF5D7C1A422B71AF1A1AB6871CF232673D4

## Flow (actual, times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, "Generating will use 100 credits"; chip 720p.
  Start = `forest_fauna_eyes_a.jpg` (slot id 2f961916).
- Submitted 14:30:21. Displayed progress: 14:30:31 5%; 14:31:03 32%; 14:31:21 45%; 14:31:39 no percentage (complete); tile video
  URL read 14:32:14; download 14:32:36. Generation about 75 s. Checks at 10 s, 42 s, then every ~18 s. No reloads, no resubmission.
- Result media id c824584b-78d2-4ff3-b14c-7aba5d80af73 (Flow caption "Alien creatures waking in garden"); downloaded via the tile's
  signed flow-content video URL. Files: `original_c824584b-78d2-4ff3-b14c-7aba5d80af73.mp4` (untouched) and `base.mp4`
  (byte-identical), SHA-256 7DFD214C4608C4E7B91739C93AA3E4B02294A531AA2D393F8BDA14E3108E3B17
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 video frames, start 0.000, video 8.000 s; disposable Veo audio present. No watermark. Cost 100 credits.
- First frame vs approved still: mean pixel difference 1.7 (64x36; the scene is very dark, so this is within noise of identical).

## Inspection (contact_every6.jpg; contact_every6_brightened.jpg and contact_0.5-3.9s_every4_brightened.jpg are brightness x2.2 for
   reading only; per-3-frame difference trace)
- Camera: locked. Framing, path and foliage layout hold; the difference against frame 0 stays at 2.5-7 for the whole take
  (dark scene), with no camera drift, zoom, cut or transition.
- Darkness, palette and foliage occlusion: preserved. No overall brightening; no dust, sparks, particles, flashes or pulses added.
- Foliage: foreground leaves and mid-distance fronds sway gently and continuously (layered motion, no melting) from the first frame.
- Creatures, 0.5-3.4 s (source frames 12-82): genuinely alive. The amber-eyed creature low left squints/blinks at ~1.5-1.7 s and
  shifts its weight; the cyan pair high left tilts and drifts slightly; the pink pair right turns toward centre; the turquoise pair
  lower right shifts and rises a little; the small distant pairs make quiet independent shifts. Each pair stays attached to its own
  hidden head, no exposed bodies, no teeth, no new mouths. Eye colours unchanged. This is real head/creature motion, not blinking or
  a camera move.
- DEFECT inside the proposed window, 3.4-3.9 s (frames ~82-93): the amber-eyed creature walks left and leaves the frame; by frame
  88-92 its eyes read as one bright amber blob at the left frame edge (looks detached). Recommend ending the visible cut by
  source frame ~82 or accepting a leftward exit in the last 11 frames of [12,93).
- Late take, 4.0-8.0 s (frames 96-192): UNSUITABLE as a handle. The amber creature is gone, the pink pair migrates to the upper
  right, and from ~5.5 s new pale white/violet eye pairs appear low in the frame (new creatures, changed colour set), i.e. the
  count and colours drift from the reference. Foliage motion remains fine, but the creature layout no longer matches the still.
- Useful interval: [0,82) clean (3.4 s); [82,93) usable only if the amber exit is acceptable; [93,192) not recommended.
  The requested 99 exit frames are therefore not usable as same-layout footage.

## Weaknesses (summary)
- Amber creature exits frame left from ~3.4 s (edge blob 3.7-3.9 s).
- New eye pairs and colour drift after ~5.5 s; amber pair absent after 4 s.
- Otherwise: locked camera, coherent layered foliage, staggered creature awakening in the first 3.4 s, no effects baked.
- Not done: no Kling, no retry, no assembly, no cue/shotlist edits, no commit. Protected static composite remains the fallback.
