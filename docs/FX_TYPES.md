# Reusable musical FX types

This is the creative catalogue, not an assembly override. Shot timing remains in
`shots/shotlist.json`; approved picture substitutions remain in
`shots/assembly_decisions.json`. A reusable look approval does not approve every
application or declare a delivery layer ready.

## FX-04 — Analog contours with anticipatory depth pulses

**Owner approved reusable mode and specific application to s056 / telescope_time_tunnel.**
Keeper reference: `out/tunnel_arrival_amber_cyan/tunnel_arrivals.mp4`.
Recipe: `python tools/tunnel_arrival_pilot.py --two-color`.
Details: `MUSICAL_CONTOUR_PILOT.md`.

Musical function: guitar deforms contours along existing rims; selected drum hits
receive approaching light pulses, starting in the distance half a second early
and arriving in front on the beat. Alternate amber and cyan per event, never
rainbow cycling. Preserve strong 10x waveform gain, near/far intensity hierarchy,
broad bloom, dwell response and circulating scan character. Adapt geometry and
musical event choices per new shot; this is not an automatic whole-film overlay.

s056 is protected in `shots/assembly_decisions.json`, with full-shot delivery
pending. Current preview covers 48 of 139 frames. Extend attachment/edge continuity,
review spoke occlusion and export clean full coverage before marking ready.
Do not loop/stretch the preview or omit the FX silently. Original footage remains
the underlying motion source. This approval does not authorize other shot assignments.

## FX-01 — Luminous airflow

### Chrome-swimmer application of tracked/material light response

Owner-approved palette: violet bloom/reflection with pearl-white cores, giving
chrome swimmers a distinct identity from amber/cyan instruments and tunnel.
Full-shot candidates s043/s044/s047 are in `shots/fx_uses.json`; see
`SWIMMER_LIGHT_PILOT.md`. Individual torso tracks and formation-wide silver
selection are distinct implementations, not interchangeable tracking claims.

**Status: owner accepted the full-strength look as a reusable FX reference.**
Garden test: s019 / forest_fauna_eyes.
Reference: `out/garden_airflow_bloom_depth/garden_airflow.mp4`.
Renderer: `tools/garden_airflow.py --bloom-depth` (run through Blender).
Implementation and reproduction: `GARDEN_DUST_PILOT.md`.

Intent: music stirs a scene-filling atmosphere, not a cluster of decorative dots.
Three depth bands separate fine distant dust, active middle-distance motes and
larger, faster foreground material. Bass shapes flow; selected drum attacks
drive disturbances and bright cores with soft bloom. Peripheral coverage,
approximate foliage occlusion and eye protection make it occupy the garden.

Owner decision: preserve this brightness as the full-strength reference. It may
need reducing over the dark still, but could be appropriate over moving footage.
Reassess in context instead of weakening the reference prematurely.

Delivery work still needed:

- Current latest preview is flattened against a still, not a reusable alpha layer.
- Export separate cores, bloom and wisps, ideally with independent depth groups.
- Keep unclipped linear-light emission (prefer half-float EXR) and explicitly
  document alpha association and compositing operations. Use emission gain for
  additive light and opacity for coverage; they are not interchangeable.
- Expose overall amount plus core/bloom balance. Preserve headroom so dialing
  down does not merely dim already-clipped white shapes.
- Rebuild visibility masks for the actual footage; static eye/foliage exclusions
  must not remain pinned to the screen when the scene moves.
- Review attachment, occlusion, facial/lyric legibility and strength on motion.

## FX-02 — Tracked practical-light pulse

**Status: first receiver-meter motion test rendered; awaiting review.**
See `TRACKED_LIGHT_PILOT.md`. Preview:
`out/tracked_light_receiver/receiver_light.mp4`. Only s010's large amber meter
is augmented; local 2D tracking and audio controls saved, no assembly change.

Intent: existing lamps, luminous plants, eyes, instrument lights or windows
appear to respond to music. Augment their photographed shape and color rather
than placing an unrelated flashing dot over them.

First test: one existing light on one short motion clip with modest movement,
stable shape and little occlusion. Prefer a lamp or luminous plant initially;
eyes require additional care around blinking, expression and changing outlines.
Choose the exact source take after inspecting available motion footage.

