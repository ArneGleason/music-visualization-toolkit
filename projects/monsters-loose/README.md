# Monsters Loose — production recovery

Current edit: **v30**, through master frame 2461 at 24 fps (102.54 seconds). Developed footage runs through frame 1506; visitors and habitat planning stills follow. The user approved the revised visible frog snatch in v28. The user also approved v29 facility beacon pulses. v30 adds synchronized elongated red water reflections; that reflection polish awaits review.

## Resume

Use the existing frame review at http://127.0.0.1:8767/ (same app and port). The swamp bridge occupies master frames **1305–1506**. `recovery/shots/shotlist.json` is the edit source of truth. Master frames are one-based; source offsets are zero-based; end frames are exclusive. Default assumed pre-roll is 12 frames (half a second), recorded per shot; consult actual source trims before changing cuts or lip-sync.

The current Blender timeline is `recovery/animatic/MonstersLoose-v30-through-habitats.blend`. The current render pointer is `recovery/animatic/frame-review-current.json`. Latest swamp effect lives in `recovery/motion-graphics/SWAMP-LIGHTS-001/`. The underlying approved movie is `video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4`.

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
4. Open the current v30 Blender file to inspect/render the edit. Effects can be rebuilt from their adjacent build scripts and README files. Historical animatic build scripts load predecessor `.blend` files; those small snapshots are retained. Restore source inputs before running them.
5. Launch `tools/frame_review.py` with `--video <current-render> --notes <job>/shots/frame-review-notes.json --state <job>/animatic/frame-review-current.json --port 8767`. See `docs/FRAME_REVIEW.md`.

To refresh this recovery snapshot after later work, run `python projects/monsters-loose/snapshot.py --source <job-directory>`, inspect the diff, then commit. The exporter copies files; it does not delete stale historical snapshots.

## Accepted editorial details

- Helicopter lights v002; creature POV motion/lens v002 (parallax version rejected).
- Gate cut at master 1012; hard rattling stops by 1034, followed by dust/settling. Dust v004 approved.
- Lab pitch, town fire, mean scientist take002, upward tall-gate reveal, and swamp snatch take002 approved.
- Three scientists retain their character references; mad scientist has one brass hand.
- No new generation credits spent on v30 lighting/reflections.
- Frame review playback/rewind fix passed real Chrome checks; zero input clamps to frame one and play at the end restarts.
