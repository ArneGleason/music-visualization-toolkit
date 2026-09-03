# Style bible — Rivers of Mars, live-action generated path

Everything the image and video models need to keep ~40 setups looking like
one film. The lock block is appended verbatim to every prompt by
`tools/prompts.py`; the cast lines are substituted into prompts verbatim.

Direction: a **live-action** music video — a Wes Anderson quirky take on a
1950s Technicolor sci-fi take on a Percival Lowell take on the environment,
flora, and fauna of Mars. Not animation, not vectors: it should read as a
meticulously art-directed film shot on a soundstage Mars, with matte-painting
vistas, practical-looking sets, and deadpan performance.

## The record

Cyanite analysis of the master: **84 BPM, C# minor, 4/4, female vocal, high
energy**. Genre R&B 0.45 / Pop 0.31 — electro-pop with indie/art-rock/dark-pop
tags; "punchy and poignant, synths, electric guitar and rhythm." Mood:
energetic, sexy, uplifting. Character: confident, resolute, strong. Movement:
groovy, steady, driving, stomping. Instrumentation: percussion and synths
throughout, bass and electric guitar frequent.

Performance direction follows the record: **confident and punchy, never
gentle**. Words clearly articulated, eyes locked on the lens, heads steady
(the lip-sync pass needs stable faces), energy carried in delivery, shoulders,
and the world moving on the beat. The Anderson deadpan is self-assurance, not
softness. Reserve true quiet for the low-light outro, which the record
actually gives us.

## The look — one film, photographed

Every frame is a **photograph**: a frame from a 35mm three-strip Technicolor
feature — real actors on practical sets, painted backdrops, miniatures, glass
shots, coloured gels. Never an illustration, a painting, a cartoon, or a
render. The first storyboard pass drifted between handsome photographic
prop-and-miniature work and illustration styles (creatures, water numbers,
and forest were the usual offenders); the lock block now says "photographed"
outright, and every still prompt leads with "Film still." Attach a style
anchor (a Character, or a world board) to every generation — style drifts
most on prompts with nothing attached.

## The world

Lowell's Mars taken lovingly but not literally: the "canals" are **rivers**
- winding natural waterways of blue-green water cut through coral-red
terrain, never straight, never engineered - with cream-and-turquoise domed
settlements grown up along their banks, built around the water rather than
the water built for them. (Owner's note after the first pass: the straight
canals and their gates read as plumbing; the film is called *Rivers of
Mars*.) Also:
needle towers, spiked ornamental flora, a striped gas planet and several
moons in a mint-green sky. Every composition is planimetric and symmetrical or
a deliberate 90° angle off; props look hand-built; signage-free
retro-futurist hardware (brass telescopes, riveted silver suits, dial-covered
receivers). Four places the film keeps returning to:

- **The observatory** on Earth — brass telescope, dome slit, desk of river
  charts, bakelite console, warm tungsten pools in darkness.
- **The colony and its river lagoon** — below the domes the river widens
  into one great mirror-calm lagoon, a natural pool with a rocky coral shore,
  big enough to stage a water ballet; the colony's fountains stand along the
  shore. No gates, no locks, no channels. The chorus water numbers happen
  **here, in open water**, never crowded into a narrow channel. (Setup names
  still say `basin`; they mean this lagoon.)
- **The river forest** — Lowell's dark vegetation belt along the rivers,
  taken as a lush alien forest, and its **fauna**: hand-built practical
  creatures cut in among the flora - a lantern-moth, a phonograph snail,
  chrome hummingbird-things, lantern-eyes in the leaves. Unlike the twins
  and the mer-folk these need no consistency: a different creature every
  cut is the point. Lush alien forest: fern-fans the size of sails, giant cupped
  leaves, pink thistle-globes on tall stalks, hanging seed-lanterns, moss and
  mist; the canopy closes overhead and the light turns green and magenta. A
  small green light travels through it and she follows it. (This replaces
  the greenhouse aisle of the first pass, which read as a nursery, not a
  psychedelic garden.)
- **Orbit** — the film goes to space when things arrive: Mars from orbit as
    the film imagines it, a coral globe threaded with winding blue-green
  rivers and dark oases, the rockets seen descending toward it before they
  land.

## The characters

**The whole cast is the two twins and the chrome mer-folk. Nobody else.**
The first pass and the first video tests kept adding little helmeted
spacemen - witnesses at frame edges, men with horns, extras in the water -
and the owner has cut them entirely. Environment shots are empty of people;
water shots are populated by the mer-folk only; the lock block now says so.

Two performers carry the register's Them 1 / Them 2 dialogue: **identical
twin sisters** — same face, same auburn hair, same voice — split across two
planets, so every crosscut reads as one mind talking to itself. This mirrors
the record: both vocal parts and the backing vocals are one singer, so one
lip-sync source serves both twins (and backing vocals can appear as
additional reflections of her — canal water, dome glass — when a shot wants
them).

What tells them apart is **hair and wardrobe, nothing else**. The first pass
used glasses as the astronomer's marker and the generator sprinkled them onto
the astronaut in a third of her shots — an accessory is exactly the kind of
token that bleeds between prompts. Glasses are gone from the film, and the
word no longer appears in any prompt or Character bio.

