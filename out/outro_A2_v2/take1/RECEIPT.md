# RECEIPT: outro_A2_v2 (Flow base done; Kling WITHHELD for owner review)

Status: base_needs_owner_review. ONE Flow continuation generated from the supplied first_frame.png (= A1 v3 base frame
155, pixel-identical). Downloaded untouched with a byte-identical base.mp4. Identity, brown wardrobe, room, camera and
the second line "Was it you?" all pass. Three material problems against base_gate.must_pass, so Kling was skipped and no
retry made: (1) during the first line "Thought I heard something." (source 42..80 = 1.75-3.33 s) she turns her head
toward the television and speaks in three-quarter to near-profile for ~1.9-3.2 s (gate: no head turned away; prompt asked
for eye-only glance); (2) the television switches on with a bright white flash at 0.85-1.0 s and then shows bright
rolling static for the remaining 7 s (gate: clear stable screen; prompt: no large flash, no new programme); (3) she
raises her right hand and points at the television 2.5-3.3 s (prompt: hands low, no reaching; the finger stops at the
bezel and does not cover the glass). Owner decides: accept and run Kling, or one retry.

## Inputs verified (SHA-256 match handoff.json)
- first_frame.png 3c0f7c873869bc0d03e85eb32252d07a44d5d5d6e729fbbba2da7b26b1c55bf9 (1280x720; equals ../outro_A1_v3/base.mp4 frame 155 exactly, mean diff 0.0)
- continuation_base ../outro_A1_v3/base.mp4 99124a5780cd629cb086e9d362db2e1d78bb5afa2a9d89ca41fc09a428c13767 (not uploaded)
- approved_anchor ../outro_anchors_v2/astronomer.png bb733e52548540403d7b4f3a5d4303999d65a8af71e7ff3317acb9565de1ebab (comparison only)
- flow_prompt.txt 96067b3bdc4b8dae565a31d7fbe5716e4f992d4f752e0a9443a318c6bb7a1adc (4093 chars; lock suffix byte-identical to style_lock_v2.txt; pasted once via
  execCommand insertText; editor text vs file with whitespace removed = identical, 3503 chars)
- lock ../astronaut_reply_v1/style_lock_v2.txt 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide.wav ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004 (byte-identical to the B2 guide; 48 kHz mono PCM16, 8.000 s; NOT used - Kling withheld).
  Her lines in it: "Thought I heard something" 1.75-3.25 s (RMS 473/204/376/398/555/309 - quiet), "Was it you?"
  4.5-5.75 s (83/640/672/1017/2016), "Say goodnight" from ~7.5 s (context). Other speaker: 0.5-1.75, 3.5-4.5, 5.75-7.25.

## Flow (times UTC)
- Fresh upload of first_frame.png via Add media > Upload (hooked file input); selected as START by real click on the top
  "first_frame.png" picker entry (preview verified: astronomer in study with television); End empty; no audio. The
  settings panel had reverted to "Omni 1.1 Flash / 12 credits"; switched the model menu to "Veo 3.1 - Quality" and
  re-read: Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100 credits". Flow's "high demand"
  banner was showing. Single send via Start generation after re-verifying prompt/slots/panel closed.
- Submitted 16:58:22. 16:58:52 23%; 16:59:12 39%; 16:59:32 100%; 16:59:50 rendered. URL read 16:59:53; download 17:00:15.
  About 90 s. No reloads, no duplicate.
