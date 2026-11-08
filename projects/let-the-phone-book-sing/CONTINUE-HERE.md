# Let the Phone Book Sing

## Continue on the MacBook

Checkpoint: 7 November 2026. The square song cover and its visual style are approved. Continue video design from that image; do not regenerate the approved cover. The singer remains unnamed, and word timing still awaits a listening review.

This is the shared repository: https://github.com/ArneGleason/music-visualization-toolkit

Clone it on the MacBook, or update an existing checkout without overwriting local work. Double-click **Setup Let the Phone Book Sing Mac.command** at the repository root (or ask Codex there to run it). This creates/reuses the Mac Python environment, restores this song's verified media snapshot, sets up the pinned Mac EffectCraft build and validates the cached timeline. The setup does not need the large DAWproject or a speech-model environment. Normal first-launch macOS approval may still be needed for EffectCraft.

Open a local chat in that checkout and say:

> Read AGENTS.md and projects/let-the-phone-book-sing/CONTINUE-HERE.md. Restore and verify the song's media if needed. Continue video design using the approved song cover's style. Preserve existing timing and references; do not rerun alignment or regenerate the cover.

The snapshot is named **let-the-phone-book-sing-20261107-v001**. media-manifest.json identifies the release ZIP and every file's checksum. Git holds the authored files; a plain Git pull does not download ignored images, master audio or the native/video previews.

To launch this song's native review after setup:

```sh
./.venv/bin/python3 tools/effectcraft.py --project projects/let-the-phone-book-sing/project.json gui
```

To recompile edited timeline annotations from the existing grid:

```sh
./.venv/bin/python3 tools/timeline.py compile projects/let-the-phone-book-sing/project.json
./.venv/bin/python3 tools/timeline.py validate projects/let-the-phone-book-sing/project.json
```

Do not run timeline **sync** on this design handoff: the 490 MB DAWproject is deliberately left on the PC. The continuous tempo curve, full bar/beat grid and compiled register are already included. Re-analysis would require restoring that source separately. Extracted stems, replaceable analysis WAVs, local model/runtime files and an intermediate picture-only render also stay on the PC. The confirmed master, all reference/cover imagery, lyric text, timing CSV/JSON, raw recognition/alignment evidence, font/license, final review MP4 and editable native project are included. Native footage uses portable relative paths.

The handoff was verified in a fresh relocated checkout on Windows, including media hashes, timeline validation and native footage loading. Mac app launch/GPU rendering must be checked on the MacBook itself. The large original sources remain intact on the PC.

This song lives inside the shared Music Visualization Toolkit repository, alongside Together Anyways. Start with project.json and intake.json. The earlier illustrated-singer folder is preserved as the character-design origin; current project copies live here.

## Ready

- First illustrated adult-female character reference: generated/character-development/character-reference-v001.png.
- Four source screenshots: generated/source-references/.
- Prompt, provenance notes and hash catalog: character-development/.
- Project configuration and timeline tracks for lyrics, scenes, transitions, action and notes. The lyric track contains all 38 supplied lines across nine sections with machine timing candidates, not listening-approved edges.
- User-confirmed master WAV copied intact to generated/source/master.wav; checksum and exact sample count are recorded in source-manifest.json. It is 48 kHz, stereo, 24-bit, 180.800291667 seconds. The native Bitwig project has been discovered; local candidate paths are in ignored project.local.json.
- Author lyric sheet preserved at lyrics/approved.txt and as an original intake copy under generated/source/. Names, addresses, numbers, repeats and section headings are retained; headings are metadata, not sung lines.

## Ready for timing review

On the PC, the original fresh DAWproject is retained at generated/source/Let-the-Phone-Book-Sing-current.dawproject. It is omitted from the design snapshot. Its continuous 795-point tempo map (82.49–91.98 BPM, 4/4) is imported and included. Source/master waveform comparison across five lead windows, with bass and guitar crosschecks, establishes master zero at project beat 7. The source stems begin 0.423551391 seconds after master zero; measured lead residual is 0.074 ms at the 8 kHz correlation resolution. See timing-import.json and generated/alignment-check/.

