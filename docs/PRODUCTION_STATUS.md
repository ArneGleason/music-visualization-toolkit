# Rivers of Mars live-action production status

LATEST CHECKPOINT: [2026-09-06 restart notes](PAUSE_2026-09-06.md).
Phrase-contained version-two opening is assembled through song frame911 in
isolated out/ review snapshots. Next: owner requests fresh astronaut performance
with verified pre-roll, not patching the old sync gap. No job submitted yet.
Older full-rough status below is historical, not the current opening edit.

Pause point: 2026-09-05

## Current state

NUMBERED REVIEW COPY: `out/rough_v04_numbered_720p.mp4`. Small top-right black
circle with white sequential cut numbers 1-71, changing at exact cut frames.
Lookup: `out/rough_v04_numbered_720p.md`, maps numbers to stable shot IDs.
This is v04 picture plus review badges; original master audio copied unchanged.
Recipe: `python tools/number_review_cuts.py`. Use version-specific lookup when
translating owner notes, since sequential numbers can change with future edits.

LATEST OUTPUT: `out/rough_v04_sync_noflash_720p.mp4`, 720p / 24 fps / 3:19.25.
Authorized frame-rate correction implemented and re-rendered. Global flash off;
local FX, cuts, lyrics and master timing preserved. Completed-file source-frame
checks confirm real-time playback, including nonzero in-points. Full decode,
preflight and 14 tests pass. See `docs/ROUGH_V04_TIMEBASE.md`. Residual model sync
and motion quality await owner review. The audit-only status below is superseded.

LATEST OWNER REVIEW: rough v03 structure/content accepted as a good rough.
Remove global beat flash next pass. A diagnostic confirmed 30 fps Kling media
plays frame-for-frame at 24 fps in this Blender assembly, causing growing lip-sync
lag in 12 shot assignments. Do not regenerate these before correcting playback.
See `docs/ROUGH_V03_REVIEW_AND_SYNC_AUDIT.md` for evidence, lead-in strategy and
ordered tasks. No implementation or replacement render performed in this audit.

LATEST ROUGH RENDER, 2026-09-05: `out/rough_v03_fx_outro_720p.mp4`.
Full 1280x720 / 24 fps review, 4782 picture frames (3:19.25), one master audio
track, existing flat animated lyrics, updated outro and coverage cutaway, all
eight protected FX selections. Previous versions retained. See
`docs/ROUGH_ASSEMBLY_RENDER.md`. This supersedes the no-render status below.

LATEST, 2026-09-05: rough preparation is integrated. See
`docs/ROUGH_ASSEMBLY_PREP.md` before the older development notes below.
71 shots / 4782 frames; continuous-coverage outro promoted; one-second weather
cutaway patches s034; eight accepted FX selections protected. Tunnel migrated
from s056 to o01 and freshly rendered at its new song time. s044 frame count
reconciled to 67. Full rough has not yet been rendered. Remaining older mentions
of pending swimmer approval and pending s056 delivery are superseded.

Finishing target confirmed: 1080p / 24 fps, not 4K. Current swim and tunnel FX
reviews are 720p; inspected swim sources are also 720p/8 seconds. Candidate-final
requirements and deferred full coverage/all-swimmer work are recorded in
`docs/CANDIDATE_FINAL_CHECKLIST.md`. No final mastering or upscaling performed.

Violet-to-pearl approved for chrome swimmers. Three full-boundary FX candidates
rendered: s043, s044, s047 (`out/swimmer_fx_full/`). Review videos plus silent
clean composites, inventory in `shots/fx_uses.json`. No final assembly rebuild.
Full-shot owner review pending; s044 also needs its one-frame metadata mismatch
reconciled. Consult the inventory before using untreated swim footage.

Surface swimmer color trial ready: `out/swimmer_palette_pilot/cyan.mp4` and
`out/swimmer_palette_pilot/violet.mp4`. Same four torso highlights and forward
response choreography, alternate bloom colors over pearl cores. Two-second
test only, awaiting review. See `docs/SWIMMER_LIGHT_PILOT.md`; one-frame existing
s044 shotlist/cue discrepancy must be reconciled before full delivery.

OWNER DECISION: amber/cyan tunnel treatment is approved as reusable FX-04 AND
the required look for s056. Protected assembly entry added. Full-shot delivery
pending (139 frames required; 48-frame review only). Motion assembly now flags
pending s056 rather than silently selecting untreated footage. No render, source
clip or shot timing changed. See `docs/ASSEMBLY_DECISIONS.md`.

