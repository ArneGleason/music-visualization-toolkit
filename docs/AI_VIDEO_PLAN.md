# Rivers of Mars — generated-footage implementation plan

An alternate production path that re-realizes the published vector video
(`projects/rivers-of-mars/`) as AI-generated footage. The register, timing
grid, and vector renderer are untouched; this plan only adds a parallel route
from the same creative source material through the existing shot pipeline
(`shotplan → prompts → animatic → ingest → render`).

## 1. Timeline → shots and setups

The register's scene lane (15 scenes), transition lane (15), and choreography
lane (63 items) already constitute a director's cut. The mapping is:

1. `tools/timeline.py sync projects/rivers-of-mars/project.json` — rebuild the
   compiled register (frame edges at project fps) from the DAW grid.
2. `tools/register2sections.py --project projects/rivers-of-mars/project.json`
   (new, in this branch) — turn the compiled scene lane into
   `shots/sections.json` and export the register's bar grid as
   `analysis/beatmap.json`, so the whole shot pipeline runs on the *same*
   frame-accurate grid as the vector renderer.
3. `tools/shotplan.py` (first run), then `tools/shotplan.py --merge` for every
   revision — cuts each scene on its bar grid per `shots/plan.json` and cycles
   through named **setups**. Choreography items are finer than economical
   generation, so setups are drawn from choreography *clusters* (e.g. the nine
   `choreo-river-*` items collapse into seven river setups), and cut density
   per scene comes from the choreography density.
4. Hand-edit `shots/shotlist.json` descriptions/prompts; scene-lane `prompt`
   text is the seed for each setup's description.

Roughly 25 setups cover ~90 cuts; reuse is what keeps the budget sane.

## 2. Shot categories

- **Character performance** (Ingredients-to-Video with fixed refs):
  `them1_*`, `them2_*`, `duet_*` — the sender/receiver dialogue scenes
  (signal-exchange, starfield waiting, mars reveal, low-light outro).
- **Environments** (drift-tolerant, no character): garden dolly, mars rings,
  semantic weather, rockets overhead, river moon descent, drum wall,
  time tunnel, starfield.
- **Objects**: puzzle pieces, inspection table, pattern tests, counterfeit
  parade, excavation.
- **Macro imagery**: signal wires, packet travel, river current, mouth
  microcosm, interference bloom — the most forgiving category; use it
  wherever the register calls for texture-level choreography.
- **Transitional material**: rain-to-river, chorus plunge, current
  switchyard, following wake, goodnight cascade, night iris — generated as
  short dedicated clips whose first/last frames tie adjoining setups
  together, standing in for the register's transition lane.

Rule of thumb from `docs/GENERATION.md`: lean non-character wherever the
narrative allows; the concept scenes are the natural home for it.

## 3. Reference images and character consistency

- Source: `refs/Rivers-of-Mars.png` (the authored figurative reference) plus
  new image generations (Nano Banana Pro / Imagen).
- Build a **character sheet per figure** (Them 1 warm/gold, Them 2 cool/teal):
  full front, 3/4 medium, close, profile, mid-movement. Iterate in images
  (cheap) until each reads as one being; only then touch video.
- Also generate a **palette board** and one **world board** (Mars terrain +
  river + garden) as environment anchors.
- Store in `refs/`, register in `shots/style.md` as `- ref name: path` lines,
  attach via Ingredients-to-Video on every performance shot. `refs/` media
  stays out of Git; only the registry lines are committed.

## 4. Style / prompt lock

`shots/style.md` (this branch) carries the lock block — painterly sci-fi
animation, gold/teal light figures, rust Mars, chrome water, music-pulsing
light, slow purposeful camera, no text. `tools/prompts.py` appends it verbatim
to every prompt; per AGENTS.md it is never paraphrased between shots. A
uniform post grade in `tools/render.py` hides residual drift.

## 5. First/last frames and durations

- `shots/shotlist.json` gives every cut exact `frames` at 24 fps via
  `to_frames`; `tools/prompts.py` notes the longest cut per setup — generate
  at least that long, choose in-points with `ingest.py --in`.
