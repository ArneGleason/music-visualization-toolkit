# Blender and resolution audit, 2026-09-07

## Finding

The project is NOT entirely native Blender and is NOT certified for a resolution-only final rerender. A .blend file or Blender assembly step can contain fixed-size PNG sequences generated outside Blender. That is not the same as regenerating effects at the requested resolution. Earlier explanations did not make this distinction adequately clear.

## Scope and evidence

Reviewed shared assembly register and revised opening decisions, inspected representative recipe code, and screened Python recipes in tools/ plus first-level out/ folders. out/outro_depth_timing_v1/renderer_inventory.json records85 matching files with evidence lines. This includes old tests and audit helpers, not85 active effects. It is a source-code inventory, not an exhaustive dependency graph or proof each named take is currently selected. Dynamic imports, deeper folders, browser assets and alternate wrappers require follow-up per selected shot.

| Family | Evidence / current implementation | Required work |
| --- | --- | --- |
| Lyrics | tools/lyric3d.py creates Blender geometry and accepts width/height | Confirm current renderer path and compare glyphs, framing and blur at target size |
| Oscilloscope | tools/screen_sync_phosphor.py uses Blender geometry/textures; explicit internal2560x1440 setting | Preserve approved look; audit texture resolution and final scaling |
| Tunnel contours / beat arrivals | tools/tunnel_arrival_pilot.py draws lines, resizes and blurs with OpenCV | Migrate contours, timing, persistence and bloom into Blender |
| Tracked lights and swimmer highlights | tools/tracked_light_pilot.py, swimmer_palette_pilot.py use OpenCV; tracked-light recipe explicitly requires1280x720 | Retain tracking as data if useful; normalize coordinates and rebuild compositing in Blender |
| Garden airflow foundations | tools/garden_airflow.py, garden_dust_fields.py, garden_dust_pilot.py use Blender | Verify selected later layers, geometry and framing, not just original pilot |
| Pressure lens | tools/pressure_lens_pilot.py uses Blender compositor but allocates fixed1280x720 vector fields | Regenerate fields at target resolution / normalize displacement |
| Opening switch-on, aerial glimmer, probes, receiver response | out/observatory_phosphor_start, opening_aerial_glimmer_v1, probe_voice_trial, receiver_interaction_v2 and receiver_now_v3 contain raster FX code | Native Blender reconstruction with timing and masks carried across |
| Garden guide, moth/ghost wings, waking eyes, birds | garden_walk_guide_v1, garden_ghost_wings_v3, garden_waking_v3 and garden_birds_fx_v2 are raster recipes | Migrate selected treatment layers, retain frame-aligned cues |
| World/meaning orbs, nebula, specimen and shop effects | world_nebula_v3, world_pullback_refined_v2, meaning_orb_loop_v4, specimen_signal_v1, shop variants use raster operations | Resolve approved versions first; reconstruct selected geometry/composites |
| Bends-your-mind | out/bends_mind_fx_v1/render.py uses raster deformation | Trace v2 selected wrapper and rebuild distortion at target size |
| Outro TV and room afterglow | Separate build.py raster layers plus blender.py sequence assembly in TV/afterglow folders | Do not treat raster layer playback in Blender as native effects |
| Recent outro sprite/reflection/iris | out/outro_additive_green_v1 and predecessors use local raster compositing | Native migration pending; accepted look remains reference |
| New shot8 motes | out/outro_depth_timing_v1/build.py: Blender perspective geometry + native glow/add compositor |720/1080 single-frame check performed; plate and prior artifact treatment still baked |

## Required migration standard

Blender is the authoritative renderer AND compositor for final graphics, masks, bloom, displacements and compositing. External scripts may prepare timing, track coordinates, extract original footage, orchestrate Blender, encode or mux audio, but may not silently generate fixed-size final FX layers as a substitute. Raw generated footage naturally remains raster. Legacy approved renders stay as look references, not proof of migration.

For every selected shot: resolve current timeline and approved take, identify original plate and all baked layers, port only selected recipes, preserve musical clocks and protected-source precedence, and record completion. Do not blindly migrate every old test. Reconcile revised review snapshots with shots/shotlist.json and shared resolver before a whole-film build.

Resolution contract: same normalized framing, tracking, geometry, line thickness, glow footprint, displacement, seeds and song time at any16:9 size. Explicit resolution-derived controls where Blender nodes use pixels. Scale/refresh input textures as necessary. Shutter sampling and adequate spatial samples are separate requirements. Verify temporal stability, not only one still. Keep linear emission and one output transform; no double mastering.

## Next work / remaining gap

Whole-film migration remains outstanding. Recommended sequence: native outro TV/room/sprite as a small end-to-end test, then shared tracked-light and vector tools reused across the film, followed by exceptional warps/transitions. Compare representative beginning/middle/end frames and short motion at720 and1080, then at any higher requested delivery size. Do not authorize a final resolution-only render until every selected dependency is accounted for.

Current work fixes shot5 timing and improves shot8 density/depth, but does not claim to finish this migration. No paid generation or mastering initiated.
