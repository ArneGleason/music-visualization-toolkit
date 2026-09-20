# Monsters Loose — production recovery

Current edit: **v45**, through master frame2461 at24fps (102.54seconds). New simple rope demonstration at1708..1767 for review replaces rejected Blender toss. Bundled coil and connected strand; no rope overlay. Cage5 remains intact. Net interception and later habitat shots remain placeholders.

## Resume

Use the existing frame review at http://127.0.0.1:8767/ (same app and port). The swamp bridge occupies master frames **1305–1506**. `recovery/shots/shotlist.json` is the edit source of truth. Master frames are one-based; source offsets are zero-based; end frames are exclusive. Default assumed pre-roll is 12 frames (half a second), recorded per shot; consult actual source trims before changing cuts or lip-sync.

The current Blender timeline is `recovery/animatic/MonstersLoose-v45-through-habitats.blend`. The current render pointer is `recovery/animatic/frame-review-current.json`. Latest swamp effect lives in `recovery/motion-graphics/SWAMP-LIGHTS-001/`. The underlying approved movie is `video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4`.

## What is backed up

Scripts, shotlists, timing grids, lyrics, generation prompts/settings, creative notes, tracking coordinates, font files/licenses, and small editable Blender projects are copied into `recovery/` with their job-relative directory structure. The frame review application is tracked in the toolkit's `review/`, `tools/frame_review.py`, and `docs/FRAME_REVIEW.md`. `inventory.json` identifies included files and omitted media; included snapshot bytes have SHA-256 hashes. URL query strings and named authentication fields are removed from text snapshots.

Large generated images, video, audio, PNG render sequences, caches, logs, and Blender backup copies are intentionally excluded. **This is not an exact media backup.** Prompts cannot regenerate identical AI footage. Preserve the external job folder separately to recover the approved pictures and takes exactly:

`C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913`

Also preserve the original DAW project and its referenced recordings:

`C:/Users/arneg/OneDrive/Documents/Bitwig Studio/Projects/MonstersUndone.cleaned-groove/MonstersLoose.dawproject`

## Restore and rebuild

1. Copy `recovery/` to the original job directory, then restore omitted source media there using `inventory.json`. Never run production builds directly inside this Git snapshot: generated content belongs outside Git.
2. Install Blender 5.2, FFmpeg/ffprobe, and Python with NumPy/Pillow. Some generation scripts additionally require the Kling CLI and a separately authenticated account. Credentials are not backed up here.
3. The Blender timelines use relative media paths where saved; older scripts and review state also contain absolute Windows paths. Restoring to the original job path is simplest. For another location, update these paths and use Blender's missing-file relinking before rendering. Font paths may also need relinking.
4. Open the current v39 Blender file to inspect/render the edit. Effects can be rebuilt from their adjacent build scripts and README files. Historical animatic build scripts load predecessor `.blend` files; those small snapshots are retained. Restore source inputs before running them.
5. Launch `tools/frame_review.py` with `--video <current-render> --notes <job>/shots/frame-review-notes.json --state <job>/animatic/frame-review-current.json --port 8767`. See `docs/FRAME_REVIEW.md`.

To refresh this recovery snapshot after later work, run `python projects/monsters-loose/snapshot.py --source <job-directory>`, inspect the diff, then commit. The exporter copies files; it does not delete stale historical snapshots.

## Accepted editorial details

- Helicopter lights v002; creature POV motion/lens v002 (parallax version rejected).
- Gate cut at master 1012; hard rattling stops by 1034, followed by dust/settling. Dust v004 approved.
- Lab pitch, town fire, mean scientist take002, upward tall-gate reveal, and swamp snatch take002 approved.
- Three scientists retain their character references; mad scientist has one brass hand.
- No new generation credits spent on v30 lighting/reflections.
- Frame review playback/rewind fix passed real Chrome checks; zero input clamps to frame one and play at the end restarts.

Latest tour: master1507..1625 exclusive, KLING-TOUR-001, 6seconds/48credits, source12..130, wider generated start and original ANCH-006-A tail. Aquarium still SCN-006-aquarium-v001 starts1625 on Watch them try to eat the keeper whole. Both new still prompts are in recovery/assets; shot direction and timing are in recovery/shots/SCN-006-tour-aquarium.md. Aquarium video has not been generated.

Latest revision v32 replaces the tour with KLING-TOUR-002: fixed camera, start image only, no tail frame. Same 6seconds/48credits and trims. Take001 rejected for background sliding. Take002 background is steadier in samples but Harper hair becomes a ponytail; flagged for user review, not approved. Aquarium still/cut unchanged.

Latest v33 uses tour003, close ANCH-006-A start plus approved Harper Element321495363652188, no tail frame, 6s/48credits. Harper likeness improved in sampled frames, but Kling ignored locked-camera direction: near cage pillars shift relative to far tower. Background criterion NOT met. This is a flagged review test, not approved footage. Takes001 and002 rejected. No further paid attempt submitted.