- Media id 9c4966e4-3c3a-4721-b49c-bc16c2830195 (Flow caption "Astronomer speaking in her study"). Files: `original_9c4966e4-3c3a-4721-b49c-bc16c2830195.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 8836ee224def240a37f4b00daa2770b52c37207142dd61f2c2262bf2864c7007. Cost 100 credits.
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, video 8.000 s; disposable Veo audio AAC 48 kHz stereo 8.000 s.
  First generated frame vs first_frame.png: mean diff 0.8 (64x36).

## Base review (contact_every6.jpg, crop_face_every2.jpg [1 s per row], crop_face_cut1_every2.jpg [frames 40-80],
   crop_face_cut2_every2.jpg [frames 109-141], crop_tv_every8.jpg, crop_tv_switch_f18-34_every2.jpg,
   crop_hand_tv_f56-88_every2.jpg, keyframes_0_42_79_111_140_155_172_191.jpg; traces)
- Identity/wardrobe: same face, red updo and fringe, brown tweed coat, checked shirt, mustard cardigan throughout. Study,
  chart, specimens, lamp unchanged. Camera locked (drift vs frame 0 only 0 -> 9, prev-3 diffs 0-3 at the head turn).
  No cut or reset.
- Television: dark dim glass 0-0.8 s (luma 31); a bright white flash 0.85-1.0 s (luma 67 at frame 24), then bright
  rolling static that settles to steady static (luma ~54) for 1.0-8.0 s. Screen glass and bezel geometry stable and
  unobstructed. This is a baked-in "switch-on" plus persistent static, not a gentle fluctuation.
- Hands: low and still except 2.5-3.3 s, when the right hand rises and points at the television (finger near the bezel,
  glass never covered), then returns low by 3.5 s.
- Mouth motion trace (24 fps): quiet 0-1.0 s; ACTIVE 1.55-2.7 s (4-7) and 2.9-3.4 s; ACTIVE 3.05-3.5 s (5-10, frontal
  return); quiet 4.0-5.0 s; ACTIVE 5.1-5.35 s (3.5-7.4) and 5.5 s; quiet 6.0-7.5 s; rising 7.6-8.0 s (Say goodnight).
- Line 1 "Thought I heard something." (cut 42..80 = 1.75-3.33 s): open articulation with teeth begins ~1.0-1.7 s
  (EARLY, frontal), eyes then head turn to the television at 1.7-1.9 s, and she keeps speaking with open shapes while
  turned three-quarter/near-profile 1.9-3.2 s; face returns frontal 3.2-3.4 s with an open mouth. Articulation present
  but FACE TURNED AWAY for most of the cut. FAIL (head turned away).
- Line 2 "Was it you?" (cut 111..141 = 4.625-5.875 s): frontal, closed smile 4.6-5.1 s, teeth-visible smile 5.2 s, open
  articulation with mouth interior 5.3-5.75 s, easing to a smile 5.8-5.9 s. PASS (slightly late in the cut).
- Other: 3.3-4.0 s frontal open articulation (early "Was it you?"), 4.0-5.0 s listening smile, 6-7 s listening, 7.0-7.5
  s eyes drop/aside, 7.6-8.0 s "Say goodnight" shapes (context). Warmth modest; no fixed grin.
- Frame 172 (7.17 s, future A3 anchor at song 4492): frontal, mouth closed, eyes slightly aside/down, hands low, TV static
  on. Usable pose; the baked static would carry into A3.
- Gate: face/wardrobe PASS; TV stable geometry PASS but clear screen FAIL (flash + persistent static); hands mostly
  PASS (pointing gesture reported); articulation line 2 PASS, line 1 FAIL on head turn; no cut PASS.

## Kling
- NOT submitted (gate failure). Balance remains 341.

## Owner options
- (a) Accept and run the single Kling pass: Kling can sync a three-quarter face, but line 1 would play mostly turned to
  the television, and Codex's planned TV composite would sit over baked static that starts with a flash at 0.85 s.
- (b) One Flow retry from the same first_frame.png with a stronger no-head-turn / no-TV-switch-on prompt (owner-authorized
  edit, as done for B2 take 2). Recommended, because the turn and the baked static affect the cut and the composite,
  not just the mouth.

## Not done
- No Kling, no retry, no A3/B3, no assembly, no FX, no production edits, no commit, no purchase, no owner approval claimed.


## ADDENDUM 2026-09-07 - Kling on this take (owner-authorized comparison; see ../RECEIPT.md for detail)
- Job 321, submitted 17:19:01Z, generated 17:22:16Z, filed 17:23:04Z, 10 credits (331 -> 321). Guide at 0:00, zero
  offset, Sound from Video OFF. Files: `original_kling_321.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256
  50f8dac28f5a9fdf98108e49077b98985027873229627d39e6df8a13cc01ecf8; native 30 fps, 239 frames, 7.967 s video / 7.895 s audio, starts 0.000. Audio corr 1.00 at lag 0.
- Line 1 articulated while turned toward the TV (finger on screen under "something" 2.5-3.3 s); line 2 frontal and
  strong 5.27-5.8 s. Sheets: mouth_synced_cut1_src1.67-3.4s_native30.jpg, mouth_synced_cut2_src4.53-5.93s_native30.jpg,
  contact_synced_every10_native.jpg.
