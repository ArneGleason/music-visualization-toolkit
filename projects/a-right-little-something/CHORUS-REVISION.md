# Chorus revision — October 10 feedback

V25 (`revision-chorus-v05.json`) revises the final orbit with distance-dependent
loop speeds, native shutter blur, a brighter tracking core and a quickly fading
bright wake with a long faint tail. Other v24 footage and fades are retained.
Review: http://127.0.0.1:8768/storyboard/chorus-revision-v05/ .

V24 (`revision-chorus-v04.json`) fills the final scale-shot placeholder with
the explicitly approved Kling `scale-reveal-motion-v01` take. It adds cloud,
light and small ship/character movement under the same editorial Ken Burns
reveal at frames 854–911. The established v23 edit and master timing remain.
Review: http://127.0.0.1:8768/storyboard/chorus-revision-v04/ .

Latest direction is v23, `revision-chorus-v03.json`: use fades throughout this
coverage/chorus sequence, including the approved portrait and scale insertion.
Reserve zoom blur for a motivated move between connected spaces. Every fade
remains centered on its existing lyric boundary; chorus entry is still 43.54s.
The foreground walking and key wide are now actual Kling animation; the scale
reveal is still an illustration with a Ken Burns move. The last orbit uses
curvature-matched continuous loops and age-decayed trails from Blender. See
[BLENDER-ORBIT-DIRECTION.md](BLENDER-ORBIT-DIRECTION.md) for the current details.
The v21 description below is retained as production history.

This is a composition and editing review of v20. The versioned proposal lives
in `shots/shotlist.json` under `editProposals.chorus-revision-v01`; the original
stills, motion selections and v20 remain available. The authored recipe is
`revision-chorus-v01.json`. Existing DAWproject-derived phrase boundaries supply
the frame counts; there is no tempo or timing re-plan.

| Song time | Song frames, inclusive | Revision |
| --- | --- | --- |
| 32.83s | 789–853 | Shorten the starward portrait to the window phrase. |
| 35.54s | 854–911 | Reveal scale using the accepted opening pullback's distant ship and planet. This is an intentional reuse, not a new Kling shot. |
| 38.00s | 912–1045 | Retain the shore / arms-wide performance. |
| 43.54s | 1046–1169 | Retain the mission performance; add a restrained image-plane push. |
| 48.71s | 1170–1227 | Retain the small water intervention. |
| 51.12s | 1228–1262 | New creature-level still composition: the life being affected looks back at Harper. |
| 52.58s | 1263–1291 | New wide still composition: branching living channels make the modest intervention consequential. A shadowed side patch leaves the outcome unresolved. |
| 53.79s | 1292–1411 | Retain the first orbit performance. |
| 58.79s | 1412–1549 | Clean three-world Kling background with gentle pullback, plus authored route / tiny ship animation. |

The two new character/ecology compositions remain stills with image-plane
motion, pending review before buying animation. The wide reveal has a more
visible Harper than the prompt requested; assess its dramatic scale in context.
The mission push is a flat image-plane transform, not a new 3D camera move.

Two otherwise identical previews compare fades and zoom blurs. Most overlaps
last ten frames; the boundaries at 1263 and 1292 use six frames so the short key
phrase remains readable. Each transition is centered on its original frame
boundary. The chorus enters at 1046, without extending the shore hold. Handles
are separate from the overlap duration. Lyrics are rendered after transitions.
The zoom-blur trial uses a bounded eight-percent centered zoom pulse and blur
over a dissolve; it does not magnify the outgoing picture indefinitely.
V21 uses the zoom-blur version as a working review draft; no final transition
selection is inferred.

The final orbit source contains no navigation curves. Kling's pullback is
modest, with foreground rotation and differential movement. World-position
anchors are estimated from the captured frames; these are not feature tracks.
The tiny craft and its trail use the exact same authored curve, preventing the
previous disagreement between a baked route and model-generated travel.

Only one new paid video was generated: `orbit-pullback-v01`, eight seconds,
193 native frames at 24fps, 1916×1080. It cost 64 credits and is collected.
Total recorded Kling spend is now 1,640 credits. The request, response,
clean source and continuity frames remain under `generated/kling-tests/`;
the ledger is `generated/review/chorus-revision-v01-ledger.json`.

Review: http://127.0.0.1:8768/storyboard/chorus-revision-v01/ .
Build with the repository Python environment and `tools/build_chorus_revision.py`.
The builder checks 761 preview frames, 5,265 full-song frames at 24fps,
1920×1080, and unchanged master AAC packets before publishing the draft.
Large media and route-frame sequences stay out of Git.
