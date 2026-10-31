# Continuing Together Anyways

Read `CONTINUE-HERE.md` before continuing production. `project.json` and
`timeline.json` use project-relative paths. Large media live in ignored
`generated/` directories and travel through the immutable GitHub Release named
in `media-manifest.json`; a Git pull alone does not restore those files.

Restore with `python3 tools/project_media.py restore projects/together-anyways/media-manifest.json`
from the repository root. Do not overwrite local differences without saving them.
Keep accepted timing, previous artwork, review caveats and rejected variants.
Before a machine switch, publish both authored changes and a new media snapshot.
