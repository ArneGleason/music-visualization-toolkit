# A Right Little Something — production checkpoint

2026-10-04. The user accepted animatic v03 as a good working edit and requested
this GitHub checkpoint before continuing. Review locally at
http://127.0.0.1:8768/ (exact-frame viewer: http://127.0.0.1:8767).

## Current edit

`shots/shotlist.json` is authoritative. Four Kling takes cover the first
632 frames / 26.333 seconds. The full animatic has 5265 frames at 24 fps and
1920 × 1080 presentation. Current local movie:
`generated/animatic/A-Right-Little-Something-opening-motion-v03.mp4`.

| Shot | Song frames, inclusive | Current selection |
| --- | --- | --- |
| opening-001 | 1–227 | Space/planet/moons; ship enters and recedes |
| opening-002 | 228–352 | Preferred locked-camera connected-lines portrait |
| opening-003 | 353–542 | One continuous pullback across both up-above phrases |
| opening-005 | 543–632 | Floating interior, hands toward the transparent field |

The former 003/004 cut restarted nearly the same pullback and felt like a
stutter. V03 merges those notes into one take, starting with "Here in orbit
up above" and continuing through "Way up here up above". The original shot
records are preserved under `supersededShots`. Five original listening notes
remain active and unchanged, revision 9. The opening-selection panel provides
shot jumps and review notes; the listening-note anchors retain their original
positions even where the edit has changed.

There is no planned footage beyond this opening yet. The rest of the song
uses a dark review canvas with the same bottom lyrics. V01 and v02 remain
local comparison movies. Generated source clips retain at least half a second
of lead-in and lead-out; no speed changes or master-audio retiming are used.

## Creative direction to carry forward

- Continue the painterly graphic-novel look and established adult Harper:
  curly auburn hair, freckles, gray tee/trousers, bare feet, expressive floating
  performance. Artistic composition takes precedence over exact physical scale.
- Favor Kling for complete illustrated character/scene animation. Keep the
  camera fixed where depth becomes unreliable; avoid troublesome moves rather
  than imposing rigid geometry on every shot.
- Use Blender for composition planning and selective composited effects:
  light, glow, blur and coordinated effects when they improve a Kling shot.
  It remains useful, but the static illustrated actor card is not the chosen
  character-animation workflow.
- Preserve a complete equatorial metal band, upper/lower circular platforms
  and an open aft engine ring. Finish: dark satin metal, continuous amber rims,
  sparse cyan rectangular lamps and cyan engine light.
- The sphere is an ultra-thin transparent technological field, capable of
  displaying/magnifying imagery on its inside. Avoid heavy shiny refractive
  glass. Connected faint cyan geodesic lines are preferred over isolated dots.
  Stable junction dots can accompany lines; localized brightness waves are a
  useful effect reference. Small display-only rotation is optional, restrained.
- Keep two distinct distant moons: larger charcoal volcanic basalt with orange
  fissures, smaller pale icy world with blue fractures. They belong to the
  astronomical background beyond the planet surface, not beside the cabin.
  An upper-right sun motivates reflected illumination; lava may self-emit.

## What worked and what did not

Blender compositions translated surprisingly well into ImageGen starting
frames. Stable ship geometry, orientation, moon identities and appearance
references are valuable planning aids without requiring every generated pixel
to match an exact mesh.

Kling's illustrated motion and character performance were much more appealing
than the native ship plus flat actor card. The native render controlled the
ring/field correctly but was stiff and its metal finish did not exactly match
the illustrations. Keep it as an experiment, not a selected opening take.

Moon depth was poor in some moving shots: they behaved like small nearby balls.
The locked-camera lines test kept them more stable relative to the stars and
was the preferred portrait take. This is not proof that arbitrary camera moves
are solved. The remaining moving pullback still merits depth/field review.

Isolated dots were disliked and could read as stars. The requested rotating-dot
Kling test restored hexagonal lines and did not reliably produce the requested
rotation. Native Blender junctions, lines and traveling brightness worked as
motion graphics, but locking down the entire shot sacrificed the performance.
Use those effects selectively around good animation.

The first nine-second continuous test changed the spacecraft into a different
design, losing the equatorial ring and adding a barrel engine. Supplying the
approved exterior as an ending reference constrained the second take much
better; it is selected in v03. A continuous generation avoids the restart
caused by joining separately generated starting compositions.

## Lyrics and timing

The master is the audio authority. DAWproject timing is used because the song
has many linear tempo ramps; MIDI step events and starting-BPM estimates are
inadequate. The approximately 2.196 ms residual was accepted for the animatic.
Every shot/caption boundary uses the existing frame timing. Preserve the
arranged/performed spelling and typos, audible repeat counts, nine "in" onsets,
"things big now" and "all, all calling".

Default lettering is stored in `production.lyricPresentation`: Bahnschrift,
34 px on 1080p, centered near the bottom, subtle outline/shadow, pale cyan
current-word highlighting. It follows the small word-timed approach from
Monsters Undone. The words are baked into the movie; a small paused lyric readout
also keeps them readable when native player controls cover the bottom of a
small preview. `tools/lyric_overlay.py` preserves frame activation despite
ASS centisecond precision. Font files are machine-local and are not committed.

## Backup and resuming

Git includes code, plans, prompts, authored lyrics, these notes, a small JSON
checkpoint and nine curated PNG references. It excludes all audio, video,
Blender files, render sequences, font copies and bulk generated assets.
Thus this is a production-data/reference backup, not a full media archive.

`checkpoint/manifest.json` maps backed-up timing, transcription and listening
note JSON to its original local paths. `reference-images/manifest.json` maps
the selected stills to their generation-reference paths. Both record SHA-256
checksums. Restore missing files after cloning with:

    python tools/project_checkpoint.py projects/a-right-little-something/project.json --restore

The restore command verifies checksums and keeps every existing local file.
Actual master/DAWproject/video sources must be recovered from a separate media
backup. Generation IDs and prompts survive in the shotlist and plans, but
provider download links may expire. Use `project_checkpoint.py` without
`--restore` to refresh the metadata checkpoint before a later commit.

Next: review the current opening in context, add scene ideas beyond frame 632,
then plan a small next batch. Replan with `tools/shotplan.py --merge` to preserve
creative work; retain identical shared prompt locks, timing-derived frame
counts, and half-second handles. Review an animatic before buying more footage.
The latest continuous-shot tests cost 144 credits; all Kling tests and selected
opening generations so far total 584 credits. No new generation was purchased
for this checkpoint.
