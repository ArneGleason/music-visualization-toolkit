# Next migration: message sprites and receiver continuity

Investigation completed while the Bends Your Mind native render was running.
Message entrance through NOW is now implemented in the message native family;
see MESSAGE.md for current render/verification status. The screen-to-garden
continuation is still pending. This note remains the source-chain reference.

## Hidden assembly layer, now traced

`out/opening_through_meant_v1/build.py` replaces song frames 971..1082 with
`out/rosette_duet_trial/preview.mp4`, source 0..111. That reference includes
lyrics and review audio. It must NOT become the plate for native sprites.
`out/full_review_v05/build.py` performs the same replacement.

The review register lists s012 as song 911..1082, source 12 onward from
`out/assembly_cfr/synced_49bb1ee673385c931ee7.mp4`. Its shot assignment alone
does not reproduce the accepted sprites. A native replacement must use this
untreated performance, preserve its source origin, and add native lyrics once.

## Numeric continuity

The accepted `out/rosette_duet_trial/render.py` uses phase-folded, phrase-gated
audio from `out/astronaut_reply_v1/guide.wav`, whose song origin is 899.
Cyan listens at 1030..1060; amber at 1060..1082. The first shape retains its
captured signal after its phrase, without reacting to the second phrase.
There are two ordered sub-samples per frame, not independent random samples.
Preserve oscillator period, radial samples, level, dwell, clipping and trails.
The colors in that script are BGR, not RGB.

Receiver continuation in `out/receiver_reply_arrival_v1/post.py` warms these
same sprite states through frames 1030..1082 before moving them onto the radio.
Later wrappers in `out/receiver_interaction_v2/render.py` and
`out/receiver_now_v3/render.py` add knob engagement, outlines and NOW accent.
`out/screen_garden_trial/render.py` extends that state to the screen transition.
Treat these as one stateful effect family with several deliveries, rather than
starting unrelated circles independently at each cut.

## Implementation contract

Extract numerical curves and tracked coordinates only. Native Blender ribbon
geometry, masks, persistence and bloom can reuse lessons from tunnel/bends.
Do not use the old preview as a pixel substrate, remove lyrics by cropping,
or call an externally painted light image a native migration.
Keep protected source selection in the shared resolver. Produce an isolated
review snapshot first; do not silently overwrite production timing.

Next test should include the end of the singing shot, the receiver arrival,
the knob interaction and NOW punctuation so continuity can be judged together.

Continuation detail found during implementation: screen_garden_trial/tracking.json
contains176 frames, versus119 in receiver_now_v3/tracking.json. Its broader vocal
normalization changes shared voice values by at most0.01535. Preserve the actual
selected treatment on each side of the cut; do not silently substitute one
tracking/voice file for both. Its record119 maps to song1201.