Latest tunnel palette test: `out/tunnel_arrival_amber_cyan/tunnel_arrivals.mp4`.
Alternating amber/cyan arrivals over muted teal contours; each pulse retains its
color through travel. Same strong waveform, bloom and timing. Prior version
preserved; awaiting review. No assembly changes.

Latest tunnel strength review: `out/tunnel_arrival_intense/tunnel_arrivals.mp4`.
10x waveform displacement, stronger foreground response and broader depth-scaled
bloom. Accepted timing unchanged; previous arrival preview preserved. Awaiting
review; no assembly changes. See `MUSICAL_CONTOUR_PILOT.md`.

Latest tunnel experiment: `out/tunnel_arrival_pilot/tunnel_arrivals.mp4`.
Multiple detected rim contours with two anticipatory distant-to-near light
arrivals on drum hits. Two-second choreography test, awaiting owner review.
Per-frame radial edge detection, not persistent per-ring tracking; temporal
phosphor history and spoke masks still pending. See `MUSICAL_CONTOUR_PILOT.md`.

FX-04 analog contour revision: `out/musical_contour_tunnel_analog/musical_contour.mp4`.
Same two-second tracking test; adds dwell-dependent width/intensity, circulating
scan head/tail, ring-local persistence, signal noise and visual soft saturation.
Original white-line version preserved. Awaiting review, no assembly change.

FX-04 musical contour opening test on s056:
`out/musical_contour_tunnel/musical_contour.mp4`. Two seconds, one guitar-deformed
ring outline with drum kicks. Constrained radial tracking, not a camera solve;
longer tracking and spoke occlusion remain pending. See `MUSICAL_CONTOUR_PILOT.md`.
Awaiting owner review; no assembly changes.

Latest FX-03 review: `out/pressure_lens_rockets_exaggerated/pressure_lens.mp4`.
Two isolated, deliberately strong drum-triggered waves reveal the added optical
effect against busy source footage. Original test preserved; no assembly change.
Deferred landing-footage correction recorded in `docs/REGENERATION_NOTES.md`;
no generation started.

FX-03 localized pressure-lens test rendered on s037 rocket exhaust:
`out/pressure_lens_rockets/pressure_lens.mp4`. Blender compositor displacement,
drum-led expanding ripples, slight dispersion, authored foreground exclusion.
Awaiting review; no assembly changes. See `docs/PRESSURE_LENS_PILOT.md`.

FX-02 receiver-meter pilot rendered: `out/tracked_light_receiver/receiver_light.mp4`.
Large amber meter follows a local 2D feature track and receives drum-driven core
brightness and soft bloom. 69 frames, song [774,843), original master audio.
Awaiting owner review; source and assembly unchanged. Details and limitations:
`docs/TRACKED_LIGHT_PILOT.md`.

Reusable FX catalogue: `docs/FX_TYPES.md`. Owner accepted garden bloom/depth as
FX-01's full-strength look; strength will be reassessed against moving footage.
Separate production layers are NOT yet exported for this version. FX-02, tracked
augmentation of an existing light, is the proposed next small motion test.
Tracking strategy, other candidate effects and handoff requirements are recorded.
No renderer, footage assignment or assembly registry changed by this planning pass.

Latest garden intensity/depth review:
`out/garden_airflow_bloom_depth/garden_airflow.mp4`. Stronger drum-led emission,
two soft halo scales around hot dust cores, and three differentiated depth bands
with fuller edge coverage. Artistic bloom approximation, not physical scattering.
Owner accepted this stronger follow-up as a full-strength FX reference. Original tests remain,
and s019 assembly selection is still unchanged. See `docs/GARDEN_DUST_PILOT.md`.

Latest garden review: `out/garden_airflow_pulse/garden_airflow.mp4`. Owner liked
the dispersed airflow; added drum-led emission pulses (22 ms attack / 200 ms
release) for stronger musical presence without changing size, density, opacity
or motion. Bass continues to drive flow. 68 frames at 24 fps verified; brightness
revision awaits review. No change to s019 assembly selection. Reproduction and
limits: `docs/GARDEN_DUST_PILOT.md`.

Previous garden alternative: `out/garden_airflow/garden_airflow.mp4`. Dispersed
fine motes and faint wisps advected through a faster 3D curl flow, with drum
disturbances, bass strength, approximate foliage deflection/occlusion and a
static perspective camera. Not a native fluid solve or reconstructed scene.
Owner liked this spatial direction; no change to s019 assembly selection. Earlier clustered
native-emitter experiment retained as comparison, not the preferred direction.

