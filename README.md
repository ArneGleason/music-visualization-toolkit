# Music Visualization Toolkit

A working collection of tools and project records for making music videos.
It combines musical timing, lyric alignment, visual experiments, shot planning,
review, and rendering. Some projects use procedural graphics; others use
illustrated references and generated footage.

This repository is both a reusable toolkit and a production notebook. It is
not yet a single application with a uniform workflow. The project folders
record the decisions, experiments, and revisions that shaped the shared tools.

## Intention

The aim is to keep visual storytelling connected to the music while making
creative decisions easy to inspect and revise.

A song's timing, lyrics, scene boundaries, shot lengths, source trims, and
transitions should remain explicit. An animatic provides a way to review those
decisions before committing to finished imagery or paid video generation.
Generated footage is selected and edited against that structure, rather than
determining the timing of the song.

The same foundation supports two approaches:

- **Procedural performance:** browser-based vector and 3D scenes driven by
  stems, MIDI notes, automation, lyrics, and musical structure.
- **Shot-based storytelling:** character and environment references, starter
  frames, directed video generations, and frame-accurate assembly.

The code favors small Python tools, JSON files, browser interfaces, and FFmpeg.
Project-specific solutions are retained alongside the more general tools;
reuse is developing through actual production work.

## How it developed

**We Be** supplied the original shot-planning and visualization tools.
[Example configuration](examples/we-be-config/README.md) preserves the shape
of that workflow without its source media.

