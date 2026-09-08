# RECEIPT: orbital_continuity_v1

Status: DONE - one Flow take generated from first_frame.png (the continuity trial matching the accepted landing rockets),
downloaded untouched and inspected across all 192 frames. PASSES the quality gate: exactly three matching smooth silver
rockets with black vertical slots and short curved fins, tail-first slow descent, narrow amber braking jets below the engine
bases only, no fire on hulls, no smoke, explosions, morphing or disappearing vehicles, no person. Caveat: the motion is very
restrained, so the intended 47-frame cut (source 12..59) will read as a slow drift rather than an obvious descent. No Kling, no
audio, no retry, no assembly, no production edits, no commit. The approved landing was not touched.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame.png`: 72e74b72f17067ed08265fa0ee3627d3c9d63ccc87a47b664a1b79b0c2f03148 (1672x941, 16:9; uploaded fresh via Add media > Upload and chosen from
  the four library files named first_frame.png by its orbital preview; generated first frame matches, mean diff 1.2 at 64x36).
  Visual QA vs `landing_design_reference.jpg` (5090652b57e4aafdcd1cff55281dd0748ed1fc997f59aba3b141504ea2c46677, inspect only, never uploaded): the new frame's
  rockets share the landing design - smooth tapered pointed noses without needle antennas, slim polished bodies, long black
  rounded-top vertical slots (plus the small upper window seen on the landing rockets), short curved swept fins, compact engine
  bases. The old orbital portholes and large angular fins are gone. Silhouettes are visibly the same family, not pixel-identical.
- prompt `flow_prompt.txt`: 281389fe10ef89dd099ef219b36cdf5587564a12b0eab2269eec702f35973c4c (2989 chars) pasted once with execCommand insertText; editor text compared to
  the file with whitespace removed = identical; lock included verbatim.
- lock `style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- End slot verified empty; no audio guide.

## Flow (times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits".
- Submitted 02:21:25. Progress 02:21:55 21%; 02:22:15 38%; 02:22:35 55%; rendered by 02:22:55. Tile URL read 02:22:57;
  download 02:23:25. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id 38c4370d-ac98-4b4b-bf58-944a20df3cd7 (Flow caption "Rockets descending toward Mars"). Files: `original_38c4370d-ac98-4b4b-bf58-944a20df3cd7.mp4` (untouched)
  and `base.mp4` (byte-identical), SHA-256 4e73e5b9c8d74bc2698190608db6694e8b6edd490d161762220ef98ca4c3f4bd
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark. 100 credits.

## Inspection (contact_every6.jpg; rockets_0-3s_every4.jpg = 800x560 centre crop every 4 frames; rockets_3-8s_every8.jpg;
   center_rocket_every48.jpg = tight crop of the centre rocket every 2 s; luma drift trace; nose-position and flame traces)
- Vehicles: three rockets in the start formation for all 192 frames; count never changes; nothing appears or vanishes. Bodies,
  noses, slots, fins and engine bases keep their geometry from frame 0 to 191 (centre-rocket crop at 0/2/4/6/8 s is the same
  design, only slightly larger). No portholes, needles, boosters, deployed parts or morphing.
- Motion: tail-first descent - the rockets sink slowly relative to the horizon (centre nose from ~16% to ~25% of frame height over
  8 s), with a very slight enlargement (approach/parallax) and a gentle symmetrical camera drift (difference vs frame 0 rises
  smoothly 0 -> 22; no cut, no sudden move). Motion is present from frame 0 (no static hold) but it is RESTRAINED: over the
  intended window source 12..59 (0.5-2.458 s) the visible change is a small downward drift plus jet flicker. Codex/owner should
  judge whether that reads as descent in a 2 s cut.
- Engines: compact narrow amber jets below each engine base, flickering, gradually dimming across the take (warm-pixel counts fall
  ~40-50%); they never engulf the hulls; no smoke, fireball, reentry flame or explosion. Jets stay lit to the end (this is orbital
  braking, not the landing).
- Composition/background: curved horizon, rivers, settlements, striped planet, moons and stars consistent with the start frame;
  no person, helmet, text or FX.
- Defects: none material. Minor: restrained motion (above); the right rocket drifts slightly right by the end but stays fully
  in frame; jets do not shorten as much as the landing's would.

