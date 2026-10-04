# Opening storyboard experiment

## Current field-shell batch · v02

The full-song listening animatic now includes this opening at the authored shot boundaries. `generated/animatic/A-Right-Little-Something-storyboard-opening-v01.mp4` contains the five illustrated starts and three end references over the first 632 frames. Applicable start/end boards switch halfway through their shot as storyboard holds, not generated motion or final editorial cuts. Lyrics and active words remain frame-aligned below the pictures. From frame 633 onward, the existing lyric-timing animatic continues. Total video length remains 5265 frames at 24 fps, and the original audio stream is copied intact (verified identical SHA-256 packet hash). Both listening and exact-frame viewer pointers now select this render; existing notes keep their positions. Rebuild with `tools/update_storyboard_animatic.py projects/a-right-little-something/project.json`.

The current review is `/storyboard/opening-v02/`. All five Blender scenes, fifteen composition stills and five handle-inclusive movies were rebuilt with the same fully transparent shell and faint geodesic field network. Camera reference fill improves geometry visibility; the shared sun remains the directional celestial light. Five Image Gen starting frames were regenerated using the same prompt lock, approved field-shell appearance and Blender framing. The face shot was corrected to keep hands out of frame. Ship entrance, pullback and widening also have new illustrated end references.

Media are in `generated/storyboard/opening-v02/`; exact tool prompts, including corrections, are preserved in `storyboard-field-generation-log.json`. The authoritative shotlist points to the selected frames. Earlier v01 media remain available for comparison. The approved shot-five v01 illustration remains the appearance reference; the new batch is pending review as a sequence.

Verified after reopening: all five scenes are retained, all use the same 150-hexagon/12-pentagon field topology, and no reflective or refractive glass shader remains on their shell. The 002→003 and 003→004 cut cameras match. All five movies have the planned frame counts at 24 fps; the combined master-audio preview is 632 frames (26.333 seconds). Timing and 12-frame handles are unchanged. Image Gen preserves the broad design and framing rather than exact mesh projections or surface textures; the illustrations are storyboard references, not proof of seamless generated motion. Two Kling motion tests are now available; see `KLING-OPENING-TESTS.md` for results and limits.

The remainder below documents the initial v01 experiment and its development.

Five shots correspond to the five listening notes saved in revision 9. The authoritative entries are in `shots/shotlist.json`; each preserves its source note. The broader transition ideas in the first note inform the batch rather than adding more shots.

| Shot | Action | Edit frames | Clip frames with handles |
| --- | --- | ---: | ---: |
| opening-001 | Planet and moons; ship drifts in | 227 | 251 |
| opening-002 | Harper's face enters foreground | 136 | 160 |
| opening-003 | Pull back to reveal floating ship | 81 | 105 |
| opening-004 | Rapid widening to orbital scale | 98 | 122 |
| opening-005 | Folded knees, palms on clear sphere | 90 | 114 |

At 24 fps, every clip has 12 frames (0.5 seconds) before and after its edit. The master-audio review trims those handles and lasts 632 frames (26.333 seconds). Note boundaries are rounded to frames using the DAWproject timing grid. The opening lead-in precedes the song by half a second. The batch ends after “So much room here up in space.”

The five editable Blender scenes are in `generated/storyboard/opening-v01/opening-storyboard-v01.blend`. Each has camera and movement keys, edit/handle markers and source-note properties. The original ship design scene remains as a library. Character, planet and glass rendering are blocking proxies. The last shot shifts the planet for an art-directed space-facing view; this is documented in its blocking entry rather than implied to be a rigid orbital simulation.

The face/pullback and pullback/widening edit boundaries have matching Blender views. The exterior-to-face and widening-to-window changes are proposed cuts. This does not yet establish a single continuous generated take.

The review surface at `/storyboard/opening-v01/` shows the master-audio preview, per-shot clips with handles, Blender start/edit/end compositions, Image Gen drafts and original notes. Exact generation prompts and their shared lock are in `storyboard-prompts-opening.json`. Starting illustrations use the lead-in frame, so the opening illustration deliberately has no ship yet.

Image Gen follows broad framing and ship finish, but the interior drafts introduce additional visible planet/moon detail compared with their Blender cameras. They are composition drafts, not approved continuity frames. Before a video trial, resolve those backgrounds and provide an end reference for the ship entrance and cabin pullback: a starting frame alone cannot specify the geometry revealed later. Kling has not been tested for this batch. Review these moves before spending on footage or expanding the storyboard.

Shot five glass correction: the source shell is one mesh surface with no Solidify modifier or inner wall. Its old transparent/Fresnel/metal material became opaque and reflective from inside, hiding part of the closed equatorial ring. Storyboard copies now use a transparent inward face, retaining the exterior rim treatment. This is a deliberately thin layout shell, not volumetric refractive glass. Shot five's camera has a verified minimum clearance of 0.312 model units inside the shell across every handle and edit frame, exceeding its 0.1 near clip distance. Its slightly wider framing retains the head; the moons have explicitly art-directed placements for this angle while retaining identities and shared sunlight. The band mesh has zero boundary or non-manifold edges. Shot three deliberately crosses the thin surface during its pullback; it does not travel inside a double-wall glass volume.

The corrected shot-five illustration is `opening-005-starting-frame-v02.png`; v01 remains for comparison. Exact edit instructions are in `storyboard-glass-fix-prompt.txt`. All five Blender scenes are explicitly retained when saving and reopening the file.

Rebuild the plan with `tools/shotplan.py --merge --project projects/a-right-little-something/project.json --batch projects/a-right-little-something/storyboard-opening.json`. Render using `tools/build_storyboard_batch.py` inside Blender, and rebuild the review with `tools/review_storyboard_batch.py --assemble`. Generated media remain ignored by Git.
