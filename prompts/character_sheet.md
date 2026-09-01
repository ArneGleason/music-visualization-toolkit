# Character sheet & board work order — image generation

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
   and centered, arms relaxed: the same young woman as the reference — auburn
   curly bob with straight bangs, riveted silver spacesuit with red piping,
   chrome backpack, silver gloves and boots. Plain coral-red seamless
   backdrop, soft even light.
2. `refs/astronaut_34.png` — Waist-up, 3/4 view, same person same suit same
   day, hands clasped, calm deadpan expression. Plain warm backdrop.
3. `refs/astronaut_close.png` — Frontal close-up, head and collar, eyes to
   camera, mouth relaxed and softly closed (this is the lip-sync anchor
   frame). Soft dark neutral backdrop, gentle moonlit key.
4. `refs/astronaut_profile.png` — True profile close-up facing frame left,
   same light and backdrop as the close-up.
5. `refs/astronaut_move.png` — Mid-movement full body: walking turn with
   arms away from the body, hair in motion, on coral terrain.

## The astronomer (Them 1) — new design, styled by the master image

6. `refs/astronomer_front.png` — Full-body studio portrait of a middle-aged
   astronomer, front-on and centered: rumpled three-piece tweed suit, knit
   tie, round brass-rimmed glasses, neat greying hair and mustache, a brass
   pocket telescope in hand. Plain cream backdrop, warm tungsten light.
   Same 1950s film world as the reference image.
7. `refs/astronomer_34.png` — Waist-up 3/4 view, same man same suit same
   day, holding a hand-inked Mars canal map. Plain warm backdrop.
8. `refs/astronomer_close.png` — Frontal close-up, eyes to camera, mouth
   relaxed and softly closed (lip-sync anchor). Desk-lamp warmth against
   darkness.
9. `refs/astronomer_profile.png` — True profile close-up facing frame
   right (he and the astronaut face each other across the edit), same light.
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
