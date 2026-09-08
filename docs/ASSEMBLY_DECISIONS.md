# Shared assembly decisions: intentional visualization replacements

Opening review patch: `opening_need_landscape`, song205..282, now requires the
owner-approved generated aerial plus garden/architecture lights from
`out/opening_aerial_glimmer_v1/clean.mp4`, source0..77 at24fps. This is a new
review cut, not an old production shot ID. Its source selection and exact
snapshot are recorded in `shots/opening_review_decisions.json`. FX baked once,
no audio or lyrics. Do not use untreated Flow in its place. Full-film merge
pending; the September7 full review predates this insert.


For the newer phrase-contained opening, also read
[OPENING_REVIEW_ASSEMBLY.md](OPENING_REVIEW_ASSEMBLY.md) and
shots/opening_review_decisions.json. The owner-approved two-rosette performance
extension uses revised review timing; do not lose it when merging the opening
into the older production edit. Review-composite approval is not clean delivery.

This is the handoff between Codex, Claude, and whoever assembles the film.
Read alongside `shots/assembly_decisions.json` before ingesting or selecting
clips. The shot list remains the timing authority; this register records
owner-approved source-selection intent and production readiness.

## Protected selection

| Shot / setup | Use in preference to generated footage | Status |
| --- | --- | --- |
| s002 / obs_console_macro | Approved still-based oscilloscope composite with imperfect rail push-in | Clean 1080p delivery ready; automatic source override enabled |
| o01 / telescope_time_tunnel (retired s056) | Amber/cyan analog contours and anticipatory beat arrivals | Fresh 57-frame silent 720p rough delivery at the new song position |
| s010 / receiver_dial_macro | Tracked amber meter light response | Silent 720p full-cut rough delivery |
| s019 / forest_fauna_eyes | Accepted full-strength three-depth-band garden airflow composite | Silent 720p full-cut rough delivery |
| s037 / rockets_landing_wide | Accepted strong pressure-lens pulses | Silent 720p full-cut rough delivery; plate regeneration deferred |
| s043, s044, s047 / chrome swimmers | Violet/pearl light response | Silent 720p full-cut rough deliveries; all-swimmer expansion deferred |

### Tunnel delivery handoff

Current o01 delivery: `out/tunnel_arrival_o01/clean.mp4`, song frames [4120,4177).
Recipe: `python tools/tunnel_arrival_pilot.py --two-color --shot o01`.
The old s056/48-frame review remains a look reference, not the current cut.
Drum events and guitar displacement were freshly sampled at the new song position.
No loop, stretch, or movement of the old baked musical timing. Four alternating
arrivals now span the cut. This is rough-ready, not final tracking/occlusion QA.
Keep the underlying generated motion clip as a spare, not an automatic fallback.
See `docs/MUSICAL_CONTOUR_PILOT.md` for settings and remaining limitations.

Approved review: `out/screen_sync_scope_rail/dual.mp4`.
Still: `codex/out/obs_console_macro_b.jpg`.
Recipe and development: `docs/SCREEN_SYNC_PILOT.md`.
It includes amber bass + 30% guitar, cyan bass rosette, phosphor persistence,
soft cyan focus, pickup/crackle, centre magnification, gentle intensity build,
and the imperfect camera move. The owner approved the rail version as the keeper.

**Do not automatically replace this picture with Flow or other generated video.**
A generated take may remain as spare/reference. Its presence, age, filename,
or successful generation does not override this selection. Do not put that take
on a higher picture layer covering the approved composite.

## Enforced assembly selection

Blender timebase correction (2026-09-05): after protected source selection,
`assembly_timebase.py` resolves mismatched-rate clips to silent timestamp-resampled
CFR copies under `out/assembly_cfr/`. Original media and in-points in seconds are
preserved. Run `python tools/assembly_preflight.py --prepare-timebase` before a
Blender assembly. Missing conversions fail closed. Protected FX remain unchanged.
The global full-frame flash is now disabled by default; `--beat-flash` is only
an explicit legacy opt-in. Local musical light, bloom and pulse effects remain.

Both `tools/blender_comp.py` and `tools/render.py` now use the shared
`tools/assembly_sources.py` resolver. For s002 they choose
**`out/screen_sync_scope_rail_clean/dual.mp4`** instead of the generated take.
The file is a silent, label-free 1920x1080 render with 69 frames at 24 fps.
It preserves the approved rail treatment. Reproduce with the approved renderer
arguments plus `--clean`. The sole soundtrack comes from the assembly master.

`shots/shotlist.json` retains the existing generated take assignment as a
candidate, so this change does not interfere with generation or lip-sync
bookkeeping. Protected source selection takes precedence at render time.
The resolver reads only; it does not rewrite clips or shot data. Ingest/re-plan
changes to a candidate do not override the protected selection.

Missing/pending clean delivery, changed setup, changed shot timing, mismatched
Blender cues, wrong source fps or insufficient frames cause a clear error,
not a silent Flow fallback. Unprotected shots retain their previous behavior.
Explicit `--stills-only` and `--overlay-only` are intentionally unchanged.
Future assemblers must use this resolver too; external editing software does
not automatically read this repository registry.

1. Use the clean delivery above, not the labelled/audio-bearing review movie.
2. Check current timing. The approved test covers song frames [86,155) at 24 fps,
   69 frames, with source frame 0 aligned to song frame 86. This matches the
   inspected overlay cue. If the cut moves, re-evaluate/re-render music-synced
   content; moving or stretching a baked movie alone may put it out of phase.
3. Preserve registry-aware selection on later merge/re-plan/ingest operations.
4. Use the final master audio once, not this preview's embedded soundtrack.
5. Inspect s002 in the assembled movie, including layer order and cut edges,
   and mark the register applied with the exact full-film output/version.
   A ready delivery is not a claim that the full film has already been rebuilt.

Verification: seven source-selection tests cover precedence, unchanged ordinary
shots, missing/pending media, timing/setup changes, and fps/frame coverage.
A one-frame actual Blender assembly selected the clean source for s002.
Existing global assembly overlays/colour treatment remain unchanged; evaluate
their interaction with the approved scope look during full-film review.

No pre-roll or exit handles were rendered in this test. Exit-only handles are
the production default; see `docs/CONTINUOUS_COVERAGE_PLAN.md`. Record actual
usable footage and sync coverage, never infer availability from rounded length.

If the approved local render is missing, flag it or reproduce it. Do not
silently substitute generated footage. A different treatment needs owner review.

## Collaboration protocol

Swimmer uses are inventoried in `shots/fx_uses.json` (s043, s044, s047).
The owner accepted these passes; all three are now automatic protected selections
for the rough. s044 has 67 frames from its rounded boundaries, now reconciled.
The request to extend highlights to every swimmer remains deferred, as do
full-source exit handles and candidate-final quality work.

- Add one entry per intentionally treated shot; identify exact shot IDs, not
  just setup names, so repeated views aren't changed accidentally.
- Distinguish proposed, treatment-approved, delivery-ready and applied states.
  Approval of a look test is not proof it is already present in the full film.
- Record the selected version, reproduction recipe, source time mapping,
  superseded takes, handle coverage, and any unresolved assembly requirements.
- Update this register and production status after an owner decision. Preserve
  spare media; no need to stop or discard another agent's generation work.
- At handoff, reconcile these decisions with the shot list and final render.
  This is a shared file record, not a live feed of another agent's activities.

Eight selections are protected. See `docs/ROUGH_ASSEMBLY_PREP.md` for the current
outro, coverage patch and preflight. Delivery-ready means usable in this rough,
not mastered, 1080p-final or already present in a rebuilt full film.
