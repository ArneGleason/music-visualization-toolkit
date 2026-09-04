# Lyric motion pilot — opening phrases

Status: first working Blender pilot rendered; awaiting owner review.

Pilot range: frames 150–725 at 24 fps (approximately 6.25–30.21 seconds).
This covers the first six phrases, from “Hey, I need you for something” through
“Then they don't quite match.”

## Review render

`out/lyric_motion_pilot_v03.mp4` is the current 1280×720 review version. It is
24 seconds long, includes the matching music segment and eight selected
storyboard cuts, and animates 116 individual glyphs. The media file remains
local and ignored by Git. `out/lyric_motion_pilot_v03_contact.jpg` is a static
QA sheet, not a substitute for judging the motion in the video.

The implementation treats rigidity as a continuum from 0.0 (soft rubber) to
1.0 (steel). Low-rigidity words pass motion through their letters with delayed
bends, squash/stretch, overshoot, and unequal follow-through. High-rigidity
words move nearly as one block and settle quickly. Because a phrase may assign
different rigidity to each word, the apparent material can change mid-phrase.

## Why the words disappeared

The current Blender compositor still has its original `--lyrics` option. The
latest favorites animatic was rendered without that option, so its captions
are absent rather than lost. That existing option creates one static text strip
per lyric line, fades it in and out, and colors it by speaker.

There is also a useful earlier treatment in `tools/stage.py`: it places words
inside the known line timing, lets vocal energy travel through the letters,
and makes active letters brighten, lift, and swell. The pilot should adapt
that idea to Blender while adding a restrained semantic gesture for a few
important words.

## Recommended visual grammar

Keep the full phrase readable at the bottom throughout. Every word receives a
timed emphasis, but only one or two **hero words** per phrase perform a larger
semantic action. That prevents the result from becoming a row of bouncing UI
labels.

### Four motion dimensions

1. **Presence** — upcoming words sit at 35% opacity, the active word rises to
   100%, and spoken words settle to 72%. Them 1 is warm gold; Them 2 is cool
   cyan; narration is warm white.
2. **Weight** — ordinary words swell no more than 6%. A hero word may reach
   18–22%, with volume-preserving squash and stretch on impact.
3. **Path** — an active word may lift up to 24 pixels or travel horizontally up
   to 18 pixels at 720p. Curved ease-in/ease-out replaces mechanical bouncing.
4. **Relationship** — selected words can separate, approach, nearly align,
   recoil, or hand attention to another word. This is where the lyric becomes
   an interpretive dance instead of karaoke highlighting.

Limits for the pilot: scale 0.90–1.22, rotation within ±4°, one line whenever
possible, and no letter deformation that makes a word hard to read. Each word
uses a two-frame anticipation, a two-to-four-frame attack, and an unequal
six-to-ten-frame settling tail. Function words usually receive presence only.

### Position and type

- Center the phrase in the lower safe area, baseline about 64 pixels above the
  bottom of a 720p frame.
- Use a bold, clean face around 44 pixels at rest, with the existing dark
  shadow/outline for contrast over changing stills.
- Preserve the complete phrase across picture cuts. Text timing belongs to the
  song, not to an individual storyboard image.
- A line appears four frames before its first word and leaves six frames after
  its last word. The next line can inherit the outgoing line's final motion.

## Phrase choreography

The catalog IDs below come from `docs/CINEMATOGRAPHIC_METAPHOR_CATALOG.md`.
The dominant vocabulary is `CAM-ATTENTION-HANDOFF`, `FRAME-SCALE-BILLING`,
`PERF-RESPONSE-CHAIN`, `ANIM-ANTICIPATION`, `ANIM-SQUASH-STRETCH`,
`ANIM-FOLLOW-THROUGH`, `SONIC-TRAVELLING-RIPPLE`, and
`EDIT-GRAPHIC-MATCH`.

### 1. “Hey, I need you for something.” — address travels outward

The phrase begins as a direct summons. “Hey” catches attention, “need” gains
weight, “you” hands the gaze toward the unseen listener, and “something” opens
a small charged void inside the line. Dominant devices:
`CAM-ATTENTION-HANDOFF`, `FRAME-SCALE-BILLING`, and
`FRAME-NEGATIVE-WAKE`.

| Word | Provisional cue | Action |
|---|---:|---|
| **Hey** | 6.483–7.307 s · f156–175 | Enter 10 px from the left, pop to 110%, overshoot by 2°, then settle—one clear attention knock. |
| I | 7.307–7.718 s · f175–185 | Quiet warm-gold anchor; presence change only. |
| **need** | 7.718–8.546 s · f185–205 | Lean 3° forward and grow to 115%, holding slightly longer than the syllable. |
| **you** | 8.546–9.370 s · f205–225 | Slide 16 px to the right while the previous words ease back, passing attention offscreen. |
| for | 9.370–10.195 s · f225–245 | Connective word; small 4% lift only. |
| **something** | 10.195–11.850 s · f245–284 | Widen tracking around the middle letters to form a brief gap, then let the letters curve back around it without completely closing. |

### 2. “It's important.” — the line acquires mass

The small lead-in yields to one heavy word. “Important” should feel weighted,
not merely large. Dominant devices: `SONIC-MASS-FOLLOWER`,
`ANIM-SQUASH-STRETCH`, and `ANIM-FOLLOW-THROUGH`.

