# Codex prompt — reference sheets (stage 1 of 2)

Paste everything below the rule into Codex, working in your project checkout.
Stage 2 (the 77 frames) gets its own prompt after the sheets are approved.

---

Work in this repo. The story and the visual register have been rewritten from
scratch since you last saw it. Everything you generated before is superseded:
the old sheets and frames are parked in `board/_v1/` for side-by-side
comparison only. Do not reuse them, do not carry over any prior look decision,
and do not consult them for character design. Start from the files as they
stand now.

## Read first, in this order

1. `board/BRIEF.md` — how the job is structured, the consistency rules, what to
   report at the checkpoint
2. `board/style.md` — the look bible. The register is new. Read the four lock
   blocks and the precedence rule carefully.
3. `world/script.md` — the shooting script, shot by shot, with the lyric each
   shot sits under
4. `board/prompts.json` — the work order. Machine-readable. Every sheet carries
   its exact `prompt`, its canonical `file` path, and the images to `attach`.

Then regenerate the work order yourself so you know it is current:

    ./.venv/bin/python3 tools/world_shots.py
    ./.venv/bin/python3 tools/board_prompts.py

It must report **16 reference sheets**, **77 frames**, and locks
`lock_global, lock_sheet, lock_studio, lock_studio_exposed`. Anything else means
your checkout is stale — stop and say so rather than proceeding.

Use `./.venv/bin/python3` for every Python tool in this repo.

## What changed, so you know what you are drawing

**The story is now one spine, not a tour of worlds.** She has to get off the
record before the needle reaches the centre, because the run-out is blank and
nothing is written past it. Force fails. Running only delays it. There is no
outside — the seabed is grooved too. So she tries to rebuild the groove from
salvaged pieces, and pays for the last piece by breaking the record she loved.
Her fix fails and takes the world down with it. At the run-out she stops,
turns, lifts the needle off herself, and carries it the whole way back to the
outer edge. She was never being chased. She was leading it.

**Five encounter characters, each a previous runner who stopped.** Each is
fused into the world where they gave up, so each costume is built from that
world's material:

- **explorer** — tried to *understand* it. Pith helmet, sun-bleached khaki,
  decades of charts made from groove rubbings.
- **warrior** — tried to *fight* it. Enormous, scarred, armour and blade cut
  from groove shards. Years of work, one scratch.
- **captain** — tried to *escape* it. Full uniform, craft pressed from vinyl,
  periscope aimed downward. He found the floor.
- **chimera** — tried to *make beautiful things instead*. Feathers of
  fluorescent tube, long neck, careful hands. Hundreds of nests, none of them
  a road.
- **witchdoctor** — tried to *remember it into being better*. Charms and
  fetishes of broken record, greasepaint, feathered headdress.

**The register is practical-effects television — cheap budget, high concept.**
Doctor Who, live studio skits. Painted floors and forced perspective, plywood
and foil, fluorescent tubes hung on black drape, dry ice, an ocean with no
water, visible wires and rig. Nothing photoreal. Everything just good enough to
read the intent and no better — but the *ideas* are ambitious and the
performances are played completely straight. That contrast is the whole style.
The model will fight you on this and keep drifting toward cinematic realism.
Push back every time.

**`lock_studio_exposed`** is the one per-world exception, and it applies to the
APART world only, where the set flats fall and the studio itself — lighting
rig, cyclorama, floor tape — is in shot.

## The job for this pass

Generate the **16 reference sheets** into `board/refs/`, one canonical file per
sheet id, at the exact `file` path in the work order. `views` means views
*inside* one image, not separate files — the character sheet is a single image
containing six views of her.

Generate in this order:

1. `char` — **first, and iterate until it is right.** Its `attach` list
   includes `refs/cover.png`, which is present in the repo and is the authority
   for her face, hair and clothing. Attach it to the generation. She must be
   unmistakably that woman across all six views. This is the highest-stakes
   image in the project: 77 frames depend on it and none of them re-describe
   her.
2. `char_explorer`, `char_warrior`, `char_captain`, `char_chimera`,
   `char_witchdoctor` — the five costume sheets.
3. `world_record`, `world_machine`, `world_ocean`, `world_lines`, `world_game`,
   `world_apart` — the world plates.
4. `obj_tonearm`, `obj_groove`, `obj_lines`, `obj_gamepiece` — the object
   plates.

Rules that are not negotiable:

- Use each item's `prompt` **verbatim**. The lock blocks are already appended
  and already resolved per item — do not merge, shorten, reword or "improve"
  them. Identical wording is what holds sixteen generations together.
- Attach exactly the images in each item's `attach` array.
- 16:9. No text, captions, titles, watermarks, logos, UI or borders.
- Keepers go at the canonical path; put every rejected attempt in
  `board/rejects/` so the choice can be reviewed.
- If `refs/cover.png` is missing, stop and ask. Do not substitute or invent a
  replacement character.

## Then stop

Build the gallery:

    ./.venv/bin/python3 tools/board_gallery.py refs

and **stop for review**. Do not begin the 77 frames.

Report:

- which sheets you consider solid and which are compromises
- anything in `board/style.md` that fought you, or that contradicts itself
- whether the cheap-budget register held, or the model kept pulling it toward
  realism, and what you did about it
- your read on whether the character will hold across 77 frames
- anything in `world/script.md` you think is wrong — report it, do not fix it
  locally; the script is generated from `world/script.json` and gets corrected
  at source