## Quality gate
- First frame and source 12..59 inspected, then full clip: done.
- Three matching rockets, slots, curved fins, no portholes/needles: PASS.
- Tail-first descent, restrained motion inside the window: PASS (restrained, see caveat).
- No fire/smoke around hulls, no morphing/disappearing: PASS.
- Material design mismatch: none. Ready for Codex to build the comparison preview and replace only s035 [2881,2928) from
  source [12,59).

## Not done
- No Kling, no audio, no retry, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.


# TAKE 2 (owner-requested dramatic re-entry, 2026-09-07 02:30 UTC)

The owner reviewed take 1 and rejected its motion as too static ("very un-rocket-landing"), asking for the rockets to come in
on a rapid orbital trajectory with the engines braking the fall - a dramatic re-entry. `flow_prompt_take2.txt` (SHA-256 f002c3fcb88b5fa23cfcfb49cd0370fa76543a99d6beeb4ef254cf8a598e0b69,
3470 chars) replaces ONLY the motion paragraph of flow_prompt.txt: steep curving descent path, real speed from frame 0, the
formation dropping and growing larger in the first two seconds with the horizon rising, long bright pulsing amber braking
plumes, the fall clearly slowing under thrust but never stopped, thin heat shimmer allowed, no fireballs/smoke/explosions,
camera tracking with the formation. Design lock, composition paragraph and style lock unchanged. Same Start frame
(first_frame.png, thumbnail cb465db9), End empty, same settings (Veo 3.1 Quality, Frames, 16:9, 720p, 8s, x1, 100 credits
verified). Take 1 files untouched; take 2 lives in `take2/`.

- Submitted 02:30:07. Progress 02:30:37 21%; 02:30:57 38%; rendered by 02:31:28. Tile URL read 02:31:50; download 02:32:14.
  Media id 66c5ad17-fc58-4ab3-956e-eb57db4cf392 (Flow caption "Three silver rockets descending..."). Files: `take2/original_66c5ad17-fc58-4ab3-956e-eb57db4cf392.mp4`
  (untouched) and `take2/base.mp4` (byte-identical), SHA-256 c03615cf66d7b9db63530285beb719d8f7c32711d3cdb68ed2a47a5bf7299c64
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, 8.000 s, disposable Veo audio. First frame vs first_frame.png: mean diff 1.3. 100 credits
  (Flow total for this handoff now 200).

## Take 2 inspection (take2/contact_every6.jpg, frames_0-3s_every4.jpg, frames_3-8s_every8.jpg, center_rocket_every48.jpg;
   drift, nose, horizon and flame traces)
- Motion: DRAMATIC and continuous. The curved horizon rises from ~39% to ~14% of frame height over the take (planet limb row
  70 -> 26 of 180) as the formation plunges toward the surface and the camera tracks with it; the rockets grow ~30-40% larger
  by 8 s; terrain and rivers slide beneath. Difference vs frame 0 climbs steadily to 47 (take 1 reached 22) with per-3-frame
  motion 4-9 throughout - smooth, no cut, no whip, no shake.
- Intended window source 12..59 (0.5-2.458 s): the braking plumes flare from short jets into long bright columns within the
  first 0.7 s and the formation is already dropping and enlarging - clearly reads as a fast descent under thrust.
- Engines: long focused amber plumes streaming straight down from the engine bases, pulsing; total warm-pixel count peaks
  ~1280 at 2-3.5 s then falls to ~270 by 8 s (the braking easing as the fall slows). Plumes never touch the hulls or noses;
  no fireball, no explosion. The plumes are far longer than take 1's compact jets (as requested).
- Vehicles: three rockets for all 192 frames, same design as the landing (smooth noses, black slots, curved fins), geometry
  constant, noses upright, tail first, all silhouettes readable; nothing morphs or vanishes. No landing, no ground contact.
- Minor deviations to note: (1) a thin white exhaust haze drifts around the formation/horizon at ~3-6 s (faint, translucent,
  not a smoke cloud); (2) the camera move is larger than the lock's "slow symmetrical push-in" (it tilts down and tracks the
  plunge), but it is smooth and symmetrical; (3) by 7-8 s the rockets sit lower against the planet but are still airborne.
- Background: planet, moons, stars, rivers and settlements consistent with the start frame; no person, text or FX overlay.

## Take 2 gate
- Matching rockets: PASS. Tail-first descent with real motion in the window: PASS. No fire on hulls / no morphing: PASS
  (faint exhaust haze 3-6 s noted). Material mismatch: none. => take 2 is the candidate; take 1 retained as a rejected reference.
