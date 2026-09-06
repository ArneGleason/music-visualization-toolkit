# RECEIPT: specimen_mismatch_v2

Status: DONE - one Flow take generated, downloaded and inspected across all 192 frames. Usable with caveats: 49+ consecutive clean
frames of separated flat rotation exist ([54,103) recommended; the manifest's [48,97) includes a lifted/edge-on piece at its start).
No Kling, no retry, no assembly, no production/cue changes, no commit. Writes only under this folder. v1 untouched.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/canal_map_macro_b.jpg`: 369C2AB8AF78FFB7CA833CB1A37933D954615980F81AA2AA41E578B7F5316828
- prompt `flow_prompt.txt`: 88926D512F95FA1F3E3E34BC090F386E9F3B863DB6FAC45C110EA90CE0923724 (3720 chars incl. the unchanged lock) pasted verbatim, once; lock: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496
- Start slot only (End verified empty); no generated-video frame used.

## Flow (actual)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, "Generating will use 100 credits"; chip 720p.
  Start = `canal_map_macro_b.jpg` (slot id a175ce12).
- Submitted once at 2026-09-06T04:22:45Z (00:22:45 local). Status checks per manifest: 60 s -> 59%; 85 s -> complete. Downloaded at
  once. Cost 100 Flow credits as quoted. No second submission.
- Result media id fb33cbdf-70cb-4243-90cd-2c1ce7e89c75 (Flow caption "Woman's hands rotating desk frag..."); downloaded via the tile's
  signed flow-content video URL. Files: `original_fb33cbdf-70cb-4243-90cd-2c1ce7e89c75.mp4` (untouched) and `base.mp4` (byte-identical),
  SHA-256 1B26A031346EC59D5107C2718BEC697D1FE1C1D981D51B4A393D8CF4151A2ABA
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; disposable Veo audio present. No watermark.
- First frame vs approved still: mean pixel difference 1.2 (64x36).

## Inspection (contact_every6.jpg full frame; contact_1.25-4.1s_every3_centre.jpg and contact_4.0-6.2s_every3_centre.jpg centre crops;
   per-3-frame difference trace)
- Camera: straight-down overhead for all 192 frames, no tilt, orbit, cut or dissolve. One continuous push-in, but MUCH stronger than
  the requested ~10%: by 4 s the frame is roughly 1.5x tighter and by 8 s roughly 2x (the outer ring of fragments leaves frame; the
  brass instruments and spectrum card exit by ~2.5-4 s). Objects scale with the camera only; no growth relative to each other.
- Action timing (source seconds):
  0.0-1.2 hands lift both central fragments and slide them apart; 1.25-2.0 the fragments are held UP, edge-on/tilted in the fingers
  (against "flat on the desk"); ~2.0-2.1 (frames 48-51) the left fragment reads pale/whitish for a few frames as it is set down (a
  highlight or brief material wobble, geometry unchanged); 2.25-4.0 both fragments flat on the leather, separated by roughly a
  finger-width gap, turned slowly with fingertips (left counter-clockwise, right clockwise), natural pauses; 4.0-5.4 the fragments
  sit side by side nearly touching (the gap closes, but they never interlock, overlap or snap); 5.5-6.1 fingertips settle and
  release; 6.0-6.6 both hands withdraw downward toward the frame edge (against "no hands exiting"; fingertips remain at the bottom
  edge); 6.6-8.0 fragments rest apart at different orientations, camera still pushing.
- Around 5 s (the v1 complaint region): no joining, no snapping, no shape change, no new lobes, no duplication; both fragments keep
  silhouettes, holes and helix pattern. Hands credible, no extra fingers.
- Clean consecutive frames of separated, flat, turning fragments: [54,110) (2.25-4.58 s) = 56 frames. Recommended 49-frame window
  [54,103) (2.25-4.29 s); alternative [57,106). The manifest's [48,97) is usable but its first 6 frames show the edge-on/pale piece.
- Late 5 s region: clean geometry; usable as tail but the fragments are adjacent there and hands are leaving.

## End state (planning reference only)
- `frame_f96.jpg` (4.00 s, editorial song 718): both fragments flat, side by side with a narrow gap, different orientations, fingertips
  on each; frame already ~1.5x tighter than the still.
- `frame_f191.jpg` (7.96 s): fragments adjacent at different orientations, hands at the bottom edge, frame ~2x tighter.
- `frame_f48.jpg` (2.00 s): the pale-fragment moment, for reference.

## Weaknesses
- Push-in far exceeds the requested 10%; the shot ends on a much tighter framing than the approved still.
- Fragments are lifted and tilted 1.25-2.0 s; brief pale rendering of the left fragment ~2.0-2.1 s.
- Separation is a finger-width, not a "broad strip", and closes to adjacency after ~4 s (no contact or joining seen).
- Hands withdraw toward the bottom edge at 6.0-6.6 s.
- Not done: no Kling, no assembly, no cue/shotlist edits, no further shots, no commit.
