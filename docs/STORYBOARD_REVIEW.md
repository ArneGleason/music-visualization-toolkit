# Storyboard pass — review notes (2026-09-01)

All 37 first-pass setups were generated as stills in Flow (Nano Banana 2,
16:9, x2 variants, 0 credits each), one prompt per setup = shot body + lock
block, with the matching Character, board, or canal vista attached. Files
land in `board/frames/<setup>_<variant>.jpg`; `tools/board_contact.py`
builds `board/contact.html` from them. Ids are harvested from the Flow media
grid (only while the Chrome window renders — the grid is virtualized; Chrome
must run with `--disable-backgrounding-occluded-windows
--disable-renderer-backgrounding` or a covered/blanked window freezes),
resolved to signed CDN URLs (`flow-content.google/image/<id>?Expires…`) via
the `media.getMediaUrlRedirect` endpoint, and pulled with curl.

## Owner review of the first pass → v2 decisions

The owner reviewed the full grid in Flow. Each note, and what changed in
`shots/style.md`, `shots/setups.json` and `shots/plan.json` because of it:

1. **The twins get mixed up** (the astronaut wearing the astronomer's
   glasses). Glasses are removed from the film entirely; the twins are told
   apart by **hair** (astronaut: bob down; astronomer: the same hair pinned
   up in a French twist) and wardrobe. The astronomer Flow Character is
   rebuilt to the new spec; one Character per shot, one twin per agent
   session. Cast descriptions are substituted verbatim from `style.md`
   (`{{astronaut}}`, `{{astronomer}}`) so no prompt paraphrases them.
2. **No continuity of style** — handsome photographic prop/miniature frames
   next to illustration-style ones. The lock block now says "photographed on
   35mm three-strip Technicolor … never an illustration, painting, cartoon
   or render"; every still prompt leads with "Film still."; a style anchor
   is attached to every generation; v2 stills use Nano Banana Pro. The
   owner's question — switch to ChatGPT's image generator? — is answered by
   an A/B on four problem setups (twin close-up, water ballet, mer-folk,
   forest walk) before committing the rest of the pass either way.
3. **The silver suit changes from scene to scene.** Two fixes: one
   canonical suit sentence (`{{suit}}`) pasted verbatim into every astronaut
   prompt with a suit turnaround board attached, and — the owner's second
   note — the suit itself **simplified** until there is almost nothing to
   drift: a plain smooth silver one-piece, one riveted collar ring, silver
   gloves and boots, nothing else (the red straps, backpack, medallion and
   belt of the reference image are gone). Variants add exactly one thing:
   a hand lantern (canal forest), a glass helmet (landing field), or remove
   the collar ring (bunk, outro).
4. **Water numbers crowded into narrow canals, illustration-ish.** New
   location: the colony's circular **canal basin** — open water big enough
   for a Busby Berkeley number. New setups `basin_moon_descent`,
   `basin_edge_sync`, `basin_kaleidoscope_top` (the overhead flower),
   `merfolk_surface_ring`, `drumwall_basin`; the plunge and junction stay.
5. **No psychedelic garden.** The greenhouse aisle is replaced by the
   **canal forest**: `forest_threshold` (hatch opens onto it),
   `forest_walk_track` (she walks through lush oversized foliage following
   the little green light, lateral track), `forest_awakening_frontal` (the
   forest lights up around her on the drums); the thistle-globe macro stays.
6. **The creature.** One fish-lizard becomes the **canal mer-folk**: a
   chrome school of twelve or more — fish tail, slender humanoid arms, a
   smooth alien head with one large lashed eye and a tiny singing mouth —
   always moving in unison. A design sheet is generated before any water
   setup is redone.
7. **Arrivals come from orbit.** `signal_crossing_space` now ends over the
   limb of Lowell's canal-scored Mars seen from orbit; `rockets_overhead` is
   replaced by `orbit_rockets_descent` (rockets sinking toward the globe)
   and `rockets_landing_wide` (touchdown on the landing field, the astronaut
   in her orbital suit); the rocket section cuts every bar so "Things clap
   overhead" lands on the descent and "like rockets coming in" on the
   landing.
