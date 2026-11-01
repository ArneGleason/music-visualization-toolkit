# Together Anyways: continue on either computer

## Current checkpoint — accepted Scene 3 timing, 2026-10-31

Start here; the sections below are historical production notes and may contain superseded statuses or spend limits. User accepted the Scene 3 timing trial v017 and stopped for the night. No new generation is requested.

- Authoritative edit: `shots/shotlist.json`, 30 cuts, 24 fps, 1956 frames / 81.5 seconds, through the news report. Scenes 1–3 have 21 selected Kling motion clips; Scenes 4–6 remain approved starters.
- Scene 3 source starts: SH01 2.5s/frame60; SH02 2.25s/frame54; SH03 0; SH04 0; SH05 0. Musical lengths unchanged. SH01 has only18 frames of tail buffer; SH03–05 consume the head buffer. Accepted by user after review.
- Scene 1 SH06: revised Harper starter and Kling v008, source start12. Scene 2 SH3B: source start0, crate continuity preserved. Keep these accepted changes.
- Latest motion/review: `generated/kling-scene03-v016/review.html`; still changes: `generated/storyboard/scene03-eyelines-v015/review.html`. Latest clean animatic: `generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4`.
- All prompts, versions, receipts, reviews and timing notes are in `shots/`. Preserve the accepted cut and existing sources; do not regenerate on resume.

### Media backup and resuming elsewhere

The current `media-manifest.json` points to a new immutable GitHub Release snapshot of reference stills, character art, review boards, audio and project assets. **MP4s and decoded video frame caches are intentionally excluded at the user's request.** Older snapshots remain available. Local Mac videos are untouched.

On another machine, pull Git and run `./.venv/bin/python3 tools/project_media.py restore projects/together-anyways/media-manifest.json` (or run the existing Mac setup script). Then use `shots/video-recovery.json` to download selected original clips from Kling into their recorded project-relative paths. Most entries have direct result links; the opening aerial uses the pilot receipt/prompt and Kling history. Do not pay to regenerate missing video. The still/reference boards work without restoring MP4s, but the video animatic requires those local sources before rebuilding.

On this Mac, files and servers are already present: reference/media server on8766, frame-review player on8767. Resume by reading this section and authoritative shotlist, check the player, and ask for the next creative direction. Scene 3 accepted; likely next work is Scene 4, but no later generation is authorized yet.

## Historical production log

Latest **news-shade-v011**: only S06SH01/ta023 revised fromv010. Extended teal awning shades broker/Taffy area without obscuring incident; abstract alien glyph headline and ticker occupy lower broadcast bar. Same presenter, close framing and larger theft footage retained. Selected into current animatic;29cuts1956frames81.5s, all timings/music unchanged. Prior render at generated/storyboard/news-shade-v011/before-news-shade.mp4; prompt/review in shots/news-shade-v011.

Latest **style-news-v010**: selected ta004 and004b revise facial proportions/rendering toward ta003 (S01SH04) realistic illustration, preserving TV distraction and sleeve cue. ta023 (S06SH01) now tight monitor insert: larger elevated theft panel clearly shows Harper distracting broker and Taffy reaching beside his belt; small faces remain indistinct, same presenter/cyan broadcast. All29cut timings,1956frames81.5s, music, one-second handles and first3Kling clips unchanged. User accepted v009 door shots and reunion; preserve these. New selected assets in generated/storyboard/style-news-v010; style comparison at review/changes-board.html; prior animatic saved before-style-news.mp4. No additional Kling spend.

Latest revision **door-grip-v009**: user flagged backwards hand/wrist anatomy in v008 S05SH02/03. Replaced020 with a naturally supported left-hand grip and021 with a tighter hand/device/receiver insert. Grip matching is no longer mandatory: correct handedness, wrist and secure grasp take priority. Preserve backward-C receiver from unchanged019; proximity operation remains valid despite its shaped recess. Green activation segments and abstract status glyphs visualize authorization; full running sequence is future video direction, not generated motion. Cut021 now1799–1834 (35frames1.458s), on that in We use that;0201749–1799 (50frames2.083s). All other cuts and total1956frames81.5s unchanged. Reunion017/017b and celebrity004/004b accepted and retained. Previous render preserved under generated/storyboard/door-grip-v009/before-door-grip.mp4.

