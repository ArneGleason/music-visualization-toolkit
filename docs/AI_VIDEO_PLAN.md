# Rivers of Mars — live-action generated-footage plan

An alternate production path that re-realizes Rivers of Mars as **live-action
style** generated footage: a Wes Anderson quirky take on a 1950s Technicolor
sci-fi take on a Percival Lowell take on Mars. The register, timing grid, and
vector renderer are untouched; this path reuses the same creative backbone
(scenes, transitions, choreography, lyric placement) through the existing shot
pipeline (`shotplan → prompts → animatic → ingest → render`), replacing only
the layer that wasn't landing — the rendered artwork — and adding one new
stage: a **lip-sync pass** against the existing lead-vocal stem.

Current production direction (2026-09-05): use continuous source coverage for
recurring views and refine the whole timeline in successive passes. The exact
outro proposal, source windows, sync strategy, and other candidate sections are
in [CONTINUOUS_COVERAGE_PLAN.md](CONTINUOUS_COVERAGE_PLAN.md). That document
supersedes earlier per-cut generation and repeated-take advice below and in
historical review notes. The proposed outro still needs its free animatic
review; v04 remains the approved edit.

The canonical look reference is the generated master image (astronaut-botanist
in a riveted silver suit kneeling by a canal, domes and needle towers, striped
planet, canal creature) — it realizes the motifs already listed in
`project.json`'s `refs/Rivers-of-Mars.png` vocabulary. Keep it as
`refs/character_master.png` (out of Git, like all media).

## 0. Phase 0 — a one-shot probe before anything else

De-risk the chain end to end on a single 4–6 s close-up before planning-scale
spend:

1. Character still from the master image (image model, Ingredients).
2. Animate it (Frames-to-Video, neutral/loosely-singing mouth).
3. Lip-sync that clip to the matching slice of the **lead-vocal stem** in each
   candidate tool (Kling lip-sync, sync.so `lipsync-2-pro`, Runway Act-Two).
4. Apply the post grade and judge at full resolution.

Pick the sync tool from this probe, not from marketing pages. If no tool holds
up on a singing close-up, the fallback direction is Act-Two style performance
capture: film yourself singing the line on a phone and drive the character
with that video instead of raw audio.

**Outcome (2026-09-01): Phase 0 passed; Kling is the sync tool.** Kling's
audio-driven sync held a sung phrase accurately end to end (drive the whole
clip); sync.so's sync-3 drifted out of sync in parts on the same inputs.
Details and credit costs in `docs/PHASE0.md`.

## 1. Timeline → shots and setups

1. `tools/timeline.py sync projects/rivers-of-mars/project.json` — rebuild the
   compiled register (frame edges at project fps) from the DAW grid.
2. `tools/register2sections.py --project projects/rivers-of-mars/project.json`
   — turn the compiled scene lane into `shots/sections.json` and export the
   register's bar grid as `analysis/beatmap.json`, so the whole shot pipeline
   runs on the same frame-accurate grid as the register.
3. `tools/shotplan.py` (first run), then `tools/shotplan.py --merge` for every
   revision — cuts each scene on its bar grid per `shots/plan.json`, cycling
   through named **setups**. Choreography items are finer than economical
   generation, so setups come from choreography *clusters*; cut density per
   scene follows choreography density. Register scene `prompt` text seeds each
   setup's live-action translation.
4. Hand-edit `shots/shotlist.json` descriptions/prompts. Each shot already
   carries the lyric text it covers — that is the lip-sync work order.

Performance cuts should land on lyric phrase boundaries; the register places
every phrase, so where a bar-grid cut splits a phrase, add `hold` positions in
`plan.json` at that phrase's start instead of hand-trimming seconds.

The current approved still edit uses 41 setups for 59 cuts. The proposed
dialogue edit adds cuts without requiring one generation per cut.

## 2. Shot categories

- **Character performance** (Ingredients-to-Video, fixed refs; `_sync` setups
  get the lip-sync pass): astronomer at the observatory, astronaut on Mars,
  lamplit duet crosscuts.