- Ceiling `max_shot_sec: 8.0` matches one generation; anything longer is
  auto-split on the bar grid or extended with Scenebuilder.
- **Frames-to-Video** (first *and* last frame) is mandatory for:
  - every *transitional* setup (rain-to-river, night iris, …) — last frame of
    the outgoing setup and first frame of the incoming one;
  - any cut that must land somewhere specific on a downbeat (the garden
    dolly arriving at the drum awakening, the chorus plunge);
  - re-entries to a repeated setup, so each chorus return starts from the
    same still.
  Stills for this come from the storyboard stage below.

## 6. Storyboard and animatic

1. Generate one still per setup (image models, refs attached) into
   `board/frames/`; review with the existing contact sheet
   (`board/contact.html`) and reject/regenerate.
2. `tools/storyboard_animatic.py` cuts the approved stills against
   `audio/song.wav` on the exact shotlist frame edges — a free, frame-accurate
   preview of the whole edit.
3. Review against the published vector video (same grid, so they can be
   compared cut for cut). Iterate `plan.json` + `shotplan.py --merge` +
   animatic until the cut works. **No paid video generation before the
   animatic is approved** (AGENTS.md invariant 5).

## 7. Generation work order, takes, ingest, budget, fallback

- **Work order**: `tools/prompts.py` writes `prompts/prompts.md` grouped by
  setup with longest-cut durations. Generate in priority order: (1) the seven
  river/chorus setups (most reused), (2) performance setups, (3) environments,
  (4) macros, (5) transitionals last (they need approved neighbor frames).
- **Takes**: 2–3 takes for setups used by 4+ cuts (chorus river, garden
  dolly, both duet setups); 1 take for single-use setups. Pick take/in-point
  at ingest, not at generation time.
- **Ingest**: download named after the setup (`river_current_macro.mp4`) into
  `clips/inbox/`, then `ingest.py --auto` files it and wires it to every cut;
  `ingest.py --status` tracks coverage; `--in` selects the musical in-point.
- **Budget**: ~25 setups × ~2 average takes ≈ 50 generations first pass,
  +20 for fixes — inside one month of a high-tier Flow subscription. API
  top-up at Veo 3.1 list prices (~$0.40/generation at 1080p, Fast ~$0.12) puts
  a full re-pass in the tens of dollars. Confirm current pricing first.
- **Fallback**: the published vector render exists, so any setup that won't
  converge can fall back to (a) the vector renderer's footage for that scene
  ingested as a clip, (b) a still + slow push (Frames-to-Video from one
  frame), or (c) macro/texture substitution. The edit never blocks on a
  stubborn generation.

## 8. Minimal tooling / schema changes

Committed in this branch:

1. **`tools/register2sections.py`** (new, ~90 lines) — compiled register →
   `shots/sections.json` + `analysis/beatmap.json`. The only new code needed:
   everything downstream (`shotplan`, `prompts`, `storyboard_animatic`,
   `ingest`, `render`) already consumes those files.
2. **`shots/plan.json`** — cutting rules per register scene with the setup
   vocabulary above.
3. **`shots/style.md`** — character/ref registry and the prompt lock block.

Deliberately *not* changed: the register schema, `project.json`,
`timeline.json`, the vector renderer, and the shot pipeline itself. The
`sections.json` written here carries an extra `register_id` field per section
(ignored by existing tools) so sections stay traceable back to the register.

## Runbook

```bash
./.venv/bin/python3 tools/timeline.py sync projects/rivers-of-mars/project.json
./.venv/bin/python3 tools/register2sections.py --project projects/rivers-of-mars/project.json
./.venv/bin/python3 tools/shotplan.py            # --merge on every later run
./.venv/bin/python3 tools/prompts.py
# storyboard stills -> board/frames/, review contact sheet
./.venv/bin/python3 tools/storyboard_animatic.py
# only after animatic approval: generate, then
./.venv/bin/python3 tools/ingest.py --auto && ./.venv/bin/python3 tools/ingest.py --status
./.venv/bin/python3 tools/render.py
```
