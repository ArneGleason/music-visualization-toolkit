# Narrative vector video

`video/` is the project-aware browser renderer for illustrated music-video
scenes. It keeps the existing deterministic capture contract while using the
authored timeline register and compact DAW-aligned waveforms instead of the
older abstract instrument actors.

## Completed project: Rivers of Mars

[![Watch Rivers of Mars](../projects/rivers-of-mars/thumbnail.svg)](https://youtu.be/FxzgJe0L55Y)

The completed 3:23.708 video is [published on YouTube](https://youtu.be/FxzgJe0L55Y).
The final local master is 1920×1080 at 24 fps with 32 temporal samples per
output frame, H.264 CRF 14 using the slow preset, and 48 kHz stereo AAC at
320 kbps. That is 4,889 output frames and 156,448 sampled exposures. The
register contains 184 timed items: 87 lyric cues, 15 scenes, 15 transitions,
63 choreography blocks, and 4 production notes.

The final HD proof exposed two resolution-dependent bugs before the full
render. The renderer now keeps a fixed 480-unit logical design height while
scaling the output canvas, including Canvas properties such as blur and shadow
that do not follow transforms. Temporal samples use an exact running average
instead of additive compositing, which preserves translucent glows rather than
turning them into saturated slabs at high sample counts.

Rendered media remains outside Git. The public upload is the durable result;
the compact register, renderer, thumbnail source, and regeneration command are
kept in `projects/rivers-of-mars/` and this repository.

## Design record

### Rendered opening sequence

The first thirty seconds, from `2.4` through `13.1.720` (0.00–29.95
seconds), now have a contiguous ten-shot score in the register and a matching
renderer sequence, `sequence-opening`. The first image is a forceful chromatic
exposure rather than a dark lead-in. Peach,
cyan and violet remain visible inside the near-white field as curved rays gather
the entire image into one hot point over roughly half a second. That same point
unfurls into an oscilloscope whose fine contour displacement comes from the
actual Guitar, bass and three drum-band signals. The trace fills the frame by
about 0.9 seconds, then its warm waveform sections reorganize into Them 1's two
eyes and mouth. Them 2 condenses later from the cool residual branch, preserving
the warm-left and cool-right identities used in the outro while making Them 1
the clear destination of the opening transformation.

The remaining instrumental lead-in assembles detached eyes and mouths at the
ends of those signal branches while twelve curved fragments make a restrained
Busby Berkeley fan and tilted ring. The arrangement is hypnotic but not
static: the camera rises toward an overhead pattern, arcs back into
three-quarter depth, and leaves one conspicuous position empty before landing
on Them 1 for the first lyric. Cropped percussion rings, one rust planetary
limb, a recursive leaf vein, a bowed river line and exact-note lights appear
only as peripheral omens. None becomes the primary Mars, garden, river,
network or Time Tunnel image before its later reveal.

From “Hey, I need you for something” through “More than that sounds,” the
opening mirrors the outro's two-perspective grammar without yet becoming a
call-and-response. Them 1 speaks in a large warm left-side setting; Them 2 is
a cool listener in a separate depth and never mouths Them 1's words. One
travelling contour hands attention between them during the silent gap. Them
1's final oscilloscope mouth contour then thickens into the first tangible
puzzle piece.

Across “I've got pieces,” the objects perform the opening's clearest Berkeley
formation: exact notes seat curved pieces into concentric fans and travelling
diagonals, with pitch controlling radial height and color, duration controlling
body length, and velocity controlling scale. “Things that almost fit” breaks
the fan into readable pair tests. On “Then they don't quite match,” the best
near-circle reveals only secondary Mars striation, river current and garden
venation; its failed seam folds the same material into courier shells. At
`13.1.720`, the camera passes through that seam directly into the existing MIDI
package and routing-network scene.

The opening also has a strict motion contract. Camera movement must reveal a
formation, commit to a subject, compare two pieces, transfer attention, or
arrive on a visible consequence; undirected pan-and-zoom drift is not enough.
Adjacent moves preserve their boundary direction, while lyric and arrangement
turns supply meaningful context refreshes. Every shot maintains at least two
independently moving environmental depth systems with unequal musical drivers
and parallax. These may be cropped drum rings, bass horizons, note bodies,
backing-vocal echoes, rust bands, current lines, leaf veins, offscreen
fragments, or star and dust motes. They remain peripheral counterpoint rather
than synchronized wallpaper.

An intentional void is reserved for anticipation, absence, a missing fit, or
an attention handoff. It is never a completely inert background: sparse motes
continue through several depths, surrounding contours create a negative wake,
and held performers retain gaze, breath, line boil, or unequal follow-through.
The centre remains quiet enough for the void to keep its narrative meaning.

The MIDI-led routing-network prototype is `scene-mtejqrtr`, from `13.1.720`
to `16.1.480` (29.95–38.33 seconds). This passage was selected from the exact
Diva events because it contains 79 notes, 22 distinct onset times, a
41-semitone span, varied velocities, up to ten simultaneous pitches, and
sustains as long as 1.62 seconds. The notes are primary actors rather than a
background visualization: pitch determines vertical lane and hue, sustain
determines physical body and memory-tail length, velocity controls scale,
bloom and apparent force, and shared-onset notes remain connected as a chord
formation.

The three shots also share one restrained phrase-scale camera journey. It
starts weighted toward the package gate, eases forward and right with the
large chord procession, then withdraws around the empty receptor before
drifting toward the wrong peripheral branch. Matching boundary keyframes keep
the pan, zoom, pitch and roll continuous while the local note choreography
continues independently. This is an authored attention handoff rather than a
constant camera preset or a camera response to every MIDI onset.

Three register-authored shots shape the passage. The package shot folds the
preceding puzzle fragments around the incoming notes. The flight shot tracks
large chord bodies through elastic routing gates; the ten-note event at 32.816
seconds stretches several gates open as one formation. At 34.436 seconds the
measured note traffic stops while “Tell me what you got” begins, so the loss
shot gathers the final four-note `Guitar AG` chord into one large curved packet
and chases it along a primary S-route. The camera gets close enough to read four
pitch-class-colored nodes inside the shell; duration determines their curved
wake length and velocity determines bloom. Exact beat positions become
elliptical route gates with four subdivision ticks, and each gate pulses when
the packet reaches its timing region. Quiet secondary branches retain network
context without competing with the packet.

The route's intended continuation points visibly toward Them 2 as a small face
in the distance. At the final gate, the active line snaps sharply right and the
packet leaves the frame, while the intended line remains faintly lit toward the
unused endpoint. The camera does not follow the error; it continues forward
toward Them 2 as instrument-mapped star depths replace the network.

The receiver bridge is `scene-mtejt6in`, from `16.1.480` to `21.3.480`
(38.33–53.98 seconds), and is exposed with its incoming loss shot and outgoing
garden threshold as `sequence-network-loss-through-garden`. Its five shots are
waiting starfield, phase demand, raw scan, constructive interference, and garden phase
plate. The first frame is the exact end state of the routing-network loss shot,
seen from the receiving side; the last receiver frame contains the exact opening
garden frame. This makes the bridge a material handoff rather than a reset.
“I don't see anything” begins only after the packet has taken the wrong branch.
Them 2 grows continuously from the route's distant target into a medium-close
eyes-and-mouth performance. There are no hands, packet, knot, phase plate or
substitute object in this shot; the gaze checks the approach direction, pauses,
and searches the surrounding star depths.

That empty space is a musical environment rather than inactive backing. Large
coral near stars respond to the low drum band; cyan middle-depth stars respond
to the mid band; small violet distant stars carry high-band detail; slow gold
stars use bass energy and the largest parallax. Exact Diva pitches create
separate colored note stars at pitch-derived heights, with velocity controlling
depth and bloom. The camera's slow drift makes the depth layers visibly unequal.

The transition's optical device is a transparent asymmetric phase plate. Two
slightly displaced copies of the scene, cyan/gold contour families, and signed
mid/high drum displacement create restrained birefringent interference. It
does not appear until “If you've got it, give it,” when bass, drums and broad
Diva notes gather several star depths into a working field. The background
remains readable and no object is hidden behind it. The macro “Don't clean it up first” insert
preserves uneven moiré seams and phase error instead of using a generic glitch.
When Them 2 begins work, the same errors acquire stable crossings: exact
`Guitar AG` note-ons light the crossings, pitch determines their height and
shared color mapping, duration retains their curved probes, and velocity sets
bloom and apparent depth. Broad Diva notes remain slower caustic bands.

During “We'll see what's your deal,” dense guitar contacts become luminous
seeds, the interference contours fork into leaf venation, and the phase-plate
rim becomes the first percussion Time Tunnel ring. The plate expands beyond
all four frame edges, revealing the static opening garden frame inside its
existing boundary. A low-opacity displaced-image and contour remnant then
persists across the first garden beat, so the optical overlay augments the
bridge and supplies the garden's construction system rather than disguising a
weak cut.

The first `Rivers of Mars` movement, from `49.1` to `55.3.720`, is the initial
biological-motion retargeting prototype. A six-second high-activity window from
CMU Motion Capture Subject 125, Trial 6 (freestyle swimming) is reduced from
120 fps Acclaim data to a compact 30 fps, ten-control upper-body motion clip.
The capture rig is never the visible design: shoulder and spine relationships
drive one chrome body ribbon, wrists drive detached fin arcs, and head movement
carries detached eye and mouth marks. The capture ends cleanly at the waist,
where a procedural flagellum uses exact DAW beat timing: bass energy shapes the
broad S-wave and selected drum energy sends tighter impulses toward the tip. The same
clip is reused in the overhead production number with unequal phase, speed,
mirroring, path, scale, and depth so the ensemble shares a movement language
without exposing synchronized clones.

Swimmer translation and captured pose are coupled rather than animated as
separate layers. Every frame samples the root path on both sides of the current
position and rotates the head-to-tail axis onto that tangent, so a swimmer always
faces its propulsion. Depth is conveyed by unequal scale, opacity, path velocity,
cross-section, and draw order across a sparse school. Continuous pan/zoom/crane
moves oppose or follow that travel, giving the otherwise graphical river visible
parallax without changing the established chrome-and-flagellum identity.

The river is not a fixed background spline. Four broad color masses and eighteen
fine current contours sample one animated flow field. Two low-frequency waves
move the stable S-shaped geography through time; per-strand phase and velocity
offsets add restrained convergence, crossing, and separation. This motion stays
slower and broader than the flagella. Smoothed bass and master energy change its
mass, while drum transients remain reserved for the smaller travelling notation.

The flow field spans from −0.58 to 1.58 frame widths and the terrain polygons
extend still farther, so camera widening and roll never expose a rectangular
panel edge. Five broad masses separate through lane offset, brightness, glow,
width, and slight lateral slippage to imply different water depths. The former
free-floating scratch ripples have been removed.

All river swimmers use global scene time rather than per-shot progress. Their
root positions, depth, facing, and capture phases therefore survive camera
boundaries unchanged. A cycle wraps only between far-offscreen endpoints.

Every exact Diva event becomes a curved note ribbon travelling counter-current
at one shared speed. Pitch class uses the same twelve-color `NOTE_COLORS` mapping
as the earlier WeBe-derived MIDI effects; absolute pitch determines vertical
current tier; duration determines the amount of river-following ribbon behind
the head; velocity determines bloom. A smaller stable depth component affects
scale, glow, and draw order without replacing pitch height. Simultaneous chord
notes consequently remain parallel, separated, and individually colored.

Eighty-two soft flow motes occupy the same animated field. They are dots rather
than scratch marks: depth changes size, opacity, and a small amount of lateral
speed, producing parallax across the river without radial motion toward camera.

Nine register-authored shots test the idea at different scales: a moon-to-river
descent, a large lateral swimmer entrance, a hard-cut macro journey inside one
current, a low waterline tail close-up whose musical flagellum changes emit
notation ripples, a sustained Spirograph bend, a detached-mouth microcosm, a
multiband drum wall, a low-angle guitar vault, and a chorus plunge.
The macro shot begins on the lyric “in the rivers of Mars” and makes individual
note ribbons, onset eddies, orbiting motes, and cropped swimmer fragments
readable before cutting back to the uninterrupted wide river clock. Across
“that bends your mind,” the live river contours progressively close into nested
hypotrochoids rather than exploding or dissolving. The completed moving iris is
the match-cut source for “Tiny mouths all agape”: its lines recede to background
billing while twelve camera-facing lips, exact-note arcs, and a slow push, drift,
and roll establish a new micro-scale shot without discarding the river material.
Add `motionDebug=1` to the video renderer query to expose the otherwise hidden
point-light controls for review. The reusable import and provenance workflow is
documented in `docs/MOTION_CAPTURE.md`.

The post-Spirograph wall-of-sound chorus spans 156.88–167.90 seconds and is
exposed with its incoming bend as `sequence-spirograph-through-wall-chorus`.
The first new shot stretches inherited mouth-orbit paths into eleven curved
seams between four flexible full-frame drum membranes. Signed control signals
from separately filtered low, mid, and high bands of the real drum stem give
the floor, side walls, canopy, and travelling edge glints different physical
jobs; they are not alternate renderings of one generic transient envelope.

The DAW's `Guitar AG` MIDI performance is exported as `guitar-notes`, preserving
note-on, note-off, pitch, velocity, and the exact tempo-ramp clock. Guitar notes
become large tensile ribs with pitch-class color, pitch-derived height,
duration-dependent retention, velocity bloom, a luminous note-on contact, and
narrow vibration from the signed guitar-stem signal. The frontal drum wall
rotates into a low-angle guitar cathedral, then its accumulated ribs curl into
a full-depth tunnel around a featured eyes-and-mouth vocalist. Sustained Diva
notes remain separate broad color columns behind the sparse plucked structure,
while four motion-capture swimmers maintain scale and parallax through all
three shots.

The following `scene-current-turns-home` sequence spans 167.90–174.03 seconds
and is exposed with the chorus-plunge handoff as
`sequence-chorus-plunge-through-answer`. It is divided at the lyric verbs into
three compact shots: the inherited tunnel curls through an off-centre guitar
switchyard on “turns”; one luminous route recruits lanes, exact-note traces,
and swimmers in staggered order on “follows”; then a reverse angle reveals two
distant respondents on “answers.” The singer remains a warm-gold, cropped
camera-side narrator rather than the main spatial subject. The respondents use
separate cyan and peach identities, so their reply cannot be mistaken for
another view of the narrator.

The turn follows the song's busy/quiet/busy contour. Exact Guitar AG notes
branch at the switchyard hinge with pitch, duration, velocity, and signed stem
vibration intact; three flexible rudders respond independently to the low,
mid, and high drum bands; broad Diva sustain supplies the current's interior
mass; and bass maintains continuous travel. The quieter middle leaves negative
space around the leader. When drums return during the answer, they remove
color and detail in successive bands instead of adding another impact layer,
stripping the field toward the low-light context of the next scene. Camera and
material states are continuous at the chorus boundary, so the change reads as
one formation turning rather than a reset.

The completed dialogue and signoff outro spans 174.03–199.25 seconds and is
reviewable with the preceding answer as `sequence-answer-through-outro`. Nine
lyric-aligned shots alternate two genuinely different vocalist perspectives:
Them 1 is a warm-gold, left-cropped face inside a flowing cyan current cavern;
Them 2 is cool cyan at frame right against peach-magenta drum tunnels and
rotating world bands. Cuts reverse vanishing point, palette, screen direction,
shot scale and camera roll. A bass-driven curved horizon graphic-matches the
settings, while each individual view continues its own push, truck, pull or
roll instead of becoming a static talking-head card.

The rhythm section receives two full-stage Time Tunnel passages. Eighteen
travelling elliptical rings and fourteen curved radial seams exceed the frame:
low drum energy dilates their broad rims, mid energy shears their centres, high
energy races glints around their edges, and bass advances the tunnel clock and
camera. Exact Diva notes remain pitch-colored duration ribbons moving through
the architecture. The first tunnel carries Them 1 at the periphery through
“La-la-la, low light”; the later reprise removes the full face and lets opposed
phonetic traces appear briefly on the tunnel walls.

From “Who?” onward, speaker onsets drive editorial crosscuts between a
river-tunnel reprise and rotating Mars-band reprise. “You first / Night /
Night” uses a medium-to-close-to-extreme-close scale cascade. During the final
instrumental breath, both settings withdraw into an empty paired aperture.
The last “Night” reveals both vocalist colors at opposite edges and gathers
tunnel rings, current traces, world bands and note colors into one rotating
guilloche iris. Its final bass sustain collapses continuously to a small
warm-cyan curved afterimage at 199.25 seconds rather than cutting early or
ending on black.

The production coda uses the DAW project's silent tail from 199.25–203.71
seconds. The final afterimage is preserved across the boundary and uncoils into
two shallow brackets around `RIVERS OF MARS`; dim guilloche orbits keep moving
behind the held typography. The colophon records the causality most useful to
a technically curious viewer: a DAW-authored register drove the cuts, voice
shaped faces, three drum bands bent the tunnel, bass carried depth, and MIDI
pitch, duration and velocity became color in motion. Its footer reads
`SCENE-DIRECTED · CODE-RENDERED · NO GENERATED FOOTAGE`. The render pipeline
uses the later of the audio duration and authored scene duration, so a silent
visual coda can continue after the muxed audio stream ends without truncation.

The apparent swimmer hesitation at the first river introduction came from the
camera rather than the swimmer paths: a smooth-step was being passed into a
second easing function at each of the two shared camera segments. Those two
segments now use one linear interpolation across their common keyframe, so the
camera and apparent swimmer travel no longer settle at the handoff; the
biological-motion and river-path clocks remain unchanged.

The opening garden sequence spans the accepted threshold scene and the first
garden scene, from `21.3.480` to `29.4.240` (53.98–77.25 seconds). The preview
exposes it as `sequence-garden-intro` so it plays as one uninterrupted camera
move. The camera dollies through real perspective depth while foreground
foliage expands beyond the lens, new growth appears ahead, and curved stems
recursively split into child branches and leaves.

For long-form pacing review, `sequence-garden-through-mars` joins the garden
threshold, psychedelic garden, pattern-aperture inspection, and Mars unmasking
without altering their authored timing. It spans `21.3.480` to `41.1.240`
(53.98–109.15 seconds), preserving the garden-to-inspection aperture and the
inspection-to-Mars lens crossing so scene rhythm can be judged across roughly
fifty-five seconds rather than from isolated excerpts.

The longer `sequence-garden-through-river` review now continues through the
semantic rocket/weather bridge and the first completed river movement. It spans
`21.3.480` to the end of `lyr-060` (53.98–156.88 seconds), giving a contiguous
102.90-second pacing strip. Intermediate review renders are intentionally not
retained; the same strip can be regenerated from the registered sequence.

The formerly unrendered `scene-semantic-rocket-weather` gap is four authored
shots rather than a generic fallback. Large face-on eyes and phonetic mouths
stage the call and response; exact Diva notes open their orbits into pressure
filaments; dense chords become curved incoming formations and drum-driven
overhead clap fronts; then the two long final notes condense eighteen weather
contours into the existing river currents. Pitch retains the shared twelve-
color palette, absolute pitch controls height, duration writes physical tail
length, note-on drives the luminous head, and stable secondary depth determines
front/back crossing. The final shot composites the actual opening river frame
progressively, making the moon, water masses, star depths, camera orientation,
and current tangents an exact material and geometry match rather than a cut to
unrelated scenery.

The current garden pass adds large abstract swirls whose centres and
trajectories continue beyond the frame, plus recursive plant generations that
continually replace their predecessors. The featured lead has a fast vocal
attack, a short gap hold, and a slow release, so she does not shrink between
words. A separate connected-phrase accumulator allows a prolonged delivery to
keep swelling. Her baseline scale and bloom are larger than the ensemble, and
beat rocking, bopping, plus occasional phrase-entry rolls keep her acting even
when her position is held. Fine lip and bass contour vibration comes from
actual band-limited signed stem samples; it is deliberately much smaller than
the envelope-driven pose so temporal supersampling makes a narrow energetic
edge instead of obscuring the drawing.

Selected exact Diva MIDI notes appear only in the green-light and drum-
awakening shots. They enter as curved seed/moon actors rather than a piano roll:
note-on is the contact time, duration elongates the shape, pitch selects color
and trajectory, and velocity controls bloom. Deterministic thinning and a
small simultaneous-event cap keep dense passages subordinate to the singer.

The combined `sequence-garden-pattern-contrast` prototype joins the
psychedelic-garden and inspection-table scenes, from `23.3` to `35.4.720`
(59.37–94.62 seconds). It deliberately changes almost every scene parameter:
the garden is warm, crowded, radial, curved, continuously growing, and driven
by percussion as architecture; the inspection table is cool, sparse, oblique,
discrete, measured, and driven by selected fragments, scan events, gaze, and
provisional connections. The transition preserves the garden's root rings,
leaves, and note seeds as material, then flattens and sorts them into the table
aperture. That material handoff is aligned to the release of “for the song to
begin” and the new phrase “Okay, there,” so the extreme change remains a
musical and semantic consequence rather than a decorative crossfade.

Four inspection shots cover delivery, pattern testing, the provisional
“world plus more,” and a failed pre-Mars fit. Bass changes table pitch and the
mass of the lifted world; selected drum transients become restrained scan/test
events; vocal phrases alternate the inspectors' detached edge performances and
which fragment is lifted. The final mismatched coral piece crosses the lens to
prepare the following Mars production number.

The inspection scene now has two unmistakable frame contexts. Delivery,
pattern testing, and “Hard to find, right?” remain in the high oblique table
view. On “I see the world plus more,” the camera drops through the near table
edge and swings into a low three-quarter orbit: the grid becomes a receding
horizon, the lifted construction shifts right of centre, and the left
inspector becomes a large cropped foreground witness. This implements the
project pacing rule that a frame context should be reviewed around eight
seconds and ordinarily receive a major lyric- or music-aligned renewal before
twelve seconds, even when the enclosing scene, palette, and objects remain the
same.

The low-orbit context reveals outer space rather than an empty dark backing.
Stars occupy several deterministic depth bands with restrained parallax, while
a small distant spiral galaxy sits away from the fragment-world as peripheral
counterpoint. Selected drum transients create brief stellar births along its
arms; bass changes its slow tilt and weight. The entire fragment-world rotates
coherently around a tilted axis at a much slower rate: projected longitude
changes fragment position, depth order, scale, brightness, and contour angle,
so the viewer can read an Earth-like turn rather than independent pieces
orbiting a static centre.

The percussion layer is also the scene architecture: broad colored annuli,
radial planes, and a full-frame wash form a curved tunnel around an enlarged
root-and-petal membrane. Stroke weight, glow, and solid color area use slower
beat/phrase followers; audio-rate stem data is restricted to fine contour
motion. Near plants and actors acquire stronger glow and weight as they pass the
lens.

Plant roots never terminate at their projected base. A segmented continuation
curves in the opposite direction, changes width and glow as though bending
toward or away from camera, and fades before its endpoint. Near branches and
leaves first draw a dark occlusion underlay, then their luminous contour, so
they interrupt the tunnel behind them instead of adding into the same flat
screen plane. This combines offscreen continuation, dynamic occlusion,
multiplane parallax, relative scale, contour weight, glow, and detail density
without desaturating the background.

Each garden cue now contains a structured `blocking.interactions` score. An
interaction names two stable blocking-element IDs, a normalized cue window,
and the intended approach, deformation or accommodation, contact, unequal
recoil, and follow-through. The renderer uses the score to draw reaches and to
modify the green light, canopy, branch fans, and counter-orbits without
pretending to run a general-purpose physics simulation.

Four register-authored shots drive the sequence: garden threshold, green-light
dolly, branching canopy, and drum awakening. The small guide light, recursive
growth gates, face-on lead eyes and mouth, persistent offstage feature orbit,
unnamed waking space, and visible root-and-petal percussion stage all have
stable blocking IDs. Drum attacks throw root rings and open different petal or
branch banks; the stage remains recognizable at rest rather than appearing as
a generic pulse. Featured performers use independent face-on lids, lashes, and
mouth shapes without enclosing head circles or required body segments.

The Mars segment is `scene-mars-unmasking`, from `35.4.720` to
`41.1.240` (94.62–109.15 seconds). It treats the scene as a miniature filmed
production number: crane-back reveal, overhead double ring, plunging spiral,
diagonal refusal, lateral chorus line, three-ring excavation, and a final
rising kaleidoscope. Phrase boundaries choose the shot; DAW drivers animate
the formation inside it.

The visual mappings are deliberately inspectable:

- lead vocal controls the featured cupid-bow mouth, upper lids, phrase-scale
  swelling, slow release, rocking, and bounded squints;
- backing vocal and drum body send staggered scale and phonetic waves around
  the camera-addressing chorus faces;
- bass changes the mass, flattening, and rotation rate of the Mars ribbon-world;
- master energy controls broad color-river illumination and line bloom;
- thirty-three exact Diva notes become travelling trails: pitch class selects
  the shared twelve-color hue, absolute pitch selects vertical lane, duration
  sets trail length, note-on creates the luminous head, and stable secondary
  depth selects foreground or background passage.

The performer vocabulary is deliberately restricted to the established
face-on eyes and phonetic mouth. There are no small anatomical chorus figures,
head circles, or connected bodies. Berkeley choreography is carried by the
performers' positions and shared formation ribbons: double rings, spirals,
diagonals, processions, excavation circles, and a final nested bloom. Each face
continues to address camera while a controlled cant, phonetic phase offset, and
scale wave travel around the formation.

Mars is inferred rather than outlined. An occluding asymmetric mass contains
broad clipped color rivers; front and back halves of rotating great-circle
ribbons establish depth, and a small open three-arm curl replaces the earlier
closed eye-like centre. There is no perimeter circle with decorative marks.

The seven Mars production shots are authored as detailed choreography cues in
the music-video register. Their camera, formation, and 27 named performers,
formations, objects, and environment elements include explicit entrances,
actions, exits, layers, and motion paths. `video/app.js` resolves shot identity
and cue timing from the compiled register; hardcoded edges remain only as a
fallback for an incomplete project.

The project manifest also registers `refs/Rivers-of-Mars.png` as figurative
and element vocabulary, not footage. Its astronaut silhouette, suit seams,
river, domes, towers, flora, swimmer, planet, and moons are source motifs to be
redrawn and choreographed as original vector linework. The raster reference is
never composited into the final video.

The live preview exposes those five values in the lower-left driver panel.
They are sampled from `projects/rivers-of-mars/generated/waveforms.json`, whose
offsets are derived from the DAW timeline.

`tools/performance.py` writes the complementary
`projects/rivers-of-mars/generated/performance.json`: spelling-derived,
damped mouth channels at 60 Hz, polarity-preserving lead/bass signals at
720 Hz, and selected exact DAW MIDI events with note-on, note-off, pitch, and
velocity. The source stems remain outside the repository. The renderer uses
the high-rate signals only for articulation and fine line deformation; broad
scale, travel, lighting, and pose remain on compact reference envelopes and
the asymmetric phrase follower.

The reusable camera, framing, editing, performance, visual-music, and growth
vocabulary is documented in
`docs/CINEMATOGRAPHIC_METAPHOR_CATALOG.md`. Choreography cues store its stable
IDs in a `metaphors` field so the intended device can be reviewed and revised
without reverse-engineering it from renderer code.

## Preview and render

```bash
./run.sh videopreview
./run.sh videodraft scene-psychedelic-garden
./run.sh videodraft scene-mars-unmasking
./run.sh videotest scene-mars-unmasking
```

The live preview uses `/api/audio` from `tools/timeline_server.py`, so source
audio remains outside the repository. Space toggles playback away from form
controls, the scrubber seeks on the master clock, and the selected scene loops
by default.

`videodraft` renders 854×480 at 24 fps with two temporal samples. `videotest`
uses a 1920×1080, 60 fps, 32-sample diagnostic profile. The published master
keeps the approved 24 fps cadence while using all 32 temporal samples across
each output exposure. All profiles step time deterministically through
`tools/world_render.py`, then mux the locally configured master WAV.

The exporter prints the actual ANGLE/WebGL renderer visible to its Chromium
GPU process and `--probe N` separates page draw/raster time from frame capture
time. This matters even for the Canvas2D prototype: repeated blurred strokes
can remain CPU-heavy while the browser compositor itself is GPU accelerated.
On Windows, system Chrome is the default render browser and `--angle auto`
selects D3D11; `--browser msedge` is also available. This is intentional: the
bundled automation Chromium used SwiftShader on the RTX test machine, while
system Chrome exposed the NVIDIA D3D11 renderer even in headless mode. Treat
the printed renderer as authoritative: RTX/D3D11 is hardware; SwiftShader is
CPU software rasterization.

The renderer supports `post`, `cdp`, `dataurl`, and `element` capture paths.
At draft settings, `--capture post` measured about 33 fps on the RTX 4080
SUPER, versus 3.6 fps through SwiftShader. At 1080p with 32 temporal samples,
frame readback and encoding—not vector drawing—become the dominant cost. The
final master used `--capture cdp` with lossless PNG transfer after the post and
JPEG routes showed no advantage at those settings.

On Windows, use the project environment directly if Bash is unavailable:

```powershell
.\.venv\Scripts\python.exe tools\timeline_server.py --project projects\rivers-of-mars\project.json
```

For a GPU-accelerated draft render from PowerShell:

```powershell
.\.venv\Scripts\python.exe tools\world_render.py --headless --browser chrome --angle d3d11 --capture post --page video --project projects\rivers-of-mars\project.json --section scene-mars-unmasking --fps 24 --blur 2 --width 854 --out out\scene-mars-unmasking_draft.mp4
```

Then open `http://127.0.0.1:8760/video/?scene=scene-mars-unmasking`.
