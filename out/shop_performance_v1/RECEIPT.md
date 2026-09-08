# RECEIPT: shop_performance_v1

Status: DONE - both Flow takes generated (one submission each), downloaded untouched, inspected across all 192 frames each.
Both are usable candidates with defects listed below. No Kling, no guide audio, no retry, no extra variants, no generated
transition, no assembly, no production edits, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496 (contained verbatim in both prompts)
- wide first frame `codex/out/counterfeit_parade_b.jpg`: e6b44f299c6c8a06f152db3771723fce9b083d5fa15c65da4e6c4667c7f16bc7 (1536x864). The Flow library copy
  named counterfeit_parade_b.jpg (uploaded from this file in the v6 pass) was selected by a real click; the generated first frame
  matches the file (mean diff 0.95 at 64x36). Not A, not a regenerated still.
- wide prompt `wide_prompt.txt`: 6f954582ae9b11b38f570eb001a6d91c369190f0638409e8454b6423177cae7e (3166 chars)
- close first frame `close_reference.png`: 2982d1190a98f263e8944c4b30a50cbf4d5bf1e0b48e86504adc2f130bd861ea (1280x720 crop of B) - uploaded fresh via Add media > Upload
  and selected from the library; generated first frame matches (mean diff 1.6).
- close prompt `close_prompt.txt`: af4a8df6593a91094075a7c42d70b48590724e6d3f727d09316a422976f12e3b (3381 chars)
- Both prompts pasted once with execCommand insertText; editor text compared to the files with whitespace removed = identical.
  Direction-only files were NOT submitted. End slot verified empty for both takes.

## Flow settings and spend (both takes)
- Settings panel read before each submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". Flow displayed a "high demand" banner; both single submissions succeeded, no retry. Total 200 credits = cap.

## WIDE (times UTC; local = UTC-4)
- Submitted 17:59:03. Progress 17:59:33 21%; 17:59:46 32%; 18:00:29 tile rendered (complete). Tile URL read 18:01:04; download
  18:01:31. Media id fcfeb49c-cbdf-483e-9de5-91d462ed2cee (Flow caption "Woman reacting to shop display").
- Files: `wide/original_fcfeb49c-cbdf-483e-9de5-91d462ed2cee.mp4` (untouched), `wide/base.mp4` (byte-identical). SHA-256 29be3d520d057b098cd9ec2f621ce15717d852c75fa93461d5184f2c34cfb874
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark.
- Camera: locked (window-area motion <=4 throughout; diff vs frame 0 rises only with her body motion). Display objects, skull,
  domes, awning unchanged; her reflection in the glass stays a plausible reflection of the same woman, no second actor.
- Actual gesture timing (source seconds; sheets wide/crop_face_0-2.6s_every2.jpg, wide/crop_face_2.6-8s_every8.jpg,
  wide/contact_every6.jpg, wide/crop_window_every24.jpg):
  * 0.00-0.40: looking left at the display, quiet breath.
  * 0.45-0.70 (f11-17): eyes close and the head dips/tilts - a SMALL head dip with a second small dip at 1.10-1.25 (f26-30).
    Reads as an amused "no" tilt rather than a crisp decisive shake; Codex should judge whether it registers as No.
  * 0.70-1.30: soft amused smile forms while still facing the display; eyebrow lifts ~1.3-1.5 s.
  * 1.30-1.60 (f32-38): head and eyes TURN to the viewer; gaze on camera from ~1.6 s. Slight lean toward the display is minimal.
  * 2.0-2.6 (f48-62): hands come up onto the hips (hip pose complete by ~2.6 s) - a body gesture the prompt did not ask for
    ("no busy hand gestures"); economical but it changes the silhouette from the reference.
  * 2.6-5.0: sustained hands-on-hips, broad open smile toward camera with teeth visible ~3.0-4.5 s - warmer/cheerier than "dry
    skeptical"; overacting risk.
  * 5.3-6.4 (f128-154): looks down/aside with a smirk, then back to camera; 7.7-8.0 (f184-190) head starts moving again.
  * No speech, no lip-shaping words; no repeated head shakes; no merchandise handling.