- **Them 2 - the astronaut-botanist on Mars** (the canonical reference
  image, re-cast in build): a ballerina's build and a dancer's carriage -
  slender, long-necked, upright, shoulders back, chin lifted, every stance a
  held position. **The face (v3, 2026-09-02, re-cast at the owner's
  request):** heart-shaped, high cheekbones, large wide-set hazel-green
  eyes under arched brows, a small straight nose, a full expressive mouth,
  fair skin with light freckles. Auburn curly chin-length bob with straight
  bangs, always
  worn down; the silver suit below. Receiver of the signal; kneels by the
  canal, inspects specimens, unmasks Mars.
- **Them 1 - her twin, the astronomer on Earth**: the same face, the same
  build and carriage, the same auburn hair worn **up** - pinned in a loose
  1950s French twist with the same straight bangs and a pencil pushed
  through it, a few curls escaping by the outro. Rumpled rust-brown tweed
  jacket, mustard knit vest, collared check shirt. Sender of the pieces.

The dancer's body is also the performance note made physical: the record is
groovy, driving, stomping, and a dancer holds still with intention and moves
on the beat with precision. Deadpan from the neck up, choreography from the
neck down.

(Working choice, one line to change: the differentiator could equally be a
longer loose style. The rule is that *hair*, which the generator treats as
identity, carries the difference — never an accessory.)

Both exist as reusable **Flow Characters** (portrait + full body) in the Flow
project "Rivers of Mars - AI video": the current ones are **`Astronaut v3 (Them 2)`** and **`Astronomer v3
(Them 1)`** (built 2026-09-02: the v3 face, dancer's build, plain suit; the
astronomer with hair up and no eyewear). Every earlier Character (`Astronaut (Them 2)`, `Astronomer
(Them 1)`, the v2 pair) is superseded and must not be attached. Attach the
Character (not loose refs) on every shot of her, and only the one Character
the shot needs — attaching both, or asking for one twin in a session that
just drew the other, is how the bleed happened.

## Cast lines

Prompt bodies name the cast with `{{astronaut}}`, `{{astronomer}}`,
`{{merfolk}}` and the suits with `{{suit}}`, `{{suit_field}}`,
`{{suit_orbital}}`, `{{suit_liner}}`; `tools/prompts.py` substitutes the
lines below **verbatim** into every prompt, so a wardrobe or hair change is
one edit here and never a paraphrase there.

The suit is deliberately **plain**. The first pass described it richly
(quilting, red straps, backpack, medallion, belt) and every generation
re-invented some of it; each element was a chance to drift. One collar ring,
gloves, boots, smooth silver, nothing else - there is almost nothing left to
get wrong, and the grade and letterbox do the rest. Variants add exactly one
thing (a lantern, a helmet) or remove one (the collar ring).

- cast astronaut: the astronaut, a young woman with a ballerina's build - slender, long-necked, long-limbed - and a dancer's carriage, upright with shoulders back and chin lifted; a heart-shaped face with high cheekbones, large wide-set hazel-green eyes under arched brows, a small straight nose, a full expressive mouth, fair skin with light freckles; an auburn curly chin-length bob with straight bangs
- cast astronomer: the astronomer, the astronaut's identical twin sister - the same heart-shaped face, high cheekbones, large wide-set hazel-green eyes, small straight nose, full mouth and light freckles, the same ballerina's build and dancer's carriage, the same auburn hair pinned up in a loose 1950s French twist with straight bangs and a pencil pushed through it - in a rumpled rust-brown tweed jacket, mustard knit vest and collared check shirt
- cast suit: her silver suit: a plain, smooth, close-fitting one-piece brushed-silver spacesuit with a single wide riveted silver collar ring and matching silver gloves and boots, unadorned
- cast suit_field: her silver suit, carrying a small brass hand lantern
- cast suit_orbital: her silver suit with a clear domed glass helmet sealed to the collar ring
- cast suit_liner: her silver suit with the collar ring removed, a plain open neckline
- cast merfolk: the river mer-folk — a school of chrome-plated swimmers polished like 1950s hood ornaments, each with a long fish tail, slender humanoid arms, and a smooth bald alien head with stripped-down features: one large eye with long lashes, no nose, a tiny round mouth open in song — moving in unison

The suit variants are used only where the script goes somewhere: the field
suit in the canal forest, the orbital suit on the landing field as the
rockets come down, the liner in her bunk for the outro. Everywhere else it is
the surface suit, unchanged.

## Wardrobe and creature consistency

- Attach the astronaut Character (portrait + body) on every shot of her, plus
  the suit turnaround board (`refs/suit_turnaround.png`, front/side/back of
  the plain suit, plus the helmet and lantern variants) once it exists.
- The mer-folk get their own design sheet (`refs/merfolk_sheet.png`: one
  swimmer front, side, and a ring of six from above) and it is attached on
  every water setup. They are always a **school** — twelve or more — never a
  single creature, and they perform Busby Berkeley geometry: rings, spokes,
  fans, in unison, in open water.
