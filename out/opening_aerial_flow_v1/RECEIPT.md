# RECEIPT: opening_aerial_flow_v1

Status: DONE - one Flow aerial take generated from first_frame.png (horizon view) as the sole Start frame, downloaded untouched
and inspected across all 192 frames with a per-frame sky/horizon trace. PASSES the quality gate: the forward glide and downward
pitch begin at frame 0 and the useful viewpoint change is complete inside the first 3.208 s (source 0..77); terrain, waterways,
domes and oasis stay coherent; no people, craft, flashes or glowing objects. Caveat: the horizon does not leave the frame
entirely - a thin sky band (~7% of frame height) stays at the top for the whole take, so the destination is a steep oblique
rather than the fully map-like angle of the reference. No Kling, no audio, no green-light FX, no retry, no assembly, no
production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: e309d2faecfcd09aa82e8e5a305faf0dd6b0ded31540c5eaf2fd01658cc977c7 (1672x941, 16:9; uploaded fresh via Add media > Upload; chosen from the
  five library files named first_frame.png by its horizon-aerial preview, thumbnail id b9c16943; generated first frame matches,
  mean diff 1.2 at 64x36).
- composition reference `downward_reference.png`: 8bb70b4b8f0adb2147c2125c3f62b555f1c184e1c6e08188898ae5c7aca80810 - inspected only (steep near-map oblique over the
  same river region with the oasis lower right); NOT uploaded, not used as End frame or ingredient. End slot verified empty.
- prompt `flow_prompt.txt`: 0e3a5ac41d738c08908e6ef5892167853f7632e07cc24e6c18c8d9ae759ff00f (3097 chars) pasted once with execCommand insertText; editor text compared to
  the file with whitespace removed = identical; lock included verbatim and unedited.
- lock `style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- No audio input.

## Flow (times UTC; local = UTC-4)
- Flow showed its "high demand ... requests may need to be retried" banner; the single submission succeeded, no retry.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
- Submitted 12:14:12. Progress 12:14:42 21%; 12:15:02 38%; 12:15:22 53%; rendered by 12:15:42. Tile URL read 12:15:54;
  download 12:16:21. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id fc50c6a7-0cee-4e38-9834-76ec9be0a496. Files: `original_fc50c6a7-0cee-4e38-9834-76ec9be0a496.mp4` (untouched) and `base.mp4` (byte-identical), SHA-256 01634208e0a5ab30df26b11ea9b6bd208b1a7e744d10fe54a995cc3a44176f0e
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark. 100 credits.

## Inspection (contact_every6.jpg; frames_0-3.3s_every4.jpg = frames 0-76 every 4; keyframes_0_24_48_77_120_191.jpg;
   luma drift trace; sky-band trace; oasis-centroid trace)
- Frame 0: matches the start image - wide horizon-facing aerial, mountains on the horizon, planet and moon top right, oasis
  centre, branching blue-green rivers.
- 0.0-1.0 s (f0-24): the glide is already under way; the sky band shrinks from 21% to 19% of frame height; planet/moon drift up
  and out by ~1.5 s; foreground ridges begin to slide down/toward camera (parallax visible).
- 1.0-2.0 s (f24-48): the tilt steepens; sky band 19% -> 13%; the oasis grows and drifts toward the lower left; near settlements
  slide past below.
- 2.0-3.2 s (f48-77): sky band 13% -> ~7% (rows 24 -> 12 of 180); at 3.208 s (frame 77) the view is a closer, steeper oblique with
  the oasis and its domes large in the lower half, river bends reading like a map, mountains reduced to a thin strip at the
  top edge. Useful viewpoint change complete within the 77-frame insert. Per-3-frame difference is a steady 9-15 (measured,
  continuous pace; no acceleration, whip, roll or cut).
- 3.2-8.0 s (f77-191): gentler continued glide forward/left over the oasis and waterways; the oasis passes beneath and drifts
  back toward centre-right by 7-8 s; the frame stays a steep oblique with the thin sky band constant (~7-8%). Coherent B-roll.
- Terrain/architecture: ridges, rivers, cream/turquoise domed settlements, bridges and the palm oasis remain stable and
  consistent; foreground detail resolves as the camera approaches, no morphing, no erupting buildings, no new characters,
  spacecraft or light objects. Subtle water shimmer only. No text.
- Deviation to note: the horizon never fully exits the top of frame; the final angle is steep-oblique, not the fully downward
  near-map view of downward_reference.png (which was directional only).

## Quality gate
- First frame, 1 s, 2 s, 3.2 s and full clip inspected; contact sheets saved: done.
- Horizon visible initially; purposeful progress and increasingly downward view within 3.208 s: PASS (thin sky band remains).
- Terrain/waterways/domes/oasis stable, no morphing or added objects: PASS.
- Destination directional, minor composition differences: acceptable; recorded above. No retry.

## Not done
- No Kling, no audio, no green glimmer/FX (left to Codex), no retry, no assembly, no production edits, no commit, no purchase,
  no owner approval claimed.
