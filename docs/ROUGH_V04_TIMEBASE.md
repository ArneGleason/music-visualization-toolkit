# Rough v04: real-time playback and no global flash

Corrections authorized 2026-09-05. Target `out/rough_v04_sync_noflash_720p.mp4`.

COMPLETED: full 1280x720 / 24 fps rough, 4782 frames (199.25 seconds), one
199.241-second master audio stream. Full decode passed without errors. All eight
protected FX selections confirmed in render log; 14 tests and final preflight pass.
Six frame comparisons in the completed movie (s003 and nonzero-in-point s034,
early/middle/late) match real-time source progression within one source frame.
The large cumulative slowdown seen in v03 is gone. Original media and v03 remain.
Owner playback review is still required for residual generated lip-sync quality.

- Preserve the 71-shot plan, source in-points, lyrics, eight accepted FX, and
  master audio. No guessed offsets or regenerated lip sync.
- Before Blender import, convert mismatched-rate sources using their timestamps
  to silent 24 fps CFR copies. Never reinterpret 30 source frames as 24 fps.
  The 239-frame / 30 fps originals become 191-frame / 24 fps copies. Endpoint
  rounding is -0.008333 seconds, not a speed change or invented handle.
- Cache key includes full source path, size, modification time, target fps and
  conversion version. JSON sidecars record each conversion. Original clips stay
  untouched; the shotlist does not point permanently at disposable proxies.
- Disable the global `beat_pulse` strip by default. Local FX pulses are untouched.
- New v04 output and segment directory prevent reuse of the faulty v03 sections.

## Checks before the full render

All 71 shots pass timebase and coverage preflight. Nine protected-selection tests
and five timebase tests pass. Actual Blender frame probes matched original
30 fps source frames with grayscale image correlation:

| Shot/song frame | v03 observed source | v04 observed source | Expected real-time source |
| --- | ---: | ---: | ---: |
| s003 / 227 | 72 | 90 | 90 |
| s034 / 2812 | 128 | 160 | 161 |

Matches were 0.9974 and 0.9951 respectively. The one-frame uncertainty on the
duet is within output-frame rounding and adjacent-image similarity. These checks
establish corrected playback, not perfect phoneme generation. Residual first-word
or wrong-speaker problems still need owner review, as described in the v03 audit.

Recipe: `python tools/assembly_preflight.py --prepare-timebase`, then
`python tools/render_lyric_animatic.py --proxy --allow-clips --out out/rough_v04_sync_noflash_720p.mp4`.
Render log: `out/rough_v04_render.log`. No new mastering or generation.
