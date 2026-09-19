# Monsters Loose generation conventions

Agreed 2026-09-19: half a second of editorial handles at each end is a flexible default, not a hard duration requirement. Log the actual assumptions for every clip, including exceptions and zero handles.

- At the current 24 fps, reserve 12 frames before the intended cut-in and 12 frames after the intended cut-out. The default source cut-in is zero-based frame 12 (0.5 seconds).
- Keep intended edit boundaries on the music timing grid. Handles extend the source footage; they do not move those boundaries or add pre-roll to the master song.
- Request at least the intended edit length plus 24 frames (one second). Round up to an available generation duration where necessary.
- Describe continuous, natural action through both handles. Place the intended opening composition/action about 0.5 seconds into the source; leave motion continuing for 0.5 seconds beyond the intended cut-out. When using a generated first/last-frame constraint, those frames bound the source, not necessarily the edit.
- Treat these as target margins, not guaranteed precise AI choreography. Inspect each take and record the actual source in-frame in shotlist.json.
- Existing approved opening clips and their current edit points are grandfathered; do not regenerate or retime them solely to add handles.

Handles give room to nudge a cut or overlap footage. Smooth continuity still depends on matching action, direction and composition.

## Required per-clip timing record

Record generation fps, requested duration, assumed pre-roll and post-roll (frames and seconds), intended master cut-in/out, and intended master time represented by source frame zero. After inspection, record actual source in/out separately; never overwrite the generation assumptions with an editorial trim. Unknown historical assumptions remain unknown, not inferred from current trims.

For lip-sync, also record the supplied audio file, its master start sample/time, any padding, and its alignment to source frame zero. A source trim change must preserve that audio-to-master mapping.

When an interstitial covers a longer continuous take, resume that take at its elapsed source position, accounting for the covered interval. Do not restart the underlying action. Keep a shared take ID and source/master mapping for the pieces on either side of the insert.
