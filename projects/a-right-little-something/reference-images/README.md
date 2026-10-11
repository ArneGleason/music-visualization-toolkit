# Curated image references

These are exact copies of useful accepted stills, not video renders or frame caches.
`manifest.json` records the original generated path, visual role, size and SHA-256.
Existing identity/opening/hologram references are retained. The V59 save point adds
the selected concourse, ship options, gantry, departure/discovery and nine zoom views,
plus the new sphere ship continuity sources for a future opening match.

Run `tools/project_checkpoint.py projects/a-right-little-something/project.json --restore`
with the repository Python environment to restore missing local metadata and image
references. Existing local files are not overwritten. Audio, generated videos,
Blender scenes, full frame sequences and final renders remain on the production
machine under ignored folders; Git does not contain a complete media backup.
