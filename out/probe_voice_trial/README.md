# Probe signal vocal-light trial

No existing shot-specific music FX was assigned to s009/s011: prior beam motion
was native generated footage. This trial adds lead-vocal RMS-driven bright core
and amber bloom to its existing emission, using local probe optical-flow tracking
and a colour/luminance mask. No new waveform, colour, geometry or global flash.
Mask follows probe translation; not a full camera solve. Inspect bright planet
features for spill in playback. Reject if tracking/segmentation reads as floating.

One complete192-frame source is processed continuously from song719, including
the hidden receiver cutaway. Both signal source in-points are unchanged, with
return at137. Voice driver uses recorded+0.178348s offset once,20ms RMS,
12ms attack/75ms release, fixed-48dB gate,94th percentile normalization.
Effect vanishes when the native beam vanishes; no invented light after it ends.
The accepted receiver_voice_review remains between both signal shots.

Owner approved this treatment on2026-09-06: the vocal-driven signal makes the
probe shots feel part of the music rather than background footage.
Preferred picture for BOTH s009 and s011 in the next phrase-contained assembly:
out/probe_voice_trial/clean.mp4, source0..86 and137..192 respectively.
Use this folder's shotlist.json and overlay_cues.json as the latest opening
review snapshot. Retain out/receiver_voice_review/receiver_decision.json for
the approved voice-reactive receiver between them. Never fall back to untreated
probe footage merely because its original assignment remains in production.
Treatment approved; full production registry promotion still pending. All
existing media, production files and Claude handoffs unchanged. No external generation.
