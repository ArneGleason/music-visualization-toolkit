# DAW-driven visual effects plan

Status: creative direction for review before implementation.

## The idea

The music should appear to be part of the physical system of Mars, not a HUD,
equalizer, or particle layer pasted over the finished video. Light can carry a
note, water can carry a drum hit, architecture can tense with a guitar pluck,
and a bass phrase can change the apparent weight of a landscape. The source of
each response should feel native to the shot.

This is a post-production layer. It uses the same DAW-aligned data as the
original vector visualization, so effects can land on exact notes and drum
events even when generated motion footage cannot.

## A small visual orchestra

| Musical source | Visual role | Typical behavior | Avoid |
|---|---|---|---|
| Bass | Gravity and mass | Slow pressure through water, roots, shadows, or the horizon; broad deformation from smoothed amplitude | Full-frame brightness pumping |
| Low drums | Impact | A localized ground, water, glass, or lens ripple on a hit | A generic screen shake on every kick |
| Mid drums | Structure | Seams flex, columns snap into alignment, a current changes direction | Cutting or flashing on every hit |
| High drums | Fine energy | Brief glints along real edges, spray, sparks, pollen, or stars | Full-screen strobes and confetti |
| Diva MIDI | Emissive performers | Selected notes become luminous filaments or small scene-native actors; pitch chooses height/lane, duration chooses trail length, velocity chooses bloom | Continuous note rain |
| Guitar AG MIDI/signal | Tension and connection | Lines or ribs briefly join real objects, recoil on note-on, then decay | Another copy of the Diva language |
| Lead vocal | Articulation and permission | The lyric typography remains primary; the phrase gate can reveal or admit an effect, and the fine vocal signal can subtly disturb an existing contour | A second literal vocal visualizer competing with the words and lip sync |
| Backing vocals | Echo and reply | Peripheral or delayed traces, paired lights, or ghost contours during actual call-and-response passages | Constant doubling |
| Master | Scene-wide ceiling | Very slow changes to halation or color density at structural boundaries | Beat-by-beat global exposure changes |

The exact DAW notes should be used selectively. Accuracy is valuable because a
visible event can truly be a played note; restraint is valuable because not
every available event needs to be visible.

## Rules that keep it photographic

1. Give each shot one dominant musical behavior and at most two supporting
   behaviors.
2. Attach effects to a surface, object, volume, or depth layer: water, sky,
   glass, a radio screen, a shop window, a plant bed, or the space between two
   people.
3. Let an effect persist long enough to become a motif—usually four to eight
   seconds—instead of replacing it on every cut.
4. Keep the lyric plane legible. Effects may pass behind the words or appear to
   be conducted by the active word, but should not distort the letter shapes.
5. Use section boundaries for the largest transformations. Use individual
   notes and transients for local motion.
6. Preserve the existing warm halation and restrained Technicolor palette.
   Surfaces may respond to sound, but should not suddenly look like a different
   material.
7. Prefer a meaningful silence in the effects to continuous proof that the
   analyzer is running.

## First pilot: the river chorus

Use the existing local motion review `out/chorus_motion_v4_retimed.mp4`, covering
approximately 2:14.5 through 2:37.4. It already contains water, swimmers,
performance close-ups, an overhead formation, and a percussion-led fountain
shot, so one short test can expose the important compositing problems.

| Shot(s) | Proposed dominant response | Supporting response |
|---|---|---|
| `s041` basin descent | Selected Diva notes arrive as turquoise-gold filaments between the swimmers | One low-drum pressure ring travels through the water rather than across the whole frame |
| `s042` lagoon-shore vocal | Keep the singer and lyrics quiet and readable; bass slowly deepens the water's caustic weight behind her | Phrase-gated background glow, never on the face |
| `s043` overhead formation | Low drums launch concentric water displacement from the formation's center | High drums send small silver glints along swimmer contours |
| `s044` surface ring | Backing-vocal entries create delayed points of light around the ring | The Diva filament motif resolves into the geometry already made by the swimmers |
| `s045`–`s046` chorus close-ups | Deliberately sparse: lip sync, face, and lyric animation lead | A slow bass response remains in the distant environment only |
| `s047` overhead return | Reprise the concentric ripple with slightly greater reach | A few exact notes bridge neighboring swimmers |
| `s048` drum wall | The most explicit percussion visualization: low, mid, and high bands act on water depth, side currents, and spray/glints respectively | No extra note layer; percussion gets the frame |

The first review should compare the unaltered clip with one restrained effects
version. An expressive version is useful only if the restrained pass proves too
quiet; making three equally elaborate versions would obscure what we are
trying to learn.

## Practical build

1. Export the compact performance controls from the local DAWproject and six
   stems. This produces deterministic bass, drum-band, guitar, vocal, and MIDI
   event data; it does not render media or call a paid service.
2. Add an effects-only mode to the existing browser visualization renderer.
   Reuse its oscilloscope, note actors, ribbons, caustics, membranes, and
   current-field ideas, but render only the selected scene effects over alpha
   or black.
3. Track a small per-shot effects map in JSON. Each entry names the allowed
   drivers, its dominant behavior, and simple screen-space regions or anchor
   paths such as `water`, `sky`, `background`, or `screen`. The shot list stays
   the edit source of truth.
4. For the pilot, use broad masks and a few keyframed anchors in Blender rather
   than attempting automatic object tracking throughout the song. If the
   result needs tighter surface attachment, solve that problem on one shot
   before expanding it.
5. Render the effects layer at the edit's exact 24 fps frame range, composite it
   over the motion chorus, and keep the existing lyric pass above it.
6. Review for four things: musical precision, scene attachment, lyric/face
   legibility, and whether the effect disappears gracefully when it has
   finished speaking.

## Expansion map if the pilot works

- Signal exchange: waveform and note traffic live inside scopes, radios, and
  the probe path.
- Garden: selected notes act as bioluminescent seeds; drums propagate growth;
  bass gives roots weight.
- City and shop: guitar plucks briefly connect windows, wires, and display
  objects; backing vocals answer from peripheral lights.
- Rocket arrival: percussion appears as localized exhaust pressure and ground
  response; bass changes the apparent atmospheric weight.
- River chorus: water, swimmers, and fountains become the fullest ensemble.
- Outro: the musical network simplifies into a few phonetic traces, television
  light, and the existing tunnel/horizon motif before going quiet.

## Approval gate

Do not propagate the system across the full song until the river-chorus pilot
answers these questions:

- Does it feel embedded in the photographed world rather than overlaid?
- Can the viewer perceive the musical relationship without being asked to
  decode it?
- Are the words and faces still the clearest elements when they need to be?
- Is there enough contrast between rigid, architectural responses and rubbery,
  organic ones?
- Would removing half the effects make the idea stronger?
