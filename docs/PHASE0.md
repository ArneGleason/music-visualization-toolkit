# Phase 0 — the one-shot lip-sync probe

Goal: prove (or disprove) the whole chain — character still → generated clip
→ lip-sync to the existing vocal → final grade — on ONE sung phrase, before
building storyboards or spending at scale. Budget: an afternoon and under
~$40 of subscriptions, most of which carries into production anyway.

**The probe phrase** (proposed): `lyr-055`, *"Chrome-plated bodies go
swimming"*, register bars 49.4.720–51.4.240 = 134.55–139.87 s (~5.3 s) — the
chorus hook, sung by the astronaut in close-up (the `chorus_close_sync`
setup).

## The window

Google AI **Ultra benefits run until 2026-09-07**, then the account drops to
Pro. Owner is willing to re-upgrade if the path proves worthwhile — the probe
and animatic are that test. Schedule the spend accordingly:

- **Aug 31 – Sep 1**: character sheet + boards (images), probe clip, sync
  tools, verdict.
- **Sep 2 – 4**: storyboard stills for all setups, contact-sheet review,
  animatic, cut iteration.
- **Sep 4 – 6**: generate the reused and `_sync` setups at highest quality,
  2–3 takes, inside the Ultra pool.
- **Sep 7+**: one-off tails, fixes, and re-takes under Pro or API top-up;
  re-upgrade only if the animatic earned it.

## Already done (Claude ran these locally)

- Master mix copied to `audio/song.wav`; compiled register grid copied into
  `projects/rivers-of-mars/generated/`; `project.local.json` points at the
  Bitwig project, Export Audio mix, and stem folder on this machine.
- `register2sections.py → shotplan.py → prompts.py` run: 15 sections,
  47 shots, 36 setups, `prompts/prompts.md` written with the lock block.
- Probe audio sliced with 0.2 s handles:
  - `clips/inbox/probe_vocal_short.wav` — lead-vocal stem, lyr-055 (5.3 s),
    **use this for the sync tools**
  - `clips/inbox/probe_vocal.wav` / `probe_mix.wav` — the full couplet
    (10.7 s) for later
- Remaining: the accounts, the in-browser generation, and the taste calls.

## Accounts needed

| Account | Why | Plan for the probe |
|---|---|---|
| Google account + **Google AI Pro** ($19.99/mo, 1,000 Flow credits) | Flow: Veo video gen + Nano Banana image gen with Ingredients | Pro is plenty for the probe; consider Ultra only at production volume |
| **Kling AI** (klingai.com) | Sync candidate A: dedicated Lip Sync accepts uploaded audio, ≤60 s clips | Free tier (66 credits/day, watermarked) is enough to judge quality |
| **sync.so** | Sync candidate B: `lipsync-2-pro` web studio, ~$0.04/s | Free tier to evaluate; Hobbyist $5/mo if needed |
| **Runway** (optional) | Fallback C: Act-Two performance capture (drive with a phone video of yourself singing) | Only create if A and B both fail on singing |

Account creation and any payment steps are yours to do manually — no tool in
this repo touches them.

## Steps

1. ~~Get the exact phrase times~~ — done, see above.

2. ~~Slice the audio locally~~ — done, see above.

3. ~~Drop the master reference~~ — done: found in Downloads and filed as
   `refs/character_master.png` and `refs/Rivers-of-Mars.png`. Image prompts
   for the full character sheet and boards are written in
   `prompts/character_sheet.md`.

4. **Make the character still** (Flow / Gemini, Nano Banana): upload the
   master image as an ingredient and ask for a frontal close-up, neutral or
   softly-parted mouth, per the `shots/style.md` lock block (paste it
   verbatim). Iterate until identity holds; save the keeper as
   `refs/astronaut_close.png`.

5. **Generate the silent performance clip** (Flow): Ingredients-to-Video with
   `refs/astronaut_close.png` attached. Prompt: the astronaut sings gently to
   camera, minimal head motion, mouth loosely singing — plus the lock block
   verbatim. 8 s, highest quality the plan allows. Best of 2–3 takes →
   download as `clips/inbox/probe_take.mp4`.

6. **Run the sync pass in both tools** on the same take + `probe_vocal.wav`:
   - Kling → AI Human → Lip Sync → upload video + audio → download as
     `clips/inbox/probe_kling.mp4`.
   - sync.so web studio → `lipsync-2-pro` → same inputs → download as
     `clips/inbox/probe_sync.mp4`.

7. **Grade and audition in context** — mux each result over the *mix* slice
   and apply the project grade:

   ```bash
   ffmpeg -i clips/inbox/probe_kling.mp4 -i clips/inbox/probe_mix.wav -map 0:v -map 1:a -vf "curves=r='0/0.02 0.5/0.55 1/1':g='0/0.02 0.5/0.5 1/0.98':b='0/0.04 0.5/0.47 1/0.94',eq=saturation=1.28:contrast=1.07,noise=alls=7:allf=t+u,vignette=PI/5.2,drawbox=y=0:w=iw:h=ih*0.128:color=black:t=fill,drawbox=y=ih*0.872:w=iw:h=ih*0.128:color=black:t=fill" -c:v libx264 -crf 16 -shortest out/probe_kling_graded.mp4
   ```

   (Same filter chain as `tools/render.py --grade technicolor`.)

8. **Judge** at full resolution, sound on:
   - Identity: still the person from the master image? Under the grade?
   - Sustained vowels: singing holds notes — does the mouth hold open
     naturally, or flap like speech?
   - Teeth/jaw artifacts, chin warping, detail smearing in the synced region.
   - Timing: onsets on the consonants, not ahead/behind.
   - Letterbox: face safe inside the 2.39 crop.
   - Note the credit/dollar cost each tool actually charged per second.

9. **Record the verdict** in this file (tool chosen, cost, artifacts seen,
   takes needed). If neither tool passes, film yourself performing the phrase
   on a phone and try Runway Act-Two before rethinking the direction. Only
   then move to storyboards.

## Exit criteria

Phase 0 is done when one graded, synced, in-context clip is judged
production-worthy — or when all three routes have failed on this phrase and
the plan needs a non-sync performance style instead.