- **Environments** (drift-tolerant, no faces): observatory dome, Mars night
  wide, the canal forest, domes wide, weather over the colony, rockets
  descending from orbit and landing, basin moon descent, the water ballet
  from above, drum-wall basin, telescope time tunnel.
- **Objects**: canal-map pieces, transmitter, receiver dials, specimen table,
  pattern tests, counterfeit parade, excavation site.
- **Macro imagery**: oscilloscope trace, radio masts, flora detail, canal
  current, the mer-folk surfacing — the most forgiving category; use it
  wherever the register calls for texture-level choreography.
- **Transitional material**: interference bloom, forest threshold,
  rain-to-canal, chorus plunge, canal-junction turn, following wake,
  goodnight cascade, night iris — short dedicated clips whose first/last
  frames tie adjoining setups together, standing in for the register's
  transition lane.

Since the owner's second review (2026-09-02): every waterway is a winding
natural **river** (the basin is the river's lagoon, no gates), and the
only figures in the film are the two twins and the chrome mer-folk.

Each setup also names its cinematographic conventions (catalog IDs);
`shots/conventions.json` phrases them for a photographed film and the
prompt tool appends them, so the register's shot language reaches the
generators.

Setup bodies are authored once, at the setup level, in `shots/setups.json`
(`still` = the frame without motion words, `motion` = the video sentence) and
applied with `tools/shotplan.py --setups shots/setups.json`. The v2 revision
after the owner's first storyboard review (canal basin, canal forest,
mer-folk school, orbit arrivals, twin differentiation by hair, canonical suit)
is recorded in `docs/STORYBOARD_REVIEW.md`.

Lean non-character wherever the narrative allows; faces are where drift and
sync cost live.

## 3. Reference images and character consistency

- **Master reference**: the generated canal image (`refs/character_master.png`)
  anchors character, wardrobe, palette, and world at once.
- Build a **character sheet per performer** — the astronaut (from the master
  image) and the astronomer, her identical twin (same face, hair worn up in
  a French twist, tweed; no eyewear anywhere in the film — an accessory bleeds
  between twins, hair does not): full front, 3/4 medium, close-up, profile,
  mid-movement, plus a neutral-mouth frontal close-up for sync shots. Iterate
  in images (cheap) until each reads as one person on one day; only then
  touch video.
- Wardrobe is one canonical sentence per outfit (the cast lines in
  `shots/style.md`, substituted verbatim into prompts) plus a **suit
  turnaround board**; the **mer-folk** get a design sheet of their own.
- Also generate a **palette board** and the **world boards** (canal + colony,
  observatory interior, canal basin, canal forest, Mars from orbit) as
  environment anchors.
- Store in `refs/`, register in `shots/style.md` as `- ref name: path` lines,
  attach via Ingredients-to-Video on every performance shot. Only the registry
  lines are committed.

## 4. Style / prompt lock

`shots/style.md` carries the lock block: live-action 1950s Technicolor
sci-fi, planimetric Wes Anderson composition, soundstage Mars, canals, domes,
silver suits, deadpan performance, slow symmetrical camera. `tools/prompts.py`
appends it verbatim to every prompt; never paraphrase it between shots.
Generate clean 16:9; the uniform post grade adds Technicolor saturation, fine
grain, halation, and a 2.39:1 letterbox equally to every clip — the grade and
letterbox are also the drift-hiders.

## 5. First/last frames and durations

- `shots/shotlist.json` gives exact editorial frame edges at 24 fps. Source
  takes may cover several cuts and the gaps between them. Size them to that
  complete window, with handles where practical; `max_shot_sec: 8.0` is an
  editorial cutting rule, not a source-duration limit.
- `tools/prompts.py` currently reports the longest single cut per setup. That
  is insufficient for continuous coverage. Use the reviewed source-window
  work order until the exporter is extended to understand coverage takes.
- Start the first take from the approved still or a reviewed calmer coverage
  anchor. For subsequent blocks, use an appropriate continuation frame from
  the preceding take at the next block's song-time origin. Re-entry to a view
  advances its source clock; it does not restart the approved board pose.
- For a designed transition or beat-critical arrival, use reviewed start/end
  anchors when supported and trim to the required arrival in post. Hide joins
  between source blocks while another view or insert is on screen.
