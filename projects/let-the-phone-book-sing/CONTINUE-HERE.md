# Let the Phone Book Sing

## Animatic viewer — added 9 November 2026

Double-click `Review Let the Phone Book Sing.command` at repository root, or run `./.venv/bin/python3 projects/let-the-phone-book-sing/production/open_review.py`. Opens the same shared frame-review UI used for Together Anyways at http://127.0.0.1:8778. Reuses its server on subsequent launches.

Current review is the approved opening through May (34.5s). Select named PB shots, navigate lyric sections, step exact frames, copy frame references, and save notes. Master frame numbering is zero-based, matching this project; preview numbering is one-based. Notes persist in `production/frame-review-notes.json` when first written, separate from Together Anyways. Navigation derives from shotlist.json; paired lyric beats inside continuous takes are markers, not extra cuts. Edit `production/review-config.json` to select the next longer native export, then rerun the launcher. The viewer does not render or alter the edit.

## Resume here — night checkpoint, 8 November 2026

**What we were doing:** building the opening of Let the Phone Book Sing in EffectCraft. The narrator, Belle at 2B, Liberty Bell and April Bloom have moving footage. May Bloom is still an illustrated placeholder. The user approved the current hair cleanup and liked the assembled opening through May before stopping for the night.

**Start next time:** briefly remind the user of this status, show the latest animatic if helpful, then develop May Bloom’s mechanical repair-shop/fan skit. Show the proposed starting frame and motion/emotional direction before generating footage. Her existing situation still is the happy fan-breeze payoff, so decide whether it needs a before-action starter variation. No generation has been authorized/submitted for May yet. After May, plan a fresh chorus performance plate.

Current editable keeper: `generated/effectcraft-edit-v006/Let-the-Phone-Book-Sing-editable-v006.ecproj`.
Latest review: `generated/effectcraft-edit-v006/animatic-through-may-bloom-1080p.mp4` — 1920×1080, 24 fps, 828 picture frames (34.5 seconds), master audio and removable small bottom lyric overlay. Stops at the current chorus insert boundary; May is a still, not missing video.

Decisions to preserve:
- EffectCraft is the compositor/editor. Keep native layers editable; do not rebuild over v006 with the initial builder or revert to custom compositing.
- v006 Screen Key plus isolated green/cyan hair color cleanup is approved. See `production/hair-color-v006.json`. Reuse as a starting point on chorus plates, adapting the soft head mask to each framing. Slight residual tint was accepted; do not keep chasing it without a request.
- Keep SING v002 whole-word orbit, amplitude swell and black narrator outline. Later independently orbiting letters were rejected for readability. BELLE lettering is spelled B-E-L-L-E and belongs on first Belle, not Liberty.
- Musical cuts stay fixed; adjust source offsets for action. Belle uses original source frames 42–166 at 124/140 source frames per edit frame. Four-frame dissolves are centered on actual cuts. Avoid duplicated frames or initial frozen action.
- April’s original footage is accepted; the tracked yellow-flower recolor was rejected. Do not reinstate it.
- Hedra is preferred for singing and expressive performance; green screen works. Use native 1080p for final plates. Kling supplies scene action, with actor motivation, subtle camera motion when useful and about one second of source handles on each end. Check uploaded references before spending credits.
- Full edit still contains a temporary lower-resolution/watermarked chorus test after this review segment. It is not final; replace with a new Hedra chorus plate and approved key/color setup.
- Reuse ONE EffectCraft GUI instance (currently v006). Use File > Open or Launch Services; never directly spawn another editor per revision. Temporary headless authoring/render processes should exit.

Backup: `backups/approved-media-20261108-v020.json` is the night snapshot with current native project, both reviews and every native footage/art dependency. Prior v001–v019 snapshots preserve earlier approved work and character references. Media remain outside Git, on GitHub Releases; authored files and notes are in Git. The native project currently stores absolute media paths for this checkout: on another machine, relink the listed files to the restored project rather than regenerating assets. Local runtime configuration stays ignored; the working app and CLI are EffectCraft 0.22.0 (the app bundle still has an older filename).

The sections below are historical context; this checkpoint supersedes stale stage/next-action statements.

## Continue on the MacBook

Checkpoint: 7 November 2026. The square song cover and its visual style are approved. Continue video design from that image; do not regenerate the approved cover. The singer remains unnamed. On 8 November 2026 the user confirmed reviewing and approving the animatic timing. Preserve it; see lyrics/timing-approval-20261108.json. Proposed listing gags, cast and chorus arc are in visual-development/story-treatment-v001.txt; these creative proposals are not yet approved.

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
- Project configuration and timeline tracks for lyrics, scenes, transitions, action and notes. The lyric track contains all 38 supplied lines across nine sections with timing reviewed and approved by the user on 8 November 2026.
- User-confirmed master WAV copied intact to generated/source/master.wav; checksum and exact sample count are recorded in source-manifest.json. It is 48 kHz, stereo, 24-bit, 180.800291667 seconds. The native Bitwig project has been discovered; local candidate paths are in ignored project.local.json.
- Author lyric sheet preserved at lyrics/approved.txt and as an original intake copy under generated/source/. Names, addresses, numbers, repeats and section headings are retained; headings are metadata, not sung lines.

