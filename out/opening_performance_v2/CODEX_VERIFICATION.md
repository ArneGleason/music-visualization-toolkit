# Verification and preview delivery

All four manifest hashes independently verified: first frame, guide, base and
synced result. Claude's receipt remains intact. No new generation or credit spend.

Guide Pearson correlation is 0.999494 at zero lag; best lag in +/-50 ms search
is zero. This replaces reliance on the receipt's differently normalized 1.006
score, which is not a conventional correlation coefficient. Clock conclusions
agree. Picture has 239 frames at 30 fps (7.966667 s); audio is 7.895011 s.
The absent tail is not counted as full eight-second delivered coverage.

Source timestamp-conformed to 24 fps without slowdown. Original files untouched.
review.py completed and verified the production shotlist hash stayed unchanged.
Both principal previews decode fully. Assembly has 192 frames at 24 fps and
eight seconds of master audio; both streams begin at zero.

- master_preview.mp4: uninterrupted new performance with the master, origin 143/24.
- comparison_guide.mp4: base left / Kling right, isolated verified guide.
- assembly_preview.mp4: same Blender assembler and lyrics, song [143,335).
  New source used only for s003 with source in-point 12/24. Scope protected
  selection retained; existing cutaway during 'It's important' retained.

Owner already reports v2 is substantially better, covers the words, and removes
blank mouth-animation gaps, though slightly too scat-like. Sampled visual review
supports increased expression through the earlier closed-looking interval.
Next-shot direction: purposeful conversational singing with groove, less scat
embellishment. Keep this test rather than repeatedly polishing it. Actual new
in-edit preview still awaits playback review; production not yet changed.

See ../HANDOFF_PROTOCOL.md for the shared-file status convention. Commits are
not necessary for local visibility and do not notify the other agent by themselves.