| Word | Provisional cue | Action |
|---|---:|---|
| It's | 11.850–12.508 s · f284–300 | Brief upward pickup, carrying the last motion of “something” across the picture cut at f293. |
| **important** | 12.508–13.817 s · f300–332 | Rise to 121%, drop 8 px with a 6% vertical squash, rebound once, then hold its visual weight through the instrumental space. |

### 3. “More than that sounds.” — comparison becomes sound

The phrase changes from measurement to vibration. Dominant devices:
`FRAME-SCALE-BILLING`, `CAM-ATTENTION-HANDOFF`, and
`SONIC-TRAVELLING-RIPPLE`.

| Word | Provisional cue | Action |
|---|---:|---|
| **More** | 16.133–16.846 s · f387–404 | Stretch horizontally to 118% while staying the same visual volume; become literally more without simply zooming. |
| than | 16.846–17.559 s · f404–422 | Take a small step right, establishing a comparison axis. |
| that | 17.559–18.277 s · f422–439 | Answer from the other side of the axis; preserve position through the picture cut at f430. |
| **sounds** | 18.277–19.350 s · f439–464 | Split only this hero word into letters; send one shallow vertical ripple left-to-right, then let the last letter trail and settle. |

### 4. “I've got pieces.” — the word becomes an arrangement

The phrase begins intact and ends as a collection. Dominant devices:
`FRAME-CENTRIFUGAL`, `PERF-RESPONSE-CHAIN`, and `ANIM-FOLLOW-THROUGH`.

| Word | Provisional cue | Action |
|---|---:|---|
| I've | 21.517–22.536 s · f516–541 | Fade up as a stable phrase anchor; no semantic deformation. |
| **got** | 22.536–23.555 s · f541–566 | Compress down 5 px like a hand taking hold, then stop firmly. |
| **pieces** | 23.555–25.100 s · f566–602 | Divide the letters into three still-readable clusters; drift them 8–14 px apart on unequal arcs, with the final cluster lagging across the cut at f568. |

### 5. “Things that almost fit.” — an incomplete convergence

Two parts approach a solution but preserve a visible seam. Dominant devices:
`FRAME-CENTRIPETAL`, `PERF-RESPONSE-CHAIN`, and `EDIT-GRAPHIC-MATCH`.

| Word | Provisional cue | Action |
|---|---:|---|
| Things | 25.817–26.296 s · f620–631 | The separated clusters from “pieces” reform into one readable word. |
| that | 26.296–26.624 s · f631–639 | Presence handoff only; it bridges the picture cut at f637. |
| **almost** | 26.624–27.107 s · f639–651 | Compress horizontally toward an invisible center seam, slowing just before contact. |
| **fit** | 27.107–27.433 s · f651–658 | Snap toward “almost” but stop 6 px short; both words give a tiny unequal recoil. |

### 6. “Then they don't quite match.” — failed alignment

The phrase briefly appears orderly, then disagreement propagates through it.
Dominant devices: `EDIT-GRAPHIC-MATCH`, `ANIM-ANTICIPATION`,
`PERF-RESPONSE-CHAIN`, and `ANIM-FOLLOW-THROUGH`.

| Word | Provisional cue | Action |
|---|---:|---|
| Then | 28.333–28.601 s · f680–686 | Quick clean reset to a shared baseline. |
| they | 28.601–28.872 s · f686–693 | Settle beside “Then”; ordinary presence change. |
| **don't** | 28.872–29.139 s · f693–699 | Anticipate inward, then tilt 3° away and open a small gap. |
| quite | 29.139–29.547 s · f699–709 | Drop 5 px below the baseline as the disagreement travels right; remain continuous across the picture cut at f706. |
| **match** | 29.547–29.950 s · f709–719 | Arrive as if it will align, miss by one baseline step and 3°, contact visually, then recoil 12 px while the earlier words settle at different rates. |

## Timing note

These word windows are **provisional**. The line starts and ends are the real
register timings; individual words were distributed inside each line using the
repository's existing length-weighted fallback. They are suitable for judging
the shape and intensity of the motion, not for final sync.

Once the direction is approved, word attacks should be derived from the lead
vocal stem, checked by ear, and snapped to musically intentional frame or
eighth-note positions. Sung holds and consonants may require manual adjustment.

## Blender implementation used in the pilot

1. The existing `--lyrics` captions remain available as the simple fallback.
2. `shots/lyric_motion_pilot.json` holds the optional choreography; the pilot
   is not hard-coded into the compositor.
3. Blender VSE uses one text strip per glyph so each letter can bend and settle
   independently. Alternating channel banks let consecutive phrases overlap.
4. Opacity, color, position, anisotropic scale, and rotation are keyframed.
   Lyric transforms use auto-clamped curves; beat flashes keep their sharp
   linear timing.
5. Every glyph is placed around its own transform pivot, allowing local
   squash/stretch and rotation without pulling the whole word apart.
6. The lyric overlay is independent of shot boundaries, so a phrase and its
   gesture continue naturally over picture cuts.
7. The audition remains limited to frames 150–725. Do not expand to the full
   song until this motion language is approved.

## Review questions

- Is the basic warm-gold phrase at the bottom the right visual presence?
- Do the hero-word gestures feel expressive or too literal?
- Should active words behave more like typography, more like bodies dancing,
  or more like physical props in the scene?
- Is the amount of motion restrained enough to read while watching the images?
- If this vocabulary works, should later passages reuse these motifs—signal,
  pieces, failed fit, ripple—or invent a new gesture for every phrase?