**Rivers of Mars** developed the narrative vector renderer and music-video
register. The register connects lyrics, scenes, choreography, transitions,
and audio/MIDI drivers to a shared musical timeline. The completed video is
[published on YouTube](https://youtu.be/FxzgJe0L55Y); its
[project notes](projects/rivers-of-mars/README.md) describe the music provenance,
rendering process, and design work.

**Monsters Undone**, retained under its working folder name
[monsters-loose](projects/monsters-loose/HANDOFF.md), developed an illustrated
character-driven video using generated performances and Blender effects.
Its records preserve shot selections, compositing work, and a final 1080p
master. Harper's established identity carries into later projects.

**A Right Little Something** extended the illustrated narrative workflow:
lyric and timing review, character references, Kling footage, Blender work,
compositing, and repeated editorial passes. Its
[production handoff](projects/a-right-little-something/PRODUCTION-HANDOFF.md)
records the accepted V65 save point and remaining refinement work. Some older
intake notes are historical rather than current instructions.

**Together Anyways** brought those tools into a full-song caper following
Harper and Taffy. Work included cast and location design, continuity reviews,
directed Kling animation, source-frame timing adjustments, camera movement,
and transitions. Early character and setting studies remain under
[desert-colony](projects/desert-colony/character-development/README.md).
The project also established checksum-verified media backups for moving work
between Windows and macOS.

## Current status

As of **November 3, 2026**:

| Project | State |
| --- | --- |
| Rivers of Mars | Completed and published narrative vector music video. |
| Monsters Undone | V94 standalone video and 1080p master recorded; selected polish items remain deferred. |
| A Right Little Something | Accepted V65 working version; further shot refinements recorded in its handoff. |
| Together Anyways | Complete first video draft: 70 animated shots, 14 scenes, 5,190 frames at 24 fps (3:36.25). Latest animatic and clean 1920×1080 export backed up. Further polish remains possible. |

Together Anyways is the most recent production checkpoint. Its
[continuation notes](projects/together-anyways/CONTINUE-HERE.md) identify the
selected shots, accepted revisions, known caveats, and restore instructions.
The [current backup release](https://github.com/ArneGleason/music-visualization-toolkit/releases/tag/together-anyways-20261103-v004-stills)
contains reference media and the two complete video renders.

The toolkit remains a working repository rather than a packaged library.
Some scripts still assume a particular project's paths, schema, or visual
layout. The DAW-driven vector workflow and the generated-footage workflow
share timing concepts but have different renderers. Existing projects are the
best examples of how the pieces fit together.

## Where to look

| Location | Purpose |
| --- | --- |
| tools/ | Timing, alignment, planning, review, rendering, and media-backup scripts. |
| projects/ | Project configuration, timelines, shotlists, prompts, production history, and handoff notes. |
| stage/, world/, video/ | Browser-based vector-stage and 3D visualization work. |
| examples/we-be-config/ | Lightweight configuration examples from the original project. |
| docs/ | Focused workflow and implementation guides. |

Useful guides:

- [Timeline register](docs/TIMELINE.md): musical positions, lyrics, scenes, and compilation to frame boundaries.
- [Alignment](docs/ALIGNMENT.md): lyric and timing work.
- [Narrative video](docs/VIDEO.md): the illustrated browser-rendering workflow.
- [Frame review](docs/FRAME_REVIEW.md): playback, precise stepping, and review notes.
- [Exports](docs/EXPORTS.md): rendering and export details.

Production notes and older generation guides describe the tools and services
used at the time. They are not guarantees about current service features or pricing.

## Working principles

- For shot-based edits, the project's shots/shotlist.json is the authority.
- Derive frame boundaries from the timing grid. Prefer DAWproject timing when
  continuous tempo ramps matter; MIDI tempo events are discrete steps.
- Re-plan existing shotlists with tools/shotplan.py --merge to preserve
  authored creative work.
- Review the animatic before spending on generated footage.
- Preserve reference identities, shared prompt locks, selected takes, source
  in-points, and the reasons for revisions.
- Keep the review presentation separate from the clean video export.

## Setup and entry points

The core tools use Python 3.10+, FFmpeg, and ffprobe. Browser-rendering tools
also use Playwright/Chromium. Individual experiments may require additional
software such as Blender. Workflows have been exercised on macOS and Windows,
but not every tool has identical setup on both.

On macOS or a compatible shell:

    bash setup.sh

Run Python tools through the repository environment:

    ./.venv/bin/python3 tools/timeline.py sync projects/<slug>/project.json

On Windows, use .venv/Scripts/python.exe in place of ./.venv/bin/python3.
For an existing project, read its README or handoff before rebuilding anything.
For a new project, use the example configuration and
[timeline guide](docs/TIMELINE.md); supply your own audio and timing inputs.

To review a rendered video:

    ./.venv/bin/python3 tools/frame_review.py --video /absolute/path/video.mp4 --notes /absolute/path/review-notes.json

The original run.sh shortcuts remain available for timing, vector-stage,
world, and shot-edit workflows. Check their project assumptions before using
them with another song.

## What Git stores—and what it does not

Git stores code, configuration, shotlists, prompts, notes, and selected compact
reference assets. Large audio, generated footage, decoded frame caches, and
renders stay outside Git, usually under ignored generated/ directories.

**A clone alone does not restore a production workspace.** Backup coverage
varies by project. Rivers of Mars has a published video; A Right Little
Something and Monsters Undone have handoffs describing their local-media requirements.

Together Anyways has two tracked manifests pointing to versioned GitHub
Release archives:

- [media-manifest.json](projects/together-anyways/media-manifest.json):
  reference stills, review boards, audio, and project assets.
- [render-media-manifest.json](projects/together-anyways/render-media-manifest.json):
  the latest annotated animatic and clean full-frame 1080p video.

Restore them from the repository root:

    ./.venv/bin/python3 tools/project_media.py restore projects/together-anyways/media-manifest.json
    ./.venv/bin/python3 tools/project_media.py restore projects/together-anyways/render-media-manifest.json

Restoration checks SHA256 hashes and refuses to overwrite conflicting local
files. Individual Kling source clips and decoded caches are not included in
these archives; selected clip recovery URLs are recorded in
[video-recovery.json](projects/together-anyways/shots/video-recovery.json).
Earlier backup releases and rejected creative variants are retained so the
production history remains recoverable.
