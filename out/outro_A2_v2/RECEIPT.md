# RECEIPT: outro_A2_v2 (two Flow takes, Kling on BOTH) - BOTH STAGES DONE

Status: claude_done_ready_for_codex_verification. Take 1 (Codex prompt) failed the base gate (head turned to the TV
during line 1, TV switch-on flash with baked static, pointing gesture); the OWNER authorized ONE Flow retry with a prompt
edit (flow_prompt_take2.txt, lock byte-identical). Take 2 is clean (frontal, dark TV, still hands) but smiles through
both assigned cuts. The OWNER then authorized Kling on BOTH takes for a per-cut comparison (chat, 2026-09-07), with the
guide at ZERO offset on both (see "Creative note" for why no offset was used). Results: take 1 + Kling (job 321,
take1/synced.mp4) articulates both lines - line 1 while turned toward the TV, line 2 frontal and strong; take 2 + Kling
(job 325, synced.mp4) stays a near-closed smile through both cuts (weak). Per-cut suggestion: take 1 for both cuts.
Current base.mp4/synced.mp4 = TAKE 2; take 1 base + synced preserved in take1/.

## Creative note for Codex (owner asked me to consider a different lip-sync offset for take 1)
- I checked the natural alignment first and kept ZERO offset on both jobs: with the guide unshifted, "Thought I heard"
  falls on her turn toward the television (1.75-2.6 s) and "something" (2.8-3.25 s) lands exactly while her finger is on
  the screen (2.5-3.3 s). A slid guide would have moved the mouth away from that beat and broken the continuous song
  clock the assembly conforms against. So no offset was chosen; the manifest clock is unchanged (source 0 = song 4320).
- The beat that falls out of take 1 for free: the television switches on (flash 0.85-1.0 s, then static) while A2 is
  OFFSCREEN (B's "No, go on" cut, song 4331..4362 = A2 source 0.46-1.75 s). When we cut back to A at source 42 the
  screen has already changed, she says "Thought I heard something" turning to it and pointing at "something", then
  returns frontal for "Was it you?". Suggested overlay: a punctuation graphic on the TV glass at source 2.5-3.3 s
  (song 4380-4399), i.e. the "something" she points at; the baked static can serve as the switched-on texture under it.
- If take 1 is chosen for A2, the A3 anchor should be TAKE 1 base frame 172 (TV static on, eyes slightly aside), not
  take 2's frame 172 - otherwise the TV state jumps between A2 and A3.

## Inputs verified (SHA-256 match handoff.json)
- first_frame.png 3c0f7c873869bc0d03e85eb32252d07a44d5d5d6e729fbbba2da7b26b1c55bf9 (= ../outro_A1_v3/base.mp4 frame 155, mean diff 0.0)
- continuation_base ../outro_A1_v3/base.mp4 99124a5780cd629cb086e9d362db2e1d78bb5afa2a9d89ca41fc09a428c13767 (not uploaded)
- approved_anchor ../outro_anchors_v2/astronomer.png bb733e52548540403d7b4f3a5d4303999d65a8af71e7ff3317acb9565de1ebab (comparison only)
- flow_prompt.txt 96067b3bdc4b8dae565a31d7fbe5716e4f992d4f752e0a9443a318c6bb7a1adc (take 1, Codex prompt, 4093 chars)
- flow_prompt_take2.txt 37748ab8858993f0df12eeb050ba10683d08f88649710e83bfe9c21762f5041f (take 2, owner-authorized edit, 4440 chars; lock suffix byte-identical)
- lock ../astronaut_reply_v1/style_lock_v2.txt 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- guide.wav ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004 (byte-identical to B2 guide; 48 kHz mono PCM16, 8.000 s; not yet used). Her lines:
  "Thought I heard something" 1.75-3.25 s at low level (RMS 473/204/376/398/555/309), "Was it you?" 4.5-5.75 s
  (83/640/672/1017/2016), "Say goodnight" from ~7.5 s. Other speaker 0.5-1.75, 3.5-4.5, 5.75-7.25 s.

## Prompt change for take 2 (three edits, everything else verbatim)
1. Line 1 direction adds: delivered straight to the colleague near camera, head level, face fully frontal for the entire
   line; she does not turn her head or body toward the television at any point.
2. "Keep the head level and face near-frontal... eye-only glance toward the television... Hands low, no reaching" replaced
   by: head level and fully frontal for all 8 s, no head turn/profile/downward gaze; she never looks at the television;
   hands low and still in her lap, no pointing, reaching, raising or gesturing toward the television.
3. TV paragraph replaced by: the television stays exactly as in the attached frame, switched off, dark dim glass with a
   faint phosphor sheen; it does not switch on, brighten, flash, flicker, roll or show static/picture/programme/text.

## Take 1 - Flow (Codex prompt) - see take1/RECEIPT.md
- Media 9c4966e4-3c3a-4721-b49c-bc16c2830195, submitted 16:58:22Z, rendered 16:59:32Z, downloaded 17:00:15Z, 100
  credits, 24 fps/192, SHA-256 8836ee224def240a37f4b00daa2770b52c37207142dd61f2c2262bf2864c7007. Line 1 articulated but head turned to TV 1.9-3.2 s; line 2 PASS frontal 5.3-5.75 s;
  TV flash 0.85-1.0 s then baked static; hand points at TV 2.5-3.3 s.

## Take 2 - Flow (owner-authorized prompt) (times UTC)
- Same first_frame.png selected as START from the picker (top entry, preview verified); End empty; no audio. The model
  menu had again reverted to "Omni 1.1 Flash / 12 credits"; switched to "Veo 3.1 - Quality" and re-read: Video, Frames,
  16:9, Veo 3.1 - Quality, 8s, x1, 720p, "Generating will use 100 credits". Editor text vs flow_prompt_take2.txt with
  whitespace removed = identical. Single send.
- Submitted 17:07:07. 17:07:37 21%; 17:07:57 38%; 17:08:17 100%; 17:08:37 rendered. URL 17:08:47; download 17:09:11.
  About 70 s. No reloads, no duplicate.
- Media id d2f6d806-4ddb-4619-bf14-8f7878a6d525 (Flow caption "Astronomer speaking in study"). Files: `original_d2f6d806-4ddb-4619-bf14-8f7878a6d525.mp4` (untouched)
  and `base.mp4` (byte-identical), SHA-256 e814d46b8fb0e65844998765c893fea3deaf47f9dae68d89a80d5dfcbd5ac956. Cost 100 credits (200 total for this handoff).
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "48000", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}]}
  => 1280x720, 24/1, 192 decoded frames, start 0.000, video 8.000 s; disposable Veo audio AAC 48 kHz stereo 8.000 s.
  First generated frame vs first_frame.png: mean diff 0.82.