- Character sheets and boards stay out of Git; drop files into `refs/` and
  register them below.

- ref character_master: refs/character_master.png
- ref astronaut_front: refs/astronaut_front.jpg
- ref astronaut_close: refs/astronaut_close.png
- ref astronaut_move: refs/astronaut_move.png
- ref astronomer_front: refs/astronomer_front.jpg
- ref astronomer_close: refs/astronomer_close.png
- ref suit_turnaround: refs/suit_turnaround.png
- ref merfolk_sheet: refs/merfolk_sheet.png
- ref palette: refs/palette.png
- ref mars_world: refs/Rivers-of-Mars.png
- ref world_basin: refs/world_basin.png
- ref world_forest: refs/world_forest.png
- ref world_orbit: refs/world_orbit.png

## The shot language

Every setup names two or three IDs from
`docs/CINEMATOGRAPHIC_METAPHOR_CATALOG.md` (`conventions` in
`shots/setups.json`): one spatial device, one performance device, one
material device. `shots/conventions.json` says each ID in camera-department
language for a photographed film, and `tools/prompts.py` appends the framing
phrases to the still prompt and the camera-and-motion phrases to the video
prompt. That is how the register's vocabulary reaches the generators, and how
a note like "more CAM-APPROACH here" becomes an addressable edit.

Cut density is a velocity control: the garden and the chorus cut every bar;
adjacent identical setups are one continuous clip across two cuts.

## Still-generation guards

Learned on the first storyboard pass (`docs/STORYBOARD_REVIEW.md`):

- Every still prompt leads with **"Film still."** and uses only the `still`
  text of the setup — camera-motion phrases in a still prompt get drawn as
  captions ("SLOW PUSH IN"). The motion sentence is added only for video.
- Night setups lead with **"Night."** and attach a night board or nothing;
  the daytime vista biases the light.
- Pure environment stills say **"no people"**; witnesses appear only where
  the setup names them.
- **"Single frame, no panels"** on continuous-move setups, or the model
  storyboards a triptych.
- One Character per shot, one twin per agent session, a fresh session every
  ~10 setups: the agent's chat context is what carried the astronomer's
  eyewear onto the astronaut.

## Framing and grade

Generate clean 16:9; the uniform post grade (`tools/render.py`) applies the
period look to every clip equally — warm Technicolor saturation, fine 35mm
grain, gentle halation, and a 2.39:1 letterbox. Compose center-weighted so the
letterbox crop never loses a face. The grade and letterbox are also the
drift-hiders: the model only has to be consistent underneath them.

## Sections

One line per register scene; setup names match `shots/plan.json`.

- **scene-01** — the observatory wakes: dome opens, oscilloscope traces the first signal.
- **signal-exchange** — the astronomer's warm plea; river-map pieces that almost fit.
- **scene-04** — the message crosses space and arrives over the limb of Mars, seen from orbit.
- **scene-05** — the astronaut waiting under the Martian night; scanning dials.
- **scene-06 / psychedelic-garden** — the garden hatch opens onto the river forest; she walks its path following the little green light; the forest wakes around her on the drums.
- **pattern-aperture** — specimen table, pattern tests, macro apertures.
- **mars-unmasking** — the reveal: domes wide, counterfeit parade, excavation.
- **semantic-rocket-weather** — filament weather over the colony, the twins' call-and-response, rockets descending from orbit and landing, rain becoming river.
- **rivers-of-mars** — the chorus in the river lagoon: moon descent, the mer-folk's water ballet from above, tiny mouths agape, sung close-ups, fountains on the drums, the plunge.
- **current-turns-home / low-light-outro / coda** — the current turns in the great eddy of the lagoon; lamplit duet; colony lights go out; night iris to title.

## The lock block

Appended, unchanged, to every generated prompt. Never paraphrase between
shots — identical wording is the cheapest consistency tool available.

```lock
Live-action 1950s Technicolor science-fiction feature, Wes Anderson style:
planimetric symmetrical composition, centered subjects, flat frontal staging,
deadpan performance. Photographed on 35mm three-strip Technicolor: real
actors, practical sets, miniatures and painted backdrops — never an
illustration, painting, cartoon or render. Soundstage Mars with
matte-painting depth: coral-red terrain, winding natural rivers of
blue-green water with settlements built up along their banks, cream and
turquoise domed buildings, needle towers, spiked ornamental
plants, striped gas planet and small moons in a mint-green sky. One riveted silver spacesuit, brass and bakelite instruments, hand-built
practical props. The only figures that ever appear are the two twin sisters
and the chrome mer-folk; no other people, no extras, no spacemen. Soft even studio lighting, saturated pastel palette. Reflected light
may move across faces and costumes but never changes the surface itself: no
glitter, no scales, no sequins forming on skin or fabric. Camera locked off
or moving in slow symmetrical push-ins and 90-degree lateral tracks; no
handheld, no zooms, no whip pans, no speed ramps. Consistent cast, wardrobe
and hair throughout. No text, no titles, no captions, no logos, no
watermarks.
```
