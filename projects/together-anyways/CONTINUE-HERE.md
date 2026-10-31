# Together Anyways: continue on either computer

Checkpoint: 31 October 2026. The current task is moving this project between
Windows and Mac, then exploring **more supporting-character diversity in body
size and clothing systems**. Do not generate another batch before reading the
existing references and discussing specific changes with Arne.

## First time on the Mac

Clone `https://github.com/ArneGleason/music-visualization-toolkit.git` into any
local folder, preferably outside cloud-synced storage. Open that folder as the
Music Visualization Toolkit project in Codex. Start a local chat there with:

> Read AGENTS.md and projects/together-anyways/CONTINUE-HERE.md. Restore the
> Together Anyways media and set up the pinned Mac EffectCraft build. Check
> the current cast board, then continue our character size and clothing design.

The assistant can do the setup. The same steps in Terminal, from the clone:

```sh
git pull --ff-only
bash "Setup Together Anyways Mac.command"
```

Python 3.10+ is needed. The script restores the verified media snapshot, downloads
the official universal Mac EffectCraft **0.18.0 app and CLI**, checks their SHA256
hashes, installs the app into `~/Applications/EffectCraft-0.18.0.app`, creates a
local Python environment, installs toolkit dependencies and validates the timeline.
FFmpeg is installed using Homebrew if it is missing and Homebrew is available;
otherwise the script explains the missing prerequisite. Playwright Chromium is
only needed for browser-based render tools: `.venv/bin/python3 -m playwright install chromium`.

Open the prebuilt cast board in a browser:
`generated/character-development/supporting-refs-v003/cast-board.html` (relative
to this project folder). All gallery image links are relative.

From the repository root, launch the native animatic with:

```sh
python3 tools/effectcraft.py gui
```

The launcher sets the bundled Barlow font directory and computes all paths from
this checkout. Normal macOS first-launch approval may be needed. The setup does
not bypass Gatekeeper. Mac app launch/GPU rendering must be tested on the Mac;
Windows verification cannot certify those. No Blender installation is required
for the current EffectCraft animatic. A separate Windows checkout keeps its own
Python environment and EffectCraft binaries.

## What Git and the media release contain

Git tracks authored prompts, reference catalogs, creative notes, plans, timing
register, tools and this handoff. `media-manifest.json` identifies an immutable
GitHub Release ZIP with SHA256 hashes for every file. Large media stay outside
Git history, following the repository's AGENTS.md.

The ZIP contains both projects' complete generated reference/history folders,
all review boards, the supplied cover and original Harper input (when available),
the current DAWproject export with embedded source audio, the master WAV, exact
tempo grid, compiled timeline, accepted v04 native EffectCraft project, rendered
lyric animatic, timing data, font and its license. Earlier audio-cleanup experiments,
model weights, virtual environments and Windows executables are outside the
music-video handoff; they are not dependencies of this project.

The portable native file is
`generated/animatic/Together-Anyways-lyric-animatic-v04.ecproj`. Only its two media
paths were changed to relative `assets/...` paths. The original Windows save is
retained beside it as `*-windows-original.ecproj` for provenance. The old
`Open in EffectCraft.cmd` inside that historical folder retains the old PC path;
use the repository launcher instead. Old generation receipts and gallery-builder
scripts may mention PC/plugin paths as provenance; use the saved images and
prebuilt galleries, and adapt a builder if needed. Do not recreate designs from
scratch because an old receipt path is unavailable.

## Switching back and forth

Before switching machines, ask the assistant to **checkpoint Together Anyways
to GitHub**, including new ignored media. A code-only commit does not transfer
new PNG/WAV/MP4/ecproj files. Work on one computer at a time.

For a media change, the assistant should:

1. Inspect Git status; stage only this project's work and intended shared tools.
2. Keep new assets under one of the roots in `media-manifest.json` (or explicitly
   add a new root). Remove machine-specific dependencies from active project paths.
3. Run `python tools/project_media.py pack projects/together-anyways/media-manifest.json --tag together-anyways-YYYYMMDD-vNNN`
   with a **new tag**. Never replace a published snapshot.
4. Commit the new manifest together with authored changes, push, then create a
   GitHub Release at that commit and upload `out/transfer/<tag>.zip` using `gh`.
   Verify release availability and restore checksums before declaring it backed up.

On the receiving machine:

```sh
git pull --ff-only
python3 tools/project_media.py restore projects/together-anyways/media-manifest.json
python3 tools/project_media.py verify projects/together-anyways/media-manifest.json
```

Restore refuses to overwrite differing local files. If it reports conflicts,
checkpoint the local edits or move the listed files into a dated backup before
restoring; do not delete them blindly. `project.local.json` is intentionally
ignored: use it only for that computer's optional source overrides. The tracked
`project.json` already has portable defaults, so Mac needs no override file.

