# Rivers of Mars: current checkpoint

The full Blender migration is complete as an isolated review edit. Start with
`out/blender_migration_v1/STATUS.md`, then `SELF_REVIEW.md` and
`AUTONOMOUS_PASS.md`. The latest local movie is
`out/blender_migration_v1/full_native_context.mp4`: 70 numbered cuts,
4854 frames at 24 fps, 1280x720. It includes the woman-to-world reveal,
the restored alien-head hoops, all migrated FX, lyrics and closing titles.

The production `shots/shotlist.json` has not been replaced. The current review
selection is `out/blender_migration_v1/full_native_review_draft.json`, with
matching cues, decisions, frame checks and native dependency receipts nearby.
Do not silently revert to the older production selection when resuming.

The full assembly uses Standard / None to avoid applying AgX again to caches
that already carry their accepted display transforms. Source timing, audio,
all 70 midpoint pictures and 140 cut-edge pictures were checked. No paid
upscaling or final mastering has been performed.

Next: review the full numbered movie, settle any edit notes, upscale only used
source spans, rerender native FX at 1080p, then relink and assemble in Blender.
Do not merely enlarge the 720p FX caches. See `resolution_delivery_plan.json`.

## What Git preserves

The recent work was developed inside ignored `out/` folders. Their authored
code, plans, handoffs, receipts, tracking, settings and edit manifests are
explicitly tracked at their original paths so relative imports still work.
The historical variants are retained for decisions and recovery, not promoted
as competing current edits. The current checkpoint above takes precedence.

Generated media, images, audio, saved Blender render scenes, dependency bundles,
binary caches and regenerable effect-control substrates remain local and are
not uploaded. The small licensed Fredoka font instance is a code dependency,
not generated film content, and is included with its existing license.

A Git-only clone is not a complete media restore: restore the local media tree
from the owner's backup as well. Receipts contain local paths and media hashes.
Rebuild generated controls and native scenes using their prepare/build scripts
if absent; rerun validation after restoring paths. Do not interpret missing
local media on a fresh clone as permission to substitute another take.
