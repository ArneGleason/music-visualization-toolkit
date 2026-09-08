# RECEIPT: A3 (Flow base + Kling) - BOTH STAGES DONE

Status: claude_done_ready_for_codex_verification. ONE Flow continuation from A3/first_frame.png (= A2 take 1 base frame
172), reviewed with three reported defects (late "Say goodnight", head down during the second half of the sung phrase,
TV switched off during "Night" plus a white flash in the exit frames). The OWNER accepted the base and authorized the
single Kling pass (chat, 2026-09-07). Kling job 590 filed as synced.mp4. Sync verdict: cut 1 usable (mouth moves on
both guide bursts), cut 2 half usable (frontal singing 3.4-4.0 s, then the downturned head stays closed while the guide
sings), cut 3 usable ("Night" frontal 6.27-6.6 s). Details below.

## Inputs verified (SHA-256 match A3/handoff.json)
- first_frame.png a5326cd101648ddaca6414c9a38d0c41940b1dc43c34279f52d7c81a4f499734 (1280x720; = ../outro_A2_v2/take1/base.mp4 frame 172, mean diff 0.0)
- flow_prompt.txt 85345fb4e56464af6b41149993a3d36edfb0b9be3497d2f8af39b1d8b0d7e441 (3790 chars; lock suffix byte-identical; editor text vs file with whitespace
  removed = identical)
- guide.wav b69e16605db4a140ba6f5c71b5d6192423f075f27a22e07f36c89ed4670b573d (48 kHz mono PCM16, 8.000 s, 384000 samples; A3 origin song 4492; NOT used yet).
  Energy (RMS/0.25 s): 0-1.0 her "Say goodnight" tail of previous line + line (794/1774/1874/1336), 1.0-1.5 low, 1.75-2.25
  loud (2854/2659 = "goodnight" end / B's "To who" context?), 2.25-3.5 quiet (B "To who" 2.75 at 403), 3.5-5.75 her
  la-la-la (1155/1006/97/1505/1343/339/1615/58/1743), 5.75-6.25 (695/580/207), 6.5-7.0 her "Night" (1512/913), 7.0-7.5
  silent, 7.5-8.0 B "Night" context (2349/1190).
- lock 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496

## Flow (times UTC)
- Upload via Add media > Upload; START = top "first_frame.png" picker entry (preview verified: astronomer, TV static on);
  End empty; no audio. Model menu had reverted to Omni 1.1 Flash (12 credits); switched to Veo 3.1 - Quality and re-read:
  Video, Frames, 16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100 credits". Single send.
- Submitted 17:56:59. 17:57:30 22%; 17:57:50 39%; 17:58:10 rendered. URL 17:58:40; download 17:59:04. ~70 s. No reloads.
- Media id 13794e3e-2597-46d9-865c-fb46c77a48a3 (Flow caption "Astronomer speaking and adjusting"). Files: `original_13794e3e-2597-46d9-865c-fb46c77a48a3.mp4`
  (untouched) and `base.mp4` (byte-identical), SHA-256 b8d54d355cc078d4c47b1bf3278c04e580d19eb8251625dbf27578f4cc1f5fa8. Cost 100 credits.
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, 8.000 s; disposable Veo audio AAC 48 kHz stereo. First frame vs
  still: mean diff 0.87.

## Base review (contact_every6.jpg, crop_face_every2.jpg [1 s/row], crop_face_cut1/2/3_every2.jpg [frames 10-66, 80-131,
   150-191], crop_tv_hand_every8.jpg, keyframes_0_12_64_82_129_152_178_191.jpg; traces)
- Identity/wardrobe/room: same face, red updo, tweed, checked shirt, mustard cardigan; study, chart, specimens unchanged.
  Camera locked (drift vs frame 0: 0-5 to 4.5 s, then 8-14 from her lean toward the TV; prev-3 diffs 0-4, one 11 at
  7.9 s = the end flash). No cut or reset.
- Television: static on, luma ~52-59 for 0-4.7 s; brighter static 4.75-6.25 s (64-68); screen goes DARK at ~6.33 s
  (48 -> 42) after her knob action; bright white flash 7.7-8.0 s (54 -> 90). Bezel/geometry stable; hand never crosses
  the glass.
- Hand/knob: hand leaves the lap at ~4.2 s, reaches the TV's lower-right knob by ~4.7 s and rests there; a visible turn
  of the knob at ~6.2-6.4 s (screen darkens), hand stays on the set to the end. Natural reach, no extra fingers.
- Mouth-box motion (24 fps): quiet 0-0.9; ACTIVE 1.0-1.3 (4.7-5.7); quiet 1.3-1.8; ACTIVE 1.85-2.8 (5-8); ACTIVE 3.0-3.6
  (2-7.6); 3.7-5.0 high values are the HEAD DROP/turn (9-14), not lips; 5.0-6.0 moderate (3-5, head returning); spike
  6.1-6.3 (9.6/14.6 = knob turn / head); 6.3-7.0 (3-7 speaking); 7.0-8.0 rising 5-14 = head/eyes down + end flash.