- Keep `clip.speed = 1` for synced performance. Set each cut's `clip.in_sec`
  from its source take's song origin and verify duration/offsets after sync.
- Performance shots destined for lip-sync are generated with the mouth
  neutral or loosely singing — the sync pass replaces mouth motion, and it
  degrades on extreme angles, profiles, and occlusion, so keep `_sync` setups
  frontal close/medium and let wides get away with plausible mouth movement.
- Sync each whole coverage take using that performer's lines at their original
  timestamps and silence during the other performer's turns. Both twins use
  the same singer; the lead-vocal stem needs reviewed speaker gating, and
  overlapping voices cannot be separated by gating alone.

## 6. Storyboard and animatic

1. Generate one still per setup (image models, refs attached) into
   `board/frames/` as Anderson-style tableaux; review with the contact sheet
   (`board/contact.html`) and reject/regenerate. These stills double as
   Frames-to-Video endpoints later, so approving them approves the film's
   compositions.
2. `tools/storyboard_animatic.py` cuts the approved stills against
   `audio/song.wav` on the exact shotlist frame edges — a free, frame-accurate
   preview of the whole edit.
3. Iterate `plan.json` + `shotplan.py --merge` + animatic until the cut
   works. **No paid video generation before the animatic is approved**
   (AGENTS.md invariant 5).

## 6b. Compositing and motion graphics: Blender, headless (2026-09-02)

The owner's call after the video tests: the browser-capture renderer is not
the tool for motion graphics or compositing (too much overhead per frame,
too much friction). This path renders in **Blender 5.2, headless**, with no
browser anywhere:

- `tools/overlay_cues.py` exports beats, lyric lines, sections, choreography
  spans and the cut from the register at the output fps into
  `generated/overlay_cues.json` (frame-accurate, derived, not committed).
