# Candidate-final picture and FX handoff

Owner target: 1920x1080, 24 fps. No 4K target. Current FX experiments establish
creative choices, not final-quality delivery. Do not regenerate successful looks
just because they were previewed at 720p.

## Inspected state

Surface-swimmer and overhead source clips: 1280x720, 24 fps, 8 seconds, H.264.
Current swim and amber/cyan tunnel composites: 1280x720 H.264 review encodes.
Scope clean composite: 1920x1080, 24 fps. The word "clean" currently means no
review audio/labels, not necessarily a high-quality finishing intermediate.
Do not infer dimensions of other sources from these samples; inspect individually.

## Before promoting a look to candidate-final

- Keep the original source, reproducible recipe, exact audio offsets and approved
  look reference. Final shot timing remains authoritative.
- Render useful full available coverage and record source origin, intended cut,
  and actual usable exit handles. Do not assume all generated frames are useful.
  Follow the exit-only default; do not invent pre-roll. Repeated source use at a
  different song time may need a separately synchronized effects render.
- Reconcile the s044 67/68-frame discrepancy before assembler promotion.
- Surface-shot expansion to all swimmers remains pending; approved current pass
  only tracks four central torsos. Do not label it all-swimmer coverage.
- Choose the best available source before final tracking. For 720p footage,
  establish its 1080p working plate once, then scale/revalidate tracks and render
  procedural lines, bloom and masks at the target resolution. Do not simply
  enlarge a repeatedly compressed preview. Test any enhancement for temporal
  consistency and preservation of chrome detail, faces and generated texture.
- Review full-length tracking, edge flicker, body/spoke occlusions, highlight
  clipping, unintended halos, lyrics and lip-sync readability. Existing pilots
  have deliberately approximate masks and incomplete tracking coverage.
- Retain high-quality frame/layer intermediates for finishing, including linear
  emission headroom where needed. H.264 preview files are not the sole masters.
  More precision in later intermediates does not recover lost source detail.
- Save brightness/bloom controls and separate effects where practical. Refraction
  needs displacement fields plus masks and the underlying footage, not just alpha.
- Validate dimensions, fps, frame coverage, soundtrack origin and silent picture
  delivery. Master soundtrack belongs in the final assembly once.
- Promote only reviewed, validated deliveries into assembly_decisions.json;
  distinguish look-approved, rendered-candidate, delivery-ready and applied.

## Finishing order to test

Prepare source at working resolution -> render/composite FX -> integrate into edit
and inspect across cuts -> unify grade -> subtle optional film texture/halation
or optical treatment -> delivery encode.

Finishing is a creative trial, not a requirement to add every artifact. Keep grain
at final resolution and avoid baking different heavy grain into every clip.
Test global distortion against lyric sharpness and existing deliberate lens FX;
do not automatically distort typography or double the per-shot bloom. Finishing
cannot repair bad tracking, source explosions, phase errors or missing coverage.

It is appropriate to build candidate renders now while keeping them revisable.
Prioritize full-film coverage and a contextual review over polishing each short
section to finality. No upscaling, regeneration or whole-film mastering was
performed merely by recording this checklist.