Latest revision **story-inserts-v008**: user accepted revised celebrity ta-004 and proposal ta-004b; dropped broker insert ta-005b (arm continuity concern); accepted ta-017b with grip correction. Active edit now29cuts,1956frames/81.5s. Split004 at559 (S01SH05/06), split017 at1549 (S04SH01/02), later shots renumbered within scenes. Reunion wide017 and reverse017b revised to match ta-013 grip and hand-relative device size. User clarified this is a proximity access credential, not a mechanical key: entrance020/021 revised to flat scanner and visible airgap; future action is scan/acknowledge/release, not insertion. Canonical working prop reference `shots/access-device-reference.txt`. First3Kling clips, music, all other cut points and one-second handles preserved; no Kling spend. Previous render saved at `generated/storyboard/story-inserts-v008/before-inserts.mp4`.

Latest still revision **story-inserts-v007**: Scene1 Shot5 / ta-004 now shows Taffy distracted by a frivolous, richly dressed celebrity panel, with Harper impatient to resume the heist. Same511–637frames. Three rendered insert proposals (not selected in active edit): ta-004b Harper redirects him (split559), ta-005b broker key close-up (split704), ta-017b Taffy reveals stolen key at reunion (split1549). See `shots/story-inserts-v007/insert-proposals.json` and `pacing-review.txt`; four-image review under `generated/storyboard/story-inserts-v007/review/proposals-board.html`. Original edit saved before this revision. Proposed splits preserve1956frames, accepted music, and24frame source handles. No more Kling credits spent. User wants stronger motivated camera action in future motion passes.

Latest motion edit: first3 Kling4 clips now downloaded into `generated/kling-pilot-v001/ta-000.mp4` through `ta-002.mp4` and selected in authoritative shotlist via videoSource/videoEdit. Current81.5s1956frame animatic includes these clips, master music only, original small lyrics/labels. A12frame dissolve centered on master109 uses handles; next cut at209. Gentle eased1–5% post push/pan. Remaining24cuts retain stills. Previous render saved as `generated/kling-pilot-v001/before-motion-animatic.mp4`. tools/animatic_media.py handles exact24fps source frames and centered transitions;2tests passed, all27timings/locks unchanged. Player8767 refreshed. No further credits spent.

Kling pilot v001: user approved375credits; first three shots submitted to Kling4.0 at1080p (7s,7s,11s), costs105+105+165. All three completed, downloaded and positively reviewed; see latest motion edit above. First two use Keyframes starters; third uses Omni references with ta002 composition plus direct Taffy v006 and Harper identity sheets. Browser Chrome Arne profile, Kling Default creation grid. Records/prompts and full-video credit estimate in `shots/kling-pilot-v001/`; screenshot `generated/kling-pilot-v001/submitted.png`. Planned local12frame dissolve trial at frame109, no fourth generation. Whole216.25s edit projects to~6524credits including10%redos at current shot density; current81.5s/27shots needs149rounded source seconds=2235basecredits/2459withredos. Includes one-second in/out handles. No further spend authorized beyond375trial.

Latest update **opening-continuity-v006**:27cuts, still1956frames/81.5seconds. Addedta000 high regional desert aerial0–109frames (4.542s), retained marketta001109–209; everylater timing unchanged. Scene01 now Planet to market, shots1–7. Opening plants settlement/canyon bridge/roads/mine/twin mesas for later ship-flight callback; altitude remains review point (still regional aerial rather than true near-suborbital). TA015 revised to rear-view forward-running Harper past Wedge, distinct from014c lookback dodge. Adjacent-pose review rule saved in AGENTS/workflow; audit and prompts under `shots/opening-continuity-v006/`. Full board `generated/storyboard/opening-continuity-v006/review/starter-board.html`; two changes at `changes-board.html`.

Player upgraded at http://127.0.0.1:8767/: previous/next shot buttons, scene/shot dropdown and [/] shortcuts, live current-shot selection. Launch with --shotlist as below. API shots read authoritative shotlist; note draft preserved when adopting renders. First/last boundaries and frame-base mapping tested. Current player opened at new intro.

