# RECEIPT: specimen_discovery_v1

Status: DONE - one Flow take generated from approved still A, downloaded and inspected across all 192 frames. Usable with
defects: the causal sequence (rotate -> hold -> look up) is there and the stop/gaze-lift land inside the intended windows, but the
rotation is delivered as a two-part re-grip rather than one wrist rotation, and the look-up comes with an OPEN-MOUTH "oh" of
amazement at 3.5-4.4 s where the prompt asked for a closed-mouth half-smile. No Kling, no audio, no retry, no assembly, no FX,
no production edits, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/astronaut_inspect_medium_a.jpg`: 6B5E47A29A59A23824CBE1796E50923E1FC911BF77F66741C26F8258ADF95D06 (1536x864 16:9; the
  copy already in the Flow project library, listed as astronaut_inspect_medium_a.jpg, was selected by a real click; Start slot only,
  End verified empty; no crop dialog appeared, Flow took the full 16:9 frame)
- prompt `flow_prompt.txt`: E61A4F74EC5BF761681314156AEAAEAD478DF3EBEFFE4CCCCE5D5A46B36BC665 (4199 chars) pasted once with execCommand insertText; the editor text was
  compared to the file with all whitespace removed and matched exactly (only blank-line rendering differs)
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496 (contained verbatim in the prompt)

## Flow (actual, times UTC; local = UTC-4)
- Flow showed a banner "Flow is currently experiencing high demand ... Requests may need to be retried ... credits refunded for
  failed requests." The single submission succeeded; no retry was needed or made.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". Start = astronaut_inspect_medium_a.jpg (thumbnail id 64f328ca).
- Submitted 16:36:07. Progress: 16:36:37 21%; 16:37:08 47%; 16:37:28 100%; 16:37:48 tile rendered. Tile video URL read
  16:37:58; download finished 16:38:19. About 100 s. Checks at 30 s then every ~20 s; no reloads, no resubmission.
- Result media id bde2940e-bf60-4459-b62f-9596c1d37b99; downloaded via the tile's signed flow-content URL.
  Files: `original_bde2940e-bf60-4459-b62f-9596c1d37b99.mp4` (untouched) and `base.mp4` (byte-identical), SHA-256 8346BEC30429E79E2ADDA23C410A3C226FAF0E8B048BA6A8D7BECB2521837D62
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 video frames, start 0.000, 8.000 s; disposable Veo audio track present (no audio uploaded).
  No watermark. Cost 100 credits.
- First frame vs approved still: mean pixel difference 1.1 (64x36) = matches.

## Inspection (contact_every6.jpg full take; crop_specimen_hands_0-5s_every4.jpg and crop_face_0-5s_every4.jpg = frames 0-120
   every 4; crop_specimen_hands_5-8s_every6.jpg; per-3-frame drift trace; specimen-box motion trace)
- Camera: locked. Difference vs frame 0 rises only with her own motion (max 14 at the end), no spike, no cut, no zoom.
- Framing, set, suit, hair, likeness: preserved throughout; background, instruments, river and domes unchanged.
- Actual gesture timing (source seconds, 24 fps):
  * 0.00-0.35 s: settles; eyes drop to the specimen by ~0.33 s; lips close gradually, essentially closed by ~1.0 s (prompt asked
    for the first half-second; slightly late but natural).
  * 0.35-0.75 s (f8-18): the specimen tilts toward the light with the right hand - a small rotation, starting EARLY (before the
    0.67 s window) and short.
  * 1.6-2.4 s (f38-58): SECOND handling action - the left glove comes up in front, takes the specimen from the front/base while the
    right hand moves behind; the left hand partly covers the specimen for ~0.5 s (f44-56). This is a re-grip, not the single
    wrist rotation requested. No rubbing, stroking, patting or repeated gesture.
  * ~2.5 s (f60): handling STOPS; from 2.6 s to 7.1 s both hands hold the specimen steady at the discovered angle with the spiral
    visible. Rotation-stop is inside the 2.3-3.3 s window.
  * 2.6-3.5 s: studies the spiral, small focus change, closed lips - reads as recognition.
  * 3.5-3.85 s (f84-92): lips part and the mouth OPENS into an "oh"; gaze lifts toward camera-right at ~3.8 s (f92). Gaze-lift is
    inside the 3.3-4.9 s window.
  * 3.85-4.5 s (f92-108): open-mouth amazed look toward the unseen speaker, eyebrows raised - larger than the "restrained
    closed-mouth half-smile" requested and could read as a spoken syllable.
  * 4.5-5.0 s (f108-120): mouth closes into a wry closed-mouth smile with lifted brows - this matches the intended reaction.
  * 5.0-7.1 s: sustained satisfied smile; gaze returns to the specimen around 6.2 s; natural blinks; hands steady.
  * 7.1-7.9 s (f172-190): hand motion resumes - she tilts/lowers the specimen slightly. Exit handle is not fully still.
- Specimen: one rigid object with a consistent spiral throughout; no morph, split or growth. A brighter glint on its tip appears
  during the re-grip (1.7-2.3 s) - highlight change from the angle, not a new light source.
- Hands/fingers: plausible glove anatomy; during the left-hand crossing (f40-56) the near glove is large and soft but has no extra
  or missing fingers.
- Mouth: no word-forming lip movement except the "oh" at 3.5-4.5 s, which Codex should judge in context.
- Useful intervals: [0,192) continuous. Cleanest: [60,172) (2.5-7.1 s) for hold + look-up + sustain. The proposed window
  [12,118) contains the early tilt, the re-grip at 1.6-2.4 s and the open-mouth reaction at 3.5-4.5 s.

## Defects (summary)
- Two handling actions (early tilt 0.35-0.75 s, re-grip 1.6-2.4 s with the left glove briefly covering the specimen) instead of
  one wrist rotation starting at 0.6 s.
- Open-mouth amazement 3.5-4.5 s instead of a closed-mouth half-smile; the closed-mouth version arrives at 4.5-5.0 s.
- Lips take until ~1.0 s to close (asked: first half-second).
- Hand motion resumes at 7.1 s, so the last ~20 exit frames are not a static hold.

## Not done
- No Kling, no audio, no retry, no assembly, no FX, no production/cue edits, no commit, no owner approval claimed.
