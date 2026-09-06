# RECEIPT: specimen_mismatch_v1

Status: DONE - one Flow take generated, downloaded, inspected across all 192 frames. The candidate window [48,97) is continuously
usable and contains the failed fit. No Kling, no retry, no assembly, no production/cue changes, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/canal_map_macro_b.jpg`: 369C2AB8AF78FFB7CA833CB1A37933D954615980F81AA2AA41E578B7F5316828
- prompt `flow_prompt.txt`: 978BDACA92D89F7A542BBCD9D7652248C93E58C8BA91AFF6B66F616A266B99A7 (3843 chars incl. the unchanged lock) pasted verbatim, once; lock `style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496
- No extracted video frame used; Start slot only (End verified empty).

## Flow (actual)
- Project "Rivers of Mars - AI video". Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1,
  "Generating will use 100 credits"; composer chip 720p. Start = `canal_map_macro_b.jpg` (slot id a175ce12).
- Submitted once at 2026-09-06T04:14:49Z (00:14:49 local); rendered by 04:17:11Z. Cost 100 Flow credits as quoted.
- Result media id 6eec485e-b867-4f3e-af1a-65cecf3d80b8 (Flow caption "Hands comparing specimen fragments"); downloaded via the tile's
  signed flow-content video URL. Files: `original_6eec485e-b867-4f3e-af1a-65cecf3d80b8.mp4` (untouched) and `base.mp4` (byte-identical),
  SHA-256 0C667A5274E6944992D3FA77DC1A91DD3EF85434D89002E53A2CAAD1182686BC
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1, 192 frames, start 0.000, video 8.000 s; disposable Veo audio present. No watermark.
- First frame vs approved still: mean pixel difference 1.1 (64x36).

## Inspection (contact_every6.jpg = every 6 frames full frame; contact_1.5-4.6s_every3_centre.jpg = frames 36-111 every 3, centre crop;
   plus a per-3-frame difference trace)
- Framing: fixed overhead for all 192 frames. No cut, dissolve, radial blur, zoom or new scene. The difference-vs-previous spikes at
  frames 72-84 are fast hand motion (the pull-apart), not a transition; the table and peripheral fragments do not move.
- Pieces: both central fragments keep their silhouettes, holes and helix patterns; no melting, fusing or multiplication. When the edges
  meet (frames ~60-69) they touch without merging. Peripheral fragments, brass instruments and spectrum card stationary.
- Hands: two tweed-cuffed hands, fingers credible; nothing passes through an object.
- Action timing (source seconds, 24 fps):
  0.0-0.5 grip adjustment; 0.5-1.5 right hand slides its fragment outward and turns it (the turn is modest, less than the requested
  quarter turn); 1.5-2.5 a different edge is brought toward the left fragment; 2.5-2.9 (frames 60-69) the edges meet with a visible
  offset, protrusions facing protrusions, a small corrective nudge, no fit; 3.0-3.5 (frames 72-84) the right fragment is drawn away
  to the right, fast, leaving a clear gap; 3.6-4.6 the right hand lowers it onto the leather to the right while the left hand keeps
  the left fragment; 4.6-5.6 both hands ease back and withdraw downward OUT OF FRAME (against the prompt); 6.5-8.0 fingertips
  re-enter at the bottom edge and rest there. No reset, no second attempt.
- Clearest failed-fit moment: frames 60-72 (2.50-3.00 s): edges together but misaligned, then the pull-apart starts.
  `frame_f66.jpg` shows the mismatch.
- Candidate window [48,97) (2.00-4.04 s, 49 frames): continuous, overhead, contains approach, mismatch, separation and the start
  of the set-down. USABLE. Alternatives if Codex wants a calmer pull-apart: [54,103) or [42,91) are equally clean.
- Usable continuous overhead footage: [0,192); but hands are absent from ~5.6 s to ~6.5 s (frames ~134-156), so windows crossing
  that read as an empty table, and the re-entering fingertips from ~6.5 s look like the start of a new action.
- 84 BPM: the pull-apart at 3.0-3.5 s is quicker than a broad-pulse gesture; the rest is deliberate. No sync claim.

## End state (for a later continuation, planning reference only, not a Flow start frame)
- `frame_f96.jpg` (4.00 s, editorial song frame 718): left fragment held at bottom-left-centre by the left hand; right fragment lying
  on the leather to the right, turned, clear gap between them; outer ring undisturbed.
- `frame_f191.jpg` (7.96 s): both fragments lying apart on the leather, hands reduced to fingertips at the bottom edge.

## Weaknesses
- Hands leave the frame at ~5.6 s and re-enter at ~6.5 s (prompt asked them to settle in frame). Outside the candidate window.
- The preparatory rotation is subtle; the mismatch reads mainly as an edge offset rather than a rotated pattern.
- Pull-apart is fast (about 0.5 s).
- Not done: no Kling, no assembly, no cue/shotlist edits, no further shots, no commit.
