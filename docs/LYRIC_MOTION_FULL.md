# Full-song flat lyric choreography

Status: first complete animatic rendered for owner timing and motion review.

## Current review render

`out/blender_animatic_flat_lyrics_v01.mp4` is the complete 1280×720 animatic:

- 4,782 frames at 24 fps (199.25 seconds)
- all 59 timed picture cuts using the 41 approved still selections
- 87 registered lyric lines and 305 individually timed words
- flat Fredoka glyph shapes with no visible extrusion, bevel, modeled lighting,
  perspective depth, or backing rectangle
- the original master mix encoded once after the frame-locked sections join

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

## Color and contrast

The renderer samples the lower portion of each selected still, chooses a
subdued complementary fill, and eases to it over 12 frames at the picture cut.
Colors are mixed toward cream to avoid rainbow-like cycling. When the actual
lyric zone is unusually bright, such as the pale specimen table, the same rule
selects a dark complementary fill instead. There is no backing rectangle.

## Timing review

Line frames come from `generated/overlay_cues.json`. Word frames after the
opening pilot are provisional length-weighted placements, intended to be
corrected by ear before lip sync or final footage.

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
  --out out/blender_animatic_flat_lyrics_v01.mp4 `
  --segment-frames 720
```

Pass `--force` after changing choreography, timing, selected stills, or palette
logic; otherwise valid existing section files are intentionally reused.

