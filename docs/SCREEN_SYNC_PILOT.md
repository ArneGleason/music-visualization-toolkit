# Screen replacement driven by the music: first effects test

Status: owner likes complete replacement, phosphor persistence, beam-speed
weighting, and amber/cyan. Latest revision fixes amber's axis and gives cyan
larger deflection, broader axis motion, and energy-spreading defocus.
Test one element; expand only after reviewing what it teaches us.

## Fixed amber and defocused cyan

Latest owner direction combines two messages: keep amber fixed and modestly
boosted; give cyan greater amplitude and a more tilted, wider wobble; emphasize
central deflection slightly. Cyan should appear dimmer because an unfocused
beam spreads its light over a wider area, giving separation and suggested depth.

Run `tools/screen_sync_phosphor.py --profile depth` inside Blender. Previous
renders remain intact; new media goes to `out/screen_sync_depth/`.
`comparison.mp4` alternates previous dual-channel and revised versions twice
(276 frames / 11.5 seconds). `dual.mp4` is the revised single passage.

- Amber's axis is fixed at 0 degrees with a fixed vertical offset; amplitude
  scale increases from 88 to 96 reference pixels.
- Cyan's amplitude scale increases from 59 to 112 pixels. Its axis follows
  `12 + 16*sin(t*1.25 + .55)` degrees, beginning at about 20 degrees and
  ranging through a wider tilt during the passage. This is an artistic
  axis skew; it does not rotate the underlying screen or reference marks.
- Both signals retain their per-excerpt normalization, source offsets,
  phosphor lifetimes, and dwell model. Gain does not pump independently on
  every frame or note.
- A gentle center-weighted gain reaches 1.20 at the middle and returns to
  1.00 at the lateral edges. It magnifies displacement from each trace's own
  axis. This approximates the requested lens-like emphasis without warping
  the photographed console or adding a full-camera fisheye.
- Cyan's accumulated light is convolved with a unit-sum Gaussian (sigma
  7.5 pixels on the 768-pixel phosphor texture). Cyan's color/exposure factors
  remain unchanged. The operation spreads light and lowers peak radiance;
  the screen aperture then clips any spill at the rim. This is separate from
  phosphor persistence and spatial supersampling.
- Per-frame `dual_energy.json` records cyan energy and peaks before and after
  spreading, before the final aperture mask, so the defocus can be checked
  independently of appearance. Full settings are in `parameters.json`.

Verification: all 69 frames retain essentially the same integrated cyan energy
before final aperture clipping; peak radiance falls to 31–45% of its focused
value (39% average). The comparison contains 276 video frames, with both audio
and video starting at zero and lasting 11.5 seconds.

The preview gives cyan a more diffuse, visually recessed layer while amber
remains the sharper reading. This is a creative depth cue on the same screen,
not a simulation of a second physical tube. Await owner review of the motion
and amplitude balance before promoting the revision to other screens.

## Phosphor and two-channel study

Owner direction: the beam should become brighter, broader, and more bloomed
where it travels slowly across the screen; fast vertical travel should produce
a finer line. Improve the ends of the trace, add actual phosphor persistence,
and make glass dirt and subtle peripheral calibration more tangible. Also
explore two differently colored audio signals, preferably mostly horizontal
with a little relative axis drift rather than a rigid cross.

`tools/screen_sync_phosphor.py` implements one controlled comparison:

1. Previous textured replacement, unchanged as a baseline.
2. Single amber bass trace with the new screen behavior.
3. Amber bass plus a quieter cyan trace from the drum body's 25–240 Hz band.

Local movie: `out/screen_sync_phosphor/comparison.mp4` (sequence repeated twice,
414 frames / 17.25 seconds, 1280x720, identical master excerpts). Separate
`single.mp4` and `dual.mp4` are in the same folder. This is still the approved
still with the shared slight camera move; it does not test moving-plate tracking.

Implementation and review notes:

- The simplified dwell proxy is `1 / sqrt(1 + (dy/dx)^2)` for a constant
  horizontal sweep. It drives both intensity and core/halo width. Small
  direction changes are taken from the audio, not random line animation.
- The beam now extends across the glass aperture and is softly clipped at
  its curved edge. It no longer ends in a blunt tube cap inside the screen.
- A light buffer accumulates and decays at eight updates per movie frame
  (192 Hz). Fast and slow components have 30 ms and 160 ms half-lives;
  the current beam remains visible over that history. It is primed with
  preceding audio so the screen is already operating when the shot starts.
  This replaces the two explicit old-curve copies in earlier tests.