## Timing reviewed; ready for visual development

On the PC, the original fresh DAWproject is retained at generated/source/Let-the-Phone-Book-Sing-current.dawproject. It is omitted from the design snapshot. Its continuous 795-point tempo map (82.49–91.98 BPM, 4/4) is imported and included. Source/master waveform comparison across five lead windows, with bass and guitar crosschecks, establishes master zero at project beat 7. The source stems begin 0.423551391 seconds after master zero; measured lead residual is 0.074 ms at the 8 kHz correlation resolution. See timing-import.json and generated/alignment-check/.

The user has reviewed timing in generated/animatic/Let-the-Phone-Book-Sing-lyric-animatic-v001.mp4 and approved it on 8 November 2026. Preserve the accepted edges. The matching .ecproj has 22 editable lyric page compositions and 203 displayed word/number groups. There are 306 spelled-out spoken-word candidates underneath the original display spelling. The review preview is 1280x720 at 24 fps; future final picture remains planned at 1920x1080. Master, lyrics and saved timing are present; do not ask for them again. Current priority is video design, not a new automatic alignment pass.

Embedded lead/backing stems and active-clip master-clock analysis WAVs remain on the PC. These proxies did not recreate track devices or clip fades. Raw Whisper/CTC JSON, CSV and diagnostic notes are included in the snapshot; redundant proxy WAVs and their standalone audition HTML are omitted. The final master is the listening authority.

## Workflow from Together Anyways

Verify source versions and export range first. Use DAWproject for the continuous tempo map and exact bar/beat grid. Derive frame boundaries from that grid. Do not reuse Together Anyways' 7.5 zeroBeat or any of its lyric timings.

Use unprompted Whisper as acoustic evidence, then align the supplied performed lyrics in broad phrases/sections. Preserve raw timings and master/source offsets. Numeric addresses and phone numbers need pronunciation review: retain the original numeric author text separately from any spelled-out alignment transcript. Review sustained notes, repeated calls and echoes; do not force word starts onto arbitrary beat subdivisions or invent extra lines from delay effects. Record user-approved corrections and retain them in later passes.

The editable native EffectCraft timing/lyric animatic now follows the previous project's workflow. The exact grid and structural/native checks are complete. The user approved the existing animatic timing on 8 November 2026. Historical machine flags remain in the evidence. A proposed story treatment is recorded; final shot planning and visual-animatic review remain outstanding.

When shots are authored, shots/shotlist.json is the edit authority. Re-plan with tools/shotplan.py --merge, preserve hand-written direction and use frame counts from the timing grid. Review the animatic before spending on generated footage.

## Creative scope

Read visual-development/cover-and-video-brief.txt for the latest user direction. Extend the singer reference's elongated illustrated proportions into a city of unusual residents and activities. As she sings each phone-book listing, cut into that address's life. She is a visible narrator within the space, performing to us; residents cannot perceive her and their behavior is unaffected. The latest direction explicitly includes her opening/singing from a ratty phone book, superseding the earlier visual exclusion.

APPROVED SONG COVER: generated/covers/patience-pleasant-avenue-v001.png. The user called this perfect for the song cover and wants the video to retain this style/look. Preserve the exact image. It shows the expressive singer and open directory in the left foreground, the plaque reading 1 Pleasant Avenue, and Patience descending from upstairs behind her while checking her watch. This approval is for the picture and visual direction, not word timing.

Patience is an impatient woman who is always late. Her tall/angular design, sculptural hair, cream glasses, coral/chartreuse/plum outfit, mustard bag and watch are recognizable anchors. The city is fictional, warm and coastal, influenced by San Francisco/San Diego and a design-conscious 1970s-inflected residential neighborhood. Continue with distinct exaggerated residents for the other listings. The singer is visible to us but unnoticed by residents. The phone book is useful in this still and optional for most video shots. Individual animation turnarounds and future scenes require their own review.

## Storage and tools

Authored JSON, prompts, lyrics and notes belong in Git. Large media belong under ignored generated/. The GitHub design snapshot is listed in media-manifest.json; local-only DAW/stem files are intentionally outside it. Machine-specific paths belong in project.local.json, which is not transferred. For subsequent machine switches, checkpoint both authored edits and a new immutable media release. Never replace the current tag/archive or overwrite differing restored assets.

Run repository tools through its own environment: .venv/Scripts/python.exe on Windows, .venv/bin/python3 on Mac/Linux. Use timeline compile/validate on the restored grid; sync requires the intentionally omitted source. Timeline validation passed for 38 timed items, and native validation checked all 203 displayed tokens and page bounds. production/README.txt records the historical full build route. The source master remains unchanged; the preview covers its complete duration with one fractional-frame silent tail. No Windows speech runtime is needed to view/revise the existing project or develop new visual designs.

## Approved visual and motion reference — 8 November 2026

