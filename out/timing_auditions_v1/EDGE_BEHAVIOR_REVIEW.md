# Phrase-edge behavior after timing auditions

Owner feedback: corrected timing is better mainly inside phrases. Opening remains
weak at entry; cut 43 improves then becomes unconvincing again; outro mouths move
after the speaker should have finished. Earlier isolated previews appeared better.

## Focused evidence

- A1 guide is eight seconds long. Samples from 1.9..3.5 seconds are exactly zero
  after decoding the uploaded WAV. The corresponding downloaded clip's embedded
  audio is also silent there (only negligible codec residue near the start).
- Inspected synced A1 images at 2.2, 2.5 and 2.85 seconds show different open-mouth
  shapes during that silent stretch. The effect is already present in the synced
  source, not invented by the assembly or the preview's audio running out.
- The generated A1 base has open-mouth performance at the same positions, but
  base and synced mouth shapes differ in inspected corresponding frames. This
  does NOT prove a literal switch back to untouched base frames. It supports the
  broader concern that silence is not producing a convincing resting/listening
  mouth in this result. Model internals remain unknown.
- Cut 43 is a different case: its eight-second retimed guide remains active at
  1.9..2.5, 2.5..3.5, 4..5 and later seconds. At 2.5..3.5 its RMS is about -20.4
  dBFS. Running out of the audio file cannot explain its visible tail behavior.
  Base-performance influence or weak phoneme tracking is possible but unconfirmed.
- The corrected opening intentionally has five held head frames, and cut 43 C
  four. These are disclosed diagnostic placeholders for absent coverage, not
  completed entrance fixes. Their onset shortcomings cannot be judged as failures
  of a new pre-roll generation, because none has been generated yet.

## Working conclusion and next test

Timing repairs and believable speech/rest transitions are separate acceptance
criteria. Do not keep shifting a correctly aligned take to compensate for a
mouth that keeps performing through silence.

Before a larger regeneration pass, test one expressive but non-speaking base
take: relaxed closed/resting lips before and after delivery, no invented talking
or broad smile, while retaining appropriate head/body acting. Give the sync pass
the correctly placed vocal with genuine preceding/following context. Include a
deliberate silent listening interval and inspect entrance, middle and rest tail
separately, first against the supplied guide and then against the same master in
the shared assembler. This is a proposed test, not generated work.

For existing shots, a listening/reaction insert after a completed thought is a
valid editorial repair when it serves the scene. It should not be used to claim
the underlying silent-mouth problem is solved. Half-second pre-roll addresses
missing entry context; it does not guarantee mouth closure in silence.

No new render, regeneration or production edit made during this focused check.
