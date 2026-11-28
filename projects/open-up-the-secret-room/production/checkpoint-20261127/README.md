## GitHub checkpoint — 2026-11-27

Current approved edit is story-stills v009:33 shots,2923frames at24fps (2:01.792). Latest selected image160 follows153: placing goods, then quietly patrolling. Images1–160 and all local illustration alternatives/references are preserved in the public media release. The later story arc remains documented; the current revised timed pass ends with the listening response155. Continue one image at a time with user review. No new motion footage generated.

Scripts, prompts, notes, review annotations, canonical shotlist and frozen animatic snapshots are in Git. Large media is in the matching [GitHub release](https://github.com/ArneGleason/music-visualization-toolkit/releases/tag/secret-room-20261127-stills-v001), listed with checksums in `media-manifest.json`. The archive includes source audio/cached timing and the two original reused Together Anyways opening clips; it excludes all rendered animatic MP4s and WIP previews. Older releases remain recovery history.

On a fresh checkout, restore and verify, then rebuild the current preview:

```sh
./.venv/bin/python3 tools/project_media.py restore projects/open-up-the-secret-room/media-manifest.json
./.venv/bin/python3 tools/project_media.py verify projects/open-up-the-secret-room/media-manifest.json
./.venv/bin/python3 projects/open-up-the-secret-room/production/render_story_stills.py --version 9 --shotlist projects/open-up-the-secret-room/production/story-stills-v009/shotlist.json
```

The renderer refuses an existing output; use a fresh version number if v009 already exists. Local review player addresses and machine-specific source paths are not portable. Original Bitwig timing rebuild sources still have their separate manifest; current cached timing is preserved here. Current notes are `production/story-stills-v009/timeline-review-notes.json` when present; earlier user annotations remain in their own version folders.