Latest garden experiment: `out/garden_dust_fields/garden_fields.mp4`. Actual
Blender emitters plus harmonic attraction, vortex, drum repulsion and turbulence;
beat-grid centre choreography and bass-modulated gathering. More collective
motion than the subdued dust test. Editable scene and controls saved alongside.
Review pending; s019 is not protected/reassigned and generated clips untouched.

New experiment for review: s019 / forest_fauna_eyes, static garden plate with
drum-disturbed luminous dust and bass-modulated drift. Preview:
`out/garden_dust_pilot/garden_dust.mp4`; separate transparent frames and audio
controls retained. See `docs/GARDEN_DUST_PILOT.md`. Not an approved substitution;
existing s019 generated footage and all lip-sync work remain untouched.

**Assembly handoff:** s002 / obs_console_macro is an owner-approved intentional
visualization replacement. Prefer the imperfect rail scope composite over Flow
footage. Read `docs/ASSEMBLY_DECISIONS.md` and `shots/assembly_decisions.json`.
Both motion assemblers now enforce this registry through `assembly_sources.py`.
Clean silent 1080p delivery: `out/screen_sync_scope_rail_clean/dual.mp4`.
Existing generated-take assignments and lip-sync files are untouched; protected
source selection wins at render time. Missing media or changed timing fails
clearly. Full-film rebuild remains pending; stills/overlay-only modes unchanged.

Latest review: `out/screen_sync_scope_rail/dual.mp4`: owner-approved scope
push-in direction with subtle lateral/vertical sway, tiny roll and uneven
travel to soften the perfect digital move. All signal/light settings retained.
Owner approved; clean push-in preserved and full animatic unchanged.

Previous review: `out/screen_sync_scope_pushin/dual.mp4`: a scope-centred push-in
with a gentle beam-intensity build, retaining 30% guitar and existing amplitudes.
Procedural trace resolution increased for close-up. This may replace generated
console footage after review; no substitution made yet. No handles in this
69-frame look test. Exit-only handles are the adopted default for production;
see `docs/CONTINUOUS_COVERAGE_PLAN.md`. Existing source sync mappings unchanged.

Previous review: `out/screen_sync_guitar_blend_30pct/dual.mp4` (new-only, 30% guitar).
Owner liked the 15% guitar blend and requested doubling its deflection gain to
30%. All other processing is unchanged; 15% preview preserved. Review pending.

Previous review: `out/screen_sync_guitar_blend/dual.mp4` (new-only, GUITAR BLEND).
Amber combines bass with a fixed 15% normalized guitar deflection; cyan remains
bass-only. Guitar uses its saved song offset and a 90–900 Hz band. The analog 2
texture is retained. Awaiting review; soundtrack and full animatic unchanged.

Previous refinement: `out/screen_sync_rosette_analog2/dual.mp4` (new-only preview),
labelled ROSETTE ANALOG 2. Owner approved analog 1 and requested a slightly
stronger, wandering noise floor with sparse soft visual pops/crackles. Rendered
as a separate local test; soundtrack and full animatic unchanged. Review pending.

Previous refinement: `out/screen_sync_rosette_analog/dual.mp4` (new-only preview).
Owner approved the rosette; this pass adds stronger centre magnification, faint
signal noise in silence, and a subtle 95–100% travelling beam brightness envelope.
Approved; full animatic unchanged. Show the standalone new clip first.

Previous screen-effect review: `out/screen_sync_rosette/comparison.mp4`, comparing
the prior defocused cyan line with an outward-expanding cyan bass rosette while
amber stays horizontal. This is a local still-plate test only, not applied to
the full edit. Cyan previously used drum body; this version uses rectified,
approximately period-locked bass. Details and reproduction are in
`docs/SCREEN_SYNC_PILOT.md`. Rosette shape approved; previous outputs preserved.

The storyboard image pass is complete enough to pause. The owner has reviewed
and approved one still for every setup: **41 / 41 selections**, serving **59
timed cuts**. The tracked decision snapshot is
[`shots/still_favorites.md`](../shots/still_favorites.md). The actual JPEGs,
source audio, and rendered animatics remain local and OneDrive-backed; Git
intentionally ignores them.

The latest Blender animatic completed with 59 stills, zero placeholder slates,
24 fps stereo audio, and a duration of 199.253 seconds. Local review files:

