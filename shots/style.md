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

Lowell's Mars taken literally and lovingly: canals as real waterways
engineered through coral-red terrain, cream-and-turquoise domed settlements,
needle towers, spiked ornamental flora, a striped gas planet and several
moons in a mint-green sky. Every composition is planimetric and symmetrical or
a deliberate 90° angle off; props look hand-built; signage-free
retro-futurist hardware (brass telescopes, riveted silver suits, dial-covered
receivers). Four places the film keeps returning to:

- **The observatory** on Earth — brass telescope, dome slit, desk of canal
  charts, bakelite console, warm tungsten pools in darkness.
- **The colony and its canal basin** — the canals meet in one great circular
  reservoir at the foot of the domes: a wide, calm expanse of blue-green
  water ringed by fountains and brass lock-gates, big enough to stage a water
  ballet. The chorus water numbers happen **here, in open water**, never
  crowded into a narrow channel.
- **The canal forest** — Lowell's dark vegetation belt along the canals,
  taken as a lush alien forest: fern-fans the size of sails, giant cupped
  leaves, pink thistle-globes on tall stalks, hanging seed-lanterns, moss and
  mist; the canopy closes overhead and the light turns green and magenta. A
  small green light travels through it and she follows it. (This replaces
  the greenhouse aisle of the first pass, which read as a nursery, not a
  psychedelic garden.)
- **Orbit** — the film goes to space when things arrive: Mars from orbit as
  Lowell drew it, a coral globe scored with a lattice of straight canals and
  dark oases, the rockets seen descending toward it before they land.

## The characters

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

- **Them 2 — the astronaut-botanist on Mars** (the canonical reference
  image): auburn curly chin-length bob with straight bangs, always worn down;
  the surface suit below. Receiver of the signal; kneels by the canal,
  inspects specimens, unmasks Mars.
- **Them 1 — her twin, the astronomer on Earth**: the same auburn hair worn
  **up** — pinned in a loose 1950s French twist with the same straight bangs
  and a pencil pushed through it, a few curls escaping by the outro. Rumpled
  rust-brown tweed jacket, mustard knit vest, collared check shirt. Sender of
  the pieces.

(Working choice, one line to change: the differentiator could equally be a
longer loose style. The rule is that *hair*, which the generator treats as
identity, carries the difference — never an accessory.)

Both exist as reusable **Flow Characters** (portrait + full body) in the Flow
project "Rivers of Mars - AI video": `Astronaut (Them 2)` and
`Astronomer (Them 1)`. The astronomer Character must be **rebuilt** to this
spec (updo, no eyewear) before her shots are regenerated. Attach the
Character (not loose refs) on every shot of her, and only the one Character
the shot needs — attaching both, or asking for one twin in a session that
just drew the other, is how the bleed happened.

## Cast lines

Prompt bodies name the cast with `{{astronaut}}`, `{{astronomer}}`,
`{{merfolk}}` and the suits with `{{suit}}`, `{{suit_field}}`,
`{{suit_orbital}}`, `{{suit_liner}}`; `tools/prompts.py` substitutes the
lines below **verbatim** into every prompt, so a wardrobe or hair change is
one edit here and never a paraphrase there. The suit changed from scene to
scene in the first pass because every prompt described it a little
differently; one canonical sentence, pasted, is the fix.

- cast astronaut: the astronaut, a young woman with an auburn curly chin-length bob and straight bangs
- cast astronomer: the astronomer, the astronaut's identical twin sister — the same face, the same auburn hair pinned up in a loose 1950s French twist with straight bangs and a pencil pushed through it — in a rumpled rust-brown tweed jacket, mustard knit vest and collared check shirt
- cast suit: her surface suit: a one-piece riveted brushed-silver spacesuit with fine ribbed quilting, a wide riveted silver collar ring and no helmet, two red webbing straps over the shoulders to a chrome backpack with a brass valve knob, a round silver chest medallion, a silver utility belt with a square buckle, ribbed silver gloves and boots
- cast suit_field: her field suit: the same riveted silver spacesuit with the collar ring and red shoulder straps, plus a brass-buckled leather specimen satchel slung across the chest and a brass hand lantern clipped to the belt
- cast suit_orbital: her orbital suit: the same riveted silver spacesuit with a clear domed glass helmet sealed to the collar ring by a brass clamp, and a bulkier chrome backpack with two brass tanks
- cast suit_liner: her off-duty liner: the ribbed silver knit undersuit worn beneath the spacesuit, collar ring removed, sleeves pushed up
- cast merfolk: the canal mer-folk — a school of chrome-plated swimmers polished like 1950s hood ornaments, each with a long fish tail, slender humanoid arms, and a smooth bald alien head with stripped-down features: one large eye with long lashes, no nose, a tiny round mouth open in song — moving in unison

