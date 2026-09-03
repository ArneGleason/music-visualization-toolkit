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

Net: 50 cuts, 39 setups (was 47 / 37). The plan is now authored at the setup
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