Git transfers files, not a chat's execution location or full chat history. A new
local chat inside the Mac clone is the simplest continuation. An existing chat
can also be handed off through Codex remote connections when both hosts and
matching repository projects are configured; opening the same chat alone does
not switch its tools to the Mac. Official reference:
https://learn.chatgpt.com/docs/remote-connections

## Accepted timing: preserve it

- 48 kHz stereo master, 216.239020833 seconds; preview **5190 frames at 24 fps**.
- Exact DAWproject curve: **932 tempo points**, linear in beat; master zero at
  **project beat 7.5**. Do not substitute a fixed tempo or stepped MIDI map.
- 57 lyric lines, 220 words; `timeline.json` is the portable musical register.
- User approved the repeated refrain correction: second **with 84.660–87.040**,
  **me 87.040–88.360** seconds. Do not rerun alignment or move that boundary.
- Approved text: “Where all attention must go” and “find a fine like you”.
- Section tags in supplied lyrics are not displayed lyrics. Echoes are baked
  into the vocal; repeats should not be invented from echo transcription.
- Existing accepted native preview is **1280×720**. Future picture work is
  planned at **1920×1080**; migration does not upscale or alter that preview.
- `timing-import.json` records checks; the importer fix retains the partial
  opening bar at beat 7.5. Run `tools/timeline.py validate .../project.json` after
  setup. `sync` regenerates grid/compiled data; it is unnecessary for viewing.

## Characters and creative direction

Read `development-brief.txt`, `character-development/biology-direction.txt`,
the supporting cast pool and each batch's catalog/review notes before changes.

Harper is 14: copper curls, freckles, rust vest, pale scarf, olive trousers;
confident street trickster. Her partner's working name is Taffy, about 12:
Black, short curls, larger rounded ears, slightly overweight, less conventionally
cute and watchful. He recently escaped bad circumstances with Harper's help.
His own culture remains visible: mulberry/plum patterned wrap top, mismatched
rope/braid belt, charcoal trousers, runnable open-toe sandals and a patched sack
rigged with shoulder cords. Exactly three curved healed scar lines on each cheek,
symmetrically arranged. v006 corrected the turned head toward the frontal identity;
all-angle identity is not yet fully locked. Retain rejected iterations as history.

The racketeer and his one shoulder lookout remain core cast. The current board
has 13 supporting candidates: A1, A3, A6, B1, B4, B5, B6, C1, C4, C6, D2, D3, D6.
Arne particularly liked subtle, job-related biological adaptations that belong
in the world and only become obvious on closer inspection.

Accepted reference directions: A3 precision eye/tactile pads; A6 four arms;
C4 vibration-sensitive ear membrane/contact pads; D6 digitigrade runner legs;
B1 Doorpost retained. v003 adds A1/B4/B6/C1/C6/D2/D3 and B5 Stillwater.
Those latest studies are not final character locks. A1's twin-thumb-tip anatomy
is **unresolved** despite two attempts; B5's lateral eyes are weaker than intended.
Do not assert those traits are fully established. Next explore size and attire
diversity while retaining these identities and the quiet adaptation approach.

## Story and environments

Desert scavenger world: worn sandstone, patched shades, chipped teal/blue pipes
and tanks; old mechanics with selective advanced technology. Influences come
from multiple cultures/planets. Painted graphic-novel rendering, controlled
ink contours, tactile materials. No generic pointed-ear/wrinkled-forehead shortcut.

Harper distracts the criminal with a blue jewel she can conceal/reveal while
Taffy steals an asymmetric horseshoe access key. Route: market approach → broker's
house-front water depot → separate decoy/covert escapes → blue-pipe reunion court
→ controlled relay entrance → interior wanted broadcast. They use the stolen
device to open an intermediate door, not the ship itself. Four environment
directions and the first-run plan were accepted; see
`environment-development/first-run-v001/plan.json` and its route map, with review
under `generated/environment-development/first-run-v001/index.html`.

Detailed environment planning ends at “I never watch the news”, 81.48 seconds.
Characters have not been inserted into timed choreography yet. Later they hijack
a ship and launch at the final “Hang on for your life”; something brings them
down during the instrumental outro. They gain ground but remain stranded on the
planet. The cause of the forced landing and later locations are still open.
No paid motion footage is approved/generated. Once shots are authored,
`shots/shotlist.json` becomes the edit authority; preserve authored work with
`shotplan --merge` and derive frame boundaries from the timing register.

Official pinned app release:
https://github.com/storytold/effectcraft/releases/tag/v0.18.0
