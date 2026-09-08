# Native migration contract

## Inputs and clocks

Source video can remain external. Extracted original image sequences are allowed
as untreated plates. Do not call a scene native when it merely plays an old
composited FX movie, a raster displacement map, or an externally drawn beam layer.
Audio envelopes, sampled waveforms, track coordinates and geometry coordinates
are numerical inputs, not FX raster substitutes.

Keep original source-frame selection and song-frame selection separate. All
intervals in receipts are end-exclusive. Blender frame 1 is delivery frame 0.
The revised overhead swimmer delivery spans 116 source frames, but the current
cut uses only source 54..116, song 3376..3438. Never restart its musical clock.

## Resolution

Rebuild with one requested width, 1280 or 1920. The recipe derives height,
coordinate transforms, masks and bloom sizes from it. Reference coordinates
such as 1280x720 describe normalized geometry, not an FX raster allocation.
Do not change only the parent scene resolution of an older multi-scene recipe.

Read original dimensions from probed source metadata. A Blender image changed
to SEQUENCE can expose placeholder dimensions before evaluation. This caused
the first native insert test to sample the wrong region; the corrected recipe
uses explicit, verified source dimensions.

## Color and light

Retain the accepted compositing operation per family. Some accepted effects
were added in display-referred space, others in linear light. Convert explicitly
inside Blender when needed. Do not introduce another global view transform or
mastering look over an already transformed delivery.

New native recipes use analytic shader fields and native compositor blur for
light masks, or native ribbon geometry for the tunnel. Native does not imply
that every effect is a solved physical 3D scene. The accepted guide and many
light masks remain authored screen-space effects, now resolution-independent.

## Verification

Check representative motion frames by eye, full frame counts and decoding,
the musical/source mapping, and representative 1080 renders reduced for a
resolution comparison. Numerical parity is diagnostic, not an aesthetic vote.
Inspect saved blend dependencies as well as generator code.

Keep clean silent renders separate from numbered, lyric-bearing review exports.
Master audio is used once per review. Adjacent old shots may be present for
context; that does not certify the context movie as fully native.

Native technical verification, owner look approval, production promotion and
final mastering readiness are distinct states. Full release must fail closed
while any of them required for that release is unresolved.
