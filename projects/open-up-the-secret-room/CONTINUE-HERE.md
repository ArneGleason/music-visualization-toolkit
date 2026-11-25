# Open Up the Secret Room

## Current checkpoint — 2026-11-25

Approved direction: **Image 16**, dark cavern city and the three civic statues,
followed by **Image 17**, Harper and Taffy exchanging bewildered discovery.
Sparse amber area lights, distant obelisk towers, high roof lost in darkness,
and a necessary flashlight replace the bright enclosed antechamber.

[Current animatic — 17.375 seconds](generated/approved/opening-v004/Secret-Room-opening-v004.mp4)
uses the original Together Anyways approach/activation MP4s, then Image 16 for
5 seconds and Image 17 for 3.667 seconds. New shots remain static holds;
future motion is only a few slow steps then a pause near the entrance.
The second original shot cuts before Harper turns and before lights reach the
arch apex. No inhabitants are revealed yet.

## Continue the work

- [shots/shotlist.json](shots/shotlist.json) is authoritative: 417 frames at 24 fps.
- [Image index](IMAGE-INDEX.md): next number is **18**; never reuse labels.
- [Character continuity](CHARACTER-CONTINUITY.md): face-picker **03A** governs
  Harper and Taffy identities, hair and graphic-novel rendering.
- [Three Pillars](THREE-PILLARS.md): left Stability, center Expression, right
  Understanding. Four arms plus two legs each. Understanding is diminutive on
  a raised chair, without size parity; all face into the assembly area.
- [Dark cavern prompts and review](production/dark-cavern-v001/review.md).
- [Entrance development](ENTRANCE-DIRECTION.md) and
  [reverse-shot development](ANTECHAMBER-TWO-SHOT.md) retain decision history.

Next: plan restrained walking and flashlight continuity for the two approved
stills before ordering generated footage. Review each motion take for faces,
hair, anatomy and architectural continuity. Current reverse flashlight angle
needs to be coordinated with the forward view during motion production.

## Restore on another machine

Use this toolkit repository for all video work; music preparation stays in its
own workspace. The public [media manifest](media-manifest.json) identifies the
GitHub Release archive with checksums. It includes approved stills, retained
illustration references and development, current animatic, master and matched
lead audio, cached timing and the two reused original MP4s at canonical paths.
Large media stays outside Git history. Run from the repository root:

```sh
./.venv/bin/python3 tools/project_media.py restore projects/open-up-the-secret-room/media-manifest.json
./.venv/bin/python3 tools/project_media.py verify projects/open-up-the-secret-room/media-manifest.json
```

`Setup Open Up the Secret Room Mac.command` sets up Python and restores the
editing bundle. Its optional `--with-bitwig` restores the historical private
Bitwig archive and requires access to that repository; native music sources
were not republished. [Source manifest](source-manifest.json) records provenance.

The original private release remains recovery history. Its prior editing-media
manifest is retained in production/media-manifest-20261123-v002.json.
Superseded opening animatic MP4s v001–v003 and the old timing-only slate were
removed at the user's request; [cleanup receipt](production/cleanup-20261125.json)
records exactly what was deleted. Full-song lyric timing is a separate retained
review. Source takes and character/reference imagery were not deleted.

## Reproduce the current animatic

```sh
./.venv/bin/python3 projects/open-up-the-secret-room/production/render_opening_review.py --version 4 --shotlist projects/open-up-the-secret-room/production/opening-reuse-v004/shotlist.json
```

This rebuilds the WIP preview from retained inputs; the approved copy remains
in generated/approved/opening-v004/. Musical boundaries use the cached DAW grid.
For re-planning use tools/shotplan.py --merge. See [project workflow](../../docs/PROJECT_WORKFLOW.md).
