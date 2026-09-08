# Green-light walk and moth audition

Preview song1374..1569,195frames at24fps, including the preceding garden entry.
Walk1412..1514 uses source0..102; moth1514..1569 uses source0..55. These are
phrase-contained review ranges, not a production shotlist edit. No generation.

The existing green guide light receives a modest vocal-level halo, then a much
broader bloom on green1475..1488 and light1488..1501, easing down on moving.
Colour/brightness tracking uses a local motion search and confidence gating.
When the source is occluded or cannot be located confidently, added light goes
away; no glow is synthesized through hidden geometry. Review crossing edges.

The moth uses a frame-local warm translucent-wing matte rather than a fixed
rigid outline. A quieter warm breath spans psychedelic1524..1553, with gentle
vocal dynamics and release into garden. Inspect peripheral matte leakage and
vein readability; this is a lightweight2D treatment, not a full creature solve.

Vocal source placement is +0.178348 seconds, applied once. Master audio and
lyrics are added once by the shared Blender assembly path. The original clips
remain unchanged. No processed handles or final mastering claimed. This is
pending owner review, not adopted. Controls and tracking confidence are saved
in controls.json; clean silent outputs are under walk/ and moth/.

The later walk return needs coverage planning: source-origin1412 implies source
238 on return1650, beyond the existing192frames. Do not restart or freeze this
take to fake continuous coverage. Choose alternate coverage or generate a longer
continuous take when reviewing that return.
