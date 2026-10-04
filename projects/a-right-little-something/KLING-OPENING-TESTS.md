# Opening Kling motion tests — 2026-10-04

Two authorized five-second Kling 3.0 jobs completed at 1080p, 40 credits each (80 total). Exact prompts and frame plans are in `kling-opening-tests.json`; all submissions, task IDs, results and source movies are under the ignored `generated/kling-tests/opening-v01/`. No automatic resubmissions or additional paid jobs.

Review: http://127.0.0.1:8768/storyboard/kling-opening-v01/

- **opening-005**: Good restrained motion and thin-field appearance. The equatorial band and two distinct moons stay recognizable. Hands drift slightly apart/away from their initial contact positions; contact is not a rigid constraint.
- **opening-003**: The first/tail frame pair produces a continuous interior-to-exterior reveal. The recognizable ship arrives in the intended wide composition. Intermediate geodesic cells rearrange, pose/head direction shifts, and the upper platform's visible detail changes. This demonstrates useful broad guidance rather than exact Blender geometry recovery.

Recommendation: continue Blender → Image Gen → Kling for composition planning and restrained shots. For large camera moves, lower the field grid's visibility, supply first/end references, and consider breaking difficult reveals at a cut if geometry changes remain distracting. For deliberate palms-on-field contact, use minimal motion and judge the contact carefully. These findings do not establish continuity for all five shots.

Reviews use the existing song master at each shot's timing-grid start. Videos are conformed to 24 fps by frame sampling without speed changes. Shot 003 is 81 edit frames, with 12 lead-in and 27 remaining lead-out frames in its five-second clip; shot 005 is 90 edit frames, with 12 lead-in and 18 lead-out frames. Exact full/trimmed counts verified with ffprobe. The initial preview downloads included a provider watermark. Clean exports supplied by Kling are now retained separately with the `-clean.mp4` suffix and used for reviews.

The original full-song storyboard animatic is retained for comparison. The current animatic now uses all five clean motion clips, as described in `OPENING-MOTION.md`. The shotlist records the candidates and pending-review state. All original notes and references are retained.

Collect existing task IDs: `tools/run_kling_test.py projects/a-right-little-something/kling-opening-tests.json`

Rebuild reviews: `tools/review_kling_tests.py projects/a-right-little-something/kling-opening-tests.json`