Previous update **hands-news-v005**: S02-SH05/ta011 broker raised hand corrected to four fingers plus thumb. All26 selected images audited; other overlapping/gripping hands explicitly marked obscured where counts cannot be verified. Audit: `shots/hands-news-v005/hand-audit.json`. News now already playing at S05-SH01/ta019, continues ta022/023: one consistent presenter with distant softened aerial depot-theft inset, tiny figures/no readable faces; no wanted mugshots. Scene6 renamed The news report, noticing ongoing footage rather than activating screen. Electrician does routine work beside active display. ta024 reaction unchanged. Current full board `generated/storyboard/hands-news-v005/review/starter-board.html`; four-change board alongside at `changes-board.html`. Prompts/reviews in `shots/hands-news-v005/`. Shared prompt lock updated uniformly to v002; all26 cut timings and81.5second audio duration unchanged. Prior render saved as `first-run-before-hands-news-v005.mp4`.

Previous revision: five new **distraction-starters-v004** frames are now selected in `shots/shotlist.json` and the clean animatic. Harper performs a small trick with an internally lit blue jewel; its light fails, exposing the fake; broker waves it away; Harper shrugs and pockets the dark prop; he orders Fast Coat after her; she ducks his reaching hand behind a shade on “fade away”. TA015 completes the escape past Wedge. The painted-underside idea was superseded. Boss has not discovered the key theft.

Previous edit before opening split: **26 cuts across six scenes**, still1956frames/81.5seconds at24fps. Five revised frames: ta010/011/014/014b/014c. Old014 split at accepted word/grid frames1322 and1340; every other existing boundary unchanged. Three short cuts: shrug1303–1322; command1322–1340; dodge1340–1388. TA012/013 theft inserts retained. Stable shot IDs kept; Scene03 shot numbers updated. Shared prompt lock and accepted lyric/tempo sources unchanged.

Open five-frame review: `generated/storyboard/distraction-starters-v004/review/distraction-board.html`; full26-frame board alongside at `starter-board.html`. Prompts, receipts and timing snapshot in `shots/distraction-starters-v004/`. Review `review-notes.txt`: light flicker remains future motion, stills show lit-to-failed contrast; short command/shrug cuts need review at speed. Previous takes preserved.

Current audio animatic: `generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4` (stable player path). Small bottom lyrics, scene/shot numbers and names, master time/frame counter. Annotate at http://127.0.0.1:8767/. Previous complete24-cut animatic preserved as `first-run-complete-before-distraction-v004.mp4`; pilot and earlier references remain history.

Access interaction is now contactless per user clarification; verify consistent device scale, grip and reader acknowledgment before motion. Reader fixed-jamb placement retained. Shot016 fitter is below ledge, so adapt waiting beat or revise. Shot022 electrician trousers drift; shot023 now shows indistinct aerial news footage instead of portraits. Kling pilot is complete and incorporated into the first three shots; later shots still use starter images. Mac original115 media files verified earlier; new assets local-only until requested GitHub/media checkpoint.

Taffy authority is `generated/character-development/taffy-front-back-v006.png`: portly broad soft torso/belly, full cheeks and large rounded projecting ears. User reaffirmed/accepted this direction; do not use skinny ta002v001 as identity. Supporting v004 accepted working silhouettes, not all-angle anatomy locks. A1 grip/B5 ocular caveats remain.

One-second(24frame) source in/out handles are stored per shot; these do not extend musical cuts. Starter default represents source pre-roll beginning; ending-frame exceptions can be chosen later. `shots/scene-index.json` gives stable scene/shot mapping. `shots/video-reference-workflow.txt` explains workflow.

Run annotator: `./.venv/bin/python3 tools/frame_review.py --video projects/together-anyways/generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4 --notes projects/together-anyways/shots/first-run-frame-notes.json --shotlist projects/together-anyways/shots/shotlist.json --master-start 0 --master-frame-base 0 --port 8767`. Notes persist in authored shots folder. Mac original115 media files verified unchanged; all new media local only until requested GitHub checkpoint. EffectCraft0.18.0 CLI GPU rendering works; GUI font appearance differs.

## First time on the Mac

Clone `https://github.com/ArneGleason/music-visualization-toolkit.git` into any
local folder, preferably outside cloud-synced storage. Open that folder as the
Music Visualization Toolkit project in Codex. Start a local chat there with:

> Read AGENTS.md and projects/together-anyways/CONTINUE-HERE.md. Restore the
> Together Anyways media and set up the pinned Mac EffectCraft build. Check
> the current cast board, then continue our character size and clothing design.

The assistant can do the setup. The same steps in Terminal, from the clone:

