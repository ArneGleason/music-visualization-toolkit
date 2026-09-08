# Closing titles, first review

Status: user text corrections recorded 2026-09-07. Recipe updated, deliberately NOT re-rendered. Existing .blend and movies still contain the previous draft until render.py is run again.

## Exact card copy

RIVERS OF MARS

Human imagination and direction, AI-assisted craft

Arne Gleason · Human

v0.1.0  |  2026-09-07T20:56:35Z

Latest owner correction: Arne Gleason is the correct full name. Remove all composition, lyric, stem, voice and instrument provenance lines. Credit the role as Human. This supersedes the longer wording, including the earlier misspelled abbreviated name.

The small ownership stamp uses UTC ISO8601. v0.1.0 begins explicit review versioning here; it is not a retroactive count of earlier edits or a final-master designation. Freeze/update this stamp deliberately per release, not per rendered frame. No tool-brand credits added.

## Assembly

Replace ONLY song frames 4782..4854 (end exclusive), the existing 72-frame silent closing placeholder. Preserve all earlier frames, cuts, and master audio from `out/outro_particle_continuity_v1/preview_numbered.mp4`. Review numbers remain on the preceding shots; the closing artwork is clean.

The two amber/cyan hoops assemble into a small world emblem. Text settles once, with the full card established by frame20 and held through72. No exit animation or looping credit carousel. Three seconds is deliberately brief; review reading comfort before locking. A longer hold is preferable to shrinking type if the full provenance needs more reading time.

## Native Blender deliverable

`closing_titles.blend` contains editable flat font curves, animated emissive materials, animated curve-reveal hoops, an orthographic camera, and native compositor glow. No raster title plates. All scene geometry and typography scale with render resolution. Font is Segoe UI from this Windows installation. No extrusion, shadows, rainbow cycling, film grain, or baked mastering look.

Run `render.py` through Blender to regenerate; saved .blend also supports direct animation rendering. `finish.py` only encodes/stitches, with existing audio copied unchanged. Current proxy1280x720,24fps. Change render resolution to1920x1080 for native final titles, with higher sampling as desired.

## Next production step

Migrate the remaining approved non-Blender effects into native Blender compositing, using current renders as visual acceptance references. This closing card does not mean the rest of the film has been migrated. See `out/BLENDER_PIPELINE_AUDIT.md` and `out/MASTERING_PLAN.md`. Preserve all existing source/guide clocks and approved frame boundaries while migrating. No paid generations, new mastering pass, or full-film migration performed here.
