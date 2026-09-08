# RECEIPT: rocket_landing_retry_v1

Status: FLOW DONE; KLING DONE after owner accepted the base (see KLING PASS section at the end). Original gate note follows. One Flow take generated from the approved rockets_landing_wide_a.jpg,
downloaded untouched and inspected across all 192 frames. The landing mechanics are largely what was asked (monotonic
descent, jets shortening and dimming, all engines off by ~3.0 s, no re-ignition, no fireball, rockets intact and planted,
plain silver chest, helmet preserved, camera locked). Two gate items do not pass cleanly: (1) the woman's singing collapses into
a FIXED GRIN from ~1.5 s to ~3.4 s, i.e. through most of the primary line "like rockets coming in" (0.5-3.208 s); (2) after
cutoff the dust does spread laterally, but from ~4.0 s to ~6.0 s it builds into a broad rolling pink dust bank that rises to
helmet height behind her head before thinning and settling by ~7.5 s. Per the handoff ("If these fail, stop and ask,
retaining the downloaded take"), no Kling credits were spent. Base retained for owner review. No retry, no assembly, no FX,
no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/rockets_landing_wide_a.jpg`: 38d78627c028938d72902026520c9b0b2011aa92fcafa2b8dd30a03d1c3c546a (1536x864; the library copy
  rockets_landing_wide_a.jpg selected by real click, thumbnail id 424acdf7; generated first frame matches, mean diff 0.9 at 64x36)
- prompt `flow_prompt.txt`: 413d426231cecc4bc3d9692715b49cb1b67996fd67ecae1fc3a6d84d957931e9 (4925 chars) pasted once with execCommand insertText; editor text compared to
  the file with whitespace removed = identical (lock included verbatim). direction.txt was not submitted.
- lock `style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide `guide.wav`: 23745680e994e9416cfa883f81ad395cd6fdb8d227edd52c863275492305db79 (48 kHz mono, 8.000 s) - verified, NOT uploaded (no Kling run, no Flow audio).
  Guide energy (RMS per 0.25 s): quiet 0-0.5, moderate 0.5-2.0, loud 2.25-3.25 (2873/2268/2159), silent 3.25-5.5, loud again
  5.75-7.5 ("Can't tell you..." context), 7.75-8.0 loud.

## Flow (times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". End slot verified empty.
- Submitted 01:49:22. Progress 01:49:52 21%; 01:50:12 38%; 01:50:32 54%; rendered by 01:50:52. Tile URL read 01:50:54;
  download 01:51:30. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id b09314b9-20fe-4c81-b20e-95d83fcc4f96 (Flow caption "Helmeted woman singing during ro..."). Files: `original_b09314b9-20fe-4c81-b20e-95d83fcc4f96.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 653071bad0731275f5f21a681c544e8bbff742d52ae1f145ab2b29b49c468d81
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark. 100 credits.

## Inspection (contact_every6.jpg; rockets_0-4s_every4.jpg and rockets_4-8s_every8.jpg = 1280x520 rocket band crops;
   crop_mouth_0-3.5s_every2.jpg; crop_mouth_3.5-8s_every6.jpg; crop_chest_every24.jpg; luma drift trace; per-rocket warm-bright
   pixel trace in the column band under each nozzle; upper-frame pink-dust pixel trace; nose-position trace)
- Camera: locked. Difference vs frame 0 rises only with the rockets/dust (0 -> 24), no cut, zoom or pan; woman stays centred.
- Descent: all three rockets descend smoothly and monotonically from the airborne start; no bounce, no lift-off, no reversal.
  Approximate touchdowns (rocket on its pad, legs down): LEFT ~2.4 s (f~58), RIGHT ~2.5 s (f~60), CENTER ~2.6 s (f~62).
  All three rest fully on their pads and stay planted and motionless to the end; bodies, fins and noses intact.
- Engines: jets are long and bright at 0-0.8 s, then progressively SHORTEN and DIM 0.8-2.5 s (warm-pixel counts fall from
  ~400/800 to <100 per band by ~2.3 s). Cutoff: LEFT flame gone by ~3.0 s (f72), CENTER by ~3.2 s (f78), RIGHT by ~3.3 s
  (f80). Prompt asked for extinction at contact; here each jet lingers as a dim short glow for ~0.5-0.7 s after touchdown,
  then is off. NO re-ignition anywhere after 3.3 s (the later warm-pixel rise in the traces is the pink dust bank, verified
  visually: no flame, no flare, no fireball).
- Dust: 0-2.5 s low pink dust sheets spread horizontally from each pad (good, matches the reference look). 3.0-4.0 s the sheets
  widen outward and merge across the pads. 4.0-6.0 s DEFECT: the dust builds into a broad rolling bank spanning the frame
  behind her, climbing to roughly the rockets' mid-body and to her helmet height (contact_every6 row 3). It is not a vertical
  plume, mushroom cap or fireball, and it stays behind her (face never obscured), but it is a "rolling wall behind the woman's
  head", which the prompt forbade. 6.0-7.5 s it thins and settles into low haze; 7.5-8.0 s low wisps, rockets clear.
- Costume/helmet: plain silver chest with only the centre seam for all 8 s (crop_chest_every24.jpg) - no dials, sockets, bands or
  attachments. Clear bubble helmet and neck ring preserved; reflections never hide eyes or mouth. Identity consistent.
- Singing (primary line 0.5-3.208 s): 0.0-0.75 s open singing shapes with upper teeth; 0.83-1.08 s smile/closed; 1.17-1.42 s
  open vowel; 1.5-3.4 s DEFECT: broad fixed toothy smile with no changing mouth shapes (the "fixed smile" the prompt excluded).
  So only ~1.2 s of the 2.7 s line is articulated. 3.5-6.4 s: relaxed smile, small mouth motion, watching (as directed).
  6.5-7.9 s: open singing shapes resume for the "Can't tell you if they're true" context tail.
- No visualizer effects, ripples, symbols or captions; no extra figures.

## Quality gate (before Kling)
1. Inspect entire base first: done.
2. Monotonic descent, engines shorten/dim and shut off at touchdown, no re-ignition: PASS with a note (each jet lingers ~0.5-0.7 s
   after touchdown; all off by 3.3 s; no re-ignition).
3. Low outward dust, no mushroom-like rising cloud or explosion: PARTIAL - lateral spread yes, no mushroom/explosion, but a broad
   rolling dust bank rises to helmet height behind her at 4.0-6.0 s.
4. All three rockets stable and intact after landing: PASS.
5. Plain silver chest and clear helmet preserved, no new hardware: PASS.
6. Active natural singing through 0.5-3.208 s, face readable through the visor: FAIL - fixed grin 1.5-3.4 s; face readable.
7. Material failure -> stop for owner review: applied. Kling NOT run (0 credits).

## Timings for Codex (source seconds, 24 fps)
- touchdown: left ~2.4, right ~2.5, centre ~2.6. engine cutoff: left ~3.0, centre ~3.2, right ~3.3.
- dust: low sheets 0-3.0; merged/widening 3.0-4.0; rolling bank behind her 4.0-6.0 (peak ~5.0-5.5); settling 6.0-7.5; wisps 7.5-8.0.
- mouth: articulated 0.0-0.75, 1.17-1.42, 6.5-7.9; fixed grin 1.5-3.4; calm 3.5-6.4.

## Not done
- No Kling (withheld), no Flow retry, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.


# KLING PASS (owner accepted the base, 2026-09-07 02:03 UTC)

The owner reviewed the base, judged the landing good, and asked for the lip sync. One Kling Lip Sync was run on `base.mp4`
(uploaded as-is; its disposable Veo audio is ignored with Sound from Video OFF, verified by zoom) with `guide.wav` at 0:00-0:08.
Kling detected ONE face through the visor: Character 1 = the helmeted woman. Add Speech placed the block on the Character 1
lane spanning 0:00-0:08. Generate quoted 10 credits.
- Submitted 02:03:11; "0/1 Generating" 02:03:42; balance 401 -> 391 (read 02:04:15). Checks 02:04:35, 02:04:55, 02:05:26,
  02:05:46 (creating); 02:06:06 "1/1 Generated". Download (Video, MP4, Without Watermark ON, existing entitlement) clicked
  02:06:36; file present and copied 02:07:19. About 3 min. No reloads/resubmits.
- Job id 2565 (download name kling_20260907_Lip_Sync__2565_0.mp4). Files: `original_kling_2565.mp4` (untouched) and `synced.mp4`
  (byte-identical), SHA-256 2b9b6fe03f22377a4d3ce036a8be99907ef745ecc5346b5d69874b4b4daacae2
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}], "format": {"duration": "7.966667"}}
  => 1280x720, NATIVE 30/1 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz stereo 7.895 s, both streams start 0.000.
  Not trimmed/cropped/retimed. Codex conforms 30 -> 24 fps by timestamps.
- Audio: normalized cross-correlation of returned audio vs guide.wav = 1.00 at lag 0.
- Picture integrity vs base (per native frame): rockets/dust region mean 2.6 / max 3.7 (noise - landing, jets, cutoff and dust
  identical to the base); whole frame mean 2.9; chest mean 3.6 (brief 13.5 at 7.5 s from jaw/neck motion); helmet region mean
  4.6 / max 11.3 (mouth motion inside the visor); mouth box mean 9.6 / max 22.1. Camera, costume, helmet, rockets unchanged.

## Kling mouth inspection (mouth_synced_src0.4-3.6s_native30_everyframe.jpg = native frames 12-107, every frame, 12 per row;
   mouth_base_src0.4-3.6s_every6.jpg; mouth_synced_src3.6-8s_every6.jpg; contact_synced_every10_native.jpg; motion trace)
Guide energy: 0.5-2.0 s moderate ("like rockets"), 2.25-3.25 s loud ("coming in"), silent 3.25-5.5 s, loud 5.75-7.5 s (context).
- like (~0.5-0.9 s, f15-27): OK. Open shapes with upper teeth, changing every few frames (motion 11-26).
- rock- (~0.9-1.3 s, f27-39): OK. Rounded open "O" with mouth interior visible.
- -ets (~1.3-1.7 s, f39-51): OK. Open narrowing to a teeth-visible smile.
- com- (~2.0-2.4 s, f60-72): PARTIAL. Small rounded/pursed "oo" shapes 2.0-2.2 s, then a relaxed smile; jaw opening modest.
- -ing in (~2.4-3.25 s, f72-97, the loudest part of the guide): WEAK. The base's fixed grin dominates: lips part slightly with
  small shape changes at 2.47-2.7 s (motion 17-19), then a closed-lip smile 2.8-3.25 s. The sustained "in" does not read as
  sung.
- 3.25-5.4 s: closed smile, calm watching (guide silent) - correct.
- 5.5-7.9 s: open singing shapes resume on the "Can't tell you if they're true" context (guide loud 5.75-7.5) - active
  articulation, later use undecided.
- No puppet jaw, no clamped-lip artifact, no distorted teeth, face readable through the visor throughout; helmet reflections
  unchanged.

## Verdict
- Primary line source 12..77 (0.5-3.208 s): "like rockets" articulated well (0.5-1.7 s); "coming" partial; "in" weak (the
  base's grin at 1.5-3.4 s limited Kling). Usable for audition; the owner may find the last word under-sung.
- Deliverables: `base.mp4` (plate) and `synced.mp4` (lip-synced), both full 8 s, untouched.
