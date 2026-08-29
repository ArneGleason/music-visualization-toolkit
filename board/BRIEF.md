# Storyboard generation brief

You are generating a complete storyboard for a 3½-minute music video. Everything
you need is already in this repo. Read this file, then `board/style.md`, then
work through `board/prompts.json`.

## The job

0. Run `./.venv/bin/python3 tools/board_prompts.py` to (re)generate the work
   order. It validates itself and refuses to write if anything is inconsistent.
1. Generate **16 reference sheets** into `board/refs/` — exactly 16 canonical
   files, one per sheet id. Six are the character and the five encounter
   costumes; the rest are world and object plates.
2. Build `board/refs.html` with
   `./.venv/bin/python3 tools/board_gallery.py refs` and **stop** for review.
3. After approval, generate **77 storyboard frames** into `board/frames/`.
4. Build `board/contact.html` with
   `./.venv/bin/python3 tools/board_gallery.py contact`.

Use `./.venv/bin/python3` for every Python tool in this repo.

## Inputs

| file | what it is |
|---|---|
| `board/prompts.json` | **The work order.** Every sheet and frame with its exact prompt, output path, and which references to attach. Machine-readable; use this, not the markdown. |
| `board/prompts.md` | The same thing, readable, for humans reviewing. |
| `board/style.md` | The look bible. Character, worlds, camera vocabulary, and the four lock blocks with their precedence rule. |
| `world/script.md` | The shooting script — her action shot by shot, with the lyric each sits under. |
| `world/story.md` | Why each world exists and what the song is doing there. |
| `refs/cover.png` | The album cover. **The character originates here.** |

Do not invent shots, reorder them, or change timings. `world/shots.json` is
generated from the edit and is the source of truth; if a frame seems wrong,
report it rather than fixing it locally.

## Order of operations — this matters

**Reference sheets must be generated and approved before any frame.** Every
frame prompt attaches sheets and says "the same person as in the attached
character reference". If the sheets change afterwards, all 77 frames are
invalidated.

Generate `char` first. Its work-order entry lists `refs/cover.png` in `attach` —
**that image must be attached to the generation**, it is the authority for her
face, hair and clothing. Iterate until she is unmistakably the woman on that
cover across all six views. This is the highest-stakes image in the project.
Then the five encounter costume sheets (`char_explorer`, `char_warrior`,
`char_captain`, `char_chimera`, `char_witchdoctor`) — each is a *previous
runner* who stopped, so each costume is built from the material of the world
they gave up in. Then the world plates, then the object plates.

If `refs/cover.png` does not exist, **stop and ask for it.** Do not substitute,
approximate or invent a replacement character.

### `views` means views, not attempts

Each sheet is **one canonical file** at the path in its `file` field. `views` is
how many views appear *inside* that single image — the character sheet is one
image containing six views of her, not six files. There are exactly **16**
files in `board/refs/` when this stage is done. Put rejected attempts in
`board/rejects/`.

## Consistency rules — do not deviate

1. **Never re-describe the character in a frame prompt.** The prompts already
   say "the woman from the attached character reference". Re-describing a
   subject per-image is the largest single source of drift. If a frame comes
   back with the wrong person, attach the reference more strongly or regenerate
   — do not add adjectives.
2. **Attach the references listed in each frame's `refs` array.** They are not
   optional and they differ per world.
3. **The locks are already resolved for you.** There are four blocks, not one,
   and `prompts.json` has applied the right ones to each item — its `locks`
   field names which, and its `prompt` already ends with them verbatim. Do not
   merge, shorten or reword them. Precedence, and why the APART world has a
   different palette, is in `board/style.md`.
4. **She is small.** Roughly one fortieth of the record's playable radius.
   Except in close-ups she should not be the largest thing in frame. Models
   drift toward making the human subject dominant; push back.
5. **16:9, no text.** No captions, titles, watermarks, logos, UI or borders.

## Checkpoint

After the 16 reference sheets, **stop**. Put them in `board/refs/`, build a
simple `board/refs.html` showing them side by side, and report:

- which sheets you consider solid and which are compromises
- anything in `board/style.md` that fought you
- your read on whether the character will hold across 77 frames

Do not start the frames until told to continue.

## Output conventions

```
board/refs/char.png            16 sheets, one canonical file each
board/refs/world_ocean.png
board/frames/w001.png          77 frames, ids from prompts.json
board/rejects/                 anything you generated and discarded
board/refs.html                built by tools/board_gallery.py refs
board/contact.html             built by tools/board_gallery.py contact
```

Every item in `prompts.json` carries its own `file` (canonical output path),
`prompt` (exact text) and `attach` (the reference image paths to supply).
Write to those paths exactly — the galleries and the render pipeline look them
up. The galleries show missing images as labelled gaps, so you can run them at
any point as a progress report.

If a generation needs several attempts, keep only the keeper at the canonical
path and put rejects in `board/rejects/` so the choice can be reviewed.

## What to report at the end

- Frames you are not happy with, and why
- Any shot whose written action you could not stage in one image
- Places where the script and the look bible disagree

Do not silently fix the script. Report it — the script is generated from
`world/script.json` and needs to be corrected at source.
