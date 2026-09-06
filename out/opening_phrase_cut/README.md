# Phrase-contained opening review

Current review reaches song frame 476, 19.833333 seconds at 24 fps, 720p.
Sources: existing s001, protected scope s002, accepted slower singing v3,
and replacement continuous overhead specimen v2. Master audio and existing
lyric choreography retained; global beat flash disabled.

| Shot | Song frames (end exclusive) | Source in at 24 fps |
| --- | --- | --- |
| s001 | [0,86) | existing assignment |
| s002 | [86,155) | protected scope frame 0 |
| s003 | [155,334) | v3 frame 12 |
| s004 | [334,476) | specimen v2 frame 12 |

The v3 take includes 'It's important' through lyric end 332, then two frames
before the cut. The specimen shot encloses 'More than that sounds' [387,464)
plus 12 frames afterward. Later shots, including old s005 at frame 430, are
excluded from this isolated opening, not allowed to interrupt the phrase.

Both shotlist and cue snapshots use these revised boundaries. Production
shotlist/cues remain unchanged. The isolated Blender adapter changes only the
cue input path in the shared renderer at runtime; protected source resolver,
timebase conversion and lyric implementation remain the shared code.

Run python out/opening_phrase_cut/render.py. Preview: preview.mp4.
No footage generation, new credit spend or production adoption in this pass.