### Take 2 base review (contact_every6.jpg, crop_face_every2.jpg [1 s/row], crop_face_cut1_every2.jpg [frames 40-80],
    crop_face_cut2_every2.jpg [frames 109-141], crop_tv_every8.jpg, crop_hands_every12.jpg,
    keyframes_0_42_79_111_140_155_172_191.jpg; traces)
- Identity/wardrobe: same face, red updo, brown tweed, checked shirt, mustard cardigan throughout; study unchanged.
  Camera locked (drift vs frame 0 only 0 -> 10, prev-3 diffs 0-1). No cut or reset.
- Television: dark dim glass for all 8 s (luma 31 -> 28, slow fade only); no flash, no static, geometry stable and
  unobstructed. PASS.
- Hands: low and still in her lap for all 8 s. PASS. Face: fully frontal, head level, eyes on camera for all 8 s (one
  blink ~2.9 s, one ~6.3 s). PASS.
- Mouth motion trace (24 fps): quiet 0-0.6; active 0.7-1.3 s (2-5); small 1.4-2.0 (1-2.6); quiet 2.0-3.0 (0.5-1.5);
  ACTIVE 3.1-3.9 s (2.6-5.0); fading 4.0-4.2; QUIET 4.2-6.4 s (0.3-0.9); active 6.5-8.0 s (3-6.6).
- Line 1 "Thought I heard something." (cut 42..80 = 1.75-3.33 s): open articulation with teeth happens EARLY at
  0.7-1.3 s; inside the cut she holds a teeth-visible then closed smile 1.75-2.9 s with only small lip changes, blinks,
  and begins new open/puckered shapes at 3.05-3.33 s. WEAK/FAIL (persistent smile through most of the cut).
- Between cuts: frontal open articulation 3.1-3.9 s (the displaced line), listening smile 4.0-4.6 s.
- Line 2 "Was it you?" (cut 111..141 = 4.625-5.875 s): closed-lip smile, static, no mouth motion for the whole cut. FAIL.
- After: listening smile to 6.4 s, then open articulation 6.5-8.0 s with teeth (late "Was it you?" running into "Say
  goodnight"), frontal.
- Frame 172 (7.17 s, future A3 anchor): frontal, level, mouth open mid-word, hands low, TV dark. Pose OK, mouth mid-shape.
- Warmth: teeth-visible smile 1.5-2.6 s, otherwise modest. No grin.
- Gate: face/wardrobe PASS, TV clear/stable PASS, hands PASS, frontal PASS, no cut PASS; articulation inside BOTH
  assigned cuts FAIL (closed smile), although she articulates plenty elsewhere.

## Kling - both takes (times UTC), guide at 0:00-0:08, gaps intact, Sound from Video OFF, MP4 Without Watermark
### Take 2 -> job 325 (this folder)
- base.mp4 (take 2) uploaded; one face, Character 1 = astronomer; Upload Local Dubbing guide.wav; playhead 0:00; Add
  Speech -> block 0:00-0:08; Generate quoted 10 credits. Submitted 17:16:19; "Task submitted / 0/1 Generating" 17:16:24,
  balance 341 -> 331. Checks 17:16:49, 17:17:09, 17:17:29 (creating); "1/2 Generated" seen 17:19:31 (take 1 job in
  flight alongside). Download clicked 17:20:43; filed 17:21:04.
- Files: `original_kling_325.mp4` (untouched) and `synced.mp4` (byte-identical), SHA-256 67f343cff2e78837e8150c4494608575e178c61fa91ad734c0de04f31da3b618
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}]}
  => 1280x720, native 30 fps, 239 frames, video 7.967 s, audio AAC 44.1 kHz 7.895 s, starts 0.000. Untouched.
