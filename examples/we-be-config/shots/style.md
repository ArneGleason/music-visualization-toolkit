# Style bible

Everything Veo needs to keep 30 separate generations looking like one film.
Written once, appended verbatim to every prompt by `tools/prompts.py`.

## The artist

Built from the album cover. Before generating any video, make a **character
sheet**: feed the cover art to Nano Banana Pro / Imagen and generate the same
person in a consistent wardrobe at several angles and distances — full body
front, 3/4, profile, medium, close-up, and one mid-movement. Keep them in
`refs/`. Those become the Ingredients you attach to every performance shot.
One album cover is one angle under one light; Veo will invent the rest
differently every time unless you pin it down first.

- ref character_front: refs/char_front.png
- ref character_34: refs/char_34.png
- ref character_close: refs/char_close.png
- ref palette: refs/palette.png

## Look

TODO — one paragraph. Era, film stock, lens, grain, color cast, how it moves.
"Throwback" is doing a lot of work for you here: heavy period grade, 4:3 or
letterbox, halation, grain and gate weave all mask the drift between
generations. The uniform grade in `tools/render.py --grade throwback` is
applied in post to every clip equally, so Veo's output only has to be
consistent *underneath* it.

## Sections

TODO — one line per section: what the concept scenes are about, and what the
performance setups are. Keep the performance setups few and repeated; the
audience reads a returning setup as a chorus, not as a shortage.

## The lock block

Appended, unchanged, to every generated prompt. Never paraphrase between
shots — identical wording is the cheapest consistency tool available.

```lock
Shot on 16mm film, 1.85:1, soft halation on highlights, visible grain, slightly
warm color cast, practical lighting only. Camera moves are slow and deliberate:
a gentle push, a slow lateral drift, or locked off. No zooms, no whip pans, no
speed ramps. Consistent wardrobe and hair throughout. Muted palette of warm
amber, deep teal shadow, desaturated skin. No text, no titles, no captions,
no logos, no watermarks.
```
