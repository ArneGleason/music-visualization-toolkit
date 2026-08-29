# Working in this repository

This is a reusable music-video and visualization toolkit.

## Core invariants

1. Treat `shots/shotlist.json` as the source of truth for a shot-based edit.
2. Re-plan an existing project with `tools/shotplan.py --merge` so hand-written
   creative work is preserved.
3. Use frame counts derived from the timing grid, not hand-trimmed seconds.
4. Keep any prompt lock block identical across shots.
5. Review an animatic before spending money on generated footage.
6. Prefer DAWproject timing when linear tempo ramps matter. MIDI tempo events
   are steps and cannot reproduce a continuous ramp exactly.

## Style

Keep the Python small, readable, and dependency-light. Run repository tools as
`./.venv/bin/python3 tools/<name>.py`. Large media, generated substrates, and
renders must stay out of Git.
