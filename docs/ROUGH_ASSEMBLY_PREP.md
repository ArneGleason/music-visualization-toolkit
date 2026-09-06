# Rough assembly preparation, 2026-09-05

The three approved catch-up tasks are integrated. No full rough render yet.

## Picture edit

- `shots/plan.json` promotes `shots/outro_coverage.json` as an exact-frame
  replacement of the old s054-s059 ending. IDs o01-o17 remain stable.
- Six longer synced takes supply the alternating speaker cuts. Every source-in
  equals the cut's song frame minus its take's song origin. No restarting a
  performance when cutting back to it. Unknown-speaker lines remain as handed off.
- o01 is the tunnel at [4120,4177), newly rendered with the approved amber/cyan
  arrival treatment driven by the audio at that position, not the former s056 audio.
- s034 ends at 2857. New s034b uses one second of filament weather at source
  [4,5) seconds through frame 2881. This replaces the unavailable duet tail with
  a deliberate environmental cutaway. It does not stretch lips or shift audio.
- Rocket entrances remain at 2881 and 2928. Hot springs and chrome bodies
  remain at 3165 and 3229. Lyric choreography is unchanged.
- Preflight found a pre-existing 17-frame uncovered opening. The observatory
  now begins at frame zero rather than leaving black before the first image.
- Ending stops at master frame 4782. The iris is still a placeholder for the
  short assembling title/provenance card, not a claim that those credits exist.

## Accepted FX, not discarded during ingest

The protected registry now selects scope s002, receiver s010, garden s019,
pressure lens s037, swimmers s043/s044/s047 and tunnel o01. All deliveries are
silent. Use the master soundtrack once. Except for the 1080p scope, these are
720p rough elements. No filmic grain or final mastering was added.

s044 uses the accepted four-swimmer pass for now. Expansion to all swimmers,
rocket smoke regeneration, final tracking/occlusion review, and full-source FX
exit handles remain on the candidate-final list. These do not block the rough.
No rendered FX handles exist; never infer synced handles from raw clip length.
O1/R1 spare outro base files are unassigned and have not been substituted.

## Rebuild and verify

Run `python tools/shotplan.py --merge`, then `python tools/overlay_cues.py`, then
`python tools/assembly_preflight.py`. Merge preserves populated clip assignments
when an old editorial placeholder has a null filename. It also preserves
conventions. Frame counts derive from boundary differences, fixing s044.

`out/rough_preflight.md` reports every actual selected file, source coverage and
song range. Current result: 71 shots, 4782 frames at 24 fps, eight protected FX
selections, no gaps, overlaps or insufficient picture coverage. Repeated merge
is stable. Nine source-selection tests pass.

For the next full rough, use the registry-aware Blender assembler and existing
`shots/lyric_motion_full.json` flat choreography. Do not regenerate word timing
just because picture cuts changed. Use a new output filename, retaining previous
assemblies. Check cutaway pacing, the new outro, FX strength and lyric legibility
in context. Existing assembler global overlays are unchanged; assess their
interaction rather than claiming this is a neutral final-grade export.

No paid generation, deletion, commit or push occurred during this preparation.
