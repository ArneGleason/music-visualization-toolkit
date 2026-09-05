# Screen replacement driven by the music: first effects test

Status: proposed next effects experiment, 2026-09-05. No effects render has been
made yet. Test one element; expand only after reviewing what it teaches us.

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

At bass attacks the trace gains amplitude and a modest amount of brightness;
as the note decays, the display settles. Use a stable triggered sweep and short
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
