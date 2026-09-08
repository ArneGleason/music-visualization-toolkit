# RECEIPT: B3 (two Flow takes; Kling WITHHELD pending owner call)

Status: base_needs_owner_review. Take 1 (Codex prompt, media 8ee4df62) was a material failure: profile from 4.2 s, long
arm reach, room dark through "Night". The OWNER authorized ONE Flow retry with a prompt edit made in this session
(flow_prompt_take2.txt, lock byte-identical: no head turn ever, room lighting unchanged for 8 s, hand rests low and only
the fingers move after the word). Take 2 (media 8bf94ffa, now base.mp4) fixes the lighting (constant luma 49-50, face lit
to the last frame) and stays frontal for 6.5 s, but Veo still plays the light-control beat: at ~6.5 s she turns her head
to her right into profile, the right arm extends to a bedside panel at the frame edge, and "Night" (source 171..189 =
7.125-7.875 s) is again delivered in profile with a closed mouth. "To who?" is only its tail inside its cut and "You first"
is a toothy smile with small lip motion. So the final line fails on both takes. Kling withheld; owner decides. Take 1
preserved in take1/.

## Inputs verified (SHA-256 match B3/handoff.json)
- first_frame.png 13f777d66862118bb85ff1fc3ebdc0cbcc64b2be7529919e061f78b55d434e45 (= ../outro_B2_v2/base.mp4 frame 180, mean diff 0.0)
- flow_prompt.txt 44c38a7af603eeb5fb739fceec0bc9b97e2ca797ec8b333f43c783f381dc9fed (take 1, Codex prompt, 3765 chars)
- flow_prompt_take2.txt 0d34802c26bfd94075405f35c8aa1c7fd3237bdac815013282da0a89871d6d5d (take 2, owner-authorized edit, 4287 chars; lock suffix byte-identical; editor text vs
  file with whitespace removed = identical)
- guide.wav 6786791ea1bb0be7418bfbb44241abafe36c3afbfaf214090a70da2d8c77bfaf (48 kHz mono PCM16, 8.000 s; B3 origin song 4500; not used). Her lines: "To who?"
  ~2.5-3.0 s (RMS 408/77/727), "You first" 5.0-5.75 s (756/1579/842), "Night" 7.25-7.75 s (2486/859).
- lock 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Prompt change for take 2 (four edits, everything else verbatim)
1. "To who?" delivered fully frontal; before it she only listens with a still, softly closed mouth.
2. "You first" fully frontal, head level; the free hand rests low beside her hip where a small bedside control sits at the
   frame edge, arm bent and relaxed, nothing extended.
3. "Night" fully frontal and fully lit; no head turn/profile/downward glance; room lighting unchanged through the last
   frame; only a tiny finger movement toward the control after the word; the room does NOT dim on screen; she never turns
   her head or body to either side.
4. Room and face fully lit for all 8 s, identical to the attached frame; no dimming, blackout or fade.

## Take 1 - Flow (Codex prompt) - see take1/RECEIPT.md
- Media 8ee4df62-654b-4be9-a844-5fd57b04efbd, submitted 18:02:04Z, rendered 18:03:14Z, downloaded 18:04:07Z, 100
  credits, SHA-256 1d87b75e5458bd74599cfbf26ec804d45d4a870bd24582dfafdb1cac58f52e80. Profile from 4.2 s, arm reach 5.3-7.5 s, room dark from 6.5 s; all three cuts FAIL.

## Take 2 - Flow (owner-authorized prompt) (times UTC)
- Run from the second Flow tab while A3's Kling job was in flight. START = top "first_frame.png" picker entry (selected
  by a direct click on the entry; Start thumbnail zoom verified: exobiologist in the bunk room); End empty; no audio.
  Settings read: Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100 credits". Single send.
- Submitted 18:19:54. 18:20:24 21%; 18:20:44 38%; 18:21:04 55%; 18:21:35 rendered. URL 18:21:42; download 18:22:23.
  ~100 s. No reloads.
- Media id 8bf94ffa-1aaf-42b1-990b-bb0e42255e3e (Flow caption "Exobiologist holding specimen in..."). Files: `original_8bf94ffa-1aaf-42b1-990b-bb0e42255e3e.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 a9e95b5ad3f8147fd549ec78077166c45e50c57e55d24d17e9973efdb87275ec. Cost 100 credits (200 total for B3).
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio. First frame vs still: mean diff 1.11.

### Take 2 base review (contact_every6.jpg, crop_face_every2.jpg [1 s/row], crop_face_cut1/2/3_every2.jpg [frames
    55-75, 120-145, 168-191], crop_artifact_hands_every8.jpg, keyframes_0_57_73_122_143_171_188_191.jpg; traces)
- Identity/suit/room: same face, red bob, plain silver suit; bunk room unchanged. Whole-frame luma constant 49-50 for all
  8 s (no dimming). Camera locked (drift vs frame 0: 0 -> 16 from her own motion). No cut or reset.
- Artifact: single fluted shell with spiral, stable in both hands on the lap to ~6.3 s, then in the left hand while the
  right arm reaches; never raised or dropped.
- Timeline: 0-0.5 s closed smile frontal; 0.5-1.0 s eyes down; 1.1-2.0 s open articulation with eyes lowered (early "To
  who?"); 2.0-2.5 s frontal small open/puckered shapes ("who?" 2.375-2.5 s); 2.5-4.0 s closed smile frontal; 4.0-5.0 s
  small lip motion, smile; 5.0-5.3 s slight open shapes; 5.3-6.0 s toothy smile frontal; 6.1-6.5 s open shapes (late
  "You first"); ~6.5 s head turns right, profile by 7.0 s; 6.3-8.0 s right arm extends to a bedside panel at the frame
  edge; 7.0-8.0 s profile, mouth closed.
- Cut 1 "To who?" (57..74 = 2.375-3.08 s): puckered "who" lips 2.375-2.5 s, then closed smile. PARTIAL (tail only).
- Cut 2 "You first" (122..144 = 5.08-6.0 s): frontal; slight open shapes 5.08-5.3 s, then toothy smile with small lip
  motion (2-3.8). WEAK.
- Cut 3 "Night" (171..189 = 7.125-7.875 s): profile, turned right, mouth closed, arm extended. FAIL.
- Hand: the "tiny finger movement" became a full reach again, though later and lit.
- Gate: face/suit/artifact/lighting PASS; frontal to 6.5 s PASS; cut 3 head turned away + silent FAIL; cuts 1-2 weak.

## Kling
- NOT submitted. Balance 311.

## Owner options
- (a) Kling on take 2 for cuts 1 and 2 (frontal, lit) and let Codex cover "Night" another way (artifact/afterglow insert,
  tight crop of the profile, or the A3 "Night" reply carrying the beat).
- (b) One more Flow with the light-control beat removed entirely (no control, no reach, hands stay on the specimen), so
  Veo has no reason to turn her.
- (c) Kling on take 1 for comparison (not recommended: dark and profile at the end).

## Not done
- No Kling, no third Flow, no assembly, no FX, no commit, no purchase. The retry and its prompt edit were owner-authorized
  in chat (2026-09-07).
