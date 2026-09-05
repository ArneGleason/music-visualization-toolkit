# Rivers of Mars live-action production status

Pause point: 2026-09-05

## Current state

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
