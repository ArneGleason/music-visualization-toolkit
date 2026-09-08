# RECEIPT: B3 (Flow base done; Kling WITHHELD - material failure)

Status: base_needs_owner_review. ONE Flow continuation generated from B3/first_frame.png (= B2 take 2 base frame 180,
pixel-identical). Downloaded untouched with byte-identical base.mp4. MATERIAL FAILURE: at ~4.2 s she turns her head to
her right into near-profile and stays turned away for the rest of the take, raises her right arm in a long reach toward
the bedside light (5.3-7.5 s), and the room dims heavily from ~6.5 s so that the final cut is dark. Inside the cuts:
"To who?" (57..74) is a frontal toothy smile with no articulation (the line was delivered early at 1.1-2.0 s); "You first"
(122..144) is sung in profile, turned away; "Night" (171..189) is dark, in profile, mouth closed. Face/identity, suit,
room and the specimen (left hand, stable) are fine. Kling skipped per the gate; no retry. Owner decides.

## Inputs verified (SHA-256 match B3/handoff.json)
- first_frame.png 13f777d66862118bb85ff1fc3ebdc0cbcc64b2be7529919e061f78b55d434e45 (1280x720; = ../outro_B2_v2/base.mp4 frame 180, mean diff 0.0)
- flow_prompt.txt 44c38a7af603eeb5fb739fceec0bc9b97e2ca797ec8b333f43c783f381dc9fed (3765 chars; lock suffix byte-identical; editor text vs file with whitespace
  removed = identical)
- guide.wav 6786791ea1bb0be7418bfbb44241abafe36c3afbfaf214090a70da2d8c77bfaf (48 kHz mono PCM16, 8.000 s; B3 origin song 4500; NOT used). Energy (RMS/0.25 s):
  0-0.75 tail of "Could've been" (2113/1712/1112), 1.0-2.0 A's "Say goodnight" context (510/850/3645/1338), 2.0-2.75
  quiet, her "To who?" ~2.5-3.0 (408/77/727), 3.0-4.75 A's la-la-la (997/929/1477/286/1372/1616/159), her "You first"
  5.0-5.75 (756/1579/842), 6.0-6.75 A's "Night" context (1396/818/723), 6.75-7.25 quiet, her "Night" 7.25-7.75 (2486/859).
- lock 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC)
- Upload via Add media > Upload; START = top "first_frame.png" picker entry (preview verified: exobiologist, frontal,
  specimen in lap); End empty; no audio. Settings read: Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p,
  "Generating will use 100 credits" (already Veo this time; re-opened and re-read before send). Single send.
- Submitted 18:02:04. 18:02:34 21%; 18:02:54 38%; 18:03:14 100%; 18:03:34 rendered. URL 18:03:44; download 18:04:07.
  ~70 s. No reloads.
- Media id 8ee4df62-654b-4be9-a844-5fd57b04efbd (Flow caption "Woman holding specimen talking..."). Files: `original_8ee4df62-654b-4be9-a844-5fd57b04efbd.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 1d87b75e5458bd74599cfbf26ec804d45d4a870bd24582dfafdb1cac58f52e80. Cost 100 credits.
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio. First frame vs still: mean diff 1.19.

## Base review (contact_every6.jpg, crop_face_every2.jpg [1 s/row], crop_face_cut1/2/3_every2.jpg [frames 55-75,
   120-145, 168-191], crop_artifact_hands_every8.jpg, keyframes_0_57_73_122_143_171_188_191.jpg; traces)
- Identity/suit/room: same face, red bob, plain silver suit; bunk room and window unchanged. Camera locked (drift vs
  frame 0: 6-11 through 6.5 s, then 17-22 from the dimming). No cut or reset.
- Artifact: single fluted shell with spiral, stable, held in the LEFT hand on the lap throughout; not raised or dropped.
- Timeline: 0-1.0 s closed smile frontal; 1.1-2.0 s open articulation frontal (early "To who?"); 2.0-4.0 s toothy smile
  frontal with small lip changes; 4.0-4.2 s open shapes; ~4.2 s HEAD TURNS to her right, near-profile from 4.3 s to the
  end; 4.5-6.0 s singing/smiling in profile; right arm rises and reaches far right toward the lamp 5.3-7.5 s (arm
  extended across the frame edge); whole-frame luma 55 -> 50 at 6.5 s -> 34 at 7.0 s -> 29 at 7.5 s (room dimmed
  heavily; face in shadow); 7.3-8.0 s dark, profile, mouth closed.
- Cut 1 "To who?" (57..74 = 2.375-3.08 s): frontal toothy smile, static (motion 0.2-1.4). FAIL (no articulation).
- Cut 2 "You first" (122..144 = 5.08-6.0 s): head in profile turned right; open singing shapes visible in profile
  5.08-5.5 s, smiling profile after. FAIL (head turned away during words).
- Cut 3 "Night" (171..189 = 7.125-7.875 s): dark, profile, mouth closed (motion 0.1-0.6). FAIL (unlit, turned, silent).
- Hand: long extended reach, not the "poised hand and first small movement" asked for; no glass/prop crossing; no extra
  fingers seen.
- Gate: face/suit/artifact PASS; mouth performance FAIL in all three cuts; head turned away FAIL; face illumination for
  Kling FAIL after 6.5 s; big reach FAIL.

## Kling
- NOT submitted. Balance 321.

## Not done
- No Kling, no retry, no assembly, no FX, no commit, no purchase.
