# FX-04 — musical contour: telescope tunnel

**Decision: owner approved amber/cyan arrivals as the keeper look, reusable FX-04,
and required treatment for s056.** Registered in `shots/assembly_decisions.json`.
Full shot [4396,4535) is 139 frames; approved review [4396,4444) is only 48.
Delivery remains pending, not assembled. Preserve timing, strong waveform and
depth bloom; finish full-length tracking/occlusion and clean export next.

## Alternating amber/cyan arrivals — latest color test

Preview: `out/tunnel_arrival_amber_cyan/tunnel_arrivals.mp4`.
Run `python tools/tunnel_arrival_pilot.py --two-color` (includes intense settings).
Owner requested an exploratory warm/cool alternation, not a rainbow cycle.
First approach is amber; second is cyan. Each event keeps its color while it
travels and decays. Event hues have at most +/-2 degrees of drift on a 12-second
period, sampled at the hit, never a continuous spin through other colors.
The short preview cannot establish the longer-term drift aesthetically.

Muted teal base contours give the arrivals color priority. Warm amber relates
to the brass; cyan contrasts with it. Intensity and hue are composed in linear
light, with natural pale/clipped cores in this SDR preview and colored halos.
Same event timing, ring detection, 10x waveform displacement and depth bloom as
the accepted intense version. Test both approaches before choosing a palette.
Previous monochromatic-green version remains untouched; no assembly change.

## Stronger depth/bloom revision — latest review

Owner liked the arrival timing and analog waveform; requested more intensity,
depth and scattering, with approximately ten times the waveform amplitude.
Preview: `out/tunnel_arrival_intense/tunnel_arrivals.mp4`.
Run `python tools/tunnel_arrival_pilot.py --intense`.

Waveform radial displacement is exactly 10x the prior version, before the
unchanged dwell response. Audio, event selection, half-second approach and ring
detection are unchanged. Near rims gain more emission and thickness; far rims
remain quieter. Three radial depth groups receive progressively broader halos
(tight, medium and wide Gaussian scatter), applied only to the effect, not the
underlying footage. This is artistic optical bloom, not physical light transport.
No new particles or random timing introduced. Prior preview remains available.
Existing per-frame edge identity/occlusion/persistence limitations still apply.

## Multi-ring anticipatory arrivals — latest experiment

Preview: `out/tunnel_arrival_pilot/tunnel_arrivals.mp4`.
Run `python tools/tunnel_arrival_pilot.py`. Same two-second source/song interval.
Two selected actual drum attacks (about 0.54 and 1.07 seconds into the preview)
receive half-second approaches from a 75-pixel distant radius to a 480-pixel
foreground arrival zone. Intensity travels across the detected rims, then decays
over 75 ms after arrival. Actual display timing is quantized to 24 fps.

Guitar-contour modulation remains underneath with depth-weighted brightness,
offset scan heads, dwell width and bloom. This lightweight multi-ring test does
not yet carry forward the single-ring renderer's temporal phosphor history.
Per-frame radial brass-edge detection is used instead of cloning a single ring's
scale: it has no persistent ring identity and can change selected edges between
frames. Authored fixed centre and missing spoke occlusion remain limitations.
Arrival is a fixed screen-radius zone, not a physically solved impact plane.
Review musical travel/readability before refining edge continuity and persistence.
Output verified as 48 frames / 2 seconds; representative arrival frame inspected.
No assembly changes. Previous single-ring tests are preserved.

## Analog contour revision

Owner accepted the basic tracking, requested the scope's analog beam character.
New review: `out/musical_contour_tunnel_analog/musical_contour.mp4`.
Run `python tools/musical_contour_pilot.py --analog`. Original white-line test
remains untouched. Same 48-frame interval and tracking method.

Changes: inverse path-speed dwell controls beam width and brightness; circulating
head at 0.65 revolutions/second has a sharp front and a long exponential tail.
Small deterministic, modulated signal noise and asymmetric soft saturation add
visual harmonic character; master audio is NOT modified. Pale green core and
two halo scales replace the flat white stroke. Two-times spatial supersampling
smooths the line. Six-frame ring-local history supplies a faint 75 ms exponential
persistence: previous traces follow the current tracked ring instead of smearing
with camera motion. This is an artistic analog approximation, not an electron
beam or film exposure simulation. Existing tracking/occlusion limitations apply.

First two-second look test: `out/musical_contour_tunnel/musical_contour.mp4`.
Run `python tools/musical_contour_pilot.py` using the same isolated OpenCV/numpy
dependencies as the receiver test. Not a Blender render or production delivery.

s056, source in-frame 0, song [4396,4444) at 24 fps; only the opening 48 frames
of the shot. One pale drawn contour uses the actual trailing 64 ms guitar waveform
for radial deflection, with selected drum attacks producing a quick radial kick.
Existing camera motion and metal geometry are unchanged. No MIDI note claims.

Tracking is a constrained prototype: optical-flow features on the initial ring
provide radial scale around an authored fixed centre (630,315), matching the
stationary central star in this excerpt. Unconstrained similarity fitting drifted
sideways as feature coverage became uneven. A longer initial test lost confidence
after two seconds, so delivery is limited to 48 frames. The fixed-centre constraint
is not a general camera solve; a full-length version needs stronger ring identity
verification and tracking. First, middle and last diagnostic outlines are saved.
No spoke occlusion masks yet; the line is a graphic annotation above the structure.

Original source remains untouched. The preview is flattened, with master audio;
tracking/control JSON retained. No assembly selection or paid generation changes.
Review the musical look first, then improve tracking/occlusion before expanding.
