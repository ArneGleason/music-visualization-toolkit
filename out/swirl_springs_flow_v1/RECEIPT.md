# RECEIPT: swirl_springs_flow_v1 (revision 2)

Status: FLOW DONE, RESULT SAVED WITH GATE FAILURES. Revision 2 was the first and only submission for this handoff (no earlier
version had been submitted). One take generated from first_frame_surface.png, downloaded untouched and inspected densely
over source 0..48 and across the full 192 frames. What works: the swimmers physically rise from below the surface and break
it in a staggered wave during the first ~0.8 s with no pop-in, and the perimeter geography is stable in the cut window.
What fails: once surfaced (~0.8 s on) the school does NOT hold the spiral - it disperses into an even scattered field, so the
"readable turning spiral by ~1 s" is not there; later the take drifts badly (heavy steam from ~3.5 s, swimmers vanishing
5-8 s, camera tilting to an oblique view by 8 s). Saved and reported; no retry (not authorized). No Kling, no audio, no
assembly, no production edits, no commit.

## Inputs verified (SHA-256 match handoff.json)
- start frame `first_frame_surface.png`: 102787475934f30ad23af3e78a029a698b0e31513d7c95ee8e02c4c5285f0426 (1672x941; uploaded fresh via Add media > Upload;
  selected by its unique name; thumbnail id 1462442a; generated first frame matches, mean diff 1.0 at 64x36). Sole START; End
  slot verified empty; no audio.
- formation reference `first_frame.jpg`: c73d155f754c45fb693e724aa60098298a6ea25dbefa226551c3f01a448ea0a3 - inspected only (surfaced clockwise spiral); NOT uploaded.
- prompt `flow_prompt.txt` (revision 2): 97e1a86ee3fe995cf4702b92f4614ad8cd9a5c1eaf136b7b4afe0818e278d9b4 (3890 chars) pasted once with execCommand insertText; editor text
  compared to the file with whitespace removed = identical; lock included verbatim.
- lock `style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC; local = UTC-4)
- Flow's "high demand" banner was showing; the single submission succeeded, no retry.
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100 credits".
- Submitted 13:16:37. Progress 13:17:07 21%; 13:17:27 37%; 13:17:47 54%; rendered by 13:18:07. Tile URL read 13:18:09;
  download 13:18:37. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id ffd91d79-b473-4486-b720-de0436b2b73b (Flow caption "Swimmers performing water ballet..."). Files: `original_ffd91d79-b473-4486-b720-de0436b2b73b.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 b527a9d1c4bc80776e2c7e5c6dc9ac00ec1ba8120a4fa685752d7ea2f3d8fa64
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio. No watermark. 100 credits.

## Inspection (frames_0-2s_every2.jpg = frames 0-46 every 2; center_0-2s_every3.jpg = 480x360 centre crop; contact_every6.jpg;
   keyframes_0_12_24_43_96_191.jpg; bright-chrome pixel/blob trace; perimeter drift trace)
- 0.00-0.45 s (f0-10): submerged spiral clearly visible and brightening as the bodies rise; the spiral arms and curved paths
  match the start image; camera straight down, perimeter unchanged.
- 0.45-0.85 s (f11-20): SURFACING as directed - heads and shoulders break the surface in a closely staggered wave with small
  ripples; submerged silhouettes stay visible while emerging; chrome blob count rises 3 -> 77 continuously, no sudden
  appearance, no dissolve.
- 0.85-1.8 s (f20-43): DEFECT - the surfaced school does not read as the spiral. Bodies spread into an evenly scattered field
  swimming in individual directions (many lateral/outward); the concentric arms of the start image and of first_frame.jpg
  are gone by ~1.0 s. Individual swimmers stay intact (no merging, morphing or vanishing in this window), spacing is
  plausible, and the perimeter geography is stable (perimeter diff <= 16). The "modest coordinated turn" is not readable;
  the "turns" beat at 0.625 s lands during the surfacing wave, before any turn.
- 1.8-3.5 s: swimmers continue drifting outward toward the rim; blob count keeps rising (deeper swimmers still surfacing -
  the school is larger than the spiral's count); a few small upwellings/ripple rings appear near the rim (acceptable).
- 3.5-5.0 s (f84-120): DEFECT - steam grows from thin wisps into dense white clouds that roll over the rim and across much of
  the pool, veiling swimmers (prompt: thin, peripheral, never obscuring).
- 5.0-8.0 s (f120-191): DEFECT - under the steam/foam the swimmers thin out and are essentially gone by ~6 s; the water
  surface becomes foamy/glaring; the camera drifts from straight-down to an oblique view with the settlement at the top edge
  and a sun glare (keyframe 191) - the locked overhead framing is lost. This tail is unusable as B-roll.
- No people/new characters, no neon/laser/strobe, no text.

## Quality gate
- Source 0..43 inspected densely, then full take; swimmers followed across consecutive frames: no pop-in/out, duplicates,
  merging, disappearance or morph inside 0..43: PASS.
- Overhead spiral readable with stable perimeter geography: FAIL - spiral dissolves into a scatter once surfaced (~0.85 s).
- Geothermal activity peripheral, not hiding swimmers: PASS inside 0..43; FAIL after ~3.5 s (dense steam).
- Result saved; no second attempt. Owner decides whether the 0..43 surfacing wave is worth using without a readable spiral,
  or whether to authorize a regeneration (suggest: pin the spiral arms explicitly through the surfacing, cap steam).

## Not done
- No Kling, no audio, no retry, no assembly, no production edits, no commit, no purchase, no owner approval claimed.