- Persistence is a temporal effect, separate from the retained 2x spatial
  supersampling. The display models brightness accumulation and decay;
  it does not simulate every aspect of an electron tube. For the reference
  distinction between intensity grading and persistence, see
  [Tektronix's explanation](https://www.tek.com/en/support/faqs/how-dpo-technology-different-persistence)
  and [oscilloscope display types](https://www.tek.com/en/documents/primer/oscilloscope-types).
- Soft amplitude compression prevents artificially flat clipped peaks.
  The existing stem offsets are applied once for both channels. This is
  an artistic display derived from the real signals, not a calibrated scope.
- Fixed glass dust/scuffs overlay the light, with faint phosphor grain.
  Peripheral ticks and a subtle ring replace the full center graticule.
  Dirt remains attached to the screen; it does not flicker randomly per frame.
- Both dual-channel axes remain near horizontal, with small different offsets
  and slow drift no greater than 1.1 degrees. The emitted colors add where
  they meet. Cyan is deliberately subordinate to amber; the two-channel
  treatment is optional, not a new requirement for every instrument shot.

Inspect the new beam on flat, steep, and decaying portions, then judge whether
the second channel adds musical information or makes the screen too busy.
Moving footage and a perpendicular X/Y composition remain future possibilities.
Record the preference and carry the chosen method to another situation rather
than defaulting to another round on this same excerpt.

## Replacement refinement

Owner feedback: complete replacement is better; add more screen texture from
the source image, a less uniform beam width, and smoothing. The first replacement
is already acceptable and remains available as the comparison baseline.

`tools/screen_sync_refine.py` keeps the same bass samples, song alignment, and
camera movement. It samples a trace-free patch of the approved screen at image
coordinates [645,405]–[745,485], mirrors it to avoid hard repeat seams, and
blends it into the clean display. This recovers some photographic texture;
it is not a reconstruction of all original glass reflections.

The beam has gently varying radius, including more thickness where vertical
travel slows, with deterministic slow irregularity and softer, fainter
persistence. Cubic interpolation smooths the sampled contour. Rendering at
2560x1440 and downsampling to 1280x720 provides 2x spatial supersampling per
dimension; temporal sampling remains 24 fps.

Local review: `out/screen_sync_refined/comparison.mp4`, old replacement then
refinement, twice, with the same master excerpt (276 frames / 11.5 seconds).
The revised single passage is `out/screen_sync_refined/refined.mp4`.
Review this refinement, record the lesson, then advance to another section
as planned rather than continuing to polish this one in isolation.

## First rendered comparison

Local review: `out/screen_sync_pilot/comparison.mp4`, 1280x720 at 24 fps.
Original, A, B, then repeat: six 69-frame passages, 414 frames / 17.25 seconds.
Each uses the exact same master excerpt and a shared slight push/drift.

- Original: approved still with its static invented amber waveform.
- A: original screen interior replaced with shaded glass and a subdued grid;
  an amber trace displays the real band-limited bass.
- B: original screen dimmed, with a cyan bass trace over it. The underlying
  invented waveform is static in this test, not generated moving footage.

Implemented in `tools/screen_sync_pilot.py`, rendered inside Blender with no
add-ons or paid generation. Signed bass samples are filtered to 25-180 Hz and
sampled at 8 kHz; the 64 ms display window uses a rising-crossing trigger search
bounded to +/-6 ms. The stem's recorded 0.178348-second offset is applied once.
Two short persistence traces follow the current line. Parameters are also
saved locally under `out/screen_sync_pilot/parameters.json`.

Technical review: active and quiet frames show changing bass shape and settling
to a line between notes; camera movement carries plate and trace together.
The comparison is assembled from the master audio directly to avoid repeated
AAC padding at its joins. Owner listening review still determines perceived
timing and the preferred visual treatment.

Visual findings: B retains more photographic surface detail but has competing
traces. A makes the response clearer, while its reconstructed glass is smoother
than the original. Actual moving-screen tracking and restored fine glass
reflections remain untested. Do not treat this proof as final screen cleanup.

Reproduce with Blender in background mode running
`tools/screen_sync_pilot.py`; `--preview` renders one frame per treatment and
`--assemble-only` rebuilds the comparison from existing rendered snippets.

## Intention and choreography

The instrument appears to be measuring the music in this world. A warm amber
trace responds to the bass being heard at that exact song moment. Its shape
comes from the signal; its persistence, brightness, and containment make it
feel like light inside the existing glass.

Start with s002, `obs_console_macro`, the opening console close-up. At 24 fps
its current picture interval is [86, 155), about 0:03.583–0:06.458. Use these
rendered frame boundaries rather than independently rounding the shot duration.
The approved image is `codex/out/obs_console_macro_b.jpg`: a large near-frontal
round display, amber trace, grid, curved glass, and a strong brass rim.

The saved bass waveform summary has activity in this passage. Use bass alone
for this first test. The opening precedes the first sung line, so a lead-vocal
trace would not be a useful first demonstration.

At bass attacks the trace gains amplitude; as the note decays, the display
settles. The latest model derives local brightness from beam dwell, so quiet,
nearly flat portions can glow more strongly than steep, energetic portions.
Use a stable triggered sweep and short
phosphor persistence so it reads as an instrument instead of changing randomly
on every movie frame. Do not animate the dials, valves, or surrounding light
in the first test. This is an audio-derived artistic instrument, not a claim
of a calibrated measurement display.

## Implementation requirements

- Source: the DAW-aligned bass stem. The 40 Hz peak/RMS summary is enough to
  inspect activity or control an envelope, but cannot reconstruct a waveform.
  Use signed audio samples for the line shape, with documented band-limiting.
  The existing 720 Hz performance signals can support a deliberately
  low-frequency display; use native-rate samples for a wider-band display.
- Alignment: the saved bass reference has a 0.178348-second offset. Use the
  project's existing stem-to-master mapping and verify it with an audible
  attack. Do not ignore the offset or apply it twice. Musical time comes from
  the master timeline; picture tracking comes from the selected source take
  and its in-point.
- Trace: a configurable short window of the real signal, initially around
  40–80 ms, with a consistent trigger such as a positive-going zero crossing.
  Trigger stabilization may choose nearby samples inside that window; keep
  any permitted shift bounded and record it. A slower amplitude envelope
  controls the visible attack. Evaluate temporal samples within the movie
  frame if needed to avoid flicker; 24 fps does not show every audio cycle.
- Old display: replace the invented waveform and its baked-in glow with a
  clean dark screen interior. Simply adding a second trace would leave two
  conflicting signals. Reconstruct the low-frequency screen shading and grid;
  preserve recoverable glass reflections, dirt, and edge falloff.
- Placement: mask inside the brass rim. Begin with a fixed surface on the
  approved still. On motion footage, track the display plane and inspect the
  fit through the entire shot. Use a warped mesh or local corrections if the
  generated display changes shape; a rigid four-corner mapping cannot repair
  arbitrary deformation.
- Integration: draw the trace as emission, with tight bloom and subtle
  persistence. Restore glass/reflections over it, apply screen curvature if
  visible, and match softness and grain. Keep the rim and foreground objects
  above the new display. Avoid a black patch that erases the glass.
- Blender: use a simple plane or shallow curved surface for the display, and
  masks/compositing for the replacement, glow, reflections, and occlusion.
  The existing VSE is the edit/assembly layer; this screen treatment needs a
  dedicated scene or compositor setup beyond the current beat-pulse strips.
  Do not build a general compositor or reconstruct the whole set for this test.
- Deliverable: a short original/replaced comparison with the same master audio
  and neighboring picture context. Also keep a diagnostic trace-on-black
  render and mask view for checking alignment, separate from the normal review.

## Two checks of the same element

1. Still-plate proof: use the approved image and exact song interval to test
   the signal, old-trace removal, glass integration, and overall readability.
   This does not establish that motion tracking works.
2. Moving-plate proof: when a suitable generated console take is available,
   apply the same signal and display treatment to its actual motion. Check
   tracking, warping, occlusion, and source-to-song mapping. The saved shot list
   had no assigned console clip when this plan was written; check fresh files
   before selecting the plate.

Keep the first pass to one chosen treatment, plus the original for comparison.
After one targeted correction, record what worked and move to a different
situation. Do not expand a still-plate success into a claim that every generated
screen can be replaced equally easily.

## What we judge

- Does the trace visibly respond to the bass heard at that moment?
- Has the previous invented trace disappeared, including its old halo?
- Does the new light sit behind the glass and stay inside the rim?
- Does it feel alive without jitter, clipping, or distracting exposure pulses?
- On a moving plate, does it stay attached through the whole shot?
- Can we swap a take or move a cut by changing the plate mapping without
  re-authoring the musical behavior?

## Open parameters and reusable records

Keep musical intention separate from the plate-specific solution. A future
effect record should include: effect ID, shot/setup, intention, musical driver,
song-frame span, behavior parameters, implementation method, source plate
path/version or hash, take song origin and in-point, mask/track assets,
review render, findings, and status (proposed/tested/accepted/applied).

A replacement clip may invalidate its mask and track. It does not automatically
invalidate the bass mapping, choreography, or lesson learned. Recheck the
geometry on each new plate.

## What follows this test

Use the result to decide the next distinct experiment. The receiver screen
(s010) can translate an arriving signal into a different display behavior;
water ripples test surface motion and depth; the telescope tunnel tests
3D geometry. Reuse the timing and review machinery, while letting each scene's
purpose determine the visible technique. The earlier multi-effect river-chorus
plan becomes a later integration test.
