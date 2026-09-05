# Rivers of Mars live-action production status

Pause point: 2026-09-04

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

### Full flat-shape lyric animatic ready for review

The approved flat Fredoka treatment now covers the complete song: 87 lyric
lines and 305 individually animated words across all 4,782 frames. The current
local review file is `out/blender_animatic_flat_lyrics_v02.mp4`: 1280×720,
24 fps, 199.25 seconds, 59 selected-still cuts, and continuous master audio.
The text has no backing rectangle or visible 3D treatment. Scene-aware color
eases over 12 frames at cuts and switches to a dark fill for unusually bright
lyric zones. Normal lines now clear four frames before the next onset; the five
registered counter-vocal overlaps remain on two baselines. The active word
turns warm white and gains a tight glyph-shaped charcoal contrast silhouette.

A v03 excerpt is awaiting owner review at
`out/lyric_scale66_alignment_check_v03.mp4` (frames 900–1300). It scales the
entire typography system to 66% while leaving the baseline fixed. A
conservative local Whisper comparison also pulled 80 late words earlier across
30 fully matched later-song phrases; no word was moved later and the first six
hand-timed phrases were preserved. Every change is recorded in
`shots/lyric_alignment_report.md`.

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

This is the safe order from here:

1. Watch the current animatic and note any desired cut changes by timestamp or
   shot ID.
2. Adjust and re-render until the picture edit feels settled.
3. Generate motion clips from the approved stills, using first/last frames for
   transitions and beat-critical arrivals.
4. Ingest clips and refine in-points against the locked frame edges.
5. Run lip sync only on the frontal `_sync` performance shots after timing is
   stable.
6. Add the beat-locked overlay/compositing pass and review again before a final
   master.

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
