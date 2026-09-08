# Returning reply review

preview.mp4 covers song971..1201 at24fps, 230 frames, with the previous approved
astronaut duet followed by receiver picture1082..1201. Master audio once; lyrics
once. Flow audio is discarded. Review pending, not production adoption.

Source: out/receiver_reply_arrival_v1/base.mp4, verified SHA-256 against receipt.
Native24fps192frames, source12..131 used, origin song1070. Twelve real lead
frames and61 raw exit frames exist. clean.mp4 has only119 treated frames; no
rendered FX handles are claimed. Camera pushes more strongly than requested.

Reproduction: python out/receiver_reply_arrival_v1/post.py. The existing duet
oscillator is reused with its original phrase-gated signals. State and phosphor
trails are warmed through1082, preserving time, size and movement at the cut.
Both then ease towards receiver-relative orbits over1.45seconds and recede
slightly. Neither restarts its entrance or switches its waveform to a new phrase.
This is stylized screen-space communication, not proof of shared physical space.

New-plate feature tracking estimates a similarity transform for the receiver.
The main amber aperture uses tracked and colour-qualified masking, core gain
and warm bloom. The restored vocal stem drives a10ms RMS envelope with8ms attack,
65ms release and -48dB gate; stem placement +0.178348 is applied once.
Tracking data and per-frame voice values are in tracking.json. This is not the
old Tell me what you got baked response or old tracking reused at a new time.

The isolated shotlist/cues extend the current opening for this review. Production
shotlist remains untouched. The preview already contains the preceding approved
duet, so do not add another rosette or lyric layer to it during later assembly.
