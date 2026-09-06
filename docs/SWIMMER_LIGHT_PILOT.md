# Surface-swimmer palette experiment

## Approved palette and full-shot candidates

Owner selected violet-to-pearl as the chrome swimmers' color language and asked
for several existing clips to receive full effects passes. Completed-use inventory:
`shots/fx_uses.json`. s043, s044 and s047 have full-boundary review videos and
silent 1280x720 clean composites under `out/swimmer_fx_full/SHOT/`.
These are rendered candidates, not a claim that final assembly has been rebuilt.

s044 extends the approved four-torso tracking through the cut. Final-frame
anchor positions inspected. s043 and s047 use current-frame bright neutral-metal
selection in an authored pool region, with opposing sectors answering selected
drum attacks. This avoids inventing persistent IDs in a morphing crowd, but can
also catch bright wakes and needs full-shot owner review. Central moon reflection
and peripheral buildings are excluded approximately, not by rotoscoped masks.
The returning overhead shot uses source frame 96 and its own song-time controls.

Use `--full --shot s043` (or s044/s047) with the pilot renderer. Full mode renders
violet only. Source media unchanged, no extra handles, no lip-sync edits. s044's
rounded cut boundaries give 67 frames while its stored frames field says 68;
that pending reconciliation is explicit in the inventory. Do not stretch the
render or silently rewrite the edit. After review/timing validation, promote the
chosen clean composites into `assembly_decisions.json` for enforced selection.

Review variants: `out/swimmer_palette_pilot/cyan.mp4` and
`out/swimmer_palette_pilot/violet.mp4`. Run `python tools/swimmer_palette_pilot.py`.
First 48 source frames of s044, master song [3438,3486) at 24 fps. No assembly
change. Full shot has a pre-existing timing disagreement: compiled cues specify
67 frames, shotlist 68. Reconcile before full-shot delivery; neither was edited.

Four torso anchors form a back-to-front diamond: rear swimmer starts 300 ms
before selected drum event, middle pair 150 ms before, foreground at the event.
The 25 ms rise means the brightest point follows the onset slightly; this is
not a claim of sample-exact peak alignment. Drum events and saved stem offset
are recorded with per-frame tracks in controls.json. Existing arm movement is
not retimed. Uses restored Drum Kit, not synthetic beat guesses.

Both palettes use identical motion, masks, envelope and pearl core. Only soft
reflection/bloom color changes; linear luminance of the two accent colors is
matched before display clipping, not guaranteed perceptually identical. Cyan
is familiar; violet is the proposed iridescent alternative. No hue cycling.

Local optical-flow points give translation-only torso tracks. Soft elliptical
regions are gated by current reflection brightness: not full-body segmentation,
not a rigid model, and no explicit face or limb occlusion masks. First/middle/last
diagnostic ellipses saved; last-frame positions inspected. Four targets retained
tracking through the test. Extend only after palette/choreography review.

Output is flattened previews, not separate production layers. Original source,
lip sync, underwater plans and assembly assignments remain untouched.
