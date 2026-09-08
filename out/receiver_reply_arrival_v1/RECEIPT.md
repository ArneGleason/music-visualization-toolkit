# RECEIPT: receiver_reply_arrival_v1

Status: DONE - one Flow plate generated, downloaded and inspected across all 192 frames; usable for the whole take. No Kling, no
guide upload, no retry, no assembly, no production/cue changes, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `codex/out/receiver_dial_macro_b.jpg`: 0C6BAF05F9CBC7FC027D26F54BAF1CB390E58075A5397BA8D7C56B6D413251B6 (approved B still, unedited; Start slot only, End verified empty; no extracted video frame)
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6DB3E45D5777CB22AE1EE7DA18B8BDE8498CAAFFB8D96E8536F3414DEA260496; prompt `flow_prompt.txt` (2816 chars incl. the lock) pasted verbatim once. prompt SHA-256 988CC7703AFA75A10EF365851764C08F13B4F39B8D6AA9E78BD0BE39642C8A87

## Flow (actual, times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, "Generating will use 100 credits"; chip 720p.
  Start = `receiver_dial_macro_b.jpg` (slot id 41315074).
- Submitted 13:43:09. Displayed progress: 13:43:19 5%; 13:43:50 30%; 13:44:08 46%; 13:44:26 no percentage (complete); tile video URL
  read 13:45:01; download 13:45:25-26. Generation about 75 s. Checks at 10 s, 41 s, then every ~18 s. No reloads, no resubmission.
- Result media id 0b449559-82fd-432f-8ed1-489995e58d06 (Flow caption "Communications receiver slow cam..."); downloaded via the
  tile's signed flow-content video URL. Files: `original_0b449559-82fd-432f-8ed1-489995e58d06.mp4` (untouched) and `base.mp4`
  (byte-identical), SHA-256 2225B920876CB65BF0B63EB2912B5AF862320494F2A8D34B4995D39A0AC6FACC
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 video frames, start 0.000, video 8.000 s; a disposable Veo audio track is present (to be discarded).
  No watermark. Cost 100 Flow credits as quoted.
- First frame vs approved still: mean pixel difference 0.9 (64x36).

## Inspection (contact_every6.jpg every 6 frames; contact_5_keyframes_full.jpg at 0/2/4/6/8 s; per-3-frame difference trace)
- Content: the receiver cabinet, round blue screen, large amber meter, two small side meters, knobs, supports and the Mars settlement
  background stay recognizable and in place for all 192 frames. No people, hands, specimen pieces, new props, rosettes, sprites,
  floating lights, beams, graphics or text. Dial markings unchanged. Meters keep steady low amber illumination; no flashes; the
  needles hold. Faint texture movement in the blue screen only.
- Camera: one steady, straight, symmetrical push-in with no pullback, orbit, reframe, focus rack, cut or freeze. The difference
  trace is uniform (about 2.2 per 3 frames against the previous sample, monotonic drift against frame 0), i.e. continuous motion
  with no events. The push is stronger than "a few percent": by 8 s the framing is roughly 15-20% tighter (the cabinet's left edge
  nears the frame edge and the planet rises toward the top edge). The receiver face stays sharp; margins remain visible.
- Usable interval: the whole take [0,192). Proposed source [12,131) after timestamp conform is clean; the exit handle [131,192)
  is 61 real frames of the same continuing push (no freeze), so it is usable, with the framing continuing to tighten.
- Nothing to time against audio here (silent plate); phrase windows 20-67 and 67-131 are ordinary continuing push frames.

## Continuity weaknesses
- Push magnitude exceeds the request; a cut back to the same still later would show the framing difference.
- The background settlement is a painted-backdrop-style plate that scales with the push (no parallax), consistent with the lock.
- Codex owns rosette carry-over, voice-driven meter light, tracking and assembly; none baked here.