- `out/blender_animatic_v6_regen_fav.mp4` — 1280×720 review master
- `out/blender_animatic_v6_regen_fav_small.mp4` — 960×540 sharing copy
- `out/blender_animatic_v6_regen_fav_contact.jpg` — six-scene QA sheet

The approved image set includes the targeted revisions made on 2026-09-04:

| Setup | Approved | Revised direction now present |
|---|:---:|---|
| `signal_crossing_space` | A | A glowing probe carries the signal between worlds; no people. |
| `mars_night_wide` | B | A genuinely dark, star-rich Mars night with one luminous fauna element. |
| `counterfeit_parade` | B | Curios displayed in a tourist-shop window instead of an isolated conveyor. |
| `rain_to_canal` | A | An underground spring bubbles up near the woman, with spring-habitat fauna. |
| `duet_lamplight_astronomer_sync` | B | A weary end-of-day beat beside a period-futurist television; pinned hair is restored, though the pencil is not clearly visible. |
| `duet_lamplight_astronaut_sync` | B | Darker exterior and dim evening interior, with small practical lights. |

### Full flat-shape lyric animatic v04 rendered and reviewed

The approved flat Fredoka treatment now covers the complete song: 87 lyric
lines and 305 individually animated words across all 4,782 frames. The current
local review file is `out/blender_animatic_flat_lyrics_v04.mp4`: 1280×720,
24 fps, 199.25 seconds, 59 selected-still cuts, and continuous master audio.
The text has no backing rectangle or visible 3D treatment. Scene-aware color
eases over 12 frames at cuts and switches to a dark fill for unusually bright
lyric zones. Normal lines now clear four frames before the next onset; the five
registered counter-vocal overlaps remain on two baselines. The active word
turns warm white and gains a tight glyph-shaped charcoal contrast silhouette.
The approved v03 treatment scales the entire typography system to 66% while
leaving the baseline fixed. A conservative local Whisper comparison also
pulled 80 late words earlier across 30 fully matched later-song phrases; no word
was moved later and the first six hand-timed phrases were preserved. Every
change is recorded in `shots/lyric_alignment_report.md`.

This typography review is explicitly stills-only. The renderer now defaults to
the 41 approved selections, so ignored motion clips that appear on disk do not
silently change the reviewed 59-cut picture edit. Motion clips are included
only when a future render deliberately passes `--allow-clips`.

### Lyric-locked picture timing v04 — approved

Four owner-approved picture changes are now locked to the refined lyric frames:

| Frame | Time | Lyric onset | Picture entering |
|---:|---:|---|---|
| 2881 | 2:00.042 | “Things clap overhead” | Rockets descending from orbit |
| 2928 | 2:02.000 | “like rockets coming in” | Rockets landing at the colony |
| 3165 | 2:11.875 | “Elsewhere, under a smaller moon” | The astronaut at the underground spring |
| 3229 | 2:14.542 | “Chrome-plated bodies” | First merfolk formation in the lagoon |

The landing composition deliberately holds through the intervening instrumental
space and “Can’t tell you / if they’re true.” Repeated bar-length EDL entries
reuse that same setup, so they create no visible picture change. The tracked
overrides in `shots/plan.json` survive `tools/shotplan.py --merge`, and the
current passage review is `out/shot_timing_review_v04.mp4`. The owner approved
this passage on 2026-09-05 as “a lot better.” The full v04 movie incorporates
all four changes. It was rendered and reviewed across the complete song on
2026-09-05: 4,782 video frames at 24 fps, 199.250 seconds of picture, 199.241
seconds of AAC audio, and no missing-image slates or accidental black sections.
The four review contact sheets are local under `out/animatic_v04_review_*.jpg`.

Next: review the proposed dialogue-led outro and continuous source coverage in
[CONTINUOUS_COVERAGE_PLAN.md](CONTINUOUS_COVERAGE_PLAN.md). The draft follows
speaker turns with fourteen performance views drawn from six overlapping
eight-second takes. Its exact cut timing is proposed, not applied to v04.

The owner has adopted whole-film refinement passes: rough out the timeline,
carry lessons into new sections, then return to earlier weaknesses. Existing
animation and lip-sync tests are useful and replaceable; keep their files for
comparison. Claude is separately preparing motion and lip-sync footage. This
coverage plan is the shared handoff for future orders; current assignments
should be checked before merging any revised cut.

