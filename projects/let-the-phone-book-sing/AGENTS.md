# Continuing Let the Phone Book Sing

Read CONTINUE-HERE.md and intake.json before production work. This project belongs to the shared toolkit repository and follows Together Anyways' timing-first workflow.

The master and current DAWproject are ingested; source-manifest.json records their checksums. The author supplied 38 lyric lines in nine sections. Do not request these inputs again unless the user changes them. timing-import.json records the verified zeroBeat 7, 795-point continuous tempo map and source offset. Do not substitute an older export, fixed tempo or stepped MIDI timing.

Preserve original references, author text and raw timing evidence. Keep phone-number/address spelling separate from performed-word hypotheses. timeline.json has 38 user-reviewed timed lyric lines; the editable EffectCraft/MP4 draft is generated/animatic/Let-the-Phone-Book-Sing-lyric-animatic-v001. The user reviewed the animatic and approved its timing on 2026-11-08; see lyrics/timing-approval-20261108.json. Preserve all accepted timing. See LYRIC-TIMING-REVIEW.txt before changing it; never rerun over user-accepted corrections. Review the timing animatic before generated footage. Once authored, shots/shotlist.json is the edit authority; re-plan with --merge and derive frame counts from the timing grid.

The user approved generated/covers/patience-pleasant-avenue-v001.png as the SONG cover and the video's visual direction. Preserve that image; it is not an album cover. Phone book is optional for most video shots. The narrator remains unnamed.

The Mac design handoff uses media-manifest.json. Restore and verify it before new work. The large DAWproject and replaceable stem/analysis WAVs remain on the PC; raw timing evidence, complete tempo/beat grid, master, artwork and native/MP4 preview are included. Use timeline compile/validate on the cached grid; do not run sync without separately restoring the original DAWproject. Do not ask for the master/lyrics again or rerun alignment just to change machines.

Large media stay in ignored generated/. Local paths/runtime settings belong only in ignored project.local.json. For a later handoff, publish a new immutable media snapshot and authored changes together; never overwrite an existing snapshot or differing local assets.

## Compositing workflow

The user explicitly requires EffectCraft for compositing, editing and motion graphics. See production/effectcraft-workflow.txt and sources.effectcraftProject. Keep effects editable in the native project; use original footage and existing artwork as inputs. Do not silently revert to Python/Pillow/FFmpeg compositing. Preserve approved renders for comparison; the native migration is a review draft, not automatically an approved visual replacement.
