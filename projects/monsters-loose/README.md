# Monsters Loose — production recovery

Current edit: **v33 (flagged test)**, through master frame 2461 at 24 fps (102.54 seconds). Developed footage runs through frame 1624; a new aquarium reference fills frames 1625-1707, then existing lasso and habitat planning stills follow. The user approved the revised visible frog snatch in v28. The user also approved v29 facility beacon pulses. v30 adds synchronized elongated red water reflections; that reflection polish is retained. v31 adds the walking tour generation and new aquarium still for review.

## Resume

Use the existing frame review at http://127.0.0.1:8767/ (same app and port). The swamp bridge occupies master frames **1305–1506**. `recovery/shots/shotlist.json` is the edit source of truth. Master frames are one-based; source offsets are zero-based; end frames are exclusive. Default assumed pre-roll is 12 frames (half a second), recorded per shot; consult actual source trims before changing cuts or lip-sync.

The current Blender timeline is `recovery/animatic/MonstersLoose-v33-through-habitats.blend`. The current render pointer is `recovery/animatic/frame-review-current.json`. Latest swamp effect lives in `recovery/motion-graphics/SWAMP-LIGHTS-001/`. The underlying approved movie is `video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4`.

## What is backed up

Scripts, shotlists, timing grids, lyrics, generation prompts/settings, creative notes, tracking coordinates, font files/licenses, and small editable Blender projects are copied into `recovery/` with their job-relative directory structure. The frame review application is tracked in the toolkit's `review/`, `tools/frame_review.py`, and `docs/FRAME_REVIEW.md`. `inventory.json` identifies included files and omitted media; included snapshot bytes have SHA-256 hashes. URL query strings and named authentication fields are removed from text snapshots.

Large generated images, video, audio, PNG render sequences, caches, logs, and Blender backup copies are intentionally excluded. **This is not an exact media backup.** Prompts cannot regenerate identical AI footage. Preserve the external job folder separately to recover the approved pictures and takes exactly:

`C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913`

Also preserve the original DAW project and its referenced recordings:

`C:/Users/arneg/OneDrive/Documents/Bitwig Studio/Projects/MonstersUndone.cleaned-groove/MonstersLoose.dawproject`

## Restore and rebuild

1. Copy `recovery/` to the original job directory, then restore omitted source media there using `inventory.json`. Never run production builds directly inside this Git snapshot: generated content belongs outside Git.
2. Install Blender 5.2, FFmpeg/ffprobe, and Python with NumPy/Pillow. Some generation scripts additionally require the Kling CLI and a separately authenticated account. Credentials are not backed up here.
3. The Blender timelines use relative media paths where saved; older scripts and review state also contain absolute Windows paths. Restoring to the original job path is simplest. For another location, update these paths and use Blender's missing-file relinking before rendering. Font paths may also need relinking.
4. Open the current v33 Blender file to inspect/render the edit. Effects can be rebuilt from their adjacent build scripts and README files. Historical animatic build scripts load predecessor `.blend` files; those small snapshots are retained. Restore source inputs before running them.
5. Launch `tools/frame_review.py` with `--video <current-render> --notes <job>/shots/frame-review-notes.json --state <job>/animatic/frame-review-current.json --port 8767`. See `docs/FRAME_REVIEW.md`.

To refresh this recovery snapshot after later work, run `python projects/monsters-loose/snapshot.py --source <job-directory>`, inspect the diff, then commit. The exporter copies files; it does not delete stale historical snapshots.

## Accepted editorial details

- Helicopter lights v002; creature POV motion/lens v002 (parallax version rejected).
- Gate cut at master 1012; hard rattling stops by 1034, followed by dust/settling. Dust v004 approved.
- Lab pitch, town fire, mean scientist take002, upward tall-gate reveal, and swamp snatch take002 approved.
- Three scientists retain their character references; mad scientist has one brass hand.
- No new generation credits spent on v30 lighting/reflections.
- Frame review playback/rewind fix passed real Chrome checks; zero input clamps to frame one and play at the end restarts.

Latest tour: master1507..1625 exclusive, KLING-TOUR-001, 6seconds/48credits, source12..130, wider generated start and original ANCH-006-A tail. Aquarium still SCN-006-aquarium-v001 starts1625 on Watch them try to eat the keeper whole. Both new still prompts are in recovery/assets; shot direction and timing are in recovery/shots/SCN-006-tour-aquarium.md. Aquarium video has not been generated.

Latest revision v32 replaces the tour with KLING-TOUR-002: fixed camera, start image only, no tail frame. Same 6seconds/48credits and trims. Take001 rejected for background sliding. Take002 background is steadier in samples but Harper hair becomes a ponytail; flagged for user review, not approved. Aquarium still/cut unchanged.

Latest v33 uses tour003, close ANCH-006-A start plus approved Harper Element321495363652188, no tail frame, 6s/48credits. Harper likeness improved in sampled frames, but Kling ignored locked-camera direction: near cage pillars shift relative to far tower. Background criterion NOT met. This is a flagged review test, not approved footage. Takes001 and002 rejected. No further paid attempt submitted.