```sh
git pull --ff-only
bash "Setup Together Anyways Mac.command"
```

Python 3.10+ is needed. The script restores the verified media snapshot, downloads
the official universal Mac EffectCraft **0.18.0 app and CLI**, checks their SHA256
hashes, installs the app into `~/Applications/EffectCraft-0.18.0.app`, creates a
local Python environment, installs toolkit dependencies and validates the timeline.
FFmpeg is installed using Homebrew if it is missing and Homebrew is available;
otherwise the script explains the missing prerequisite. Playwright Chromium is
only needed for browser-based render tools: `.venv/bin/python3 -m playwright install chromium`.

Open the prebuilt cast board in a browser:
`generated/character-development/supporting-refs-v004/review/cast-board.html` (relative
to this project folder). All gallery image links are relative.

From the repository root, launch the native animatic with:

```sh
python3 tools/effectcraft.py gui
```

The launcher sets the bundled Barlow font directory and computes all paths from
this checkout. Normal macOS first-launch approval may be needed. The setup does
not bypass Gatekeeper. Mac app launch/GPU rendering must be tested on the Mac;
Windows verification cannot certify those. No Blender installation is required
for the current EffectCraft animatic. A separate Windows checkout keeps its own
Python environment and EffectCraft binaries.

## What Git and the media release contain

Git tracks authored prompts, reference catalogs, creative notes, plans, timing
register, tools and this handoff. `media-manifest.json` identifies an immutable
GitHub Release ZIP with SHA256 hashes for every file. Large media stay outside
Git history, following the repository's AGENTS.md.

The ZIP contains both projects' complete generated reference/history folders,
all review boards, the supplied cover and original Harper input (when available),
the current DAWproject export with embedded source audio, the master WAV, exact
tempo grid, compiled timeline, accepted v04 native EffectCraft project, rendered
lyric animatic, timing data, font and its license. Earlier audio-cleanup experiments,
model weights, virtual environments and Windows executables are outside the
music-video handoff; they are not dependencies of this project.

The portable native file is
`generated/animatic/Together-Anyways-lyric-animatic-v04.ecproj`. Only its two media
paths were changed to relative `assets/...` paths. The original Windows save is
retained beside it as `*-windows-original.ecproj` for provenance. The old
`Open in EffectCraft.cmd` inside that historical folder retains the old PC path;
use the repository launcher instead. Old generation receipts and gallery-builder
scripts may mention PC/plugin paths as provenance; use the saved images and
prebuilt galleries, and adapt a builder if needed. Do not recreate designs from
scratch because an old receipt path is unavailable.

## Switching back and forth

Before switching machines, ask the assistant to **checkpoint Together Anyways
to GitHub**, including new ignored media. A code-only commit does not transfer
new PNG/WAV/MP4/ecproj files. Work on one computer at a time.

For a media change, the assistant should:

1. Inspect Git status; stage only this project's work and intended shared tools.
2. Keep new assets under one of the roots in `media-manifest.json` (or explicitly
   add a new root). Remove machine-specific dependencies from active project paths.
3. Run `python tools/project_media.py pack projects/together-anyways/media-manifest.json --tag together-anyways-YYYYMMDD-vNNN`
   with a **new tag**. Never replace a published snapshot.
4. Commit the new manifest together with authored changes, push, then create a
   GitHub Release at that commit and upload `out/transfer/<tag>.zip` using `gh`.
   Verify release availability and restore checksums before declaring it backed up.

On the receiving machine:

```sh
git pull --ff-only
python3 tools/project_media.py restore projects/together-anyways/media-manifest.json
python3 tools/project_media.py verify projects/together-anyways/media-manifest.json
```

Restore refuses to overwrite differing local files. If it reports conflicts,
checkpoint the local edits or move the listed files into a dated backup before
restoring; do not delete them blindly. `project.local.json` is intentionally
ignored: use it only for that computer's optional source overrides. The tracked
`project.json` already has portable defaults, so Mac needs no override file.

Git transfers files, not a chat's execution location or full chat history. A new
local chat inside the Mac clone is the simplest continuation. An existing chat
can also be handed off through Codex remote connections when both hosts and
matching repository projects are configured; opening the same chat alone does
not switch its tools to the Mac. Official reference:
https://learn.chatgpt.com/docs/remote-connections

## Accepted timing: preserve it