The suit variants are used only where the script goes somewhere: the field
suit in the canal forest, the orbital suit on the landing field as the
rockets come down, the liner in her bunk for the outro. Everywhere else it is
the surface suit, unchanged.

## Wardrobe and creature consistency

- Attach the astronaut Character (portrait + body) on every shot of her, plus
  the suit turnaround board (`refs/suit_turnaround.png`, front/side/back of
  the empty suit and the three variants) once it exists.
- The mer-folk get their own design sheet (`refs/merfolk_sheet.png`: one
  swimmer front, side, and a ring of six from above) and it is attached on
  every water setup. They are always a **school** — twelve or more — never a
  single creature, and they perform Busby Berkeley geometry: rings, spokes,
  fans, in unison, in open water.
- Character sheets and boards stay out of Git; drop files into `refs/` and
  register them below.

- ref character_master: refs/character_master.png
- ref astronaut_front: refs/astronaut_front.png
- ref astronaut_close: refs/astronaut_close.png
- ref astronaut_move: refs/astronaut_move.png
- ref astronomer_front: refs/astronomer_front.png
- ref astronomer_close: refs/astronomer_close.png
- ref suit_turnaround: refs/suit_turnaround.png
- ref merfolk_sheet: refs/merfolk_sheet.png
- ref palette: refs/palette.png
- ref mars_world: refs/Rivers-of-Mars.png
- ref world_basin: refs/world_basin.png
- ref world_forest: refs/world_forest.png
- ref world_orbit: refs/world_orbit.png

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
- **signal-exchange** — the astronomer's warm plea; canal-map pieces that almost fit.
- **scene-04** — the message crosses space and arrives over the limb of Mars, seen from orbit.
- **scene-05** — the astronaut waiting under the Martian night; scanning dials.
- **scene-06 / psychedelic-garden** — the garden hatch opens onto the canal forest; she walks its path following the little green light; the forest wakes around her on the drums.
- **pattern-aperture** — specimen table, pattern tests, macro apertures.
- **mars-unmasking** — the reveal: domes wide, counterfeit parade, excavation.
- **semantic-rocket-weather** — filament weather over the colony, the twins' call-and-response, rockets descending from orbit and landing, rain becoming canal.
- **rivers-of-mars** — the chorus in the canal basin: moon descent, the mer-folk's water ballet from above, tiny mouths agape, sung close-ups, fountains on the drums, the plunge.
- **current-turns-home / low-light-outro / coda** — the current reverses at the canal junction; lamplit duet; colony lights go out; night iris to title.

## The lock block

Appended, unchanged, to every generated prompt. Never paraphrase between
shots — identical wording is the cheapest consistency tool available.

```lock
Live-action 1950s Technicolor science-fiction feature, Wes Anderson style:
planimetric symmetrical composition, centered subjects, flat frontal staging,
deadpan performance. Photographed on 35mm three-strip Technicolor: real
actors, practical sets, miniatures and painted backdrops — never an
illustration, painting, cartoon or render. Soundstage Mars with
matte-painting depth: coral-red terrain, engineered canals of blue-green
water, cream and turquoise domed buildings, needle towers, spiked ornamental
plants, striped gas planet and small moons in a mint-green sky. Riveted
silver spacesuits, brass and bakelite instruments, hand-built practical
props. Soft even studio lighting, saturated pastel palette. Reflected light
may move across faces and costumes but never changes the surface itself: no
glitter, no scales, no sequins forming on skin or fabric. Camera locked off
or moving in slow symmetrical push-ins and 90-degree lateral tracks; no
handheld, no zooms, no whip pans, no speed ramps. Consistent cast, wardrobe
and hair throughout. No text, no titles, no captions, no logos, no
watermarks.
```