The DAW effects direction remains in
[DAW_VISUALIZATION_OVERLAY_PLAN.md](DAW_VISUALIZATION_OVERLAY_PLAN.md).
Latest effects direction: test one bass-driven replacement of the opening
oscilloscope display, as specified in [SCREEN_SYNC_PILOT.md](SCREEN_SYNC_PILOT.md).
The multi-effect river chorus is a later integration study. The first screen
test is now `out/screen_sync_pilot/comparison.mp4`: a 17.25-second comparison
of the original pattern, an amber bass replacement, and a cyan bass overlay
over the dimmed original. All use the approved still with a slight shared
camera move. The owner selected complete replacement. The follow-up comparison
is `out/screen_sync_refined/comparison.mp4`: reference-derived screen texture,
varying beam width, and 2x spatial supersampling, compared with the first
replacement. Actual moving-footage tracking is still untested.

Latest screen review: `out/screen_sync_phosphor/comparison.mp4` compares the
previous replacement, a new amber trace with beam-speed-dependent intensity
and accumulated phosphor decay, and an optional amber-bass/cyan-drums pair.
The two-channel option uses near-horizontal axes with slow relative drift.
Glass dirt and peripheral calibration are included. Owner preference between
the latest variations is pending; the underlying complete-replacement choice
remains accepted.

Owner approved the persistence/beam weighting and liked amber with cyan, then
requested fixed amber, wider cyan axis motion, more amplitude, center emphasis,
and cyan defocus that spreads its energy. Latest review is
`out/screen_sync_depth/comparison.mp4`, previous versus revised dual-channel
twice. The earlier tests remain local for comparison; this revision awaits
owner review of its new focus/motion balance.

The latest plan is authoritative; generated clips may be replaced or reused
as spare material. The shared repository records saved decisions and assets,
not a live registry of another agent's in-flight generation jobs. At assembly,
reconcile the current shot list, coverage proposal, saved takes, and sync
origins. Keep proposed/tested/accepted/applied states distinct: a new plan is
not evidence that an older render already implements it.

Editable full-song choreography is tracked in
`shots/lyric_motion_full.json`. Heard word-timing corrections can be marked in
`shots/lyric_timing_review_full.md`. The first six hand-authored pilot phrases
are preserved; later word attacks are provisional until checked by ear. See
`docs/LYRIC_MOTION_FULL.md` for motion grammar, rendering, and review guidance.

## Timing remains editable

The selected stills define compositions and future start/reference frames;
they do **not** bake in shot duration. Timing remains an editable 24 fps cut:

- `shots/shotlist.json` is the downstream source of truth for every frame edge.
- `shots/plan.json` contains the section-level cutting rules and setup order.
- `shots/setups.json` contains reusable setup descriptions and motion intent.
- Re-plan with `tools/shotplan.py --merge --setups shots/setups.json` so
  hand-authored prompts and clip assignments survive.
- Re-render the animatic after any timing change. A cut can be advanced,
  delayed, shortened, or lengthened before generated motion or lip sync is
  committed.

For broad rhythmic changes, edit the bar/beat rules in `shots/plan.json`. For a
specific editorial adjustment, record the desired frame edge in the shot list
and then keep the planning source in agreement. Generated video can be longer
than its cut: `clip.in_sec` and `clip.speed` in the shot list choose the useful
portion without regenerating a shot.

The production order now follows broad passes across the film:

1. Review changed passages in a free animatic and map source coverage across
   the timeline, including cutaways and later returns.
2. Assemble a first motion pass with one candidate per source window and
   adequate existing tests. Log problems and advance to other sections.
3. Sync usable performance coverage and check speaker ownership, listening
   gaps, individual in-points, and continuity across the whole song.
4. Apply lessons from later sections to selected earlier weaknesses in a
   refinement pass; do not repeatedly polish a single short passage.
5. Review/test the DAW effects plan, extend the successful treatment, then
   review the full composite before finishing.

## Reproducing the current animatic

With the ignored local images and audio present:

```powershell
python tools/blender_comp.py --proxy `
  --out out/blender_animatic_v6_regen_fav.mp4 `
  --favorites shots/still_favorites.md `
  --variant-order p,q,n,m,f,e,d,c,b,a
```

The favorites resolver supports both the reviewer's ignored
`codex/out/still_favorites.md` and the tracked
`shots/still_favorites.md`. The latter is the durable Git-backed record.

## What Git should contain

Commit and push the planning JSON, prompt/style sources, compact manifests,
review decisions, documentation, and pipeline code. Do not add paid/generated
stills, audio, video clips, Blender renders, contact sheets, or API keys. The
repository's `.gitignore` already enforces that separation.