- 48 kHz stereo master, 216.239020833 seconds; preview **5190 frames at 24 fps**.
- Exact DAWproject curve: **932 tempo points**, linear in beat; master zero at
  **project beat 7.5**. Do not substitute a fixed tempo or stepped MIDI map.
- 57 lyric lines, 220 words; `timeline.json` is the portable musical register.
- User approved the repeated refrain correction: second **with 84.660–87.040**,
  **me 87.040–88.360** seconds. Do not rerun alignment or move that boundary.
- Approved text: “Where all attention must go” and “find a fine like you”.
- Section tags in supplied lyrics are not displayed lyrics. Echoes are baked
  into the vocal; repeats should not be invented from echo transcription.
- Existing accepted native preview is **1280×720**. Future picture work is
  planned at **1920×1080**; migration does not upscale or alter that preview.
- `timing-import.json` records checks; the importer fix retains the partial
  opening bar at beat 7.5. Run `tools/timeline.py validate .../project.json` after
  setup. `sync` regenerates grid/compiled data; it is unnecessary for viewing.

## Characters and creative direction

Read `development-brief.txt`, `character-development/biology-direction.txt`,
the supporting cast pool and each batch's catalog/review notes before changes.

Harper is 14: copper curls, freckles, rust vest, pale scarf, olive trousers;
confident street trickster. Her partner's working name is Taffy, about 12:
Black, short curls, larger rounded ears, slightly overweight, less conventionally
cute and watchful. He recently escaped bad circumstances with Harper's help.
His own culture remains visible: mulberry/plum patterned wrap top, mismatched
rope/braid belt, charcoal trousers, runnable open-toe sandals and a patched sack
rigged with shoulder cords. Exactly three curved healed scar lines on each cheek,
symmetrically arranged. v006 corrected the turned head toward the frontal identity;
all-angle identity is not yet fully locked. Retain rejected iterations as history.

The racketeer and his one shoulder lookout remain core cast. The current board
has 13 supporting candidates: A1, A3, A6, B1, B4, B5, B6, C1, C4, C6, D2, D3, D6.
Arne particularly liked subtle, job-related biological adaptations that belong
in the world and only become obvious on closer inspection.

Accepted reference directions: A3 precision eye/tactile pads; A6 four arms;
C4 vibration-sensitive ear membrane/contact pads; D6 digitigrade runner legs;
B1 Doorpost retained. v003 adds A1/B4/B6/C1/C6/D2/D3 and B5 Stillwater.
Those latest studies are not final character locks. A1's twin-thumb-tip anatomy
is **unresolved** despite two attempts; B5's lateral eyes are weaker than intended.
Do not assert those traits are fully established. The v004 size and attire direction is now accepted for working use; retain these biology caveats.

## Story and environments

Desert scavenger world: worn sandstone, patched shades, chipped teal/blue pipes
and tanks; old mechanics with selective advanced technology. Influences come
from multiple cultures/planets. Painted graphic-novel rendering, controlled
ink contours, tactile materials. No generic pointed-ear/wrinkled-forehead shortcut.

Harper distracts the criminal with a blue jewel she can conceal/reveal while
Taffy steals an asymmetric horseshoe access key. Route: market approach → broker's
house-front water depot → separate decoy/covert escapes → blue-pipe reunion court
→ controlled relay entrance → interior wanted broadcast. They use the stolen
device to open an intermediate door, not the ship itself. Four environment
directions and the first-run plan were accepted; see
`environment-development/first-run-v001/plan.json` and its route map, with review
under `generated/environment-development/first-run-v001/index.html`.

Detailed environment planning ends at “I never watch the news”, 81.48 seconds.
A 24-shot timed blocking proposal and location-card animatic now cover this section; all24 staged starter images are now available for full first-run review. Later they hijack
a ship and launch at the final “Hang on for your life”; something brings them
down during the instrumental outro. They gain ground but remain stranded on the
planet. The cause of the forced landing and later locations are still open.
Only the first three-shot Kling pilot was approved and generated; no further spend is authorized. Once shots are authored,
`shots/shotlist.json` becomes the edit authority; preserve authored work with
`shotplan --merge` and derive frame boundaries from the timing register.

Official pinned app release:
https://github.com/storytold/effectcraft/releases/tag/v0.18.0

