# Swamp facility beacon lights v001
Seven tracked red warning lamps receive feathered suppression of their existing steady light and red glow overlays rendered in Blender. Gaussian pulses have a 29-frame period and 3.4-frame width, staggered by four frames across lamps, matching the opening beacon cadence. Warm architectural lights stay steady. No generation or credits.

Input: video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4 (227 frames). Output: Swamp-frog-lights-v001.mp4. Trim source 12..214 exclusive to master 1305..1507 exclusive, 24fps. Assumed handles 12 frames each; edit unchanged.

Run animatic/prepare-swamp-lights.py to regenerate tracking and build script; run Blender in background with --python motion-graphics/SWAMP-LIGHTS-001/build.py; composite overlay/lights-%04d.png at 24fps over the source with FFmpeg overlay=0:0:format=auto, libx264 crf18 yuv420p. Run animatic/build-opening-v29.py after restoring predecessor project/media.

The underlying frog snatch take002 is user approved. This light polish awaits review. Original footage and v28 remain available.
