# RECEIPT: archaeology_discovery_v1

Status: DONE - one Flow take generated from first_frame.png, downloaded untouched and inspected across all 192 frames.
The proposed window [12,92) (0.5-3.83 s) contains the requested choreography in order: two brush strokes, brushing stops, a
fingertip check. The specimen stays embedded and unchanged through that window. Two defects: the camera is NOT locked (slow
push-in over the take) and from ~6.0 s both hands cup/grasp the specimen as if to lift it, so the late exit handle is unusable.
No Kling, no audio, no retry, no assembly, no FX, no production edits, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `first_frame.png`: 1f5e2ea0d4881dce1abe8491351e9178606fd9ddcccc84b61611aa0ea5188850 (1280x720; uploaded fresh via Add media > Upload; chosen from the two
  library files named first_frame.png by its excavation preview; the generated first frame matches it, mean diff 1.3 at 64x36).
  The old conical excavation prop image was not used. generated_reference.png and the continuity still were not uploaded.
- prompt `flow_prompt.txt`: 0792afc2534a2728bad1d1577494bf40fa6da9019827eeae7bf0acc9f41847d0 (3871 chars) pasted once with execCommand insertText; editor text compared
  to the file with whitespace removed = identical. Includes the lock verbatim.
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- End slot verified empty.

## Flow (times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". Flow still showed its "high demand" banner; the single submission succeeded, no retry.
- Submitted 19:23:50. Progress 19:24:20 21%; 19:24:40 38%; 19:25:00 55%; 19:25:20 tile rendered (complete). Tile URL read
  19:25:31; download 19:25:55. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id 9cafc314-0ddd-48bb-ae02-cd58b8176307. Files: `original_9cafc314-0ddd-48bb-ae02-cd58b8176307.mp4` (untouched) and `base.mp4` (byte-identical),
  SHA-256 2d4b3e894a0556b8ee691e7f4c70a25c5a25bf83146d9580b5963fa0724c9576
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio (nothing uploaded). No watermark. 100 credits.

## Inspection (contact_every6.jpg full take; crop_specimen_brush_0-4s_every3.jpg = frames 0-93 every 3; crop_specimen_brush_4-8s_every8.jpg;
   crop_specimen_close_every12.jpg = tight specimen crop every 12 frames; per-3-frame drift and region traces)
- Camera: NOT locked. A slow, steady push-in/tilt runs through the whole take: the specimen grows from roughly 120 px to ~170 px
  across in the fixed 240x200 crop, the top-of-frame band (water/body) differs from frame 0 by 28 by 3.5 s and stays there, and
  the difference vs frame 0 rises monotonically (0 -> 25) with no cut or spike. Smooth, but it contradicts "locked camera".
- Specimen: same fluted clear shell with a golden spiral for the whole take; no morphing, growth or new detail. It stays fixed in
  the ground from 0 to ~6.0 s. The spiral is readable from frame 0 (the start frame already exposes the upper shell) and reads
  cleaner after the second stroke (~2.0 s); the lower edge is visibly clear of soil by ~2.5 s.
- Actual action timing (source seconds, 24 fps):
  * 0.00-0.40: brush already at the specimen's left edge; small preparatory move.
  * 0.40-0.90 (f10-21): STROKE 1 - bristles pass over the specimen's upper face from left toward the right/outward; bristle
    contact with the shell and soil is visible (f15-21).
  * 0.90-1.25: brush returns left.
  * 1.25-1.90 (f30-45): STROKE 2 - second pass over the shell face, same direction, bristles in contact; loose dust moves off
    the surface. No cloud, sparks or blowing sand.
  * 2.00-2.75 (f48-66): brushing stops; the brush is withdrawn to the left and SET DOWN on the ground (~2.9 s) rather than held
    just clear - a small deviation.
  * 2.75-3.25 (f66-78): the free (right) hand comes in from the right, index finger extended.
  * 3.25-3.90 (f78-93): FINGERTIP CHECK - fingertip touches the specimen's right edge without shifting it. This is the
    recognition pause; it lands at the end of the 2.25-3.83 window.
  * 3.90-5.70 (f94-136): calm hold with the fingertip resting at the edge; small breathing movement. Good.
  * 5.70-6.00 (f136-144): right hand withdraws, then BOTH hands come in from the sides.
  * 6.00-8.00 (f144-191): both gloved hands cup/grasp the specimen's sides and slide under it; by ~7.7 s it is held between the
    hands as if about to be lifted. It has not left the ground in the last frame, but the pose is a lift. Violates "never lift";
    not usable.
- Hands/brush: gloves and fingers stay plausible; the brush keeps its shape; no morphing tools. The free hand rests clear of the
  specimen until 2.75 s as asked, then does the fingertip check.
- Proposed window [12,92) (0.5-3.83 s): usable choreography (stroke 1, stroke 2, stop, fingertip check) with the specimen in
  place. Caveats inside the window: the slow push-in, and the brush being set down at ~2.9 s.
- Usable coverage: [0,136) (0-5.7 s) with the push-in caveat; [136,192) unusable (grasp/lift pose).

## Defects (summary)
- Camera pushes in slowly across the take (not locked).
- Both hands grasp the specimen from ~6.0 s (lift pose) - exit handle beyond 5.7 s unusable.
- Brush set down on the ground at ~2.9 s instead of held just clear.
- Otherwise: specimen fixed and unchanged 0-6 s, two contact strokes, fingertip check, no FX baked, no new characters.

## Not done
- No Kling, no audio, no retry, no assembly, no FX, no production edits, no commit, no owner approval claimed.