Current decision: user explicitly APPROVED tour003 as perfect, superseding earlier assistant background concerns. v34 adds five tracked rooftop red-beacon pulses using the swamp29-frame cadence and soft bloom. No regeneration. Lighting polish awaits review; earlier-shot lighting consistency noted as future work.

Latest v35 animates aquarium1625..1708 with KLING-AQUARIUM-001,5seconds40credits, Harper Element, source12..95. Starting mouth open, then closes early and snout presses toward glass; this deviates from sustained open-mouth prompt and was disclosed for user review. Keeper likeness and intact separation appear coherent in sampled frames. No automatic retry. Tour lights v34 retained.

Latest v36 adds aquarium expanding speech balloon: SORRY. then I'M NOT ON / THE MENU. One continuous ivory shape with integrated curved tail, ink pressure outline, Bangers lettering, word reveal, restrained settle. No new credits. Editable effect in AQUARIUM-SPEECH-001. Source trims and cuts unchanged; polish awaits review.

Latest v37 adds tracked red structure beacon pulses to edit shots2-5 (landing, Harper intro, bolt inspection, creature POV), matching swamp/tour29frame cadence. Existing aircraft lights, bubbles, POV effects and trims preserved. EARLY-BEACONS-001 stores scripts/tracks/timing and original input paths. No credits.

Latest v38 selects retained illustrated lasso KLING-TEST-004-clean source60..131 for master1708..1779 (2.96seconds). User requested best earlier corrected-rope take in context; no regeneration. Net interception concept begins1779 on One; existing still is explicitly marked placeholder, no incident asset created yet. Timing and next-shot concept: shots/SCN-006-lasso-net.md.

Latest v39 uses lasso take004 source0..60: opening2.5seconds only, before lowering/coiling deterioration. Master1708..1768; next planned incident begins11frames before One cue1779. Normal speed, no loop/freeze, no leading handle for this historical take. Supersedes v38 lasso source60..131. No credits.


Rigid-prop experiment KLING-LASSO-PROP-001:4seconds32credits, cleaned start only plus Harper Element. Failed loop shape/head-clearance criterion; raw output retained outside Git, prompt/settings/review backed up. No v40 edit, no overlay applied, no further paid retry. LASSO-PROP-001/build.py is only an unrendered accent prototype.


v40: KLING-LASSO-TOSS-001 empty-hand gesture,4s32credits, start-only corrected-pose plate plus Harper Element. Blender loop/lead replaces unpredictable generated rope physics. Use source24..84 for master1708..1768; assumed pre-roll12, extra editorial trim12. Imagegen cage5 correction applied as localized video patch without regeneration. Performance is broader than requested; awaiting review. Old take004 and failed prop001 retained. All creatures stay behind barriers until deliberate breakout shots.


v41: user retired toss/twirl experiments. KLING-ROPE-DEMO-001,4s32credits, new two-hand reference, Harper Element, start-only. Hands separate to show connected rope; main coil bundled. Source12..72 atmaster1708..1768, assumed/actual lead-in12frames. Wider arm spread and less slack than requested; awaiting review. No Blender rope overlay. Prompt, timing and sampled review recorded.


v42: rope-demo001 user accepted as candidate keeper; head/body acting could improve but rope works. Added five facility red beacons with matching29frame staggered sequence, source/master phase1696, same source12..72 trim. ROPE-DEMO-LIGHTS-001 includes tracking, Blender scene and composite recipe. No new generation credits. Lighting awaits review.


v43: new net-interception starting-frame storyboard at1768..1893, enclosure5 service hatch, Harper release lever, contained horned boar-like monster, overhead rolled rope net. Next eye-roll reference placeholder starts1893; existing later cuts preserved. Net video not generated. Future7second clip allows125frame edit plus12frame handles. See SCN-006-net-interception.md.


v44: supersedes lever/roller net storyboard with SCN-006-net-feeding-v003: creature fully inside eating, Harper withdrawing from bowl, discreet floor stomp pedal, soft net gathered under exterior canopy. Future dash surprises Harper; she stomps and net drops onto creature. No escape in starting frame, no hand switch. Same1768..1893 placement. Net animation not submitted.


v45: SCN-006-net-vestibule-v004 replaces net-feeding-v003. Larger natural habitat, deep recessed containment vestibule, discreet folded net in ceiling recess above central catching floor. Creature still eating fully inside rear threshold; Harper at left. Foot-trigger action remains planned. Still only, no net video credits. Same1768..1893 timing.


KLING-NET-001:7s56credits, Harper full-body/face Element bound. Test failed event choreography: monster retreats into habitat, net lowers afterward as curtain/sack, no capture. Raw video external; prompt/settings/review in recovery. Not integrated, current edit staysv45. No further paid retry.