- Audio corr vs guide 1.00 at lag 0. Picture vs base: full 2.7 / max 3.2; mouth 4.4 / max 10.5; TV 2.6 / max 2.9; hands
  2.7; desk 2.5 => only the mouth changed; TV stays dark.
- Line 1 (cut 42..80 = 1.75-3.33 s; mouth_synced_cut1_src1.67-3.4s_native30.jpg): small lip changes over the smile with
  teeth showing 1.67-2.5 s, closed smile 2.5-2.85 s, open shapes 2.9-3.4 s. "Thought I heard" barely reads; "something"
  reads late. WEAK (guide quiet, base smiling).
- Line 2 (cut 111..141 = 4.625-5.875 s; mouth_synced_cut2_src4.53-5.93s_native30.jpg): open shapes 4.53-4.7 s (before
  the word), teeth smile 4.8-5.2 s, closed smile 5.27-5.8 s, slight parting 5.87 s. "Was it you?" does NOT read. FAIL.
- Elsewhere: strong shapes 6.9-8.0 s ("Say goodnight" context). No puppet lips or face change.
### Take 1 -> job 321 (take1/)
- take1/base.mp4 uploaded on a fresh Lip Sync page while job 325 was running (Kling allows parallel jobs; distinct
  inputs, not a duplicate); one face, Character 1; guide.wav; Add Speech 0:00-0:08; 10 credits. Submitted 17:19:01;
  "0/2 Generating" 17:19:06, balance 331 -> 321. Checks 17:19:31, 17:19:51, 17:20:11, 17:21:16, 17:21:36, 17:21:56;
  "1/1 Generated" 17:22:16. Download clicked 17:22:33; filed 17:23:04.
- Files: `take1/original_kling_321.mp4` (untouched) and `take1/synced.mp4` (byte-identical), SHA-256 50f8dac28f5a9fdf98108e49077b98985027873229627d39e6df8a13cc01ecf8
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "30/1", "start_time": "0.000000", "duration": "7.966667", "nb_frames": "239"}, {"codec_name": "aac", "codec_type": "audio", "sample_rate": "44100", "channels": 2, "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "7.895011", "nb_frames": "341"}]}
  => same native format (30 fps, 239 frames, 7.967 s / 7.895 s, starts 0.000). Untouched.
- Audio corr vs guide 1.00 at lag 0. Picture vs take-1 base: full 2.9 / max 8.0 (0.87 s = base's own TV flash);
  mouth 4.2 / max 10.1; TV 4.2 / max 36.8 at 0.87 s (base flash timing, not Kling); hands 2.7 / max 6.2 (base's point);
  desk 2.4 => only the mouth changed.
- Line 1 (take1/mouth_synced_cut1_src1.67-3.4s_native30.jpg): open articulation throughout 1.67-3.1 s while the head is
  turned three-quarter toward the TV (jaw and vowel shapes visible in profile), frontal open shapes 3.13-3.4 s.
  "Thought I heard something" READS, but turned away; finger on the screen 2.5-3.3 s under "something".
- Line 2 (take1/mouth_synced_cut2_src4.53-5.93s_native30.jpg): frontal; open shapes with teeth 4.53-4.7 s, small shapes
  4.8-5.2 s, then big open vowels 5.27-5.8 s for "Was it you?", closing 5.87 s. STRONG, best of all A2 material.
- Elsewhere: quiet 6-7.5 s, small shapes 7.5-8.0 s (context). No puppet lips or face change.

## Per-cut suggestion (for Codex/owner, not applied)
- Line 1 (42..80): take 1 (job 321) - articulated, and the turn + point is the "something on the screen" beat; needs
  the TV overlay at 2.5-3.3 s to pay it off. Take 2 is frontal but mouth barely moves.
- Line 2 (111..141): take 1 (job 321) - frontal and strong. Take 2 fails here.
- Both cuts from take 1 keeps the TV state continuous (static from 1.0 s). A3 anchor then = take 1 base frame 172.

## Credits
- Flow 200 (two takes), Kling 20 (two jobs). Kling balance 321.

## Not done
- No third Flow, no further Kling, no A3/B3, no assembly, no FX, no production edits, no commit, no purchase. The
  retry, the prompt edit and the double Kling were owner-authorized in chat (2026-09-07). Codex verifies and picks.
