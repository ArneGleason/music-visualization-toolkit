# codex/ — self-contained handoff: generate the v6 storyboard stills

This folder is everything an outside agent (Codex desktop, or anything with
an `OPENAI_API_KEY`) needs to generate the storyboard stills for "Rivers of
Mars" with the OpenAI image model. Read from here, write into `out/`,
touch nothing else in the repository.

```
codex/
  README.md              this file: context, procedure, guards
  PROMPT.txt             the message to paste into Codex
  stills_manifest.json   THE JOB LIST (generated; do not hand-edit)
  refs/                  reference photographs to attach (inputs)
    astronaut_likeness.jpg      the lead's locked face (both twins share it)
    merfolk_likeness_gpt.jpg    the approved chrome mer-folk school
    specimen_ref.jpg            the helical alien specimen
    world_anchor.jpg            photographic world anchor for non-character shots
  out/                   generated stills go here (outputs)
    <setup>_a.jpg, <setup>_b.jpg   two variants per setup, 16:9 JPEG
    _log.md                        refusals / errors, appended as they happen
    _report.md                     written once at the end
```

All paths inside `stills_manifest.json` are relative to this folder.

## Why this pass exists

The film is being re-realized as live-action-style generated footage: a
Wes Anderson take on a 1950s Technicolor science-fiction feature. Stills are
generated per **setup** (41 setups cover 59 cuts); an approved still later
becomes the start frame of a short video clip. The owner's comparison on
2026-09-03 found the OpenAI image model gives the preferred look and holds
the lead's face when her likeness photograph is attached. This pass
regenerates every setup there.

## Procedure

1. Read `stills_manifest.json`. For each entry in `setups`, in order:
   - Call the image **edit** endpoint (the one that accepts input images),
     model `gpt-image-1` or newer, with every file in `refs` attached as
     input images and `prompt` passed **verbatim**. Size `1536x1024`,
     quality `high`, two outputs. If the API offers a 16:9 size use it;
     otherwise crop `1536x1024` to `1536x864`, centered.
   - Save as `outputs[0]` and `outputs[1]` (`out/<setup>_a.jpg`,
     `out/<setup>_b.jpg`), JPEG quality 92.
   - Skip an entry whose two outputs already exist (the run is resumable).
   - On a content-policy refusal or API error, append the setup name and
     the message to `out/_log.md` and continue.
2. Never paraphrase, shorten or "improve" a prompt. The lock block at the
   end of every prompt is identical on purpose; identical wording across
   shots is the consistency mechanism.
3. Stills only; do not generate video.
4. When all entries are done, write `out/_report.md`: generated, skipped,
   failures, total spend if the API reports it.
5. Write only inside `out/`. Do not edit the manifest, the refs, or any
   file outside this folder. Do not commit.

## Acceptance guards (check before saving; regenerate once if violated)

Each entry carries its own `guards`; the universal ones:

- No text, captions, titles or lettering anywhere in the frame.
- Photographed, never illustrated. Miniatures, matte paintings and stage
  work are fine; drawn or painted looks are rejects.
- Character shots: the face matches `refs/astronaut_likeness.jpg`; no
  eyewear; the plain smooth brushed-silver suit with one riveted collar
  ring and nothing else on it.
- Mer-folk shots: exactly one large round eye centered in each face, no
  second eye, no nose; a fish tail below the waterline and no legs; all
  identical to the attached school.
- Non-character shots: no people. Only the two twin sisters and the
  mer-folk ever appear anywhere in this film; no extras, no spacemen.

Judge by eye if you can view the image; otherwise trust the prompt and let
the owner cull from the contact sheet.

## Cost and time

82 images at `high` quality on `gpt-image-1` is on the order of USD 15 to 25
of API spend (billed separately from a ChatGPT subscription). Sequential
calls take roughly one minute each; run four in parallel if the account's
rate limit allows.

## Where the manifest comes from (owner side)

`python tools/still_manifest.py` regenerates `stills_manifest.json` from
`shots/shotlist.json`, `shots/style.md` and `shots/conventions.json`. The
prompts are byte-identical to the Still blocks in `prompts/prompts.md`.
After the pass, keepers are copied into `board/frames/<setup>_p.jpg` /
`_q.jpg`, `python tools/board_contact.py` rebuilds the contact sheet, and
`python tools/blender_comp.py --variant-order p,q,n,m,f,e,d,c,b,a` renders
the animatic with the new stills on top.
