# FX-02: receiver meter pulse

Status: first motion test rendered for owner review; no assembly change.

Source: `clips/raw/receiver_dial_macro_v6.mp4`, s010, source in-frame 0.
Song interval from `generated/overlay_cues.json`: [774,843), 69 frames at 24 fps.
Preview: `out/tracked_light_receiver/receiver_light.mp4`, 1280x720 with master audio.
Run: `python tools/tracked_light_pilot.py`. Requires numpy and opencv-python-headless;
this test installed isolated dependencies under `out/fx_tracking_deps`, not globally.

Only the large amber meter is augmented. The upper screen and two small meters
retain their source animation. Selected attacks from the restored Drum Kit stem
(100–2800 Hz) drive a quick 18 ms rise and 190 ms decay. Saved stem offset is applied;
event times and per-frame strength are in `out/tracked_light_receiver/tracking.json`.

Tracking uses OpenCV optical flow on nearby housing detail, forward/backward
checks and a robust local homography, not Blender or a 3D camera solve. It fails
on insufficient features or excessive residuals. Maximum median inlier residual
was 0.715 pixels; this measures feature fit, not guaranteed mask accuracy. Diagnostic
outlines at frames 0, 24 and 68 are saved for inspection. End-frame outline checked.

An authored aperture follows the track. Current-frame color gates the light mask
so the moving needle does not leave an old shadow in the augmentation. The core
is increased multiplicatively in linear light to retain markings; two soft amber
halos add local bloom. Display output is clipped to SDR: not an HDR delivery layer
or physical relighting. Peak frame inspected; visible meter markings retained.
Existing source brightness changes are not removed or synchronized by this pass.

Current outputs are flattened frames/video and reusable tracking/control data,
not separate delivery layers. No handles added, source altered, registry change,
paid generation, or lip-sync modification. Review attachment, musical clarity,
clipping and halo strength before adding other lights or exporting production passes.
