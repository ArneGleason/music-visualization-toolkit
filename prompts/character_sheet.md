# Character sheet & board work order — image generation

> **Status 2026-09-02:** both Characters must be REBUILT to the v2 spec
> (ballerina's build and dancer's carriage; plain silver suit; astronomer
> with hair up, no eyewear) before any v2 still is generated. The 08-31
> builds below are superseded.
>
> **Status 2026-08-31:** both performers are BUILT as Flow Characters
> (portrait + full body) in the Flow project "Rivers of Mars - AI video":
> `Astronaut (Them 2)` and `Astronomer (Them 1)` — the astronomer recast as
> the astronaut's **identical twin sister** (same face and bob; round brass
> glasses, rust-brown tweed suit, mustard vest). Attach the Character on
> performance shots instead of loose refs. The four boards (11–14) are also
> generated and live in the project's media library: palette board,
> observatory study, canal-to-colony vista, greenhouse aisle. Sections below
> are kept as the spec that produced them and for regenerating extra angles.

Paste-ready prompts for Flow / Gemini (Nano Banana). Attach
`refs/character_master.png` as an ingredient on **every** prompt below —
it anchors identity, wardrobe, palette, and world at once. Append the lock
block from `shots/style.md` verbatim to every prompt.

Acceptance test per set: line the keepers up side by side — they must read
as **one person, one wardrobe, one day**. Regenerate misses; images are
cheap, video is not. Save keepers under the exact filenames given (they stay
out of Git). After saving, add any new `- ref name: path` lines to
`shots/style.md`.

## The astronaut (Them 2) — from the master image

1. `refs/astronaut_front.png` — Full-body studio portrait, standing, front-on
   and centered in a dancer's first position, arms relaxed: the same young
   woman as the reference but with a ballerina's build and carriage — slender,
   long-necked, upright, chin lifted, a small delicate pixie nose — auburn curly bob with straight bangs,
   in the plain silver suit (smooth close-fitting one-piece, single wide
   riveted collar ring, silver gloves and boots, nothing else). Plain
   coral-red seamless backdrop, soft even light.
2. `refs/astronaut_34.png` — Waist-up, 3/4 view, same person same suit same
   day, hands clasped, calm deadpan expression. Plain warm backdrop.
3. `refs/astronaut_close.png` — Frontal close-up, head and collar, eyes to
   camera, mouth relaxed and softly closed (this is the lip-sync anchor
   frame). Soft dark neutral backdrop, gentle moonlit key.
4. `refs/astronaut_profile.png` — True profile close-up facing frame left,
   same light and backdrop as the close-up.
5. `refs/astronaut_move.png` — Mid-movement full body: walking turn with
   arms away from the body, hair in motion, on coral terrain.

## The astronomer (Them 1) — the astronaut's identical twin

Generate every astronomer image with the astronaut character (or the master
image) attached, so the twin faces stay identical.

6. `refs/astronomer_front.png` — Full-body studio portrait, front-on and
   centered: the astronaut's identical twin sister — same face, same
   ballerina's build and dancer's carriage, the same auburn hair pinned up in
   a loose 1950s French twist with straight bangs and a pencil through it —
   in a rumpled rust-brown tweed jacket and trousers, mustard knit vest,
   collared check shirt, brown brogues. No eyewear. Plain cream backdrop,
   warm tungsten light.
7. `refs/astronomer_34.png` — Waist-up 3/4 view, same woman same suit same
   day, holding a hand-inked Mars canal map. Plain warm backdrop.
8. `refs/astronomer_close.png` — Frontal close-up, eyes to camera, mouth
   relaxed and softly closed (lip-sync anchor). Desk-lamp warmth against
   darkness.
9. `refs/astronomer_profile.png` — True profile close-up facing frame
   right (the twins face each other across the edit), same light.
10. `refs/astronomer_move.png` — Mid-movement: reaching up to a telescope
    eyepiece, jacket in motion, observatory interior soft behind.

## Boards

11. `refs/palette.png` — A painted palette board for the film: large flat
    swatches of coral-red soil, blue-green canal water, mint sky, cream and
    turquoise dome enamel, riveted silver, warm brass, tweed brown, deep
    night blue; each swatch with a small painted texture chip.
12. `refs/world_canal_colony.png` — Wide symmetrical matte-painting master:
    the canal running dead-center toward the cream-and-turquoise domed
    colony and needle towers, spiked flora on both banks, striped gas planet
    and small moons in a mint sky.
13. `refs/world_observatory.png` — Interior master: the astronomer's
    observatory study — brass telescope through the dome slit, desk of canal
    charts, bakelite console with round oscilloscope, warm tungsten pools in
    darkness, symmetrical one-point staging.
14. `refs/world_greenhouse.png` — Interior master: the Martian greenhouse's
    central aisle in one-point perspective, ranked spiked plants, hanging
    glass globes, mist, green-gold light.

Attach the matching world board alongside the character refs when a video
prompt takes place in that set.
