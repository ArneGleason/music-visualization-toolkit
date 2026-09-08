# RECEIPT: spring_geyser_flow_v1

Status: FLOW DONE, RESULT SAVED - one take generated from the new first_frame.png, downloaded untouched and inspected across all
192 frames. The eruption mechanics are largely what was asked (mid-eruption start, summit above frame, low locked camera,
pressure loss, a big falling-water splash readable inside the first 3.25 s, then settling), BUT the take carries one GROSS
FAILURE that the owner must see before use: the small distant striped planet in the start frame GROWS into a huge sphere that
rises behind the geyser from ~1.9 s and hangs over the terrace for the rest of the clip. There is also a solid-blob phase of
the column at 1.0-2.2 s. Reported separately below; no retry was made (not authorized). No Kling, no audio, no assembly, no
production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: 2d306b956cf8f0cc1e77ffbf0e7b1f4a1f1d644753c17c1300ed2974b63c43a9 (1672x941, 16:9; uploaded fresh via Add media > Upload; chosen from the
  six library files named first_frame.png by its geyser preview, thumbnail id 36d493a9; generated first frame matches, mean diff
  1.4 at 64x36). The old arched-hose still was not used. End slot verified empty; no audio.
- prompt `flow_prompt.txt`: f34fce4add1ab23323636a71c63caaa66c0ae9d47675edfcafc244ae7fe2da29 (3410 chars) pasted once with execCommand insertText; editor text compared to
  the file with whitespace removed = identical; lock included verbatim.
- lock `style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC; local = UTC-4)
- Flow's "high demand" banner was showing; the single submission succeeded, no retry.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
- Submitted 12:46:55. Progress 12:47:25 21%; 12:47:45 38%; 12:48:05 55%; rendered by 12:48:25. Tile URL read 12:48:27;
  download 12:48:56. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id bef34bee-1e3b-4c6c-9dca-838a6a21f8e5 (Flow caption "Geyser erupting on Mars"). Files: `original_bef34bee-1e3b-4c6c-9dca-838a6a21f8e5.mp4` (untouched) and
  `base.mp4` (byte-identical), SHA-256 e62d30cef23dee2bb7f8db8ec3cb6f041ed00a623f14888d1292269ea5988a53
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark. 100 credits.

## Inspection (contact_every6.jpg; frames_0-3.3s_every4.jpg = frames 0-76 every 4; keyframes_0_12_24_48_78_191.jpg;
   pool_splash_every8.jpg = pool/terrace crop; column-brightness, pool-motion and background traces)
- Camera: locked, low at water level for all 192 frames; no tilt, widen, zoom or cut. The geyser summit never enters the frame.
- 0.0-0.9 s (f0-21): mid-eruption from frame 0 - tall turbulent white column exits the top of frame from the ground vent; older
  spray already falling beside it; terrace overflow and pool ripples as in the start frame. Reads as the requested surge.
- 1.0-2.2 s (f24-52): DEFECT - the column changes character into a shorter, dense, smooth white mass (meringue/foam-like, not
  coarse liquid spray) that thickens rather than breaks up; column-brightness trace peaks 1.2-2.0 s. At ~2.2 s (f52-56) this
  mass drops as one body - the "entire column reversing as one solid object" the prompt excluded. Pressure loss reads as an
  abrupt collapse at ~2.2 s rather than a one-second decay.
- 2.3-3.3 s (f56-80): the collapse throws a wide lateral splash wall across the terrace and into the foreground pool - large
  splash crowns, churning, expanding ripples; pool-motion trace peaks 2.8-3.3 s (f68-80). Readable falling/splashing water is
  therefore inside the first 3.25 s (the "falls"/"heaven" targets at 0.375 s and 2.29 s fall respectively in the surge phase
  and at the start of the collapse-splash).
- 3.3-8.0 s (f80-191): splash subsides, low steam/mist rolls across the terrace (translucent, partially veiling the vent area
  for ~1.5 s), surface settles into ripples; the vent shows only small trickles/overflow by 5-8 s. One pressure event, no
  repeat cycle. No rigid arch/hose shape at any point.
- GROSS FAILURE (background continuity): the small striped planet at top right of the start frame grows steadily from ~1.9 s
  (f46) into a very large near sphere behind the column's top, centred above the terrace, and stays there from ~2.5 s to the
  end (keyframes_0_12_24_48_78_191.jpg tiles 4-6). The background-vs-frame-0 trace rises 3 -> 23 because of it. This is a
  "new giant object" inside the visible window [0,78) and violates the stable-geography gate. Domes, terraces, spires and the
  cyan insects otherwise stay consistent.
- Water is water (no smoke, fire, beam); no rain; no people or props.

## Quality gate
- Tall vertical water exiting the top of frame, low framing, visible vent: PASS.
- 0 / 0.5 / 1 / 2 / 3.25 s and tail inspected: pressure drops and airborne water falls and splashes: PASS in effect, but the
  decay is a blob-collapse at 2.2 s rather than a gradual break-up (defect).
- Liquid detail, stable geography, no smoke/explosion, no disappearing water or rigid arch: FAIL on stable geography (planet
  grows into a giant sphere from 1.9 s); liquid detail partial (solid-mass phase 1.0-2.2 s); no smoke/explosion; no arch.
- Result saved; no retry. Owner/Codex decision needed: the splash beat may still be usable if the planet region can be masked or
  the cut avoids it, otherwise a regeneration (owner-authorized) is the fix.

## Not done
- No Kling, no audio, no retry, no assembly, no production edits, no commit, no purchase, no owner approval claimed.
