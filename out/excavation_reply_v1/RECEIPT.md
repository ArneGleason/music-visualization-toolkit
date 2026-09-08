# RECEIPT: excavation_reply_v1

Status: DONE - one Flow take generated from first_frame.png, downloaded untouched and inspected across all 192 frames.
Candidate with defects: the emotional turn is there (ironic first phrase -> sincere direct question, sincere singing 3.1-4.6 s is
good), but the irony is overplayed (eyes squeezed shut 0.75-1.25 s, then a broad toothy grin with an upward eye-roll and a
SILENT mouth from ~1.4 s to ~3.1 s), and singing starts early at ~0.25 s. No Kling, no audio, no retry, no assembly, no FX,
no production edits, no commit. Writes only under this folder.

## Inputs verified (SHA-256 match handoff.json)
- first frame `first_frame.png`: 560f85802221135c920d32842a030e512bd1269748db81a4c0293a60f9afadf3 (1280x720; uploaded fresh via Add media > Upload; chosen from the three
  library files named first_frame.png by its kneeling close-up preview; generated first frame matches it, mean diff 1.6 at 64x36).
  The old s031 close-up and shop references were not used; generated_reference.png was not uploaded.
- prompt `flow_prompt.txt`: e2e71568c4e0bf85c07c73225fc9b65bebb2f4ccb5dd5239e39894ef1fdaa721 (4475 chars) pasted once with execCommand insertText; editor text compared
  to the file with whitespace removed = identical. Lock included verbatim.
- lock `out/astronaut_reply_v1/style_lock_v2.txt`: 6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496
- End slot verified empty.

## Flow (times UTC; local = UTC-4)
- Settings panel read before submit: Video, Frames, 16:9, "Veo 3.1 - Quality", 8s, x1, chip 720p, "Generating will use 100
  credits". Flow's "high demand" banner was still up; the single submission succeeded, no retry.
- Submitted 19:41:03. Progress 19:41:33 21%; 19:41:53 38%; 19:42:13 55%; 19:42:33 tile rendered (complete). Tile URL read
  19:42:51; download 19:43:13. About 90 s. Checks at 30 s then every 20 s; no reloads, no resubmission.
- Media id 5440b7cc-1c0e-4404-ba17-ba62af34a613. Files: `original_5440b7cc-1c0e-4404-ba17-ba62af34a613.mp4` (untouched) and `base.mp4` (byte-identical),
  SHA-256 d7c268d3f466277922651125dbe953d3b66897d4193d87e3d8f6dfd0d63e2ca0
- ffprobe: {"programs": [], "stream_groups": [], "streams": [{"codec_name": "h264", "codec_type": "video", "width": 1280, "height": 720, "r_frame_rate": "24/1", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "192"}, {"codec_name": "aac", "codec_type": "audio", "r_frame_rate": "0/0", "start_time": "0.000000", "duration": "8.000000", "nb_frames": "377"}], "format": {"duration": "8.000000"}}
  => 1280x720, 24/1 native, 192 frames, start 0.000, 8.000 s, disposable Veo audio (nothing uploaded). No watermark. 100 credits.

## Inspection (contact_every6.jpg; crop_mouth_0-4.6s_every2.jpg = frames 0-110 every 2, 8 per row; crop_face_0-4.6s_every4.jpg;
   crop_mouth_4.6-8s_every8.jpg; per-frame mouth-motion trace; drift trace)
- Camera: locked; background water/earth pattern holds; no cut, zoom or drift. Kneeling continuity: same framing, collar and
  shoulders; she gradually sits up a little from ~3 s (torso less inclined) but never stands or moves out of position. No hands
  in front of the face, no props, no scene change. Identity, hair, freckles, collar consistent; teeth natural and warm.
- Actual timing (source seconds, 24 fps):
  * 0.00: gaze already near the lens (as in the reference); no large head lift needed.
  * 0.25 s (f6): SINGING ONSET - mouth opens with teeth visible, brows knitted. Early (window asked for 0.875).
  * 0.25-0.70 (f6-16): open-mouth articulation with a slight frown - reads a touch harsh rather than dry.
  * 0.75-1.25 (f18-30): EYES SQUEEZED SHUT in a wince/grimace with the mouth held open - comic mugging, not a tiny glance.
  * 1.33-1.95 (f32-46): eyes open into a SIDEWAYS GLANCE (screen left), eyebrow raised, smile widens with teeth.
  * 1.4-3.1 (f34-74): mouth FROZEN in a broad toothy grin; the mouth-motion trace sits at 1-2 for this whole stretch, i.e. no
    articulation - a silent gap covering most of "stupid" (target 0.875-2.83).
  * 2.0-2.6 (f48-62): eyes roll up/sideways while grinning - broader than the requested fleeting half-smile.
  * 2.9-3.25 (f70-78): gaze returns to the lens, blink, smile recedes - the TURN TO SINCERITY. Clear and readable.
  * 3.1-4.6 (f74-110): SINCERE SINGING - varied jaw/lip shapes, upper teeth and mouth interior visible, brows lifted, steady
    direct eye contact; "Can you hear what I meant?" reads as an earnest question. Onset ~0.27 s later than the 2.83 target;
    ends ~0.2 s after the 4.417 target.
  * 4.6 s (f110): mouth SETTLES closed.
  * 4.6-8.0: attentive listening hold at the lens, blinks, small settle; one small lip press/parting at ~6.7-6.9 s (f160-166),
    no words, no scat, no gaze drop. No "duh" mouthed.
- Proposed window [12,106) (0.5-4.42 s): contains the early singing, the wince, the grin gap, the turn and the sincere phrase.
  The sincere half (3.1-4.6 s) is a strong base; the ironic half is overacted and mostly silent, so a later lip-sync pass would
  have to animate "Especially stupid" over a frozen grin (Kling can move the mouth but not remove the squeezed eyes/eye-roll).
- Usable coverage: [70,192) (2.9-8.0 s) clean for the sincere question and hold; [0,70) usable only if the owner accepts the
  broad ironic mugging and the silent grin.

## Defects (summary)
- Singing starts at 0.25 s, before the 0.875 s window.
- Eyes squeezed shut 0.75-1.25 s; broad toothy grin with upward eye-roll 1.4-3.1 s (mugging, not a fleeting half-smile).
- Silent mouth 1.4-3.1 s: "stupid" not articulated.
- Sincere phrase onset ~3.1 s (target 2.83) and end ~4.6 s (target 4.42).
- Minor: she sits up slightly over the take; tiny lip motion at 6.7-6.9 s.

## Not done
- No Kling, no audio, no retry, no assembly, no FX, no production edits, no commit, no owner approval claimed.
