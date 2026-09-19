# Frame review

A local review surface for rendered constant-frame-rate video. It does not edit
the shotlist. Paused pictures are decoded by FFmpeg, and playback uses the
browser's displayed-frame timestamps.

Run from the toolkit root (Windows uses .venv/Scripts/python.exe):

```sh
./.venv/bin/python3 tools/frame_review.py --video /absolute/path/preview.mp4 --notes /absolute/path/frame-review-notes.json --master-start 1
```

Open http://127.0.0.1:8767 in Chrome. Add `?frame=1000` to start at master
frame 1000. Use Chrome when the in-app browser cannot play the video's codec.
Requires FFmpeg and ffprobe on PATH.

- Space toggles playback; arrows step one frame; Shift+arrows step ten.
- Quarter/half speed helps identify an action before precise stepping.
- Master frame and preview frame are both one-based. Set master-start to the
  master frame represented by the first frame of a trimmed preview.
- Mark this frame appends a note atomically to the chosen JSON file. The agent
  can read this file to apply exact edit directions; notes do not automatically
  change the edit.
- Copy frame reference includes the render filename, frame numbers and fps.

The server binds only to 127.0.0.1 and serves the selected video, not arbitrary
workspace files. Use --state /absolute/path/frame-review-current.json to keep one server and URL. Update that JSON atomically with video (absolute path) and master_start after a render finishes. The open player adopts it while paused, preserving master position and waiting for unsaved notes. Media requests are pinned to their render revision.


Playback robustness: Play waits for the requested seek to settle, stale seek/still completions cannot replace a later transport action, and Play at the final frame restarts from frame1. Frame-number input stays authored while playback updates counters; Go consumes it before updates resume. Failed playback can recover the media decoder without page refresh. Counters remain one-based; input0 clamps to first frame.
