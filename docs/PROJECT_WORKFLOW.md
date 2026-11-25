# One home for video production

Music preparation and video production are separate workspaces. Keep Bitwig,
stem-processing tools and original music sessions in the music workspace.
All video projects belong in this repository under `projects/<song-slug>/`.
Do not create a separate video repository for a new song or computer handoff.

Shared tools belong in `tools/`; shared procedures belong in `docs/`.
Keep one-off production scripts in the project's `production/` directory.
Promote useful general behavior into shared tools as it proves reusable.

## Bitwig to video handoff

1. In the music workspace, choose the master and export range. Export the final
   master WAV and matching DAWproject; include a loop-matched lead vocal and
   any useful stems. Preserve the native Bitwig session in the music workspace.
2. Create `projects/<song-slug>/` here. Record the upstream repository/session,
   export version, range, sample rate and checksums in `source-manifest.json`.
   Store machine-specific absolute paths in ignored `project.local.json`.
3. Copy exports into ignored `generated/source/`; preserve author lyrics in
   `lyrics/author.txt`. Never overwrite a different master under the same name.
4. Verify the master/DAW offset, meter and continuous tempo map. Compile the
   cached beat grid to frame boundaries. Review the lyric-timing animatic.
5. Record accepted timing, then develop `shots/shotlist.json`. Re-plan using
   `--merge`. Review the storyboard animatic before paid motion generation.
6. Keep compositing editable in EffectCraft, following Phone Book Sing's
   workflow. Preserve selected footage, source trims and dependency assets.
7. Update `CONTINUE-HERE.md` with the current edit, preview, approval state,
   known issues and next action. Update the root project index.

When music changes, create a new named handoff and assess timing changes before
replacing any accepted video timing. A filename alone is not proof of identity.

## Switching computers

Use this repository on both machines. Push authored work and publish a new
immutable media release together; record the repository, tag and checksums in
the project's media manifest. Pull, restore and verify before editing.
Use `compile`/`validate` with the cached timing grid when the DAWproject is absent.
Do not re-align accepted lyrics simply because the computer changed.

Secret Room was consolidated locally on 2026-11-24 from
`ArneGleason/open-up-the-secret-room-video`, commit
`22d5c7e`, branch `codex/open-up-the-secret-room`. Its existing private release
remains the recovery source; manifests intentionally still point there.
The original clone is a recovery copy, not the active video workspace.
This consolidation must be committed/pushed before the PC can pull it.
Do not delete the old repository or rewrite release locations until a new
backup is published and verified. Check publication visibility before moving
private handoff material into a public remote.

## Media lifetime

| Class | Examples | Retention |
| --- | --- | --- |
| Source and identity | Masters, DAW exports, paid takes, character references | Preserve; back up |
| Editable work | Shotlists, recipes, native EffectCraft projects and dependencies | Preserve; compact/archive only after dependency review |
| Milestones | Approved animatics, final masters, useful comparisons | Preserve explicitly |
| Disposable previews | Re-renderable review MP4s and contact sheets | Latest two per series, seven-day grace, explicit pins |
| Caches | Decoded frames, temporary renders | Regenerate; classify and verify originals before removing legacy caches |

An old MP4 may be original paid footage. An old native project may contain
embedded assets. Age, extension or version number alone does not make either
disposable. Existing production folders are not automatically swept.

For new disposable previews use:

    generated/wip/previews/<series>/v001/preview.mp4
    generated/wip/previews/<series>/v001/.disposable

Write `.disposable` only after a successful render. It must contain the command
or recipe needed to reproduce the preview, using retained inputs outside `wip`.
Keep these version folders flat. Do not put original footage, unique artwork,
native projects or dependency assets here. Do not use these preview files as
inputs to production edits. Put `.keep` in any version that must survive.
Promote approved milestones into `generated/approved/` and update the handoff.

Report inventory and eligible previews (no deletion):

    ./.venv/bin/python3 tools/media_retention.py projects/<song-slug>

After a replacement preview has been successfully rendered and reviewed, while
rendering/playback is idle, run the same command with `--apply`. This is the
routine session cleanup hook; no background timer is installed. It retains
the newest two eligible versions per series, all pinned versions, and anything
modified within seven days. It refuses native projects, unknown file types,
symlinks and nested folders. Neither source media nor legacy folders is swept.
Add `*/generated/wip/*` to future media-pack exclusion lists; don't mutate
existing immutable archive manifests to pretend their contents changed.

For legacy cleanup, inventory first, identify a reproducible cache/preview,
verify its retained inputs and current-edit dependencies, preserve approved
comparisons, then migrate only confirmed disposable previews into this layout.
Do not bulk-delete old EffectCraft versions without inspecting their assets.

### Verified decoded-frame cleanup

`tools/clean_decoded_frames.py` handles the PNG caches produced by
`animatic_media.Artwork`. It requires a matching local MP4 and source stamp,
decodes the entire video and compares every cached frame's RGB pixel checksum.
Any mismatch leaves that cache intact. Only verified numbered PNGs and their
cache stamp are deleted; JPEG review samples and other files remain.
The next render automatically recreates the cache from the retained MP4.

Run while no render is using the cache; use a new receipt path each time:

    ./.venv/bin/python3 tools/clean_decoded_frames.py projects/<slug> --report out/cleanup-<date>/decoded-frames.json --apply

Omit `--apply` to verify without deleting. Receipts record source SHA256 hashes,
frame counts, byte totals and exact regeneration commands. Original paid takes
remain local: provider download links are supplementary recovery, not the sole
backup. New generation receipts and edits should point to one canonical local
source file rather than copying footage into each revision directory.

DAWproject exports may embed all stems. On the Mac, preserve the ingested
version that matches the video's timing. A separate PC/music-workspace audit
must establish which old exports can be regenerated from retained native music
sessions before applying any DAW retention rule there.