Choreography: selected drum attacks give a quick lift and smooth decay; start
with one driver. Keep a nonzero base light. Later, bass can supply a slow floor,
or guitar attacks can activate a different group of lights. Do not flash every
light on every beat or introduce global exposure pumping.

Implementation:

1. Track stable nearby texture or the light housing, not just a saturated or
   flickering core. Inspect the track across the entire test, not only endpoints.
2. Attach a feathered source-shaped mask; animate scale/rotation or outline when
   needed. Separate the tight core, soft bloom and optional nearby surface spill.
3. Use original color/texture as a guide. Add controllable emission in linear
   light, protecting detail; additive augmentation alone cannot turn an already
   bright source off. Dimming requires a separate masked correction of the plate.
4. Track occlusion masks and hide the effect when its source disappears. Spill
   needs its own receiving-surface mask; a halo alone is not physical relighting.
5. Retain original footage and compare original / restrained / full strength.
   Test a few clear musical hits before extending the method to other shots.

Pass criteria: light remains attached, no sliding halo, no glow through foreground
objects, no track jumps during brightness changes, readable source detail and
audible/visible synchronization. Record failures as well as the successful range.

## Tracking: use only as much as the shot needs

## FX-03 — Localized pressure lens

First test rendered: `out/pressure_lens_rockets/pressure_lens.mp4`, s037.
Music-driven textured wavefronts refract the background exhaust region, with
slight dispersion and a protected foreground performer. Native Blender compositor
displacement, not ray-traced glass. See `PRESSURE_LENS_PILOT.md` for reproduction,
mask limitations and review criteria. Not yet approved. Production needs a
displacement field and mask applied to the actual plate, not just an alpha overlay.

### Tracking choices

| Shot/effect | Starting approach | Escalation or limitation |
|---|---|---|
| Static camera and fixed light | Authored mask | Moving subjects still need occlusion masks |
| Small light translating in frame | 2D point track and local mask | Multiple anchors or manual keys for scale/rotation |
| Screen/window changing perspective | Planar tracking / corner mapping | Nonrigid shape changes need animated masks, not one plane |
| Dust occupying space during camera travel | Camera solve plus approximate depth and occlusion geometry | A single 2D track cannot reproduce near/far parallax |
| Independently moving rigid object | Separate object tracking as needed | Camera motion alone does not describe it |
| Generated footage warps or changes topology | Short local tracks, mask corrections, or a different take | Do not force a physically inconsistent shot into a confident 3D solve |

Blender provides 2D tracking, camera/object reconstruction and planar tracking.
See [Blender tracking introduction](https://docs.blender.org/manual/id/5.1/movie_clip/tracking/introduction.html)
and [Blender VFX capabilities](https://www.blender.org/features/vfx/).
Availability is not proof that a particular generated clip will solve reliably.
Start with built-in tools; no add-on purchase or installation is required by this plan.

## Other candidates — backlog, not simultaneous experiments

- **Surface glints:** guitar or high-drum attacks travel along existing wet or
  metallic edges. Needs surface tracking and foreground masks; less intrusive
  than adding new objects.
- **Localized ripple:** a low-drum hit spreads through a visible pool or water
  surface. Needs a surface plane and occlusion; avoid full-frame distortion.
- **Exhaust/steam response:** bass shapes an existing plume while selected hits
  briefly brighten its base. Soft masks tolerate more uncertainty, but the source
  still needs attachment and the plume must not cover faces.
- **Light conversation:** two existing light groups answer one another on musical
  phrases. Reuses FX-02 tracking rather than inventing another visual system.

## Per-shot handoff contract

Before production, record FX type/version, source take and fingerprint, source
in-frame, song-frame origin, fps, exclusive output end, actual lead/exit handles,
audio driver and stem offset, tracking/mask files, blend settings, layer outputs
and review status. Reconcile edits against the timing grid. Never assume rounded
generation length guarantees usable exit footage. No new lead handles by default;
retain the existing exit-only policy and explicitly record any exceptions.

Next action: inspect candidate nighttime motion clips and test FX-02 on one light.
Do not expand the garden simulation or attempt a whole-film camera-tracking pass
before this small attachment test has been reviewed.