The user approved the reference-assisted courtyard push test ("Yeah, that actually works great."). See environment-development/style-guide-approval-20261108.json for the approved exterior, narrator integration, detailed couple reference and motion example. Use textured graphic-novel rendering, strong tapered figure contours and distinct depth planes. Detailed references for characters approached by the camera improved close-view style in this test. Old Church Quarter is approved as the initial guide; remaining neighborhood exteriors are still to be developed one at a time. No more Kling tests are implicitly scheduled.

Spring–Worth exterior v002 palette was approved on 8 November 2026. Reference: generated/environment-development/spring-worth-v002.png. Petrol blue, dusty teal, burgundy and cream distinguish its shops/homes from Old Church peach and terracotta. See environment-development/spring-worth-approval-20261108.json. Remaining areas: Financial District, Park–Orchard/Pleasant Avenue, Canal District. Continue one at a time.

Canal District v002 approved on 8 November 2026: converted brick warehouses/lofts, industrial windows, preserved loading doors/hoist, restrained modern additions. Reference: generated/environment-development/canal-district-v002.png. Canal connects toward the provisional financial skyline beyond the bridge. See environment-development/canal-district-approval-20261108.json. Remaining areas: Financial District and Park–Orchard/Pleasant Avenue.

Financial District v003 approved 8 November 2026, including revised casually dressed wealthy man with toupee. User requests Park–Orchard next, before revisiting supporting characters in previous areas.

Park–Orchard v001 approved 8 November 2026. All five neighborhood environment directions now reviewed. Next: character revisions to Old Church, Spring–Worth and Canal, one at a time. User considering later standalone character and clean architecture references; preserve populated scenes as staging guides.

Old Church supporting-cast revision v005 approved 8 November 2026. Keep generated/environment-development/old-church-quarter-v005.png as latest populated exterior. Five residents leave room for narrator. Next: Spring–Worth character revision, then Canal.

Spring–Worth supporting cast v003 approved 8 November 2026. Latest populated shop exterior: generated/environment-development/spring-worth-v003.png. Next: Canal supporting cast.

Canal supporting cast v008 approved 8 November 2026. Latest populated canal exterior: generated/environment-development/canal-district-v008.png. Original action-comedy bike mechanic and older comic plant enthusiast replace celebrity likenesses; preserve corrected bridge railing and recessed warehouse doorway staging. See environment-development/canal-district-cast-approval-20261108.json. All five neighborhood populated references are now approved. Standalone character references and clean architecture plates remain possible future work, not yet commissioned.

Old Church Quarter second pass v006 approved as keeper 8 November 2026, superseding v005 as latest populated reference. Performer archetypes guide expressions and behavior, never recognizable celebrity caricatures. User authorized second pass on remaining neighborhoods, continuing one at a time: Spring–Worth, Financial District, Park–Orchard. Canal v008 already incorporates this approach. See environment-development/old-church-quarter-second-pass-approval-20261108.json.

Spring–Worth second pass v004 approved 8 November 2026, superseding v003 as latest populated shop reference. See environment-development/spring-worth-second-pass-approval-20261108.json. Next: Financial District second pass, followed by Park–Orchard, with review between scenes.

Financial District second pass v004 approved 8 November 2026, superseding v003 as latest populated financial reference. See environment-development/financial-district-second-pass-approval-20261108.json. Park–Orchard is the last neighborhood awaiting its second character pass and review.

Park–Orchard latest review image is v005: older Italian-American lawn trimmer in too-tight blue tracksuit, weight reduced slightly from v004. User moved on to featured-cast inventory. Canal bridge woman remains background; user explicitly declined further revision unless featured. See character-development/featured-cast-register-v001.txt for all 16 lyric residents plus narrator, proposed reuse of existing designs, and unresolved casting. Casting suggestions and old skit premises are not approvals; next work is matching characters and stronger skits to listings.

Featured characters now being developed one at a time, starting with Belle Bell. First reference: generated/character-development/belle-bell-reference-v001.png, awaiting review. Proposed retired cabaret performer carefully choosing extravagant earrings for taking out rubbish. Character identity sheet first; scene staging images follow when shots are settled. See character-development/belle-bell-reference-v001.notes.txt.

Belle identity v002 (left-cheek beauty mark) and situation v001 are approved; see their approval records. User requests individual facial signatures across cast, and a visible telephone in each room whether used in gag or not. Situation may be interior or exterior according to skit. Next character Liberty Bell: generated/character-development/liberty-bell-reference-v001.png is proposed, awaiting review. Retired stage technician with cleft chin and asymmetric brows; exact skit and setting remain open.

Liberty identity v003 approved: cowboy hat, braided pigtails, spotlight-logo tee, olive utility skirt. User chose rabbits instead of tortoise for her urban-ranch gate skit. generated/scene-development/liberty-bell-situation-v001.png now awaits review: three rabbits and cream wall phone visible inside doorway at number 76. Future animation start frame may precede the pictured rabbit release. Next lyric resident after Liberty is April Bloom; continue one at a time.
