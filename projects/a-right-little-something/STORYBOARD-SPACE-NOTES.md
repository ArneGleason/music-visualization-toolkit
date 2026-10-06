# Space continuation — first blocking proposal

Source: listening-notes revision 22. Five active new notes at frames 581, 633,
737, 789 and 854. The deleted eye-reflection note at 789 is superseded by the
active close-up at 854. Original notes are preserved verbatim in the register.

Review: http://127.0.0.1:8768/storyboard/space-notes-v01/

This is a proposal in `shots/shotlist.json` under `storyboardProposals`, merged
using `tools/shotplan.py --merge`. The accepted v03 shot selection and its
selected source shot records are unchanged. The first new note revises the last
52 frames of opening-005; it is not an additional overlapping selected shot.

The full listening animatic now selects `A-Right-Little-Something-space-blocking-v04.mp4`:
v03 picture before frame 581, Blender proposal motion at frames 581–911, then
the existing lyric canvas. It retains all 5265 frames, the exact master AAC
packets and small bottom lyric timing. The presentation is 1920×1080; the
inserted 640×360 blockouts are scaled review proxies, not final-resolution
footage. `reviewEdits.space-blocking-v04` in the shot register records this
temporary review assembly, leaving the accepted source shot selections intact.

Moon placement is inherited from the shared world, not attached to the camera.
Most interior compositions look toward the same background hemisphere, which
explains their recurring positions. Final illustrations need not feature both
moons in every angle; preserve distant identity when visible, and allow them
to leave the frame naturally.

| Beat | Song frames inclusive | Cinematography / transition |
| --- | --- | --- |
| space-006 | 581–632 | Cut on “To” to the immense world below; small ship, restrained widening |
| space-007 | 633–736 | Cut to three-quarter interior and holographic map; locked camera, expansion in the diagram |
| space-008 | 737–788 | Cut to reaction: wonder becomes longing; start continuous approach |
| space-009 | 789–853 | Continue that same take toward the boundary; no cut or starting-frame reset |
| space-010 | 854–911 | Cut to close portrait, cosmic light reflected in eyes; hold |

Five note beats become four generated/edit shots. Reaction and window approach
share one source take (117 edit frames + 24 handle frames = 5.875 seconds;
request at least six seconds if the provider requires integer durations).
The map holds through the gap after “So much room here up in space.” Finish
before “Stretch your arms wide,” where no further direction is yet provided.

The review has 38 frames of accepted “All windows” context, then 331 proposed
frames: 369 frames / 15.375 seconds at 24 fps, song 22.583–37.958 seconds. Master
audio comes from the existing accepted full animatic. Small bottom lyrics use
the original word frames and performed spelling. Every Blender source has
12-frame handles on both sides. Review motion is a rough 640×360 blockout,
presented at 960×540; it is not clean 1080p generated footage.

## How to make the illustrated shots

Use these Blender compositions as framing references, then approved Harper
and ship stills to make ImageGen starting/ending frames. Keep Kling responsible
for the living illustrated performance. Do not turn the proxy mannequin into
the final actor or force the whole ship into a native Blender production.

The hologram is the strongest candidate for a separate Blender effect:
planet → orbital system → local stars with stable invented glyphs and finger
interaction targets. The current Blender orbit rings are only a spatial
layout proxy; the actual scale transitions, glyphs and interaction animation
remain to be authored. Match the generated hand performance before final
effect alignment. Avoid a whole complicated map expansion in one Kling prompt.

Use one beginning/end-conditioned take for reaction and approach. Keep the
camera safely inside the thin shell; the Blender builder checks every camera
frame for clearance. Preserve direction toward the bow (-Y). The final portrait
uses rough eye-position cues, not a demonstration of the reflected-eye effect.
ImageGen should establish the expression; Kling supplies restrained movement;
Blender can add controlled cosmic glints if they otherwise crawl.

Prompt-lock revision 2 now permits the requested diegetic holographic display
and invented glyphs while retaining the ban on unrelated interface graphics.
All active shots and proposals share this new lock. See HOLOGRAM-DIRECTION.md
for the three illustrated scale states and full-song animatic v05.

Rebuild:

    python tools/plan_next_space_batch.py
    python tools/shotplan.py --merge --project projects/a-right-little-something/project.json --batch projects/a-right-little-something/storyboard-space-notes.json
    blender -b --python tools/build_storyboard_batch.py -- projects/a-right-little-something/project.json projects/a-right-little-something/storyboard-space-notes.json --motion
    python tools/review_space_notes.py
    python tools/insert_blocking_animatic.py projects/a-right-little-something/project.json projects/a-right-little-something/storyboard-space-notes.json