- Proposed visible interval source [12,50) (0.5-2.08 s): contains the head dip(s), the eyebrow lift and the start of the turn to
  the viewer (turn lands at 1.3-1.6 s, so it is completed inside the window). Hands start rising at ~2.0 s, right at the end of the
  window. Usable for the reaction; exit frames beyond 50 carry the hip pose and broad smile.

## CLOSE (times UTC)
- Submitted 18:02:13. Progress 18:02:43 21%; 18:03:30 tile rendered (complete). Tile URL read 18:04:22; download 18:04:41.
  Media id 9d951335-60b8-4aaf-bb13-06a679c455ff.
- Files: `close/original_9d951335-60b8-4aaf-bb13-06a679c455ff.mp4` (untouched), `close/base.mp4` (byte-identical). SHA-256 510d47b9198a99cd3fddd48b34eaf498f9f98c32d2c0ee42a8144d400e754347
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark.
- Camera: locked; framing, window edge, domes, planet, collar and hair stable; identity consistent throughout; teeth warm/natural.
- Actual timing (sheets close/crop_mouth_0-3s_every2.jpg, close/crop_face_0-3s_every3.jpg, close/crop_mouth_3-8s_every6.jpg,
  close/contact_every6.jpg; per-frame mouth-box motion trace):
  * 0.00: gaze left, lips closed (matches reference).
  * 0.08 s (f2): SINGING ONSET - the mouth is already open on a vowel while she still looks at the shop. Too early: the prompt asked
    for the gaze turn first (0.0-0.5) and singing from 0.5.
  * 0.33-0.50 (f8-12): gaze arrives near camera while singing continues.
  * 0.67-0.83 (f16-20): eyes close/drop downward - a downward blink-look, not the requested upward eye flick.
  * 0.9-1.45 (f22-34): generous articulation, upper teeth and mouth interior visible on open vowels, eyebrows up.
  * 1.5-1.9 (f36-46): bared-teeth grin/grimace (both rows of teeth clenched) - reads as a sneer/clench on the judgment word;
    stronger than "dry conviction".
  * 2.0-2.45 (f48-58): mouth closing through a toothy smile.
  * ~2.5 s (f60): mouth SETTLES to closed lips with a faint half-smile and firm look - matches the 2.458 s target.
  * 2.5-5.4: quiet closed-mouth reaction, small eyebrow play; no babbling, no repeated line.
  * 5.5-6.5 (f132-156): eyes lower and head tilts down/aside (looks away from viewer); 7.0-8.0: head turning down-left.
  * Mouth-box motion trace: active f2-48, quiet after f60 (values 1) until f156, i.e. no silent gap inside the singing window and
    no mouth motion in the tail.
- Proposed visible interval source [12,59) (0.5-2.46 s): fully inside the singing (onset at 0.08 s precedes it; settle at 2.5 s
  just after it). Suitable as a performance base for later lip-sync; note the bared-teeth stretch at 1.5-1.9 s and the downward
  eye drop at 0.7-0.8 s. Exit frames after ~5.4 s have her looking away.

## Defects (summary)
- Wide: head "shake" is a soft dip/tilt (0.45-0.7 and 1.1-1.25 s), not decisive; hands-on-hips pose from 2.0-2.6 s onward;
  broad smile 3-4.5 s is warmer than skeptical.
- Close: singing starts at 0.08 s before the gaze turn; eye move at 0.7-0.8 s is downward, not an upward flick; clenched/bared
  teeth 1.5-1.9 s; looks away 5.5 s onward.
- Neither take has identity, reflection, prop or framing changes; no captions; no cuts.

## Not done
- No Kling, no guide audio, no retry or extra variants, no generated push/zoom, no assembly, no production edits, no commit,
  no owner approval claimed.
