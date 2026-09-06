# Rough v03, 2026-09-05

Output: `out/rough_v03_fx_outro_720p.mp4`.

1280x720, 24 fps, 4782 frames / 199.25 seconds of picture. One master audio
track, 199.241 seconds. Approximately 190 MB. Previous renders retained.

Built with `python tools/render_lyric_animatic.py --proxy --allow-clips --out
out/rough_v03_fx_outro_720p.mp4`. Seven bounded Blender sections, joined with
one encode of the master soundtrack. Log: `out/rough_v03_render.log`.

Includes current 71-shot edit, new 17-cut outro, s034b weather cutaway, original
flat lyric choreography, and all eight protected effects: s002, s010, s019,
s037, s043, s044, s047, o01. Render logs confirm protected selections and no
stills/slate fallbacks. Source preflight passes; output frame count, dimensions
and single audio stream verified. Spot checks cover opening lyrics, cutaway
and outro. Owner playback review is still needed for pacing and lip sync.

No extra mastering, upscaling pass or new generation. Existing assembler
overlays/color behavior retained. The end iris is still the closing-title
placeholder. Known deferred work from ROUGH_ASSEMBLY_PREP.md remains unchanged.

Review the whole arc first: duet cutaway at about 1:59, swimmer treatments
around 2:20, and the new tunnel/outro beginning around 2:52. Make a timing and
strength notes pass before further polishing individual effects.
