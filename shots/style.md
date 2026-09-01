# Style bible — Rivers of Mars, live-action generated path

Everything the video model needs to keep ~25 setups looking like one film.
The lock block is appended verbatim to every prompt by `tools/prompts.py`.

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

## The world

Lowell's Mars taken literally and lovingly: canals as real waterways
engineered through coral-red terrain, cream-and-turquoise domed settlements,
needle towers, spiked ornamental flora, a small canal creature, a striped gas
planet and several moons in a mint-green sky. Every composition is planimetric
and symmetrical or a deliberate 90° angle off; props look hand-built;
signage-free retro-futurist hardware (brass telescopes, riveted silver suits,
dial-covered receivers).

## The characters

Two performers carry the register's Them 1 / Them 2 dialogue:

The two Thems are **identical twin sisters** — same face, same auburn curly
bob — split across two planets. Wardrobe and glasses are the only visual
difference, so every crosscut reads as one mind talking to itself. This
mirrors the record itself: both vocal parts and the backing vocals are the
same singer, so one lip-sync source serves both twins (and backing vocals
can appear as additional reflections of her — canal water, dome glass —
when a shot wants them).

- **Them 2 — the astronaut-botanist on Mars** (the canonical reference image:
  auburn curly bob, riveted silver suit with red piping, chrome backpack).
  Receiver of the signal; kneels by the canal, inspects specimens, unmasks
  Mars.
- **Them 1 — her twin, the astronomer on Earth**: the same woman in round
  brass-rimmed glasses, rumpled rust-brown tweed suit, mustard knit vest,
  collared check shirt; a warm tungsten world of canal charts, brass
  telescopes, and bakelite consoles. Sender of the pieces.

Both exist as reusable **Flow Characters** (portrait + full body) in the
Flow project "Rivers of Mars - AI video": `Astronaut (Them 2)` and
`Astronomer (Them 1)`. Attach the character (not loose refs) on every
performance shot.

Before any video generation, build a character sheet per performer from the
master reference image: full body front, 3/4 medium, close-up, profile, one
mid-movement pose, and (for lip-sync shots) a neutral-mouth frontal close-up.
Regenerate until each set reads as one person on one day, then register the
keepers here and attach them via Ingredients-to-Video on every performance
shot. Media stays out of Git; drop files into `refs/` locally.

- ref character_master: refs/character_master.png
- ref astronaut_front: refs/astronaut_front.png
- ref astronaut_close: refs/astronaut_close.png
- ref astronaut_move: refs/astronaut_move.png
- ref astronomer_front: refs/astronomer_front.png
- ref astronomer_close: refs/astronomer_close.png
- ref palette: refs/palette.png
- ref mars_world: refs/Rivers-of-Mars.png

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
- **scene-04** — the message crosses space: masts, relays, a signal in flight, then loss.
- **scene-05** — the astronaut waiting under the Martian night; scanning dials.
- **psychedelic-garden** — one continuous forward dolly through the greenhouse of spiked flora; drums wake it.
- **pattern-aperture** — specimen table, pattern tests, macro apertures.
- **mars-unmasking** — the reveal: domes wide, counterfeit parade, excavation.
- **semantic-rocket-weather** — filament weather over the colony, rockets overhead, rain becoming canal.
- **rivers-of-mars** — the chorus canal: moon descent, chrome current, the creature, sung close-ups, drum wall, plunge.
- **current-turns-home / low-light-outro / coda** — the current reverses at the canal junction; lamplit duet; colony lights go out; night iris to title.

## The lock block

Appended, unchanged, to every generated prompt. Never paraphrase between
shots — identical wording is the cheapest consistency tool available.

```lock
Live-action 1950s Technicolor science-fiction feature, Wes Anderson style:
planimetric symmetrical composition, centered subjects, flat frontal staging,
deadpan performance. Soundstage Mars with matte-painting depth: coral-red
terrain, engineered canals of blue-green water, cream and turquoise domed
buildings, needle towers, spiked ornamental plants, striped gas planet and
small moons in a mint-green sky. Riveted silver spacesuits, brass and bakelite
instruments, hand-built practical props. Soft even studio lighting, saturated
pastel palette. Camera locked off or moving in slow symmetrical push-ins and
90-degree lateral tracks; no handheld, no zooms, no whip pans, no speed ramps.
Consistent cast, wardrobe and hair throughout. No text, no titles, no
captions, no logos, no watermarks.
```
