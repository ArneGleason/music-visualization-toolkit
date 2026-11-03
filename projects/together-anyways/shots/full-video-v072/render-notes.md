# Full-frame first draft v072

User requested a full 1080p video rather than the annotated animatic.
Preserve the selected 70-shot edit, musical timing, source in-points, digital camera moves, and all transitions.

Output: generated/full-video-v072/Together-Anyways-1080p.mp4
1920×1080, 24 fps, 5190 frames (216.25 seconds), H.264 CRF18, AAC320k.
Full-frame artwork: aspect-preserving center/focus crop to fill 16:9, no review matte.
No lyrics, timecodes, scene/shot labels or review overlays.
Closing text centered near bottom, final72frames/3seconds, first12frames fade in:
Together Anyways (28px)
copyright Arne Gleason 2026 (19px)
Warm ivory lettering with subtle dark shadow; no separate end card or extra runtime.

Reproduce:
./.venv/bin/python3 tools/shot_video_render.py projects/together-anyways/project.json --output projects/together-anyways/generated/full-video-v072/Together-Anyways-1080p.mp4 --title 'Together Anyways' --copyright 'copyright Arne Gleason 2026'

Shared Artwork full_frame option defaults off, preserving review rendering.
Export is independent of the existing animatic; shotlist is unchanged.