- `tools/blender_comp.py` builds a Video Sequence Editor scene from the shot
  list and the cues and renders it (`blender -b`, it relaunches itself):
  the cut on channel 1 (clips trimmed to the exact frame count, otherwise the
  setup's storyboard still, otherwise a slate), the master mix, the 2.39
  letterbox, an additive **beat pulse** keyframed on every beat (harder on
  downbeats and section starts), and optional per-twin **lyric captions**.
  `--overlay-only` renders the overlay channels over transparency as
  PNG+alpha. A 10 s proxy audition renders in ~5 s including startup.
- Next elements are functions reading the same cue file: bar rings and
  ribbons (a 3D Scene strip with emission and bloom over the footage), the
  drum-wall geometry, section wipes, and the choreography lane's
  `rendererShot` spans as element triggers. `--save-blend` keeps a .blend for
  hand tweaking when wanted.

## 7. Generation work order, takes, ingest, budget, fallback

- **Work order**: Phase 0 and the chorus tests have established a usable path.
  Review the new outro coverage next, then carry the learning through the
  opening, reply, action/insert scenes, and remaining timeline. Rough motion
  coverage, sync/continuity, and selective refinement are whole-film passes.
- **Takes**: one initial candidate per planned source window during the first
  pass, with at most one targeted correction for a clear failure. Record the
  lesson and move on with a usable test, still, or insert. Additional takes
  belong to a later refinement pass supported by a specific hypothesis.
  Sync the selected usable take once; do not default to multiple sync variants.
- **Take review (owner's dailies rule)**: candidates are approved in
  **batches and in context**, never in isolation — each candidate is viewed
  butted against the current best take of the previous and next cut, with
  the master mix over the join, because a take that reads fine alone can be
  a discontinuity against its neighbors (radically different performance
  energy across a cut). Rejections go onto a ranked issue list while the first
  pass advances to other sections. Later passes revisit weak footage with
  lessons learned elsewhere. Smallest tooling: a
  generated review page (like `board/contact.html`) that plays each
  candidate in a prev/candidate/next strip and records approve/regen per
  take back into the shotlist clip assignment.
- **Ingest**: name media by setup, coverage window, take, and sync version.
  Record the source's song start and assign each cut its own in-point.
  `ingest.py --auto` currently assigns the same zero in-point to every matching
  setup use, so it is unsuitable for these coverage returns without further
  individual assignments. Preserve those assignments through `--merge`.
- **Budget**: count source windows and full synced seconds, not editorial
  cuts. The draft outro uses six 8-second motion takes and up to six sync
  jobs. Check current tool durations and pricing before an order. Longer
  coverage buys editing freedom but can cost more per visible second; there
  is no automatic blanket allowance for repeated variants.
- **Fallback**: any setup that won't converge falls back to (a) a still +
  slow push (Frames-to-Video from one approved board frame), (b) macro/insert
  substitution, or (c) for stubborn sync shots, a non-sync medium where the
  mouth is turned away or in shadow. The edit never blocks on a stubborn
  generation. (The vector render is no longer a per-shot fallback — it's a
  different film now.)

## 7b. Beat-locked overlay pass (post)

In-generation motion cannot be trusted to hit musical events — lip sync is
the one in-generation sync we get (and the probe proved it). Every other
musical punctuation happens **in post, over the footage**, driven by the
same data that drove the vector video: `analysis/beatmap.json` (bars/beats),
the compiled register (sections, lyric phrases, transitions), and
`generated/performance.json` (drum low/mid/high, bass, guitar envelopes and
exact MIDI note events). No hand-keyframing, no guessing — cues land on the
grid by construction.

Three layers, in order of preference:

1. **Blender effects and screen replacement**: reuse the vector path's musical
   data and selected behavior ideas in dedicated Blender scenes/compositor
   treatments, assembled in the existing VSE. Start with the opening
   oscilloscope: remove the invented trace and replace it with actual
   bass-driven light beneath the glass. See `docs/SCREEN_SYNC_PILOT.md` for
   the single-element test. Geometry, masks, emission, and depth-aware
   compositing can support later rings, ribbons, and surface responses.
2. **ffmpeg expression cues** generated from the beatmap into a filter
   script: exposure kicks on downbeats, vignette/letterbox micro-breathing,
   lantern-flare pulses on the kick, subtle scale punches on section
   boundaries. Cheap, deterministic, good for the whole-film grade pass.
3. **Optional manual polish in a free/open NLE**, never for sync-critical
   work: export beat/section/lyric markers from the compiled timeline
   (CSV/EDL) so DaVinci Resolve (free) or Kdenlive/Blender (open source)
   display musically exact cue points for taste edits.

Aesthetic guardrail: overlays obey the lock — warm halation, technicolor
palette, no text; light behaves like sound, surfaces never change material.

Smallest next tooling: a Blender screen-treatment scene with explicit audio
mapping and a plate mask. Add tracking for the moving-plate test, and expand
the reusable tooling only after the experiment demonstrates what is needed.

## 8. Minimal tooling / schema changes

Committed in this branch:

1. **`tools/register2sections.py`** — compiled register → `shots/sections.json`
   + `analysis/beatmap.json`; everything downstream already consumes those.
2. **`shots/plan.json`** — cutting rules per register scene, live-action setup
   vocabulary; the `_sync` suffix marks shots that get the lip-sync pass (a
   naming convention, not a schema change — `ingest.py --status` and the
   prompts file group by setup name, so sync coverage is visible for free).
3. **`shots/style.md`** — character/ref registry and the prompt lock block.

Deliberately unchanged: the register schema, `project.json`, `timeline.json`,
the vector renderer, and the shot pipeline itself. Sections carry a
`register_id` back-reference (ignored by existing tools).

## Runbook

```bash
./.venv/bin/python3 tools/timeline.py sync projects/rivers-of-mars/project.json
./.venv/bin/python3 tools/register2sections.py --project projects/rivers-of-mars/project.json
./.venv/bin/python3 tools/shotplan.py            # --merge on every later run
./.venv/bin/python3 tools/prompts.py
# Phase 0: one-shot probe (still -> clip -> lip-sync tools -> grade)
# storyboard stills -> board/frames/, review contact sheet
./.venv/bin/python3 tools/storyboard_animatic.py
# after animatic approval: generate coverage windows, sync selected takes,
# assign each cut with its own --assign / --file / --in mapping, then
./.venv/bin/python3 tools/ingest.py --status
./.venv/bin/python3 tools/render.py
```
