# Generating in Flow

## Do this first: the character sheet

You have one image of the artist — an album cover. That is one angle, one
lens, one light. Veo will invent every other angle differently on every
generation, and inconsistency across cuts is the single thing that makes an
AI music video look cheap.

So before any video: use the cover as a reference in Nano Banana Pro / Imagen
and generate the same person, same wardrobe, same hair, at

- full body, front
- 3/4, medium
- close-up, face
- profile
- mid-movement (dancing, arms away from the body)

Keep the best of each in `refs/`. Regenerate until they look like one person
on one day. This is an hour of image generation that saves a week of video
generation, and images are far cheaper than video.

Then register them in `shots/style.md` (`- ref character_front: refs/...`) and
attach them via **Ingredients to Video** on every performance shot.

## Flow features worth using

- **Ingredients to Video** — the character refs. Every performance shot.
- **Frames to Video** — give a first *and* last frame. This is how you make a
  shot arrive somewhere specific by the downbeat, instead of hoping.
- **Scenebuilder / Extend** — for the handful of setups that need to run
  longer than one generation.
- Generate at the highest quality your plan allows while it's available.
  Downscaling later is free; regenerating is not.

## The rule about setups

`ingest.py --status` lists every setup with the longest cut that uses it.
**Generate at least that long**, then choose your in-point with
`ingest.py --in`. A setup used by nine cuts is worth two or three takes; a
setup used once is worth one.

Name the download after the setup (`perf_chorus_wide.mp4`) and
`ingest.py --auto` files it and wires it to every cut that uses it.

## Consistency, in order of effectiveness

1. **Lean on non-character imagery** where you can. Environments, objects,
   macro, texture, light. Enormously more forgiving of drift, and the concept
   sections are already the natural home for it.
2. **Fixed character refs** via Ingredients, every single time.
3. **The lock block**, verbatim, every prompt.
4. **A strong uniform grade in post** (`render.py --grade throwback`). Period
   grade, grain, halation and letterbox hide a remarkable amount. Veo only has
   to be consistent underneath the look.
5. **Repetition as structure.** Returning to the same performance setup every
   chorus reads to an audience as a deliberate refrain, not as a shortage of
   footage. Braid your setups so repetition lands on repeated music.

## Budget shape

~25 setups, 2–3 takes on the ones that carry weight, call it 60 generations
for a first pass and another 20 for fixes. That fits inside a month of a
high-tier subscription with room to spare. If you run out of subscription
credits, the Vertex API lists Veo 3.1 at $0.40 per generation with audio at
1080p and the Fast variant around $0.12 — priced per generation rather than
per second, so a top-up pass is tens of dollars, not hundreds. Worth
confirming against current pricing before relying on it.