8. **The performer's body.** The owner re-cast the twins with a
   **ballerina's build and a dancer's carriage** — slender, long-necked,
   upright, shoulders back, chin lifted, stillness held with intention and
   movement landing on the beat. It is in both cast lines, and both Flow
   Characters are rebuilt to it before any v2 still.

9. **Rivers, not canals** (owner, after the video tests). The straight
   engineered channels and their brass gates read as plumbing; the film is
   *Rivers of Mars*. Every waterway is now a winding natural river with the
   settlements grown up along its banks; the "basin" is the river's wide
   mirror-calm **lagoon** below the colony (setup names keep `basin` and
   `canal_*`; the text is all river); `canal_junction_turn` is now the great
   eddy where the river enters the lagoon, no gates. The lock block says
   "winding natural rivers of blue-green water with settlements built up
   along their banks".
10. **No little spacemen.** The cast is the two twins and the chrome
    mer-folk, nobody else. Witness figures are gone from every setup, water
    scenes are populated by the mer-folk only, and the lock block now ends
    the wardrobe line with "the only figures that ever appear are the two
    twin sisters and the chrome mer-folk; no other people, no extras, no
    spacemen."
11. **The music has to show.** The owner's read of the video tests: the
    shots are interesting but on their own will not convey the music; the
    beat-locked overlay pass (plan section 7b — the vector engine's
    register-driven elements composited over the footage) is what makes it
    a music video. It moves up the order: build the overlay renderer and
    judge it on the animatic before volume generation.

12. **Shot language.** Every setup now carries two or three IDs from the
    cinematographic metaphor catalog (`conventions` in `setups.json`);
    `shots/conventions.json` phrases each ID for a photographed film and
    the prompts append them (framing on the still, camera-and-motion on the
    video). Direction notes can now name the device instead of describing
    it.
13. **Fauna in the garden.** Four practical-creature setups cut in among the
    flora (lantern-moth, phonograph snail, chrome hummingbird-things,
    lantern-eyes in the leaves); no consistency needed, a different creature
    per cut. The mer-folk are the one creature that must stay consistent:
    next browser task is to make them a Flow Character from the design
    still so they can be attached like the twins.
14. **Velocity by cut density.** The garden and the chorus now cut every bar
    (2.8 s) instead of every two; adjacent identical setups are a single
    continuous clip across two cuts. 59 cuts, 41 setups.

Net (v2.2): 59 cuts, 41 setups (was 47 / 37). The plan is now authored at the setup
level in `shots/setups.json` (`still` = the frame, `motion` = the video
sentence) and applied with `tools/shotplan.py --setups shots/setups.json`.

### v2 order of work

1. Sheets first, all free: rebuild the astronomer Character; generate the
   suit turnaround, the mer-folk design sheet, and the basin / forest / orbit
   boards; register them in `style.md`.
2. The A/B (Flow Nano Banana Pro vs ChatGPT) on the four problem setups;
   pick the generator for stills.
3. Regenerate every changed or rejected setup with the guards; keep the
   first-pass keepers listed below.
4. Contact sheet → owner batch review → animatic → video inside the Ultra
   window (ends 2026-09-07).

## The v2.2 pass (2026-09-03): all 39 setups in the cut, regenerated

Nano Banana Pro, x2, the v3 Characters attached on every twin shot, the
river/lagoon world, "no people" on every non-twin still, the catalog's
framing phrases appended. 78 stills, filed as `_m`/`_n` variants in
`board/frames/` (originals in `board/v4/`, rejects in `board/rejects/`).
The pass holds: winding rivers and the lagoon everywhere, the mer-folk
school consistent across nine water setups, the v3 face across 24 twin
stills, the four fauna setups reading as practical creatures. Rejects:
one mer-folk ring that drew a caption ("THE CHROME MER-FOLK EMERGE"), one
observatory dome with two spacemen and a "MARS" sign, and the first
console attempt that seated two space-suited women at the console before
"nobody at the console" was added. Watch items: the bunk-lamplight astronaut
drifts older in one variant; the night-wide astronaut is dusk in one and
day in the other; the astronomer's desk keeps putting an empty spacesuit
and helmet behind her (charming, but decide). Next: owner batch review on
the Blender animatic, then Frames-to-Video from the approved variants.

## Owner review of the v2.2 pass (2026-09-03)