Taffy correction: user reaffirmed the portly, big-eared v006 direction. v006 is present locally. Shot ta-002 v002 restores fuller build and large visible ear; original v001 retained as history. Prompt/review in shots/first-run-starters-v002. Key ownership still needs correction before motion.

Current animatic layout: explicit SCENE number/name and SHOT number/name in the narrow footer; lyrics smaller (20px at1080p), bottom center; master time/frame bottom right. User accepted corrected Taffy direction. Annotator remains on port8767.


## Scene 1 Kling continuation — 2026-10-31
Kling4.0 1080p batch `shots/kling-scene01-v002/batch.json`: five shots S01SH04–08 generated and downloaded, 480 credits total. Sources in `generated/kling-scene01-v002/`. S01SH04–07 selected in shotlist with sourceInFrame24 and original musical timing. S01SH08/ta-006 generation invents a man handing Taffy a credential from ~4s, contradicting the theft: rejected for edit, approved starter retained. Needs focused redo; no extra credits spent. Sampled source frame review only, user motion review still required. Prior animatic preserved as `generated/kling-scene01-v002/animatic-before-scene01.mp4`.


## Active action revision — Kling action v003
User rejected Scene1 ambient motion and requested all except opening aerial redone. Seven Keyframes takes S01SH02–08 submitted at1080p to Kling4.0;750credits, durations7/11/7/4/6/8/7seconds, approved starters. `shots/kling-action-v003/batch.json` tracks status. New common MOTION CONTINUITY LOCK v003 is confined to animation/style/anatomy; authoritative original story promptLock stays unchanged. Prior render preserved `generated/kling-action-v003/animatic-before-action.mp4`. Actions: supply interruption, avoid guard detection, physically demonstrate routes, celebrity reaction, tug and departure, guards block lane, jewel pocket/rise/split. Awaiting motion review before selection.

Action v003 status: six replacement clips (ta001/002/004/004b/005/006) downloaded, inspected in sampled action sequences and selected into current animatic. Original aerial ta000 retained. ta003 first attempt was submitted before starter upload completed (assistant error), produced entirely wrong cast, saved as ta-003-rejected-no-starter.mp4. Corrected ta003 submitted after visually confirming thumbnail upload complete, +105 credits; total this pass855. Corrected take remains Creating with stalled30s estimate as of handoff; do not submit a duplicate. Find latest card with "Harper actively lays out their two-route plan" in Kling grid; older card with identical prompt is rejected two-men output. Prior ta003 motion remains in animatic until corrected result reviewed. Six new sources have 24frame in/out handles; master1956frames/81.5s unchanged. Review board http://127.0.0.1:8766/kling-action-v003/review/index.html includes old/new players. Some face simplification; ta004b wider shot invents boots for Taffy instead of sandals, four-arm market anatomy needs closer review. These are action review candidates, not final polished clips. Batch receipts in shots/kling-action-v003/batch.json. Finish corrected ta003 download/QA, select its videoSource and rerender animatic. No other paid retries needed without review.


## Boss whisper revision — v004
User accepted improved acting, replacing S01SH04/ta003 partners planning with companion whisper → broker harsh order → E1 minion reaction. Companion is brains, broker muscle/charisma. New built-in ImageGen starter `generated/storyboard/boss-whisper-v004/ta-003.png`, new title The voice behind the boss. Kling4 Keyframes7s1080p submitted105credits after visually confirming uploaded frame. Receipt/prompt in `shots/boss-whisper-v004`; prior shotlist/render preserved. Previous corrected planning generation is superseded by this new creative direction; do not insert it. Current animatic provisionally uses boss starter while motion renders.
S01SH06/ta004b slipped one second EARLIER: sourceInFrame0 instead24, same78-frame cut559–637. Later slip would include more late wide-view hair drift. Earlier reduces exposure but is not complete repair. Opening handle fully consumed; availableInFrames0/out67; record exception, do not claim one-second head handle still available. Comparison at generated/storyboard/boss-whisper-v004/review.html. All29cut boundaries/sharedstorylocks preserved.

Boss whisper v004 complete: new 169-frame/24fps Kling source downloaded, sampled and selected for S01SH04 at sourceIn24 (101-frame edit), with 24-frame head and44-frame tail available. Companion at ear → boss leans forward and points threateningly → minion wide-eyed response. 105credits this revision. Previous corrected partners-planning take is superseded. Stable animatic rebuilt with this motion and S01SH06 earlier source0 slip; user review pending.

