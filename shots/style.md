# Style bible — Rivers of Mars, generated-footage path

Everything the video model needs to keep ~25 setups looking like one film.
The lock block is appended verbatim to every prompt by `tools/prompts.py`.

This is the alternate AI-video production path. The published vector video is
the reference edit; this document translates its look, not replaces it.

## The characters

Two abstract presences from the register: **Them 1** (the sender, warm
gold-amber) and **Them 2** (the receiver, cool teal-white). They are stylized
luminous figures, not photoreal humans — closer to sculpted light than to
actors. Before any video generation, build a character sheet per figure from
`refs/Rivers-of-Mars.png` plus new image generations: full body front, 3/4
medium, close-up, profile, and one mid-movement pose each. Regenerate until
each set reads as one being under one light, then register them here and
attach them via Ingredients to Video on every performance shot.

- ref them1_front: refs/them1_front.png
- ref them1_close: refs/them1_close.png
- ref them1_move: refs/them1_move.png
- ref them2_front: refs/them2_front.png
- ref them2_close: refs/them2_close.png
- ref palette: refs/palette.png
- ref mars_world: refs/Rivers-of-Mars.png

## Look

Painterly sci-fi animation over black: deep space blacks, glowing gold and
teal signal light, rust-red Martian terrain, chrome river water, recursive
psychedelic foliage. Light behaves like sound — everything luminous pulses,
flows, or ripples. Camera language follows the register's motion contract:
every move has an origin and a destination; slow dollies, drifts, and locked
frames only.

## Sections

One line per register scene; setup names match `shots/plan.json`.

- **scene-01** — oscilloscope ignition: light condenses into a waveform that becomes the performers.
- **signal-exchange** — Them 1's warm plea; puzzle pieces that almost fit.
- **scene-04** — the MIDI network: packets in flight, then loss.
- **scene-05** — Them 2 waiting in the starfield; scanning the raw signal.
- **psychedelic-garden** — one continuous forward dolly through recursive foliage; drums wake the garden.
- **pattern-aperture** — inspection table, pattern tests, macro apertures.
- **mars-unmasking** — the reveal: rust rings, counterfeit parade, excavation.
- **semantic-rocket-weather** — filament weather, rockets overhead, rain becoming river.
- **rivers-of-mars** — the chorus river: moon descent, chrome current, spirograph mouths, drum wall, plunge.
- **current-turns-home / low-light-outro / coda** — the current reverses; low-light duet; night iris to title.

## The lock block

Appended, unchanged, to every generated prompt. Never paraphrase between
shots — identical wording is the cheapest consistency tool available.

```lock
Stylized painterly sci-fi animation, not photorealistic. Deep black space
background, luminous gold-amber and teal-white light figures, rust-red Martian
terrain, chrome-silver water, glowing recursive vegetation. All light sources
pulse gently as if driven by music. Camera moves are slow and purposeful: a
gentle push, a slow lateral drift, or locked off. No zooms, no whip pans, no
speed ramps, no camera shake. Consistent character design throughout. 16:9,
high detail, soft bloom on highlights, no text, no titles, no captions, no
logos, no watermarks.
```