Concept approved; consistency is the open problem: face drifts between
shots, some stills slip into illustration, the mer-folk vary. Decisions:

- **Likeness locked** to the moonlit lagoon close-up
  (`refs/astronaut_likeness.jpg`, media db9e4b1e); v4 Characters built from
  it; attached as an ingredient on every twin still.
- **Mer-folk** get a Flow Character of their own and "exactly one eye" in
  the cast line.
- **Photographic anchor** attached on every non-twin still to stop
  illustration drift.
- **Story:** the astronomer is an exobiologist; the "pieces" are fragments
  of an alien specimen with a helical, DNA-like structure (not maps), and
  the strange organic shape she holds (`refs/specimen_ref.jpg`, media
  4d6510c1) is the same organism.

On the tool question: Flow's Characters do most of the identity work and
Veo keeps a start frame's identity through a clip, so the fix is procedure
(references attached, anchors attached, pick from x2/x4) before it is a
different generator; ChatGPT stays the fixer for single stills.

## Lock comparison, Flow vs ChatGPT (2026-09-03)

Four setups regenerated in both generators with the locked likeness
attached (`refs/astronaut_likeness.jpg` on the twin shots,
`refs/merfolk_likeness.jpg` on the ring); Flow also had the `Astronaut v3`
Character attached. Sheet: `board/v5/lock_compare.jpg` (reference, Flow A,
Flow B, ChatGPT per row); sources in `board/v5/`.

| setup | Flow (Character + photo) | ChatGPT (photo) |
|---|---|---|
| astronaut_close_sync | same face in both variants; near-identical to the reference | same face; slightly rounder cheek, otherwise a match |
| astronaut_inspect_medium | same face; A holds the helical specimen (keeper), B a limp membrane | same face; specimen reads as a glowing helix; environment is lusher, more painted |
| mars_night_wide | same face at a distance; honors the lock's striped gas planet and small moons; lantern post and winding river — usable as is | face holds; drops the gas planet; matte-painting look, but the winding river with settlements on its banks is the better reading of the world |
| merfolk_surface_ring | practically a re-print of the reference (identical school, one eye) | one eye held, but the tails are gone and the ring became a splashing crowd |

**Verdict.** The lock comes from the attached likeness photograph, not
from the generator: with it attached, both tools hold the face across a
close-up, a medium and a wide. Flow stays primary (free stills, the
Character, and the still goes straight to Veo as a start frame); ChatGPT
stays the fixer, and is the stronger choice when a wide environment
matters more than the figure. Consequences for the regen pass:

- Every twin still: Character + `astronaut_likeness.jpg` attached, x2, pick.
- Every mer-folk still: `merfolk_likeness.jpg` attached; the school is
  now a fixed prop, so vary the framing, not the creatures.
- Flow follows the lock block more literally (the gas planet, the
  backdrop); ChatGPT follows the prose and the photo. Keep the lock block
  as the contract and write ChatGPT prompts from it, not freehand.
- Build the v4 Characters from the likeness (astronaut, astronomer twin,
  mer-folk) so the photo can be dropped from prompts that are short of
  ingredient slots.

## The v6 pass, both generators (2026-09-03)

All 41 setups regenerated twice from the same manifest
(`codex/stills_manifest.json`, prompts verbatim, likeness / mer-folk /
specimen / world-anchor photos attached per entry): Codex desktop on the
OpenAI image model (`gpt-image-2`, 82 images, one guard failure) into
`codex/out/`, and Flow / Nano Banana Pro x2 (84 images, the basin edge
sent twice) into `board/v6flow/`. Side-by-side sheets:
`board/v6_compare/v6_compare_1..6.jpg`.

**Verdict: the Codex pass is the storyboard.** Both hold the face, but:

- **Night is night in Codex.** Flow turned most "Night." prompts into
  mint-green daylight (mars_night_wide, basin_moon_descent,
  colony_goodnight_cascade, night_iris_title) because the attached world
  anchor is a daylight-looking plate; the anchor overrode the prompt.
- **Cast discipline.** Flow put spacemen, helmets and extra figures into
  non-character shots (obs_dome_open, forest_fauna_moth, rain_to_canal,
  interference_bloom, chorus_plunge, basin_edge_sync). Codex broke the
  rule once (signal_crossing_space: twins and mer-folk in a group shot).