When reviewing timing, watch generated/animatic/Let-the-Phone-Book-Sing-lyric-animatic-v001.mp4 against the music and record corrections. The matching .ecproj has 22 editable lyric page compositions and 203 displayed word/number groups. There are 306 spelled-out spoken-word candidates underneath the original display spelling. The review preview is 1280x720 at 24 fps; future final picture remains planned at 1920x1080. Master, lyrics and saved timing are present; do not ask for them again. Current priority is video design, not a new automatic alignment pass.

Embedded lead/backing stems and active-clip master-clock analysis WAVs remain on the PC. These proxies did not recreate track devices or clip fades. Raw Whisper/CTC JSON, CSV and diagnostic notes are included in the snapshot; redundant proxy WAVs and their standalone audition HTML are omitted. The final master is the listening authority.

## Workflow from Together Anyways

Verify source versions and export range first. Use DAWproject for the continuous tempo map and exact bar/beat grid. Derive frame boundaries from that grid. Do not reuse Together Anyways' 7.5 zeroBeat or any of its lyric timings.

Use unprompted Whisper as acoustic evidence, then align the supplied performed lyrics in broad phrases/sections. Preserve raw timings and master/source offsets. Numeric addresses and phone numbers need pronunciation review: retain the original numeric author text separately from any spelled-out alignment transcript. Review sustained notes, repeated calls and echoes; do not force word starts onto arbitrary beat subdivisions or invent extra lines from delay effects. Record user-approved corrections and retain them in later passes.

The editable native EffectCraft timing/lyric animatic now follows the previous project's workflow. The exact grid and structural/native checks are complete. Word timing and numeric pronunciation remain provisional. Read LYRIC-TIMING-REVIEW.txt for review points; no listening approval or shot planning is recorded yet.

When shots are authored, shots/shotlist.json is the edit authority. Re-plan with tools/shotplan.py --merge, preserve hand-written direction and use frame counts from the timing grid. Review the animatic before spending on generated footage.

## Creative scope

Read visual-development/cover-and-video-brief.txt for the latest user direction. Extend the singer reference's elongated illustrated proportions into a city of unusual residents and activities. As she sings each phone-book listing, cut into that address's life. She is a visible narrator within the space, performing to us; residents cannot perceive her and their behavior is unaffected. The latest direction explicitly includes her opening/singing from a ratty phone book, superseding the earlier visual exclusion.

APPROVED SONG COVER: generated/covers/patience-pleasant-avenue-v001.png. The user called this perfect for the song cover and wants the video to retain this style/look. Preserve the exact image. It shows the expressive singer and open directory in the left foreground, the plaque reading 1 Pleasant Avenue, and Patience descending from upstairs behind her while checking her watch. This approval is for the picture and visual direction, not word timing.

Patience is an impatient woman who is always late. Her tall/angular design, sculptural hair, cream glasses, coral/chartreuse/plum outfit, mustard bag and watch are recognizable anchors. The city is fictional, warm and coastal, influenced by San Francisco/San Diego and a design-conscious 1970s-inflected residential neighborhood. Continue with distinct exaggerated residents for the other listings. The singer is visible to us but unnoticed by residents. The phone book is useful in this still and optional for most video shots. Individual animation turnarounds and future scenes require their own review.

## Storage and tools

Authored JSON, prompts, lyrics and notes belong in Git. Large media belong under ignored generated/. The GitHub design snapshot is listed in media-manifest.json; local-only DAW/stem files are intentionally outside it. Machine-specific paths belong in project.local.json, which is not transferred. For subsequent machine switches, checkpoint both authored edits and a new immutable media release. Never replace the current tag/archive or overwrite differing restored assets.

Run repository tools through its own environment: .venv/Scripts/python.exe on Windows, .venv/bin/python3 on Mac/Linux. Use timeline compile/validate on the restored grid; sync requires the intentionally omitted source. Timeline validation passed for 38 timed items, and native validation checked all 203 displayed tokens and page bounds. production/README.txt records the historical full build route. The source master remains unchanged; the preview covers its complete duration with one fractional-frame silent tail. No Windows speech runtime is needed to view/revise the existing project or develop new visual designs.
