# RECEIPT: opening_specimen_v2

Status: DONE - one Flow take generated, downloaded, inspected across all 192 frames; the required interval [12,154) is continuously
usable. No Kling, no retry, no assembly, no production or timing-file change, no commit. Writes only under out/opening_specimen_v2/.

## Inputs verified
- first frame `codex/out/canal_map_macro_b.jpg` SHA-256 369C2AB8AF78FFB7CA833CB1A37933D954615980F81AA2AA41E578B7F5316828 (matches manifest)
- prompt `flow_prompt.txt` (3445 chars, includes style_lock_v2) pasted verbatim, once; no extra lock, no other reference.

## Flow (actual)
- Project "Rivers of Mars - AI video". Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1,
  "Generating will use 100 credits"; composer chip 720p. Start slot = `canal_map_macro_b.jpg` (slot id a175ce12); End slot verified EMPTY.
- Submitted once at 2026-09-06T03:37:24Z (2026-09-05 23:37:24 local); rendered by 03:39:36Z. Cost 100 Flow credits as quoted.
- Result media id 39dfb9e7-c901-49aa-9e39-eb2899d16cde (Flow caption "Hands adjusting objects on desk"). Downloaded through the tile's
  signed flow-content video URL (original filename on the CDN is the media id). No browser protections touched.
- Files: `original_39dfb9e7-c901-49aa-9e39-eb2899d16cde.mp4` (untouched) and `base.mp4` (byte-identical copy), SHA-256 0CB72B1F0C58E4D97C933488392D203BA4A75EC49A281796E32B20D418A9AC17
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 video frames, start 0.000, video 8.000 s; disposable Veo audio track present (not used; no vocal offset applied).
- Watermark: none (Flow output carries no visible mark).
- First frame vs approved still: mean pixel difference 1.1 (64x36 downscale).

## Inspection (contact_every6.jpg = every 6 frames; contact_3.25-4.7s_every2.jpg = frames 78-112 every 2; plus a per-3-frame
   difference trace against frame 0 and against the previous sample)
- Framing: fixed directly-overhead view for all 192 frames. No cut, dissolve, radial blur, zoom, push-in, angle change or new scene.
  The old failure region (3.5-4.5 s) is clean: hands and pieces only.
- Pieces: the two central fragments keep their silhouettes, holes and internal helix patterns; the peripheral ring, brass instruments
  and spectrum card stay put. No morph, melt or shape change seen.
- Hands: two tweed-cuffed hands, credible throughout; no face, no third hand.
- Action (single progression, no reset): 0-0.5 s grip adjustment; ~0.5-2.5 s edges brought closer; ~2.5-4.5 s the right piece is
  rotated a few degrees in the table plane and compared, small mismatch visible; ~4.5-6.2 s the right piece is eased aside and set
  on the leather at bottom centre-right while the left hand keeps its piece; the state is established before 6.4 s.
  6.5-8.0 s: the right hand releases and reaches up to the upper-right cluster of fragments (more than the prompt's "tiny hand
  movement", but no reset and still overhead). The difference trace shows this as the only large change (from ~frame 156).
- Usable intervals: the whole take [0,192) is continuous overhead footage. Required [12,154) = 142 frames: USABLE.
  Exit handle beyond 154: 38 frames of real footage, but from ~156 the right hand is travelling upward, so a dissolve out of s004
  should end by about frame 160; a straight cut at 154 is clean.
- 84 BPM: movement is slow and deliberate; no claim of beat synchronization.

## End state for a later continuation
- `end_state_f153.jpg` (source frame 153, 6.375 s = editorial song frame 475): left hand holds the left central piece near bottom
  centre; the right central piece rests on the leather slightly right of centre, rotated a few degrees relative to the start; outer
  ring unchanged.
- `end_state_f191.jpg` (source frame 191, 7.958 s): same arrangement, right hand raised toward the upper-right fragments.
- A continuation should start from the approved-still chain only if a later still is made; per owner rule, these Veo frames are
  reference for planning, not Flow start frames.

## Weaknesses
- The final 1.5 s adds an unrequested reach upward (usable as a motivated move toward the next return, or trim before it).
- Comparison/mismatch beat reads subtly at contact-sheet scale; judge in motion.
- Not done: no continuation, no assignment to s006/s008, no assembly or cue changes (Codex), no commit.