- **Mer-folk.** Codex keeps the tails, the single eye and the identical
  school in every water setup; Flow's school drifts toward drawn fish
  (canal_junction_turn, basin_kaleidoscope_top).
- **Illustration drift.** Flow slips into painted looks on forest_fauna_eyes,
  rain_to_canal, canal_junction_turn; Codex stays photographic throughout.
- **Flow alternates worth keeping:** telescope_time_tunnel A,
  duet_lamplight_astronaut_sync A/B, obs_console_macro A, forest_threshold
  A/B. Everything else is a Codex keeper by default.

**Regen list (Codex, single stills):** signal_crossing_space (no people:
the gold pulse over the globe only), chorus_plunge B (apparatus in frame),
basin_edge_sync (bring the mer-folk ring up beside her).

Those three were re-run as single stills in ChatGPT (same prompts, the
photos attached in the chat; `board/v6_compare/fix_sheet.jpg`):
signal_crossing_space now has no people (the gold pulse between globes;
several Mars globes, so still a "usable, not final"), chorus_plunge got the
clean overhead with a tail crossing the lens (keeper, staged as
`chorus_plunge_r`), basin_edge_sync got one mer-folk beside her at the
water's edge (alternate, staged as `basin_edge_sync_r`).

The Codex pass is staged in `board/frames/` as variants `_p`/`_q`
(contact sheet rebuilt, 41/41), and the Blender animatic was re-rendered
with them on top: `out/blender_animatic_v6.mp4` (540p copy sent).