## Shot6 pacing trial v005
User found source0 cut repeats the preceding beat. S01SH06 now uses sourceIn36 (1.5s), sourceOutExclusive114, unchanged78-frame musical cut559–637. Starts with pull underway and carries toward departure. Available head36/tail31frames, both exceed24. Hair drift still present; pacing now takes priority. No new Kling generation or credit spend. Previous shot metadata in shots/shot6-pacing-v005/shot-before.json. Supersedes earlier source0 hair-mitigation selection.

## Shot6 unchanged reroll v006
User approved sourceIn36 timing and requested one unchanged-prompt reroll to try for more stable Harper hair. Submitted Kling4.0 Keyframes1080p6s,90credits; exact v003 prompt and same style-news-v010/ta-004b.png starter (upload visibly complete). Prompt and receipt in shots/shot6-reroll-v006. Current accepted v005 cut stays selected until new output review. No hair-specific correction added.

Shot6 v006 reroll finished/downloaded,145frames24fps. Selected as review candidate with unchanged sourceIn36,78-frame music cut. Sampled hair silhouette more compact; action timing differs slightly, user review pending. Previous v003 take preserved. Exactly90credits; no prompt changes. New clip generated/storyboard/shot6-reroll-v006/ta-004b.mp4.

## Harper likeness starter v007
User identified S01SH03/ta002 as preferred Harper likeness. Two built-in ImageGen edits of S01SH06 starter; take02 at generated/storyboard/harper-likeness-v007/ta-004b.png is candidate for user review, tracked under starterCandidate. Leaner cheek/jaw profile and revised curls, same sleeve-pull staging. Reference first-run-starters-v003/ta-002.png. No new video generation; v006 motion/sourceIn36 unchanged. Prompts in shots/harper-likeness-v007. Review board generated/storyboard/harper-likeness-v007/review.html.

## Shot6 revised-starter motion v008
User approved v007 starter and requested new Kling motion. Submitted one Kling4 Keyframes1080p6s take90credits using harper-likeness-v007/ta-004b.png; exact unchanged v003/v006 motion prompt. Upload thumbnail confirmed complete. Receipt and prompt in shots/shot6-new-starter-v008. Prior v006 motion remains until output review; preserve accepted sourceIn36/music559–637.

Shot6 v008 complete:145frames24fps, selected sourceIn36 for78frames. Approved v007 starter promoted to starterImage; old candidate marked approved. Shorter hair silhouette persists through sampled turn; facial simplification still visible, user motion review pending. Prior v006 preserved. Animatic rebuilt with unchanged master1956frames/81.5s.90credits this pass.

## Shot6 timing v009
User accepted v008 take, requested start one second earlier within source. Selected sourceIn12 (0.5s) instead36 (1.5s), same78-frame edit/master559–637. Source out90 exclusive; available head12/tail55frames. Full1s head handle unavailable. Prior metadata saved shots/shot6-timing-v009/shot-before.json. No new generation.

## Taffy approach v010 and timing UI
User accepted S01SH06 earlier start/source12. S02SH03 Direct threat split at frame1040: original988–1040 (52frames/2.167s), new ta009b/Shot3B Under the armrest1040–1093 (53frames/2.208s). Later shot numbers4–7 and all later boundaries retained. New ImageGen starter uses original diversion-theft-v005 blocking and v006 Taffy identity; credential remains holstered.30cuts,1956frames unchanged. UI now shows Play length and Clip start; stills explicitly have no clip start. No Kling generation.

Taffy approach take02 selected after user flagged right elbow/wrist and exposed head: deep squat, right forearm resting on knee, face tucked below armrest. Image ta-009b-take02.png; first take preserved.

## Chair/crate continuity v011
User identified missing boxes in ta009b/ta012. Revised both with S02SH02/ta008 as exact layout authority (S01SH07 secondary): low cloth-draped crate front-right of chair, cup on left top, tall crate behind, blue column farther right, bucket foreground. ta009b now Beside the cover crate, Taffy crouching at its right edge. ta012 reaches up by feel from behind same low box, face concealed, device still in holster at starter. Generated/storyboard/box-continuity-v011, prompts/review in shots/box-continuity-v011. Timings unchanged; no Kling generation.