- Cut 1 "Say goodnight" (12..65 = 0.5-2.7 s): closed smile with small lip/eye movement 0.5-1.85 s (one small open at
  1.0-1.3 s); open singing articulation with teeth 1.9-2.7 s. LATE (guide has the line at 0-1.0 and 1.75-2.25 s).
  PARTIAL: readable mouth for the last 0.8 s of the cut only.
- Cut 2 sung phrase (82..130 = 3.42-5.42 s): frontal open singing 3.42-4.0 s with teeth; eyes close and head drops
  down-right toward the knob 4.1-4.3 s; 4.3-5.42 s head turned down-right, mouth closed, reaching. PARTIAL: first ~0.7 s
  sung frontal, remaining ~1.3 s turned away with closed mouth while the guide sings.
- Cut 3 "Night" (152..179 = 6.33-7.46 s): frontal, open articulation with teeth 6.25-6.6 s, closed calm 6.7-7.46 s,
  eyes to camera. PASS (guide "Night" 6.5-6.9 s overlaps). TV already dark from 6.33 s inside this cut.
- Exit frames 179-191 (7.46-7.96 s): eyes drop to the set, then the white flash 7.7-8.0 s. Codex plans the phosphor
  shutdown locally; the baked flash sits in the tail only.
- Gate: face/wardrobe PASS; TV shape/hand action PASS (early switch-off, end flash reported); mouth: cut 3 PASS, cut 1
  late/partial, cut 2 half turned away => not waved through; owner decides.

## Kling (times UTC) - job 590
- Lip Sync editor: base.mp4 uploaded; one face, Character 1 = astronomer; Upload Local Dubbing -> A3/guide.wav
  (0:00-0:08, gaps intact); playhead 0:00; Add Speech -> block 0:00-0:08; Sound from Video OFF (zoom verified); Generate
  quoted 10 credits. Submitted 18:17:53; "0/1 Generating" 18:17:58, balance 321 -> 311. Checks 18:20:24 (creating);
  "1/1 Generated" by 18:21:04. Download (Video, MP4, Without Watermark ON) clicked 18:21:26; filed 18:22:20.
- Files: `original_kling_590.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256 8f47e4ffa2b55eef994bf58c3c51725a976e33b39ce1c6db3587a412776fe868
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}]}
  => 1280x720, native 30 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz 7.895 s, starts 0.000. Untouched.
- Audio corr vs guide 1.00 at lag 0. Picture vs base (30 fps compare): full 2.9 / max 4.9; mouth 5.4 / max 14.5; TV
  3.9 / max 17.1 at 7.5 s (base's own end flash); hands 2.8 / max 6.5 (base knob action) => only the mouth changed.
### Sync checks (mouth_synced_cut1_src0.47-2.73s_native30.jpg [every 3rd frame], mouth_synced_cut2_src3.4-5.43s_native30.jpg
    [every 3rd], mouth_synced_cut3_src6.27-7.53s_native30.jpg [every 2nd]; contact_synced_every10_native.jpg)
- Cut 1 "Say goodnight" (12..65 = 0.5-2.7 s): closed smile with small lip motion 0.5-1.1 s; open shapes with teeth
  1.2-1.5 s (motion 6.7/11.3 at 1.0-1.1 s); smile 1.6-2.0 s; open singing shapes 2.1-2.7 s (motion 5-11). The guide has
  voice at 0-1.0 s and 1.75-2.25 s; Kling animates both bursts, though the first one reads as a small opening over the
  smile. USABLE; opening phoneme soft, ending strong.
- Cut 2 sung phrase (82..130 = 3.42-5.42 s): strong open singing 3.4-4.05 s with mouth interior; eyes close 4.1 s; head
  drops toward the knob 4.3 s; 4.3-5.42 s head down-right with a CLOSED mouth - Kling did not articulate on the
  downturned face while the guide still sings (4.25-5.3 s). HALF: frontal first 0.65 s good, remainder silent.
- Cut 3 "Night" (152..179 = 6.33-7.46 s): open "Night" shapes 6.27-6.6 s frontal (motion 11.5/9.4 at 6.13-6.2 s), closed
  calm 6.7-7.46 s, eyes to camera; TV dark in the background from 6.33 s. USABLE. Unsynced motion after voice: none
  until the exit frames (7.6-8.0 s eyes down + flash from the base).
- Other: no puppet lips, no teeth artefacts, no face change.

## Not done
- No retry, no second Kling, no assembly, no FX, no commit, no purchase. Base acceptance was the owner's call in chat.