**Owner's A/B picks** live in `codex/out/still_favorites.md` (41/41
reviewed, written by Codex's review tool). `tools/blender_comp.py
--favorites codex/out/still_favorites.md` uses that file per setup ahead of
the variant order. The letterbox bars are now opt-in (`--letterbox`): on a
16:9 still they covered the top 13% of the frame, which took the heads off
the standing shots. The full frame is shown by default.

## Approved stills and pause point (2026-09-04)

The owner completed a second A/B review after six targeted regenerations. All
41 setups now have an approved favorite, recorded in the tracked
`shots/still_favorites.md`; generated JPEGs remain local under `codex/out/`.
The updated favorites animatic is
`out/blender_animatic_v6_regen_fav.mp4` (59 still cuts, zero slates, 199.253 s),
with a 540p sharing copy beside it. See `docs/PRODUCTION_STATUS.md` for the
current handoff, timing-edit workflow, and recommended order before lip sync.

**Procedure notes.** Flow's `+` picker: uploading two files at once lands
both in Recent but selects only one; upload one, Add, reopen, upload the
next, Add. Reloading the page clears the chips. The panel entries and the
grid tiles share `data-index`, which is how the harvest maps media ids back
to prompts (`scratchpad/flow6/map6b.py`).

## Chorus motion test (2026-09-04)

Approved set for the whole film: `shots/still_favorites.md` (41/41, tracked)
with the images under `codex/out/`. First sequence taken to motion: the
chorus, s039–s051 (129.0–166.0 s, 13 cuts, 8 setups). Each approved still
was uploaded to Flow and used as the Frames-to-Video start frame with the
setup's Video prompt, Veo 3.1 Quality, 720p, 8 s, x1 (100 credits each).

- First round: 6 of 8 clips animated from the wrong still, because
  selecting a picker option by script did not change the selection and
  "Add to prompt" re-added the previous frame. Only a real click on the
  option (then a check of the slot thumbnail) is reliable. ~600 credits
  lost; all 8 regenerated correctly.
- Owner spotted a second slip: `basin_kaleidoscope_top` had animated from
  a Flow-generated daylight still that the picker offered from Recent,
  not from the approved Codex night still. A first-frame check against
  `codex/out/` (mean pixel diff, `clips/v6/*_f0.jpg`) confirmed it: seven
  clips within 1.2 of their approved still, the kaleidoscope at 70.
  Regenerated from `basin_kaleidoscope_top_a.jpg`. Rule: after every
  Frames-to-Video request, diff the clip's first frame against the
  approved still before filing it.
- Clips in `clips/v6/<setup>.mp4`, filed as `clips/raw/<setup>_v6.mp4` and
  assigned to the 13 cuts with `tools/ingest.py` (adjacent identical
  setups run as one continuous clip via `in_sec`).
- `out/chorus_motion_v1.mp4`: the section cut in Blender from the clips,
  with beat pulse and captions, before lip sync.
- Lip sync: Kling (production sync tool per PHASE0) on the two sung
  setups, `chorus_close_sync` (s045–s046) and `basin_edge_sync`
  (s041–s042), driven by 8 s lead-vocal slices
  (`clips/inbox/chorus_close_vocal8.wav`, `basin_edge_vocal8.wav`) so the
  audio covers the whole clip. Both ran (10 credits each, free tier, one
  task at a time, KlingAI watermark bottom right): `clips/raw/
  chorus_close_sync_kling.mp4`, `basin_edge_sync_kling.mp4`, assigned to
  s045–s046 and s041–s042. `out/chorus_motion_v3_sync.mp4` is the chorus
  with the synced mouths under the master mix.
- Kling driving notes: the Lip Sync editor stalls at "Uploading video" while
  its tab is hidden; it needs the tab in front. Result cards only expose a
  Download button (browser download), so the clips come in through
  `~/Downloads`. The share icon next to it opens Publish, not download.

## Generator A/B, Flow side (2026-09-02)

Nano Banana Pro, 16:9, x2, the v2 Characters attached, "Film still." lead,
cast lines verbatim. Filed in `board/v2/` and copied into `board/frames/`
as the `_c`/`_d` variants (`_a`/`_b` for the brand-new kaleidoscope):

- **astronaut_close_sync** C/D: the pixie-nosed face and the plain suit hold
  exactly; singing mouth; both ignored "dark neutral backdrop" and put the
  colony behind her — fine as chorus-style close-ups, re-run with a board
  of the dark backdrop for the true neutral one.
- **forest_walk_track** C/D: lush canal forest, magenta canopy, hanging
  seed-lanterns, she walks side-on with the lantern and the green light
  ahead — exactly the psychedelic garden asked for; photographic.
- **basin_kaleidoscope_top** A/B: chrome mer-folk in concentric rings in
  the circular basin, fountains around the rim, moon at center — the Busby
  Berkeley geometry lands; A is the more kaleidoscopic.
- **merfolk_surface_ring** C/D: the school with the single lashed eye,
  tiny mouths and fanned tails, surfacing in open water — the creature
  redesign works on the first try; D (basin center, domes far) is the
  keeper layout.

Owner review of these: liked the lot except the face — first the nose
(pug → pixie, then the pixie came out with slit nostrils), then a request
for a different face altogether. **v3 face** (Claude's pick, owner to
confirm): heart-shaped, high cheekbones, large wide-set hazel-green eyes,
small straight nose, full mouth, light freckles. Both Characters were
rebuilt as `Astronaut v3 (Them 2)` / `Astronomer v3 (Them 1)`; the twin
sheet held the face across the tweed/updo change on the first try. The
astronaut A/B stills were re-run with v3 (`_e`/`_f` in `board/v3/` and
`board/frames/`): close-ups now on the dark neutral backdrop with the new
face and plain suit, photographic; forest walks with lantern and green
light, face consistent. v3 is the production cast unless the owner says
otherwise.

Verdict so far: with the plain suit, verbatim cast lines and Nano Banana
Pro, Flow holds identity and style well enough that switching generators
is not needed on this evidence.

**ChatGPT side** (one close-up, reference photo attached, same prompt):
a genuinely handsome photographic close-up that obeyed the "soft dark
neutral backdrop" Flow ignored, with the face close to the reference.
So: prompt adherence and style are at least as good; what ChatGPT lacks is
the reusable Character, the free x2 volume, and the direct hand-off to
Frames-to-Video. **Decision: Flow (Nano Banana Pro + v3 Characters) for
the pass; ChatGPT as the fixer for individual stills Flow will not obey
(upload the result into Flow as a start frame).**

## Video tests (2026-09-02)

Frames-to-Video, Veo 3.1 Quality, 8 s, x2, start frame = the labeled still
uploaded straight into the composer's asset picker (its hidden file input
accepts a local file, so the exact variant is used).

- **counterfeit_parade** (from A): both takes play the hidden-conveyor gag
  with the procession gliding left to right. Take 1 (`clips/inbox/
  test_parade_1.mp4`): she holds still, deadpan, objects keep their shapes —
  the keeper. Take 2: she turns to watch and the objects drift (masks vanish,
  globes multiply). Lesson: name the objects again in the motion sentence and
  say "each object keeps its shape" — Veo re-invents props that only the
  frame defines. The other four (specimen table from A, weather from B, canal
  junction from A, colony vista from A) were submitted the same way on
  2026-09-02 evening, two takes each (`clips/inbox/test_*.mp4`).
- **specimen_table_macro**: both takes are keepers — the silver-gloved
  hands lift a map fragment and try it around the circle, deliberate, and
  every pod, globe and fragment keeps its shape (the "every object keeps its
  exact shape" line earned its place). Hands-and-props macros are a safe
  category.
- **mars_domes_wide**: take 2 is a clean slow push up the canal axis with
  nothing invented — the keeper, and proof the vista category is easy.
  Take 1 added two large silver-suited witnesses in the foreground that the
  still never had — Veo's own "uninvited witness" habit; say "no people"
  in the motion sentence too.
- **weather_over_colony**: both takes turned the luminous filaments into
  lightning bolts and grew the two tiny figures into foreground astronauts.
  Reject. The phrase "glowing threads" reads as lightning to Veo; rewrite
  as "slow silk-like streamers of pastel light, no lightning, no flashes",
  and drop the figures from this setup.
- **canal_junction_turn**: both takes animate the brass gates and churn the
  current with the swimmers wheeling; mechanism reads. The swimmers are the
  v1 silver-suited humans from the old still — redo from a mer-folk still
  before it counts.
- Lessons so far: Veo respects the frame but invents people and reads
  "glowing" as electrical. Every environment motion sentence now ends with
  "no people" and names what must not appear.

## Systematic findings from the first pass (feed the regen pass)

- **Astronaut gets the astronomer's glasses.** Seen in astronaut_close
  (one variant), excavation (one variant), and both lamplight-astronaut
  variants. Twin bleed via the agent's conversation context. Resolved by
  decision 1 above (no glasses in the film).
- **Day where night was asked** (mars_night_wide, colony_goodnight A,
  drumwall A). The attached daytime canal vista biases the light. Guard: for
  night setups attach a night board (make one) or nothing, and lead the
  prompt with "Night."
- **Text leakage**: telescope_time_tunnel A rendered "SLOW PUSH IN" labels.
  Camera-direction phrases in the body can be drawn as annotations; the
  setup library now separates `still` (no motion words) from `motion`.
- **Uninvited witness figures**: environment setups (greenhouse, drumwall,
  weather, iris, goodnight) keep adding two silver-suited men, sometimes with
  horns/saxophones. Sometimes charming (drumwall B), sometimes wrong. Guard:
  "no people" on pure environment stills; witnesses only where the setup
  names them.
- **Triptych/strip layouts** on continuous-move setups (chorus_plunge A)
  — reject; "single frame, no panels" is now in the still text.
- **Agent context contamination**: one stray desk-lamp astronaut still
  appeared inside another setup's request. Long agent sessions drift; start
  a new session per batch of ~10 setups.

## Per-setup verdicts

All 76 first-pass stills are downloaded and labeled in `board/frames/`
(`board/contact.html` shows 37 of the 39 v2 setups; only the two brand-new
setups, `basin_kaleidoscope_top` and `rockets_landing_wide`, have nothing
yet). The four boards now live in `refs/` too (`world_observatory`,
`world_greenhouse`, `world_canal_colony`, `palette`). Stills of setups
renamed in v2 are filed under the new names; "superseded" means the setup
was redesigned by the owner's notes and the still is reference only.

**Keepers as they stand** (usable as Frames-to-Video start frames now):
obs_dome_open A (night dome, photographic), obs_console_macro A/B,
canal_map_macro A/B, interference_bloom A/B, receiver_dial_macro A/B,
specimen_table_macro A/B, mars_domes_wide A (B has witnesses),
counterfeit_parade A/B, excavation_site A, astronaut_inspect_medium A,
astronaut_mars_medium A, weather_over_colony A/B, flora_detail_macro A/B,
canal_junction_turn A/B, chorus_plunge B, drumwall_basin B,
colony_goodnight_cascade B, telescope_time_tunnel B, night_iris_title A/B,
chorus_close_sync C/D (the Phase 0 "singing on Mars" night stills — no
eyewear, correct suit).

| setup | verdict |
|---|---|
| obs_dome_open | A only (one variant survived): night hillside dome, blade of light — excellent |
| obs_console_macro | A/B both excellent brass consoles with waveform |
| astronomer_desk_sync | A/B good desk compositions (B hangs spacesuits behind her — a nice Anderson beat, keep as an option); regen for the new hair, no eyewear |
| canal_map_macro | A/B both excellent overhead map pieces |
| astronomer_close_sync | A good (warm backdrop); B is the astronaut in a silver suit with eyewear — twin bleed, reject |
| signal_crossing_space | A (gold beam onto a console) and B (dollhouse observatory) both misread the shot — reject; superseded by the orbit version |
| receiver_dial_macro | A/B both good; A's porthole with the striped planet is the keeper |
| astronaut_close_sync | A (dark backdrop, singing) is the ideal composition but wears eyewear; B same — regen |
| mars_night_wide | A/B both daytime — reject; regen with "Night." and no daytime board |
| interference_bloom | A/B both excellent leaf-on-cathode screens |
| forest_threshold (was greenhouse_threshold) | A: hatch opening onto lush green foliage — the closest thing to the lush garden the owner wants, keep as reference; B adds two witnesses — reject; superseded |
| forest_walk_track (was greenhouse_dolly_wide) | A/B nursery aisles with witnesses — superseded by the canal forest |
| flora_detail_macro | A/B both good thistle-globe macros; B more graphic |
| forest_awakening_frontal (was greenhouse_drum_awakening) | A/B greenhouse aisles with a green lamp — superseded |
| specimen_table_macro | A/B both excellent overhead mandalas |
| astronaut_inspect_medium | A good (no eyewear, field table); B eyewear — reject |
| mars_domes_wide | A excellent, empty vista; B has two tiny witnesses — usable |
| astronaut_mars_medium | A usable (frontal among canals); B eyewear, turned pose — reject |
| counterfeit_parade | A/B both excellent deadpan conveyors of masks, domes, globes |
| excavation_site | A good (no eyewear); B eyewear — reject |
| weather_over_colony | A/B both good filament weather; B more saturated |
| duet_call_response_sync | A/B both good split-screen twins, matching faces — keeper layout; regen for hair/no eyewear |
| orbit_rockets_descent (was rockets_overhead) | A illustration — reject; B photographic rockets-and-shadows — good but superseded by orbit + landing |
| rain_to_canal | A/B both add silver-suited figures — reject; regen "no people" |
| basin_moon_descent (was canal_moon_descent) | A drawn storyboard with text — reject; B one-point canal with floating swimmers — superseded by the basin |
| basin_edge_sync (was duet_canal_bank_sync) | A night with lamp and creature but her wardrobe drifts dark/tweed-like — check; B daytime — reject; both narrow canals, superseded |
| canal_current_macro | A/B illustration-style underwater cross-sections with suited swimmers — reject; regen with the mer-folk sheet |
| chorus_close_sync | A/B eyewear and daylight — reject; C/D (Phase 0 night stills) are the keepers |
| merfolk_surface_ring (was creature_swim_macro) | A cartoon eel, B chrome fish-lizard — the owner's "okay" creature; superseded by the mer-folk school |
| drumwall_basin (was drumwall_colony) | B (night fountains) excellent; A daytime jazz band — reject |
| chorus_plunge | B usable (splash + underwater cross-section); A triptych — reject |
| canal_junction_turn | A/B both excellent top-down brass junctions; keep, mer-folk added in video |
| duet_lamplight_astronomer_sync | B (desk lamp, colony painting) excellent — regen anyway for the new hair; A is just her portrait — reject |
| duet_lamplight_astronaut_sync | A, B, C all wear eyewear — regen; B's bunk/porthole composition is the keeper layout |
| telescope_time_tunnel | B good (stage apparatus); A text leak — reject |
| colony_goodnight_cascade | B (night, bridge figures) good; A is daytime — reject |
| night_iris_title | A and B both strong; A (moon over canal in iris) preferred |
