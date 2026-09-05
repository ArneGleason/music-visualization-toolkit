# Full-song flat lyric choreography

Status: third complete animatic rendered with the owner-approved smaller type
and conservative early-only word-alignment corrections.

## Current review render

`out/blender_animatic_flat_lyrics_v03.mp4` is the current complete 1280×720
animatic:

- 4,782 frames at 24 fps (199.25 seconds)
- all 59 timed picture cuts using the 41 approved still selections
- 87 registered lyric lines and 305 individually timed words
- flat Fredoka glyph shapes with no visible extrusion, bevel, modeled lighting,
  perspective depth, or backing rectangle
- ordinary lines clear four frames before the next line; the five registered
  counter-vocal overlaps retain their separate baselines
- the active word turns warm white and carries a tight charcoal silhouette for
  contrast; the support follows the deformed glyphs and is never a rectangle
- the original master mix encoded once after the frame-locked sections join
- the picture track is explicitly locked to approved stills; ignored motion
  clips appearing later on disk cannot silently replace reviewed images

Generated movie files and section renders remain local under `out/` and are
ignored by Git.

## Choreography data

`shots/lyric_motion_full.json` is the editable full-song motion register. The
first six phrases preserve the hand-authored pilot. Later phrases use a shared
semantic grammar rather than unrelated bounces:

- signal and travel: horizontal handoff and delayed follow-through
- pieces, things, words, and bodies: readable cluster scattering
- fit, match, attach, pattern, and shape: convergence, seams, and recoil
- sound, music, rivers, swimming, and repeated syllables: travelling waves
- world, Mars, moon, turn, spin, and around: planar curves and rotation
- important, hard, subject, define, and true: compact rigid impacts
- dig, underneath, low, and falling: downward anticipation and settling
- light, waking, beginning, and night: lifted, softer deformation

Only one or two content words receive the large semantic gesture in a normal
line. Function words retain the presence handoff with restrained motion.
Overlapping call-and-response lines use a second baseline 58 pixels higher.

## Typography scale

`type_scale` at the top of `shots/lyric_motion_full.json` scales the font,
tracking, word gaps, and active-word shadow offset as one system. The approved
v03 render sets it to `0.66`; changing it to `0.75` remains a reversible
alternative if two-thirds size later proves too quiet. The lower-third baseline
itself does not move.

## Color and contrast

The renderer samples the lower portion of each selected still, chooses a
subdued complementary fill, and eases to it over 12 frames at the picture cut.
Colors are mixed toward cream to avoid rainbow-like cycling. When the actual
lyric zone is unusually bright, such as the pale specimen table, the same rule
selects a dark complementary fill instead. There is no backing rectangle.

While a word is active, its letters turn warm white and a subtly expanded,
slightly offset charcoal copy follows the same deformation behind them. This
keeps the live word readable over pale or busy picture detail without making
the letterform itself modeled or extruded. The support disappears with the
word's active window.

## Line handoff

Normal lines enter one frame before their first word and have no post-roll.
When the next lyric follows directly, the outgoing line clears four frames
before the next onset, leaving a brief empty beat between lines. A later phrase
whose `baseline_offset_px_720` is nonzero is an intentional counter-vocal and
is exempt from this clearance only for the registered vocal overlap.

These values are editable at the top of `shots/lyric_motion_full.json` as
`line_preroll_frames`, `line_tail_frames`, and `line_clearance_frames`.

## Timing review

Line frames come from `generated/overlay_cues.json`. The first six phrases
retain their hand-authored word frames. A conservative local Whisper pass over
the master mix has moved 80 demonstrably late words earlier across 30 fully
matched later phrases. It never moved a word later. Remaining later-song word
frames are provisional length-weighted placements, intended to be corrected by
ear before lip sync or final footage.

`shots/lyric_alignment_report.md` records every applied frame change and its
lexical match and confidence. `tools/align_lyric_words.py` can reproduce the
early-only correction from a local word-timestamp transcript. The generated
Whisper transcript stays under `out/` and out of Git.

Use `shots/lyric_timing_review_full.md` as the listening sheet. Enter `OK`,
`on -3f`, `on +2f`, or an exact value such as `on=181`, plus a listening note.
Apply accepted values to `shots/lyric_motion_full.json`; that JSON is what the
renderer consumes. Motion fields remain independent of timing fields, so a
timing correction does not discard the choreography.

`tools/lyric_choreography.py` rebuilds the baseline full-song file from the
lyric register and the opening pilot. Do not rerun it after manual corrections
unless replacing those corrections is intentional.

## Rendering

The complete render is sectioned to keep Blender's dependency graph bounded.
All animation keys remain on absolute song frames, so gestures continue across
section joins. Finished sections are reused on resume.

```powershell
python tools/render_lyric_animatic.py `
  --choreography shots/lyric_motion_full.json `
  --favorites shots/still_favorites.md `
  --out out/blender_animatic_flat_lyrics_v03.mp4 `
  --segment-frames 720
```

The section renderer defaults to approved stills only, keeping typography-only
reviews visually comparable even if motion clips are added under `clips/`.
Pass `--allow-clips` only when intentionally reviewing the motion-clip edit.

Pass `--force` after changing choreography, timing, selected stills, or palette
logic; otherwise valid existing section files are intentionally reused.
