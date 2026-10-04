# Clean opening motion animatic

Review: http://127.0.0.1:8768/

## Current edit: v03

`generated/animatic/A-Right-Little-Something-opening-motion-v03.mp4` combines
the former opening-003 and opening-004 into one continuous Kling take. The
second, endpoint-constrained test is selected; it retains the complete
equatorial band and open engine ring much closer to the established design.
The single-reference test is retained as a rejected design variation.
Both nine-second jobs cost 72 credits each, 144 total.

The combined shot begins at performed lyric frame 353 (14.6667 seconds),
eleven frames earlier than the previous shot 003 cut, and ends exclusively at
543. Shot 002 is shortened to 125 frames; the combined shot has 190 frames.
Thus both complete up-above phrases share one continuous move without a cut
at the old frame 445 boundary. Shot 005 and the opening's final frame 632
remain in place. There are now four shots, with no retiming. The two original
shot records and creative notes are retained under `supersededShots` in the
authoritative shotlist, and the five original listening notes remain untouched.

Small bottom lyrics use the presentation described below across the entire
song, with current-word highlighting and preserved performed text. Moon depth
and field behavior during the pullback still need visual judgment; this edit
specifically addresses the camera restart and missing lyric context.
The v01 and v02 movies remain available.

## Bottom lyric presentation

`production.lyricPresentation` in `project.json` is the default for future
motion animatic assemblies. It uses Bahnschrift at 34 pixels on a 1080p
canvas, centered 45 pixels above the bottom, with a small dark outline/shadow
and a pale cyan highlight on the current word. Full phrase wording and
performed typos come directly from `animatic-data.json`; none are rewritten.
`tools/lyric_overlay.py` derives every cue from the existing frame boundaries,
including the nine repeated "in" words. ASS centisecond boundaries are floored
so they activate on the intended 24 fps video frame.

Lyrics are baked into the review movie, so they also appear in the exact-frame
viewer and downloaded copies. Beyond the planned opening, the old large lyric
timing picture is replaced by a plain dark canvas carrying the same small
bottom lyrics. The listening timeline remains available for timing navigation.
The master audio is still copied without any change.

## Continuous two-phrase pullback test

`kling-opening-continuous.json` records two nine-second 1080p attempts,
72 credits each. The first uses one portrait reference and changes the ship
design: missing equatorial band and a barrel-shaped engine. The second adds
the approved exterior ending image to constrain those structures. Original
generation requests and results remain under `generated/kling-opening/continuous-v01/`.
The intended continuous edit starts at lyric frame 353, the onset of
"Here in orbit up above", and continues through frame 542, covering
"Way up here up above" without restarting the camera. Its 190 edit frames
plus two 12-frame handles fit within the nine-second source.

## Current best-available edit: v02

The current animatic is `generated/animatic/A-Right-Little-Something-opening-motion-v02.mp4`.
Shot 002 now uses the preferred locked-camera, connected-lines Kling take
from `generated/kling-experiments/depth-field-v01/depth-lines/`. Its earlier
moving-camera take is retained in the shotlist's `motionAlternates`.
Shots 001, 003, 004 and 005 retain their existing clean Kling takes.
No Blender image-card or field test replaces character animation in this edit.
No new footage was generated for this assembly.

All five shots fill the opening 632 frames (26.333 seconds), with the original
cut positions and 12-frame source lead-ins. The remainder is the existing lyric
timing animatic. Shot 002 is preferred; the other takes are best available for
review. Pullbacks 003 and 004 remain provisional for moon depth and field
continuity. Shot 001's large entrance/recession and the cuts between shots also
need judgment in context. This selection does not claim those problems are fixed.

The listening surface has a collapsible opening selection list with direct
links to each shot's playhead position and short review notes. It is generated
from the authoritative shotlist, independently of the editable listening notes.

Production direction: prioritize Kling performance and illustrated motion;
keep the camera fixed when depth becomes unreliable and avoid troublesome
moves. Use Blender for blocking and selective composited light, blur and other
effects. The native geometry/energy experiments remain references.

The original v01 movie is retained. Both review pointers now select v02;
5265 frames at 24 fps, 1920×1080 presentation and unchanged master AAC packets
were verified before switching. The sections below document the original assembly.

Five noted opening shots are selected in `shots/shotlist.json` via `motionRef`. Shots 003 and 005 reuse the two tests the user liked, using their watermark-free provider exports. Shots 001, 002 and 004 were generated with the same Kling 3.0 model and identical prompt lock, at 1080p, without generated audio or automatic cuts. Exact requests are in `kling-opening-completion.json`. The three added jobs cost 88 + 56 + 48 = 192 credits; all five cost 272 total.

| Shot | Requested clip | Edit frames at 24 fps | Song interval |
| --- | ---: | ---: | --- |
| opening-001 | 11 s | 227 | 0–9.458333 s |
| opening-002 | 7 s | 136 | 9.458333–15.125 s |
| opening-003 | 5 s | 81 | 15.125–18.5 s |
| opening-004 | 6 s | 98 | 18.5–22.583333 s |
| opening-005 | 5 s | 90 | 22.583333–26.333333 s |

Each edit begins after its 12-frame lead-in and retains at least 12 lead-out frames in the source clip. Provider whole-second durations leave extra handles. Edit boundaries come from the DAWproject timing grid in the authoritative shotlist. No speed changes, audio retiming, transitions or manual duration trimming were added.

`tools/update_motion_animatic.py` builds `generated/animatic/A-Right-Little-Something-opening-motion-v01.mp4`. The first 632 frames contain full-frame animation with no lyrics or shot labels over the picture. Native 1080-high Kling pixels are preserved; sources slightly narrower than 1920 receive a few pixels of side padding rather than enlargement. The remaining lyric-only picture is scaled from the previous 720p timing render to the 1920×1080 review canvas. The original master AAC stream is copied unchanged. All 5265 frames at 24 fps and the audio packet hash are checked before updating both review pointers.

The sequence is pending creative review. These are recognizable coherent shots, not a reconstruction of the exact Blender mesh. Shot 001 enters large from the left and recedes more than the blocking intended. Shot 002 adds some body/foot motion during its drift. Field cells rearrange in the pullback, and camera/pose framing at the 002→003 and 003→004 cuts may jump. The user can assess those transitions in context before deciding whether to revise any individual shot. No additional paid variations were generated.

Sources, submissions and result JSON are ignored under `generated/kling-opening/completion-v01/` and `generated/kling-tests/opening-v01/`. The old still animatic and source movies are retained. Listening notes stay unchanged.