## Harper solo entrance v012
User flagged S02SH01 repeating the pair after S01SH08 separate departures. ta007 now frontal confident Harper approach alone, shade stitcher left and scrap appraiser right noticing her. No Taffy/broker; Taffy reappears S02SH02. Starter generated/storyboard/harper-approach-v012/ta-007.png; prompt/previous metadata/review in shots/harper-approach-v012. Existing 50-frame cut883–933 retained, shared promptLock unchanged. No Kling generation.


## Scene 2 Kling acting v013
User approved all Scene2 starters and authorized generation. Eight Kling4 Keyframes1080p takes submitted,570credits total,5/5/5/5/4/5/5/4seconds for ta007/008/009/009b/010/011/012/013. Exact prompts/receipts in shots/kling-scene02-v013/batch.json. All eight completed in Kling; downloads and QA underway. Primary action timed inside source1s onward; shared motionlockv003 preserved. ta009b briefly raises head above crate during approach: flag for user motion review. No retries submitted.

Scene2 v013 complete: all eight downloaded, sampled, selected as motion-review candidates and animatic rebuilt. SourceIn24 on all, original50/55/52/53/46/68/67/29 frame cuts retained. Full head/tail24frame handles available. Review caveats: ta009b head briefly rises above crate; ta011 rejection wave lands near end of cut. All sources in generated/kling-scene02-v013; prior animatic preserved there. User playback review pending; no paid retries.


## Scene2 Shot3B timing v014
User requests starting ta009b one second earlier to avoid head touching broker arm during sidle. SourceIn0 instead24; same53frame cut1040–1093. Entire head handle consumed; tail68frames remains. No regeneration. Prior metadata in shots/scene02-3b-timing-v014.


## Scene3 eyeline starters v015
User requested S03SH01/ta014 and S03SH02/ta014b starters revised: Harper leaves casually while broker and both henchmen watch her; next cut boss commands pursuit, guards still looking toward public-left exit. Built-in ImageGen replacements selected in shotlist, original artwork/metadata retained. Single companion restored in shot1 second pass. Sources generated/storyboard/scene03-eyelines-v015, prompts/reviews shots/scene03-eyelines-v015. Original19/18-frame slots and shared promptLock unchanged. No Kling generation.


## Scene3 motion direction v016
User approved Scene3 starters and supplied motion direction. Authored five Kling-ready prompts in shots/scene03-motion-direction-v016 and linked each under shotlist.motionDirection; no generations submitted. Shot1 casual shrug/departure under suspicion. Shot2 single shoulder companion whispers as angry boss orders BOTH guards into pursuit (supersedes Doorpost staying). Shot3 Fast Coat misses deke, skids and falls on side. Shot4 existing Wedge misses side-route interception, Harper accelerates clear. Shot5 renamed Waiting above the water: Taffy watches from cover, irritated fitter repairs spurting joint. Existing frames/timings/locks preserved; shots1/2 are19/18frames so actions overlap, no sequential pauses. Planned sources4/4/4/4/5sec, sourceIn24 and one-second handles. No footage or animatic rebuild required for authored motion direction; live UI reads title change.

Scene3 v016 generation: user authorized clean clips. Five Kling4 Keyframes1080p takes submitted using approved starters and exact v016 prompts;4/4/4/4/5sec,315credits. All upload thumbnails confirmed ready before Generate. Await completion/download/QA; do not duplicate submissions. Receipt shots/scene03-motion-direction-v016/batch.json. Prior animatic saved generated/kling-scene03-v016/animatic-before-scene03.mp4.

Scene3 v016 complete: five clips downloaded, sampled and selected as motion-review candidates;315credits, no rerolls. Sources generated/kling-scene03-v016, review.html. sourceIn24/54/0/24/24 respectively. SH02 slipped later to catch command/launch; both guards fully depart only later in full source. SH03 consumes entire head handle to retain early deke and fall (0–48); near reach may read as scarf brush. SH04 has pronounced low stumble/recovery. SH05 Taffy ducks to cover while fitter reacts to spurt and adjusts fitting.30cuts/1956frames/master81.5sec unchanged. User playback review required.


## Scene3 timing trial v017
User requests SH01 later at2.5s/source60, SH04 at beginning/source0, SH05 earlier interpreted as source0. SH02 source54 and SH03 source0 unchanged. All musical slots preserved. SH01 now only18frames tail; SH04/05 headhandle consumed. Original shot metadata in shots/scene03-timing-v017. No new generation.
