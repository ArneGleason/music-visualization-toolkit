## Accepted V65 save point — October 12, 2026

User accepted V65 and requested a complete commit/push before ending the session.
This is the baseline for the next review. Planned next-session work: improve
beginning shots to match the accepted sphere ship design, then selectively retry
other shots. No new generations or spending are requested during the break.

Canonical decisions and frame timings remain in `shots/shotlist.json`. Curated
first-contact, community, cosmic destination and independent composite reference
images are now included in `reference-images/manifest.json`. Small metadata,
prompts, generation receipts and reproducible Blender/assembly scripts are saved
in `checkpoint/`. Audio, videos, renders, Blender scenes and frame caches remain
local under ignored `generated/`; GitHub is not a full media backup.

Resume with the repository Python environment:
`tools/listening_review.py projects/a-right-little-something/project.json --port 8768`
and open `http://127.0.0.1:8768/?v=v65`.

## V65 — separated sphere optics and ending refinements, 2026-10-11

Current review: `http://127.0.0.1:8768/?v=v65`. V64 preserved. No new generation credits.
Full movie remains 5265 frames at 24 fps / 1920x1080; original V64 AAC packets verified identical. All canonical shot boundaries are unchanged.

- Both early rear warp (frames3144–3204 exclusive) and Travel27 (4649–4683) now use a stronger dark cyan optical middle layer. Stack: warp background, sphere-masked refraction/transmission, original keyed ship-and-Harper foreground. Only the underplate is refracted and attenuated; the foreground source and its compositor path remain untouched. Native keyed alpha retains normal slight background contribution around partially transparent pixels.
- Sphere transmission uses linear RGB absorption .90/.77/.60, with mild local radial refraction (roughly4px maximum). The mask tracks the sphere in each shot. Separate editable maps and Blender nodes are retained.
- Central-world departure light swells from4550, peaks4567 (3:10.25), then accelerates along a curved escape path from4583 through4648. The base system camera move remains intact.
- Harper's rear/profile planet shot (4446–4484) now pushes and pans toward the planet side. Reversed Travel28 at3:18 is unchanged.
- Final Harper video is slipped48 source frames forward: native frame73 instead of25. The final composite still enters at5031; fade starts5137 (3:34), reaches zero5185 (3:36). Padded portrait tail occurs only after she is already invisible.
- Ending type uses clean sans serif Bahnschrift: uppercase title68px with3px tracking, copyright30px. Enters5185 and reaches full opacity5197.

Reproduction: `generated/storyboard/outro-polish-v02/prepare.py`, Blender5.2 `effects.py -- --shot <opening|travel|system-departure|planet-push|finale>`, then `build.py`. `qa.py` compares timings and samples the assembled edit. No re-plan required. Review notes: `outro-v64-review.json`; exact plans, source offsets and QA live in that storyboard directory. Large media remains outside Git.

## V64 — outro editorial polish, 2026-10-11

Current review: `http://127.0.0.1:8768/?v=v64`. V63 preserved. No new generation credits.
Full movie remains 5265 frames at 24 fps / 1920x1080; original V63 AAC packets verified identical.

- Harper World shortened to frames4446–4484. System View now begins on DAW bar71 beat2, frame4484 (3:06.792), fully visible by3:06.958. Next travel cue stays4649. Existing system footage smoothly retimed and given a Blender camera move.
- Travel28 at3:17.833 reversed using exactly original selected frames57 through25; reverse handles follow from24 through17.
- Stronger Blender movement on Stellar Nursery, Red Star System moon, and Galactic Possibilities.
- Travel27 plated sphere: mild radial refraction (approximately4px maximum) and subtle dark cyan transmission, applied only to background under the transparent dome. Harper and hull remain independent. No reflected-streak generation.
- Finale retains its accepted entry at5031. Harper fade begins5137 (3:34), reaches zero5185 (3:36). Cosmic source continues. Title A Right Little Something and smaller © 2026 Arne Gleason enter at5185 and are fully visible by5197 (3:36.5).

Reproduction: `generated/storyboard/outro-polish-v01/prepare.py`, `effects.py -- --shot <contact-027|contact-029|contact-030|contact-031|travel|finale>`, then `build.py`. Run effects through installed Blender5.2. The prepare script preserves the original V63 shotlist snapshot; do not re-plan existing creative work.
Review notes: `outro-v63-review.json`. Exact media choices and time map: `assembly-plan.json`; visual/timing QA: `verification.json` and `qa-observations.json`. Title overlay source `title.ass` is included in metadata checkpoints. Large media and renders remain outside Git.

# A Right Little Something — production checkpoint

## October 11 — V63 targeted motion revisions and simple warp composites

V62 review is recorded in `first-contact-v62-review.json`. The side-on warp
start was rejected; the rear warp take lost Harper. V63 replaces both with
one continuous 60-frame rear-oblique departure, retaining their existing
18/42-frame metadata split. Independent native ship/Harper video is keyed over
a separately animated illustrated warp background in Blender. The first outro
travel insert uses the same two-layer approach with its own side-oblique plate.
Harper has visible weightless motion. The user explicitly wants the simple
composite tested first; synthesized reflections from warp streaks are deferred.
The previous single-generation travel is preserved in V62 for comparison.

Other replacements: creatures walk into a canopy clearing instead of the
unexplained cyan wisp; a creature lowers its home awning instead of merely
picking up a gardening tool; both gliders travel across the valley; Harper
watches the planet in profile/turned away without turning toward the viewer.
Existing tidal and grounded-foot shots gain gentle Blender moves. Six existing
stars receive tracked, independent twinkles. Ecology transitions use four-frame
dissolves; outro transitions use six, with four into the finale. These use
outgoing source handles and do not shorten the song or move the final cue.

Down-here now ends at DAW bar 69 beat 1, frame 4334. Harper's projection retains
37 frames, followed by a 45-frame eye glint (previously 27). Night orbit remains
at frame 4416. The Harper finale still starts at 5031 (3:29.583), becoming fully
visible before 3:30. Full edit: 5265 frames, 1920x1080 at 24 fps; original V62
AAC packets verified identical. V62 remains intact.

Review: http://127.0.0.1:8768/?v=v63
Composite comparison: http://127.0.0.1:8768/storyboard/first-contact-motion-v02/
Six new Kling takes cost 248 credits. First-contact total is 1880, project
cumulative 5264, and the verified remaining balance is 17001. All jobs are
collected. Both isolated plates use source frame 1; the side plate's later
unwanted scenery is excluded. Magenta padding and a custom Blender key remove
background and edge contamination while retaining the cyan engine and dome.
Source stills were made with built-in ImageGen; exact prompts, plans, frame
sources, QA and editable Blender scenes are in
`generated/storyboard/first-contact-motion-v02/`. V63 is pending user review.

## October 11 — V62 clean first-contact motion ready for review

User approved the V61 timing and authorized Kling generation after the credit
estimate. V62 replaces the first-contact still section from frame 3144 through
5266 exclusive with 36 timed shots using 37 selected silent 1080p Kling sources.
All V61 shot boundaries are retained. The full edit is 5265 frames at 24 fps,
1920x1080, with original V61 AAC packets verified identical. V61 remains intact.

Review: http://127.0.0.1:8768/?v=v62
Clean takes: http://127.0.0.1:8768/storyboard/first-contact-motion-v01/
The direct galaxy-to-Harper cut remains at frame 5031 (3:29.583). Independent
cosmic and portrait video plates are trimmed to 235 frames and superimposed
in Blender; the overlay was not generated by Kling. Editable compositor:
`generated/storyboard/first-contact-motion-v01/finale-two-videos.blend`.

Actual spend: 1528 credits for the first 37 generations, plus 104 for three
targeted corrections (creature profile 011, tidal life 017, binary suns 028).
Total for this pass: 1632 credits; project cumulative spend: 5016. Live balance
after completion: 17249 credits. All 40 paid jobs are collected; none pending.
Shot 005 uses clean source frames 1–25 to avoid an unwanted later hologram,
without another generation. Original and corrected sources remain available.

Every selected source was checked at its edit in/middle/out, with native frame
counts and format validated. Motion remains pending the user's review. Assembly
scripts, selected-take overrides, QA notes and verification are in
`generated/storyboard/first-contact-motion-v01/`. Caption export disables filter
reinitialization so the finale boundary does not drop one frame. Small metadata,
prompts and receipts are checkpointed; large media and Blender sequences stay
local and excluded from Git. Intro ship matching remains future work.

## October 11 — V61 earlier Harper finale

User requested the final Harper superimposition by 3:30 and removal of the
last ship insert. The galaxy now cuts directly to the two-plate Blender
composite at frame5031, DAW beat79.3 (3:29.583). Harper is visible immediately;
the finale continues for235frames to the unchanged song end. Earlier destination
holds are tightened on the DAW beat grid to make room. Four travel inserts
remain; `contact-031-travel` is archived in superseded storyboard proposals.
The sequence now contains36shots. V60 remains available as a fallback.

Active review: http://127.0.0.1:8768/?v=v61
Full5265frames, 1080p24; original V60 AAC packets verified identical. No new
paid generation. Scripts, timing plan, verification and editable Blender file:
`generated/storyboard/first-contact-animatic-v02/`. Next: review the earlier
galaxy-to-Harper cut before preparing clean footage; keep the two finale
video sources separate and composite them in Blender.

## October 11 — V60 first-contact still animatic ready for timing review

The approved first-contact V03 board is assembled from frame3144 (2:10.958)
through the end, frame5266 exclusive. All 37 shots follow the canonical timing
grid, including five travel inserts alternating with the ending destinations.
The finale previews the separate cosmic and Harper portrait plates composited
in Blender. Keep those sources separate for two future clean video generations;
the overlay belongs in the Blender edit. The editable compositor is
`generated/storyboard/first-contact-animatic-v01/finale-two-plates.blend`.

V60 is the active review: http://127.0.0.1:8768/?v=v60
The full edit remains 5265 frames, 1920x1080 at24fps. Original V59 AAC packets
verified identical; V59 remains available. Picture spot checks cover the new
section start, revised interfaces, projection, travel inserts and final overlay.
Assembly scripts, frame plan and verification are in
`generated/storyboard/first-contact-animatic-v01/`. No new paid generation.
Next: review pacing in the animatic before preparing clean footage.

## October 11 — accepted V59 save point / break

User accepted V59 as the save point before taking a break: stronger optical zoom overlaps, Blender departure pullout and enlarged cyan twinkle.
Full edit: 5265 frames, 1080p at24fps, original master audio. No paid jobs
pending; cumulative spend3384credits. V57 softer zoom and V58 prior twinkle
remain local fallbacks. New work resumes at frame3144 (2:10.958), the second
chorus/new jungle world; no new generation or planning is requested during
the break. Matching intro ship shots to the accepted sphere design is still
future work. Canonical decisions: `shots/shotlist.json`. Curated exact image
references: `reference-images/manifest.json`. Small metadata, prompts and
rebuild scripts: `checkpoint/`. Large footage, audio, frame caches, blends
and full renders stay local and excluded from Git.

## October 11 — V59 more visible cyan twinkle

User accepts V58 stronger zoom and Blender pullout; requests a more noticeable
twinkle. Doubled its spatial size and multiplied linear light by2.5 in Blender.
Same cyan, anchor and pulse timing (peak local6, gone by17). Only pulse picture
frames differ; accepted pullout and optical overlaps retained. Full5265frames,
24fps1080p, original master AAC packets verified identical to V58. No new spend.
V57 and V58 remain available. Review: http://127.0.0.1:8768/?v=v59
Editable scene and verification: `generated/storyboard/departure-discovery-motion-v05/`.

## October 11 — V58 stronger zoom and Blender departure effects

User accepted V57 blur and explicitly requested keeping it as a fallback.
V58 uses longer radial trails and greater opacity at the same eight optical
transitions, still one or two frames each; no timing changes.
Departure now has an editable Blender compositor pullout: 1.18x at frame2665
(1:51.0), smoothly reaching 1.0x at frame2723 (1:53.417). Cyan station twinkle
at source pixel960,514 peaks at localframe6 and fades by17. Source video speed
is unchanged. Blender renders local1–59;60–140 reuse the original picture.
Full-frame return differs by less than0.17 average code values per RGB channel.
Full5265frames,1080p24fps; original master AAC packets verified. No new spend;
cumulative3384credits. V57 full video and passage remain intact.
Comparison and editable blend: http://127.0.0.1:8768/storyboard/departure-discovery-motion-v04/
Current review: http://127.0.0.1:8768/?v=v58
Frame stepping verified: focus the timeline, then Shift+Left/Right; no app change.

## October 11 — V57 brief optical zoom overlaps

User requested a rapid outgoing zoom blur to connect the static magnification
steps. Eight transitions now expand the outgoing view toward camera with a
radial shutter blur, fading over the next static image on its original cue.
Two frames per overlap; one frame into the shortest three-frame views
(cues 3 and 8), leaving clear settled views. Fourteen picture frames affected.
All nine cue frames and the final planet hold/reveal are retained; lyrics
are composited afterward and stay sharp. V56 reversed departure retained;
user noted its distant opening might linger but was undecided about changing it.
Full 5265 frames, 1080p/24fps; master AAC packet hashes match V56.
No new generation or spend; cumulative 3384 credits. Playback review pending.
Review: http://127.0.0.1:8768/?v=v57
Effect manifest and build: `generated/storyboard/departure-discovery-motion-v03/`.

## October 11 — V56 departure reversed

User requested literal reversal of “To the bigger sky beyond” so the ship
comes out from the station. Reversed the accepted clean 140-frame picture
 at frames 2665–2805 (exclusive end); forward lyrics and original music retained.
All other shot selections and timings retained. Full 5265 frames, 1080p/24fps,
master AAC packets verified identical to V55. No new generation or spending;
cumulative 3384 credits. V55 retained as prior version.
Review: http://127.0.0.1:8768/?v=v56
Clean reversal and provenance: `generated/storyboard/departure-discovery-motion-v02/`.

## October 11 — V55 clean departure/discovery assembled

All seven approved silent1080p Kling takes collected, reviewed and assembled.
Actual280credits, cumulative3384; no jobs pending or additional spend.
V55 active: frames2595–3144,549frames at24fps. Full5265frames1920x1080;
original master AAC packet hashes verified identical to V54. Assembled cut
samples reviewed; user playback review pending.

Important departure adjustment: raw take lingered and introduced a bright
flare around1.5s before a changed angle. Exclude native1–72. Native73–193 is
retimed to140frames using cubic ease-out with adjacent-frame blending:
immediate brisk pullback into distant ship/station, no old dissolve. Begins
after the turn with engine ring on opposite side from the starter. Small
inner edging exists briefly in generated geometry; rapid recession limits
its visibility. Exact map in `pullback-frame-map.json`; clean retimed take
`departure-retimed-clean.mp4`. Approved still remains ship design reference.

Other selections: signing25–94, target25–92, planet25–72, cabin25–69,
affirmation25–66, confirmation25–87. Planet rotation is stronger than prompt
but coherent; quiet reaction retained before stronger later hair/head turn.
Nine optical still cuts remain at exact V54 cues through2920, final view
holds until2946, then native48-frame planet reveal. Full master audio intact.
Plan/prompts/receipts: `kling-departure-discovery-v01.json`.
Full: http://127.0.0.1:8768/?v=v55
Passage/clean takes: http://127.0.0.1:8768/storyboard/departure-discovery-motion-v01/

## October 11 — departure clean-motion batch running

User accepted V54 and requested clean shots/assembly, with a fairly quick
initial pull-away so simplified Harper is not held large. Explicit approval:
“Approve eight Kling uploads and 280 credits.” Seven silent1080p Kling3.0
jobs submitted once; all RUNNING at first query. Actual charge280, confirmed
cumulative3384. Plan: `kling-departure-discovery-v01.json`; receipts under
`generated/kling-tests/departure-discovery-v01/`. Do not resubmit these jobs.

Takes: signing5s, immediate departure pullback8s (first/tail stills), target5s,
planet4s, cabin4s, affirmation4s, course confirmation5s. Nine optical views
remain stills. Departure should shrink the close ship view immediately,
with camera moving much faster than ship; no static opening dwell or dissolve.
Selected native framing and timing require QA before V55. Assembly scripts
prepared at `generated/storyboard/departure-discovery-motion-v01/`.
V54 remains active while collection/review proceeds. No further spend approved.

## October 11 — V54 larger Harper; ship continuity reference selected

User prefers the larger Harper from the first floating draft; the smaller
V53 adjustment was only to expose feet. V54 retains that larger head/torso
scale and tucks both legs to show complete shoes. One built-in ImageGen edit;
same ship composition, single outer equatorial band, no inner cockpit ring.
Exact timing unchanged; no Kling spending.

User explicitly requested this ship design be marked as reference for later
intro matching. Canonical `continuityReferences.personalSphereShip` now names
`sphere-ship-continuity-v01`, with userSelectedDesign=true and the reference
asset `generated/storyboard/departure-discovery-v04/undocking.png`. Original
empty ship v01 is the geometry source; the preferred larger figure draft is
preserved as `larger-harper-scale-source.png`. Board tile and app note are
labeled SHIP CONTINUITY REFERENCE. Intro revisions are future work; when
undertaken preserve one equatorial band, entry, aft ring, pole plates, field
and personal scale rather than inventing inner cockpit structures.

Full V54 review: http://127.0.0.1:8768/?v=v54 at1:51. Updated figure review
pending; selected ship design reference is recorded. Earlier edits retained.

## October 11 — V53 ship geometry and weightless Harper

User rejected V52's extra inner cockpit ring and hidden feet. Original
`departure-discovery-v01/undocking.png` is the authoritative ship geometry:
one outer equatorial band, entrance point, one aft engine ring, upper/lower
technical plates, open transparent volume. V53 removes the invented inner
ring/railing and places Harper floating in her gray coverall, knees relaxed,
both complete graphite shoes and entire body visible above the equatorial
band. V52 camera/station composition and all exact timing are retained.

One replacement still via built-in ImageGen, two attempts; first still hid
one shoe, second corrected it. Files/prompts/receipt in
`generated/storyboard/departure-discovery-v03/`. No Kling charges.
User tentatively prefers updating earlier opening shots to this newer ship
model later; that broader revision is recorded but not performed here.
Review pending: http://127.0.0.1:8768/?v=v53 at1:51.

## October 11 — V52 forward departure correction

User identified missing Harper and ambiguous ship/gantry scale in the first
exterior after signing, departure-002 at frame2665 (“bigger sky beyond”).
Replaced only this image with a forward three-quarter view: ship already
clear and turned toward camera, Harper visible inside at controls, station
and retracted gantry receding behind in depth. Aft ring stays to the side of
her silhouette. Native action should move gently toward camera, not sideways
past the gantry. Original V51 and image preserved.

New asset and exact prompt: `generated/storyboard/departure-discovery-v02/`.
One built-in ImageGen edit; no Kling submission/spending (3104 cumulative).
Ship fills roughly 77% height rather than requested48%; explicit depth and
visible Harper now establish personal-craft scale. Same exact V51 timing,
including dissolve to far station. V52 still review pending; continuous
pullback remains to be animated. Review: http://127.0.0.1:8768/?v=v52

## October 11 — V51 departure/discovery still animatic

User requested the selected route's stills edited and timed for review. V51 is
now active: 17 separately generated ImageGen stills in 18 holds, frames
2595–3144 (549 frames, 22.875 seconds). The nine optical cuts land at 2873,
2887, 2891, 2894, 2899, 2903, 2908, 2912 and 2915. Final zoom holds through
2945; the full jungle planet appears on “big” at 2946 for 48 frames, then
wide cabin at 2994, quiet affirmation at 3039 and course confirmation at 3081.

Gray long-sleeved survival clothes, spherical ship and open dome cabin remain.
Undocking is represented by two held exterior keyframes with a 12-frame
dissolve at 2747–2759; continuous camera pullback and native action await
later motion work. Nine zoom views are distinct generated assets; small
editorial reframing on 04/05 centers the target and preserves increasing
disc size. Generated scale differs from prompts: far station remains about
6% of image height, last zoom about 42%, hero about 87%. These are review
stills, with prompts, receipts and framing recorded alongside the assets.

Full V51 verified 5265 frames, 1920x1080, 24fps; original master AAC packet
hashes match V50. Rendered cut samples reviewed. User playback review pending.
No Kling submissions or charges; cumulative confirmed credits remain 3104.
Accepted V50 is preserved. Source of truth: `shots/shotlist.json`.
Full review: http://127.0.0.1:8768/?v=v51
Stills: http://127.0.0.1:8768/storyboard/departure-discovery-v01/board/index.html
Passage: http://127.0.0.1:8768/storyboard/departure-discovery-v01/timed-still-board.mp4

## October 11 — V50 accepted; departure/discovery direction selected

User accepted the concourse result and selected the full A/B path:
1A → 2A → 3A → 4A → 5A → 6B → 7A → 8B, explicitly retaining the nine-step
4A zoom montage after considering 4B. Direction is recorded in canonical
`departureDiscoverySequence` and eight `departure-001` through `departure-008`
proposals, batch `departure-discovery-v01`. Eight timed app notes saved.

Span: frames 2595–3144, 549 frames at 24fps (1:48.083–2:10.958).
Boundaries: 2595 signing/handover; 2665 careful undock plus continuous camera
pullback; 2805 interior profile/target control; 2873 nine optical zoom steps;
2920 resolving target; 2994 wide cabin/distance; 3039 quiet close reaction;
3081 hand confirms course; 3144 second chorus begins, action still unplanned.
Nine in cues: 2873, 2887, 2891, 2894, 2899, 2903, 2908, 2912, 2915.
Full new-planet reveal on big at2946, now at2953; hold until2994.

Preserve gray survival coverall, established spherical ship and accepted cabin.
Owner is distinct from the rejected ferry captain; boarding is elided between
handover and departure. Target stays anchored across substantial magnification
steps. The jungle planet is remote, not an instantaneous arrival. Selected
planet palette/geography: dark-emerald jungle continent, copper inland seas,
ivory storm systems; exact appearance awaits still review. Main cuts must
change viewpoint, subject or scale decisively. Affirmation is discovery and
commitment, not proof she has already helped the world.

Text planning only: no new stills, footage or charges. V50 remains the accepted
active render. Next step is first-frame/storyboard development for this route;
review the animatic before paid motion. Cumulative Kling credits remain3104.

## October 11 — V50 native concourse, still ship flips

User approved five Kling uploads and 240 credits. All five silent 1080p/24fps
renders are collected; actual charge 240, cumulative confirmed 3104 credits.
No paid jobs pending. Plan, prompts, receipts and selections are recorded in
`kling-station-concourse-v02.json`; canonical edit is `shots/shotlist.json`.

V50 retains the arrival, directory and first promising-option native takes.
The two brief bioship and sailcraft flips now use the exact accepted stills,
with the existing four-frame right-to-left soft-boundary wipes. No image
translation or extra light-flash overlay. New native takes cover the captain
exchange, populated food court, parts/outfit market, gantry walk and restrained
entrance-view close-up. The 12-frame dissolve into the food court is retained.

The gantry ending preserves V49 timing: wide 2425–2507, close-up 2507–2539,
resumed wide 2539–2595. Both wides use ONE continuous take: source 25–106 then
107–162. Kling walked continuously rather than pausing on schedule, so the
close-up supplies the consideration beat and the wide resumes on the next
source frame. This avoids a position jump and cuts before boarding. Gentle
native camera drift remains; there is no added editorial pan or retiming.
Captain source 13–95 retains more of his offering gesture; this uses a shorter
12-frame leading handle, sufficient for its incoming wipe. Slight mouth
movement remains late in the refusal, with no generated audio.

All five takes and assembled transition/ending samples reviewed. Full export
is 5265 frames, 24fps, 1920x1080; passage is 490 frames. Original master AAC
packet hashes match V49. User playback review is pending.
Full review: http://127.0.0.1:8768/?v=v50
Passage and clean takes: http://127.0.0.1:8768/storyboard/station-concourse-motion-v02/
Earlier held-still/no-generation statements below are historical.

## October 11 — V49 walk, consider, continue

User accepted V48 stills and requested continuing movement across the long
gantry scene: walk first, stop and consider in close-up, then resume walking
in the wide. V49 reuses the approved images, with no new image or video jobs:
concourse-010 walk2425–2507 (82frames/3.42s), concourse-012 consideration2507–2539
(32frames/1.33s), new concourse-013 resumed walk2539–2595 (56frames/2.33s).
Anchors are DAWproject bar40 beat1, bar41 beat2, bar41 beat4 and existing vocal.
Full5265frame/24fps/1920x1080 export and original master AAC hash verified.

This is a HELD-STILL timing preview. Next native pass must use successive
parts of ONE continuous wide take, with her pause covered by the close-up,
then resume at her stopped position. No reset/loop or changing gantry geometry.
Keep her outside and visible until the next transition. Motion planning in
`station-concourse-v05/motion-plan.json` and canonical concourseSequence:
proposed10second wide take (source25–106, pause107–138, resume139–194) and
4second close-up (source25–56), at least24frame handles. Not submitted.
The old V45 wide walking take reaches the entrance too soon for this structure;
it is preserved, not silently retimed into the new draft. No credits spent;
cumulative2864. Earlier captain/markets unchanged.

Full review http://127.0.0.1:8768/?v=v49 . Passage and three-part blocking:
http://127.0.0.1:8768/storyboard/station-concourse-v05/ . Canonical shotlist and
revision-checked app notes include all three beats and updated handoff.

## October 11 — V48 annotated original gantry and entrance POV

User rejected the consecutive altered gantry views for spatial inconsistency
and annotated the original board item `concourse-011-still-v01`, titled
Discover the opening ship, with back to using this one. The exact source
`station-concourse-v01/concourse-011.png` is now restored without edits;
SHA256 confirms the `station-concourse-v04/original-gantry.png` copy is identical.
Its original ship scale supersedes the earlier approximate80percent variation.

V48 consolidates frames2425–2556 into this one original exterior composition
(active shot concourse-010), followed by a new close-up from the SHIP ENTRANCE
looking BACK toward Harper and the station at2556–2595 (concourse-012).
Harper is near-frontal, station portal and gantry rails behind her, restrained
positive decision with closed lips. Sphere is behind camera. No cabin/boarding.
The superseded concourse-011 approach marker is addressed and its shot archived.

New close-up made with one built-in ImageGen call, exact prompt/receipt and
source references in `generated/storyboard/station-concourse-v04/`. Original
board selection retained; new board item concourse-v04-entrance-pov, revision52.
Review: http://127.0.0.1:8768/storyboard/station-concourse-v04/ . Full V48:
http://127.0.0.1:8768/?v=v48 . This remains a still/pacing review. Native motion
will keep exterior camera steady or very slow, stop Harper on gantry, then
use the distinct entrance POV; no new Kling jobs or charges, cumulative2864.
Earlier captain/markets retained. Full5265frames,24fps,1920x1080 and original
master AAC hash preserved; both ending samples visually checked. Canonical
source `shots/shotlist.json`, active batch station-concourse-v04.

## October 11 — V47 stop outside, then decide

User accepted all V46 shots except the final boarding view because its port
interior did not match the established sphere cabin. V47 replaces only that
final 88-frame slot: concourse-011 approaches along the gantry and stops before
the dark/closed entrance (2507–2556, 49 frames); concourse-012 cuts to a calm
positive-decision close-up (2556–2595, 39 frames). The split is DAWproject bar42
beat1. Keep camera fixed or moving very slowly in later motion. Expression is
quiet and practical, not a broad smile. No boarding or cabin interior is shown.

Two built-in ImageGen stills, exact prompts and receipts are in
`generated/storyboard/station-concourse-v03/`. The approach used two attempts
(the first floor-contact error is archived); close-up passed in one. Same
Creative Production board revision36. The accepted captain, food concourse,
outfitter market and first gantry pause are retained. Revised ending stills
await user review; no Kling generation or spending. Cumulative credits2864.

Full V47: http://127.0.0.1:8768/?v=v47 . Ending stills and timed passage:
http://127.0.0.1:8768/storyboard/station-concourse-v03/ . Source of truth is
`shots/shotlist.json`, active batch station-concourse-v03. New close-up marker
and corrected handoff note saved: at frame2595 she has chosen the ship while
still outside. A later transition into the established cabin remains unplanned.
Earlier assertions that she has already boarded by this cue are superseded.

Verified 5265 frames at24fps,1920x1080; original master AAC packet hashes match
V46. Final two sampled frames visually checked. Prior media and versions kept.

## October 11 — V46 interaction, markets and boarding still revision

User reviewed V45 and requested a longer captain exchange, busier alien-populated
station areas, an approving gantry pause and a roughly 20% smaller ship with a
closer boarding cut. Stills first: five built-in ImageGen compositions are now
in `generated/storyboard/station-concourse-v02/`, with exact prompts and receipts.
Same Creative Production board, revision 33. No new Kling generation or charges;
cumulative confirmed spend remains 2864 credits. New motion awaits still review.

V46 keeps the first five concourse native takes and all three right-to-left
flip wipes. The third flip now leads to one continuous captain two-shot at
frames 2211–2294 (3.46s), replacing the brief rejection/near-duplicate departure.
A 12-frame dissolve centered at 2294 leads into the food concourse (2294–2359),
then the parts/outfitter/exotic-goods market (2359–2425). Harper pauses approvingly
at the gantry (2425–2507), then cuts closer to board (2507–2595). All boundaries
come from existing lyric cues or the DAWproject beat grid. The old six-frame
reaction proposal remains archived as superseded; its review note is addressed.

The new five images are HELD STILLS: captain pitch, head-shake, walking and
boarding are directions for a later motion pass. The two markets contain
varied alien vendors, diners and travelers. Gray coverall and ship identity
remain. Gantry first attempt selected for its readable expression and plausible
staging; the alternative has weaker staging and is retained only as a draft.
Ship looks more compact, but exact 80% physical scale is not verifiable from
the changed perspective. Boarding gives a human-sized threshold and tighter
view; review the amber entry recess against the eventual cabin continuity.

Review five stills and timed passage:
http://127.0.0.1:8768/storyboard/station-concourse-v02/ . Full V46:
http://127.0.0.1:8768/?v=v46 . Visual samples, metadata, source frame counts and
master AAC packet equality checked. Full edit remains 5265 frames, 24fps,
1920x1080. V45 and all raw/generated media preserved locally, ignored by Git.
Canonical source remains `shots/shotlist.json`; active batch station-concourse-v02.

## October 11 — V45 clean concourse motion assembled

The user explicitly approved eleven Kling uploads and 392 credits. All eleven
silent 1080p Kling 3.0 takes completed and were collected exactly once. Actual
charge: 392 credits; cumulative confirmed spend: 2864. No paid jobs pending.
The earlier approval-pending section below is historical and superseded.

V45 replaces the accepted concourse stills at frames 2105–2595 with reviewed
native footage. Source inpoints are frame 25, with at least 24 frames of lead
and tail handles. Three four-frame vertical reveal wipes are centered on
frames 2192, 2203 and 2211, moving right to left with a 64px soft boundary and
restrained 3px pale accent. The images do not slide. The full edit retains
5265 frames at 24fps, 1920x1080; original master AAC packet hashes match V44.

The two ship-only flip takes invented a foreground figure. Local first-frame
station plates restore the left 25%, feathering to 30%; generated ship motion
is retained. No additional paid generation was needed. Raw clips and repaired
derivatives are both preserved. The brief six-frame rejection uses a blink
and small head/eye shift; the next shot carries her departure. The final take
shows Harper crossing the bridge and entering the spherical ship. Existing
third-flip/Guess timing remains unchanged. All eleven takes and assembled
wipe samples were visually reviewed; user playback review remains pending.

Full review: http://127.0.0.1:8768/?v=v45 . Passage and individual clean clips:
http://127.0.0.1:8768/storyboard/station-concourse-motion-v01/ . The same folder
contains `native-picture.mp4` without lyrics/audio, the timed captioned review,
authoring scripts, per-shot reviews and verification metadata. Canonical
selection and transition details are in `shots/shotlist.json`; generation IDs
and exact prompts are in `kling-station-concourse-v01.json`. Large media stay
local and ignored by Git. The accepted still gallery remains available.

## October 11 — concourse motion prepared; explicit Kling approval pending

User accepted the latest three-part bioship and the placed still sequence,
requested clean video and assembly, and specified stationary-image vertical
reveal wipes traveling right to left on the flips. Eleven silent Kling3.0
1080p takes are prepared in `kling-station-concourse-v01.json`: durations
4,4,4,3,3,3,3,5,5,7,8 seconds, 49 seconds total, estimated392credits at the
previous confirmed8credits/sec. Each includes one-second source handles.
Live CLI verified duration support3–15seconds and available19793credits.
The existing Harper element323570155312565 is bound where she appears;
current starter images control wardrobe. All11 identical prompt locks retained.

Automatic approval review REJECTED submission because the user had not
explicitly authorized the eleven nonpublic still/prompt uploads to Kling and
estimated392credit charge. No process ran, no jobs submitted or paid, no
request receipts created. Async question asks approval of those exact uploads
and cost. Do not submit until explicit approval arrives. Cumulative confirmed
spend remains2472credits. V44 remains the active full edit.

Unaffected work completed: a490frame still-based wipe preview with original
segment audio and word-timed captions. Three4frame wipes centered on frames
2192,2203,2211;64px soft boundary and3px pale22percent accent at1080p;
no image translation. Review and exact prepared prompts:
http://127.0.0.1:8768/storyboard/station-concourse-motion-v01/ .
`build.py --stills` renders this preview; without the flag it assembles collected
clean native takes. Native collection, visual QA, selection registration and
full V45 insertion remain. Existing final-flip/Guess lyric timing caveat retained.

## October 11 — V44 elegant three-part organic craft

The user rejected the nodular appearance of V43 and requested functional ribs
and bones, then explicitly replaced the U silhouette with three connected
elements. Only concourse-004 changes: `concourse-004-v05.png` has a compact
boarding body, tall tilted ribbed shell and smaller offset propulsion body,
joined by rounded supports with clear negative-space gaps. Smooth jade shell,
light celadon ribs and narrow plum recesses retain the color direction while
removing the fleshy/nodular appearance. No hooks, claws or windows.
Generated with built-in ImageGen; exact prompt and receipt saved alongside
the image and previous versions. New draft awaits review. Other shots and
frame timing remain. Review: http://127.0.0.1:8768/?v=v44 .
Same Creative Production board, revision 27. Earlier U-shape direction is
superseded. The interrupted U-refinement call produced no observed output;
the three-part design completed in one call after the user's steering.

## October 11 — V43 compact microbial U-shaped ship

The user approved the jade/plum colors but rejected hooked points and the
long body. Only concourse-004 is revised, to `concourse-004-v04.png`: compact
asymmetrical U-shaped personal craft with unequal rounded lobes, compound
jade shell volumes and plum folds, inspired by enlarged microscopic life.
There are no claws, hooks, spikes or windows. Its opaque amber-edged hatch
still joins the station ramp. The source image, exact prompt and receipt are
preserved alongside earlier versions; the new shape awaits user review.
All other shots and timings remain. Full review: http://127.0.0.1:8768/?v=v43 .
Same Creative Production board, revision 24; one built-in ImageGen edit.

## October 11 — V42 windowless craft and color rhythm

The user requested greater bioship asymmetry, no windows on the two flip
craft, and coherent color variation across the lead-in and three flips.
Current drafts are `concourse-004-v03.png` and `concourse-005-v03.png` in the
existing station-concourse-v01 folder, generated with built-in ImageGen.
The bioship has a single leaning crest, uneven organic masses, a hooked prow,
desaturated jade shell and plum recesses, with an opaque amber-edged hatch.
The light-sail craft keeps its gold geometry and now has an opaque ivory cabin.
Station corridor windows remain. Previous stills and exact prompt histories
are preserved; new drafts await review.

Color progression: warm ivory at I think my movie's on, cool jade/plum on
the first flip, warm gold/ivory on the second, then rusty ochre on the ferry.
The jade body separates from indigo space; shared cyan and amber station
lighting connects the cuts. Other imagery, timing and master audio remain.
Review: http://127.0.0.1:8768/?v=v42 . Board revision 22, same board ID.

## October 11 — V41 contrasting ships on the first two flips

User requested changes only to concourse-004 and concourse-005, retaining the
junk ferry/captain and the rest of the passage. The revised built-in ImageGen
stills are `concourse-004-v02.png` (grown biomechanical vessel with a bone crest,
organic ribs and green boarding entrance) and `concourse-005-v02.png` (gold
diamond light-sail structure with triangular sails and a suspended cabin).
Both live in `generated/storyboard/station-concourse-v01/`, beside exact
`.prompt.txt` and `.actual-generation.json` records. Original images remain.
All prompts retain the same sequence lock. New designs await user review.

The art-direction comparison considered Chris Foss's spacecraft archive
(https://chrisfossart.com/category/spaceship/), Bruce Pennington's exotic
paperback-cover imagery (https://www.brucepennington.co.uk/covers.htm), and
Barsoom's illustrated sailing-vessel tradition
(https://www.erbzine.com/mag28/2806.html). The original light-sail design was
chosen for immediate geometric contrast with the biomechanical ship; this is
an artistic judgment, not a measured claim about style popularity or rarity.

V41 retains the existing frame grid: first flip 2192–2203 (11 frames), second
2203–2211 (8 frames), both at 24 fps. Other source images remain unchanged.
Full review: http://127.0.0.1:8768/?v=v41 . Gallery:
http://127.0.0.1:8768/storyboard/station-concourse-v01/ .
The existing final-flip/Guess timing caveat remains. No new Kling job ran.

## October 11 — V40 concourse stills and pod-issued survival outfit

The user requested stills for the selected concourse route and allowed Harper
to change into clothing found aboard the escape pod. Eleven linked built-in
ImageGen drafts now cover frames 2105–2595 in the full V40 animatic. Draft
wardrobe is a roomy warm-gray long-sleeve survival coverall, plain adjustable
belt, graphite utility shoes and a small unlettered amber upper-arm tab. The
change happens offscreen during transit; she keeps the suit throughout the
station and ship discovery. A later change into the opening short-sleeve gray
outfit remains to be staged. Wardrobe and images await user review.

Full movie: http://127.0.0.1:8768/?v=v40 . Still gallery and timed passage:
http://127.0.0.1:8768/storyboard/station-concourse-v01/ .
`shots/shotlist.json` contains the image drafts, exact actual prompts, identical
sequence lock and V40 placements. Files, per-image receipts, review manifest
and verification are in `generated/storyboard/station-concourse-v01/`.
Creative Production board: `ce27973e-c009-4d44-8eab-ed01be58c996`, revision 16,
with all eleven items completed. Source assets are local; generated media stay
outside Git. Existing production checkpoint tooling preserves authored text.

The review retains the saved 490-frame passage and the full 5265 frames at
24 fps / 1920x1080. Original master AAC packets verified identical to V39.
These are held composition stills; boarding is planned motion, not a completed
action in the stills. No new Kling job ran; confirmed spend remains 2472 credits.

Review points: third flip / Guess not still share the provisional lyric edge;
the discovery sphere retains a glossier rim than the thin-field intent; the
directory view has a broad window hex grid while later concourse views are
clear. Premature sphere reveal and an unintended bag were corrected before
assembly. Earlier V39 and pre-wardrobe statements below are historical.

## October 11 — concourse route selected and timed directions saved

The user selected the dockside concourse route with a brief directory moment
for orientation. Arrival at a transport hub leads to real ship options on the
three flips, a terrible ferry and overly eager captain, rejection, then a quiet
walk to a remote berth and discovery of the spherical ship from the opening.
Boarding leads into All, all calling at frame2595 (108.0833seconds).

`shots/shotlist.json` is the authority: `concourseSequence` records the selected
route and continuity notes; `concourse-001` through `concourse-011` in
`storyboardProposals` cover frames2105–2595. Twelve timed notes, including the
handoff cue, are saved in the review app at notes revision25. Prior notes are
preserved. Frame anchors derive from existing lyric/word timing and musical
grid markers; these are proposed blocking cues, not locked cuts.

The third flip and Guess share provisional frame2211, and that flip currently
has a zero-frame compiled span. Review playback before locking those cuts.
Frame2223 is the current not onset and proposed rejection accent. Let the
captain/rejection action continue into the instrumental so it reads clearly.
The remote-berth reveal starts at frame2458 (102.375seconds). Wardrobe continuity
from the escape silver outfit to the opening gray outfit remains to be staged
before generating imagery. Arrival uses the ovoid escape pod; the discovered
ship is the established thin-field spherical craft.

V39 remains the current rendered movie; the additions are direction markers.
Next: review this passage and develop station/ship starter frames for a still
animatic. No new generation or paid job ran; confirmed spend remains2472credits.

## October 10 — accepted V39 save point, files-only GitHub backup

The user accepted V39 and requested a clean commit/push of production files,
without new media. Full working edit remains5265frames at24fps,219.375seconds,
1920x1080, with the original master AAC packets. Latest native escape clips and
their canonical selections are now user accepted. Confirmed cumulative Kling
spend2472credits; no paid jobs pending. Continue at frame2105 (87.6667seconds),
“All the way to the next channel,” after the pod's rolling departure.

`shots/shotlist.json` remains the edit authority. Shared locks, source in-points,
handles, exact prompts, job IDs/charges, previous directions and shelved ship
experiments are retained. `project.json` records checkpoint2026-10-10-v39.

`tools/project_checkpoint.py` now also preserves small authored production
scripts (including Blender builders), exact image prompts, selected production
metadata and request/submission receipts from ignored generated folders.
Receipts contain no provider download URLs or account credentials. Cached
account/model captures and provider result responses remain local. Checkpoint
manifest records original paths, byte counts and SHA256 hashes. Restore missing
text/metadata files without overwriting existing local work with:

    python tools/project_checkpoint.py projects/a-right-little-something/project.json --restore

This save point adds no images, audio, video, fonts, rendered substrates or3D
model files to Git. Existing tracked curated references are unchanged. Source
media and the full rendered movie remain in the local ignored production tree;
restoring the files checkpoint alone does not restore those media assets.
Older “playback pending” statements below describe earlier review stages.

## October 10 — V39 native escape motion,112 approved credits

The user approved both starter-frame uploads and the8second interior/6second
exterior1080p Kling batch. Both completed; actual64+48=112credits, cumulative
confirmed2472. No paid jobs pending. `kling-escape-ejection-v01.json` preserves
authorization, exact prompts, task IDs and actual charges.

Full V39: http://127.0.0.1:8768/?v=v39 . Escape context:
http://127.0.0.1:8768/storyboard/escape-ejection-motion-v01/escape-passage.mp4 .
Native interior source25–137 fills1897–2010 (113frames),24lead-in/56lead-out.
Harper is secured and glances toward the viewport; external hull falls away
around Leaving orbit. Native exterior25–119 fills2010–2105 (95frames),24lead-in/
26lead-out. Pod gains clearance, makes a broad rolling turn and accelerates;
mother ship recedes. Roll is more pronounced than the small-bank intent and
the near-pod wake broader/brighter than thin mist. See canonical QA and
`ESCAPE-DIRECTION.md`; new motion is agent reviewed, user playback pending.

Nine earlier prepared native chunks retained. Exact shot grid, phrase fades,
full5265frame24fps1920x1080 edit and original master AAC retained. New clips
have no retiming or additional editorial camera move. Next channel starts2105.
Earlier V38 still-stage approval/pending statements below are historical.

## October 10 — V38 ejection starting frames at 1:19

The latest user direction shortens Bright night to frame1897 (79seconds), then
cuts to secured Harper inside a new escape capsule through2010. Ejection is
planned as the robot ship falling away through the side window during Leaving
orbit. Exterior2010–2105 starts safely clear, extends the gap, banks once and
accelerates on a new heading, with a quickly fading curved wake.

Two linked ImageGen starter stills are staged with editorial pans in full V38:
http://127.0.0.1:8768/?v=v38 . New frames:
http://127.0.0.1:8768/storyboard/escape-ejection-v01/review-board.html .
These are timing/design drafts, not native ejection footage. Compact ivory/
graphite ovoid pod derives from the accepted boarding cabin, distinct from the
opening spherical craft; original submarine-like robot ship remains selected.
First eight prepared native lab/ship clips are reused; Bright night reuses its
first28editframes instead of89. Canonical prior records are archived before
changing timing. Existing phrase grid, full5265frames/24fps/1920x1080 and original
master AAC packets remain unchanged. See `ESCAPE-DIRECTION.md` for exact timing.

Prepared `kling-escape-ejection-v01.json`:8second interior plus6second exterior,
1080p, one-second handles each side, estimated112credits total. No new paid job
submitted or authorization recorded. Confirmed cumulative spend2360credits.
The earlier after-Bright-night hold and unresolved pod plan below are historical
and superseded by this latest1:19 direction. Route beyond2105 remains open.

## October 10 — user accepted V37 and requested full-song review

The user accepted the escape setup and asked to review the FULL animatic before
designing the next starting frames. V37 was already integrated through the full
song; no further render or paid generation was needed. Current player:
http://127.0.0.1:8768/?v=v37 . It loads the5265frame,219.375second full edit and
the existing timed-note interface. User notes were preserved untouched.

Canonical lab2-08 motion selection and placement are now user accepted.
Stale six-biopod still descriptions in the full player's exterior-shot metadata
were corrected to the actual restored native robot-ship footage.
Next direction: pod cut loose, dropped or ejected from the ship at Leaving orbit,
frame1958(81.5417s), followed by an interesting path across the next part of the
song. `escape-001` preserves the52frame initial cue. Pod identity, release
mechanism and trajectory remain undecided until full-song review/notes; no new
starting frames or departure footage have been generated. Credits stay2360.

## October 10 — V37 So bright becomes an escape setup

The user judged the no-streak sun shot too close to a collision course and then
changed direction before the revised sun composition was generated. So bright
is now Harper approaching a lit escape-pod boarding hatch inside the original
robot laboratory ship. The abandoned sun-behind-ship placeholder is marked
superseded; no image/video job ran for it. The earlier paid sun take is retained
as user-rejected history.

Built-in ImageGen used Harper's established lab portrait and lab architecture;
starter frame, exact prompt and provenance are in `generated/storyboard/escape-approach-v01/`.
Creative Production board completed `escape-approach-v01` at revision73.
Adult Harper's freckles, curls and silver halter top remain; hands and full pod
exterior are offscreen. The bright cabin/seat destination contrasts with the dark
graphite passage. The shared lock is identical across nine lab/ark records and
the planned departure, with growth-tank restrictions now scoped to tank shots.

The user requested another take at the prior known six-second1080p48credit setup,
then changed its subject to the escape setup. One48credit Kling job completed;
`kling-escape-approach-v01.json` records request, task and collection. No additional
departure job was submitted. Source1916x1080,145frames at24fps; source37–67 fills
the unchanged1838–1869 slot (31frames), with source35–69 for four-frame fades.
Sampled face/top/hatch remain coherent. The short beat is her turn from a backward
glance toward the passage; later motion does not complete boarding. Hair blur
during the turn is pronounced. Do not claim verified full boarding action.

Current film: `generated/animatic/A-Right-Little-Something-selected-motion-v37.mp4`.
Escape setup sequence:
http://127.0.0.1:8768/storyboard/escape-approach-motion-v01/escape-setup-passage.mp4 .
Through Bright night:
http://127.0.0.1:8768/storyboard/escape-approach-motion-v01/animatic-through-bright-night.mp4 .
Eight existing prepared clips are reused; only So bright changes. Bright night
stays the original ark exterior. The user explicitly places departure AFTER it,
on Leaving orbit at the moment atframe1958(81.5417s). Canonical `escape-001`
plans1958–2010,52frames; no starter frame/footage exists. Pod identity is undecided
(existing spherical personal ship or different escape pod). See `ESCAPE-DIRECTION.md`.

Full5265frames,24fps,1920x1080 and original master AAC packet hash verified.
Native approach is agent-reviewed, user playback pending. No paid jobs pending.
Confirmed cumulative Kling credits:2360(previous2312 + requested48).

## October 10 — V35 original robot ship restored, So bright replaced

The user chose the original graphite submarine-like robot laboratory ship after
reviewing the six-biopod, Blender and ImageGen-pose experiments. These experiments
are shelved with their source assets retained. Active design reference:
`generated/storyboard/lab-verse-v01/lab2-06.png`.

The user rejected the original So bright take's luminous starward streaks.
Built-in ImageGen created a new original-ship starter frame beneath a large
textured cropped solar limb, gold rimlight, cyan galleries and open dark space
between ship and sun. Exact prompts and provenance are in
`generated/storyboard/robot-ship-so-bright-v01/`. Creative Production board item
`robot-ship-so-bright-v01` completed at revision 69.

After the timed V34 still review, the user explicitly approved one six-second
1080p Kling replacement for 48 credits. `kling-robot-ship-so-bright-v01.json`
records the completed job. Native source is 1916x1080,145frames at24fps; selected
source37–67 fills exact1838–1869 song frames (31frames), with source35–69 for
four-frame fades. No time stretch; the native camera move needs no added zoom.
Samples retain hull/galleries/spars and show no starward streaks. The early edit
avoids the bow approaching the solar limb late in the source take.

Current film: `generated/animatic/A-Right-Little-Something-selected-motion-v35.mp4`.
Ship sequence:
http://127.0.0.1:8768/storyboard/robot-ship-so-bright-motion-v01/original-ship-passage.mp4 .
Through Bright night:
http://127.0.0.1:8768/storyboard/robot-ship-so-bright-motion-v01/animatic-through-bright-night.mp4 .
All nine lab/ark shots are animated. Eight prior prepared chunks are reused;
the original native ship clips are restored for lab2-06/07/09. Exact phrase
grid, shared prompt lock, fades, schematic dissolve and master audio are retained.
Full5265frames,24fps,1920x1080 and original AAC packet hash verified by insertion.
New replacement is agent-reviewed; user playback pending. No paid jobs pending.
Confirmed cumulative Kling credits: 2312 (previous2264 + approved48).
See `ROBOT-SHIP-SO-BRIGHT.md` for detailed provenance and QA.

## October 10 — Blender-pose / ImageGen-finish experiment

The user judged the native V04 look below the approved illustration and requested
an experiment: use the 3D model's poses as guides for reference-quality first frames.
Two built-in ImageGen edits, forward and aft, succeeded on their first attempts.
Each used its native V04 render as Image 1 (pose/layout authority) and the accepted
`ark-replacement-v01/lab2-06.png` illustration as Image 2 (finish/detail authority).
The identical ship lock block is saved with both exact prompts.

Review: http://127.0.0.1:8768/storyboard/ark-pose-transfer-v01/review-board.html .
Images, prompts, provenance and actual QA:
`generated/storyboard/ark-pose-transfer-v01/experiment.json`.
Both outputs are 1672x941. Six pods, broad pose, spacing and overlap order survive;
illustrated hull/galleries/habitats and field-ring quality improve substantially.
Local fidelity is approximate: the forward nose rounds slightly, and fine panels,
reflections and terrain are reinterpreted. This supports pose-guided starter-frame
development with per-image continuity review, not an exact frame-by-frame 3D style
transfer. The experiment is user-review pending; neither output is selected.
Creative Production board completed both items at revision 67.
V33, canonical frame ranges, selected edit assets, prompt locks and audio remain
unchanged. No Kling submissions or new video charges; cumulative credits 2264.

## October 10 — illustrated native Blender look development

The user accepted the V02 ship direction and requested illustrated graphic-novel
lighting and rendering. Current working model is
`generated/design/ark-blender-v04/headquarters-ark-v04.blend`.
Review: http://127.0.0.1:8768/storyboard/ark-illustrated-v01/review-board.html .
It compares the approved illustration, V02, updated forward/aft/detail renders
and the new textured render before the restrained native brush finish.

V04 adds physical recessed galleries, fitted surface detail, small varied alien
flora, procedural surface shading, habitat haze, warm/cool directional lighting,
blue-violet space atmosphere and restrained bloom. Native anisotropic compositor
finish uses radius 3px blended at 35%. Proofs are 1600x900 Cycles/OptiX, 96 samples,
AgX Medium High Contrast, exposure +0.25. Six pod centres remain identical to V02;
saved-model verification confirms live Render Layers and no external textures.
The style is user-review pending; geometry and ecology remain simpler than the
illustration. Temporal brush-finish evaluation is pending. The linked V02 camera
sweep still demonstrates geometry only, not the updated look.

See `ARK-BLENDER-MODEL.md` for sources, verification and render controls.
Creative Production board revision 64 has completed native V04 hero/aft/detail.
V33 remains the film. Only development metadata was updated for lab2-06–09;
phrase frame ranges, prompt locks, selected edit assets and audio are unchanged.
No paid jobs pending or new charges; confirmed cumulative credits remain 2264.

## October 10 — native Blender headquarters ark model

The user accepted lab2-06's balanced design but rejected the other three ark
angles as warped. They requested an actual Blender reconstruction, starting
simple and then refining geometry and materials. First blockout V01 and
refined working model V02 are saved under `generated/design/ark-blender-v01/`
and `generated/design/ark-blender-v02/`. See `ARK-BLENDER-MODEL.md`.

Review: http://127.0.0.1:8768/storyboard/ark-blender-v02/review-board.html .
Camera sweep: http://127.0.0.1:8768/storyboard/ark-blender-v02/camera-sweep.mp4 .
V02 is actual editable geometry with six fixed mirrored pod centres, procedural
terrain/materials, internal habitat lights and a camera orbit controller. It
remains a proportion/material study, with simpler detail than the illustration.
The previous replacement Kling plan is superseded without submission. Three
distorted image candidates are marked user-rejected in canonical shot metadata.
V33 remains the film; this model review has not changed shot timing or audio.
No paid jobs pending or new charges; confirmed cumulative credits remain 2264.

## October 10 — v33 six-biopod ark starter-frame review

The user accepted headquarters ark V04 with muted, terrain-scale habitats and
requested four replacement exterior stills before Kling video go-ahead.
`ARK-REPLACEMENT-SHOTS.md` records exact phrase frames and motion directions.
Full-size review: http://127.0.0.1:8768/storyboard/ark-replacement-v01/review-board.html .
Timed passage: http://127.0.0.1:8768/storyboard/ark-replacement-v01/new-ark-passage.mp4 .
Review through Bright night: http://127.0.0.1:8768/storyboard/ark-replacement-v01/animatic-through-bright-night.mp4 .

V33 uses five unchanged native laboratory takes followed by four new ark still
previews at the original 47/29/31/89-frame slots. Earlier edits, fades and master
audio are preserved. Current movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v33.mp4`.
Canonical batch `ark-replacement-v01`; recipe `storyboard-ark-replacement-v01.json`.

Continuity caveats: habitat details shift in the aft view; the final nebula shot
has a larger, more compact ship than intended. All four candidates have six
pods. These remain user-review drafts, not approved video sources. Exact image
prompts, QA, failed first attempts and proof frames are preserved in the batch.

`kling-ark-replacement-v01.json` prepares four six-second 1080p takes, estimated
192 credits total, with a shared prompt lock and one-second source handles.
No new uploads, jobs or paid charges. Confirmed cumulative spend remains 2264.
User must review the stills before authorizing these replacement animations.

## October 10 — v32 native robot holographic-control replacement

Current full movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v32.mp4`.
Review through Bright night:
http://127.0.0.1:8768/storyboard/lab-robot-motion-v01/animatic-through-bright-night.mp4 .
Robot cutaway in context:
http://127.0.0.1:8768/storyboard/lab-robot-motion-v01/robot-cutaway-in-context.mp4 .

The explicitly approved 48-credit replacement completed and was collected.
Its 145-frame, 1080p/24fps source has moving projected cyan inputs, aiming
emitters, amber confirmations and evolving data-ring feedback. Robot geometry,
sealed chamber edge and external display remain coherent in sampled frames.
No human anatomy or mechanical finger-hand appears. Source25–98 supplies the
74-frame lyric slot at1624–1698, with24leading and47trailing available source
frames. Later source100–145 has larger amber rings; the central edit is restrained.
Existing editorial pan and fades lead back to Harper's separate calculation.

All nine lab/ark views are native motion again. The user-rejected three-finger
take remains in history and is not used in the current cut. Eight unchanged
lab/ark chunks were reused. Canonical batch `lab-robot-motion-v01`, recipe
`storyboard-lab-robot-motion-v01.json`, provider plan
`kling-lab-robot-cutaway-v01.json`. Full5265frames, exact phrase grid,1920x1080/24fps
and original master AAC packets are preserved. Native take and edit are
agent-reviewed drafts for user playback, not marked user-approved footage.

No jobs pending. Additional confirmed48credits; cumulative2264. Source/animatic
proofs, verification and generation ledger are in
`generated/storyboard/lab-robot-motion-v01/`. The six alien habitat ship reference
is separately catalogued as v03; current exterior clips still use the old ark.

## October 10 — v31 robot-only control cutaway and alien ark reference

The user accepted the six lateral pod/field-ring ark geometry and requested
six radically different alien habitats. New still reference:
`generated/design/ark-biopods-v03/ark-biopods-design-v03.png`.
Physical pod assignment and continuity anchors are in `ARK-BIOPOD-DESIGN.md`;
exact ImageGen prompt/QA are alongside the image. The reference is catalogued
in project.json but not applied to the four native ark exterior clips yet.

The user found a three-finger defect in lab2-03's native Harper hand. Earlier
agent QA missed it. The old take is now marked user-rejected in the canonical
motion history and replaced in v31 with a robot-only still cutaway at the SAME
1624–1698 frame slot. Small ivory/graphite crab drone, two projected cyan light
manipulators, large luminous external data display and amber confirmations;
no Harper, human anatomy or physical button caps. Returns to Harper in lab2-04.
Eight other native lab/ark chunks are reused unchanged, with existing fades.

Current movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v31.mp4`.
Review:
http://127.0.0.1:8768/storyboard/lab-robot-cutaway-v01/animatic-through-bright-night.mp4 .
Local edit context:
http://127.0.0.1:8768/storyboard/lab-robot-cutaway-v01/robot-cutaway-in-context.mp4 .
Canonical batch `lab-robot-cutaway-v01`, recipe
`storyboard-lab-robot-cutaway-v01.json`. Full 5265 frames and original AAC
preserved; this revision adds no paid generations.

Prepared native replacement plan: `kling-lab-robot-cutaway-v01.json`.
One six-second 1080p take, estimated 48 credits, with brisk alternating light
taps/sweeps and responding cells. Native locked camera plus later editorial
move, 24 source-frame handles on each side. No character element binding
because Harper is absent. Exact upload still and prompt are ready for review.
The user explicitly replied “Approve replacement upload and 48 credits.” The
new take was submitted once, returned QUEUING and charged 48 credits. Confirmed
cumulative is now 2264. Task:
`AU3vEZBszj8WzP2LMjQuwJR1fgraz7WJZnRKmzAdnAQ8hoCBej-lliIMmRfaNGQbgKJnLBvs`.
Collect without resubmitting, inspect native robot/light-input motion, and insert
v32 using prepared helpers in generated/review. V31 remains the active still
preview until the native source is reviewed and v32 assembled.

## October 10 — v30: all nine lab and ark shots animated

Current full movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v30.mp4`.
Review through Bright night (81.54 seconds):
http://127.0.0.1:8768/storyboard/lab-silver-motion-v01/animatic-through-bright-night.mp4 .
Lab and ark passage:
http://127.0.0.1:8768/storyboard/lab-silver-motion-v01/lab-and-ark-passage.mp4 .

The user explicitly approved five revised silver-bikini still and prompt
uploads for 240 credits. All five were submitted once, completed and collected.
Together with the four completed ark clips, this batch cost 432 credits;
cumulative confirmed credits are 2216. No jobs remain pending. Provider request,
submission and result records remain in the two Kling output folders.

All nine shots now use native Kling motion. Five lab shots retain the silver
wardrobe and sealed tank; human hand gestures and interfaces remain inside
unbroken glass. Motion includes floating curls and bubbles, expression changes,
external caretaker arms, a restrained internal lattice response and a clearer
finger/ring manipulation. Kling introduces external service arms at the right
edge of the first close-up, consistent with the following wide caretaker view.
The concentration close-up has geometric glints across the cheek. These are
agent-reviewed drafts for user playback, not marked user-approved footage.

Lab source selections: 01 source25–70, 02 source25–52, 03 source25–98,
04 source25–69, 05 source43–61, with at least 24 source frames available
on each side. Purposeful editorial camera moves remain. The four ark chunks
are reused unchanged from v29; the starward pan breaks up consecutive hull
views. Recipe: `storyboard-lab-silver-motion-v01.json`. Canonical batch:
`lab-silver-motion-v01` in `shots/shotlist.json`.

The full edit retains 5265 frames at 24fps and 1920x1080. The developed review
contains 1957 frames, and the lab/ark passage contains 408. Original master
AAC packets and lyric boundaries are preserved; the v28 schematic-tail fade
into “Why’m I so cramped?” remains. Verification and sampled visual proofs:
`generated/storyboard/lab-silver-motion-v01/verification.json`,
`source-proof.png` and `animatic-proof.png`.

## October 10 — v29 silver wardrobe and four native ark shots

Current full movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v29.mp4`.
Review through81.54s:
http://127.0.0.1:8768/storyboard/lab-silver-v01/animatic-through-bright-night.mp4 .
Ark passage only:
http://127.0.0.1:8768/storyboard/lab-silver-v01/spacecraft-passage.mp4 .
Wardrobe still inspection:
http://127.0.0.1:8768/storyboard/lab-silver-v01/review-board.html .

The user explicitly approved nine uploads and432credits. The first original
tank request was rejected by Kling with400content-guideline error, no
generationId or charge field returned. It was not retried. Four unaffected
exterior shots were submitted with exterior-only prompts,48credits each,
completed and collected. Plan: `kling-lab-space-motion-v01.json`. All four
sources are145frames/1080p/24fps. Confirmed new charges192; cumulative1976.

Native source selection: reveal06 source25–71, dark-sky07 source46–74,
bright-star08 source86–116, bright-night09 source25–113. All retain at least
24frames each side.06 native movement is restrained, with editorial reveal;
07 has lateral travel;08 pans toward the star as the ark exits at lower-left,
providing a cosmic interlude that breaks repeated hull compositions;09 is the
tiny-ship/immense-nebula ending.08 includes two long Kling illustrated star
streaks, visible in the review. Native cameras drive07/08; editorial movement
is retained for06/09. No extra transition effect beyond existing short fades.

User then directed a SILVER BIKINI for the five lab shots.02 is a successful
wardrobe edit; original-input wardrobe edits01/03/04 were rejected by ImageGen
input safety. Fresh close views using the already clothed02 anchor succeeded,
including05. These new clothed views preserve adult identity, calm laboratory
framing, sealed tank, hand/interface inside at head level. Exact successful
and failed prompts are preserved separately in `generated/storyboard/lab-silver-v01/`.
One new identical silver-wardrobe prompt lock governs current canonical batch
`lab-silver-v01`; previous shots and actual provider payloads remain in history.

V29 contains these FIVE SILVER STILLS with editorial movement and FOUR native
exterior clips. Recipe: `storyboard-lab-silver-v01.json`. Full5265frames,
review1957frames, original master AAC hash and1920x1080/24fps verified.
The repaired v28 schematic fade is retained. New lab native plan:
`kling-lab-silver-motion-v01.json`, five six-second1080p takes,240credits
estimated, within original432cap when combined with192completed exteriors.

Automatic approval review rejected submitting the five replacement images and
prompts because those exact revised private assets were not explicitly approved
for upload. The user explicitly replied Approve five revised uploads and240credits.
All five jobs were submitted once and are running,48credits each. Current
confirmed total2216 including all432newcredits. Collect, QA and insert these
five native lab clips; the four exterior jobs are already complete. Active
review remainsv29 until completed motion QA and v30 assembly.

## October 10 — v28 schematic dissolve; lab Kling batch awaiting approval

User approved v27 and requested Kling for all nine lab stills, plus recovery of
the star-system schematic tail in a fade into “Why’m I so cramped?” The rich
schematic source contains144frames: nominal edit29–132 leaves12 trailing
frames. V28 uses source121–144 against inlet13–36 for a24frame (one-second)
fade centered at the unchanged737 lyric boundary. Patch frames725–749,
end exclusive. All12 previously unused schematic frames participate in the
overlap; no held frames or timing shifts. Master AAC hash and full5265frames
verified. Transition:
http://127.0.0.1:8768/storyboard/schematic-fade-v01/fade-review.mp4 .
Full developed sequence through81.54s:
http://127.0.0.1:8768/storyboard/schematic-fade-v01/animatic-through-bright-night.mp4 .

Exact native-motion plan: `kling-lab-motion-v01.json`, nine six-second1080p
takes,48credits each /432total estimated. First five bind established adult
Harper identity; all shots retain identical lab prompt lock and sealed-chamber
constraints. Character/robot/interface motion uses locked native cameras plus
editorial moves. Ark exteriors specify reveal, lateral travel, bright-star pan
and vast-space opening, so the bright-star pan can serve as a visual interlude
without requiring a new still. Review actual output together before choosing
trims or replacing an exterior.

Automatic approval review rejected submission because the user had requested
Kling generally but had not explicitly approved the exact nine private still
and prompt uploads with432credits. An async approval request is pending.
No CLI execution, task submissions or request manifests occurred. Do not submit
until the user explicitly approves the nine uploads and432credit batch, then
use the prepared plan once. No new charges; cumulative1784. Continue with
collection/QC and native insert after approval. V27 and its stills are retained.

## October 10 — v27 sealed chamber correction

User liked the lab verse and the coherent submarine-like ark, but rejected
Harper's arm protruding through the suddenly introduced tank aperture. V27
replaces only `lab2-03` and `lab2-04`. Her hand is now raised beside her head
inside the culture fluid, manipulating the same kind of cyan/violet geometric
interface inside the chamber. Continuous tank glass separates hand and face
from the external robot and its physical control. No human limb crosses the
tank wall. Other seven images and their prepared camera chunks are retained;
their original rendered chunks were verified byte identical before assembly.

Recipe: `storyboard-lab-verse-v02.json`; imagery and exact prompts:
`generated/storyboard/lab-verse-v02/`. Canonical shots retain v26 composition
history. The seven retained stills are user accepted; revised03/04 await review.
Shared sequence prompt lock, grid frames1550–1958, fades, lyric timing and
master audio are retained. V26 remains available. New full movie is
`generated/animatic/A-Right-Little-Something-selected-motion-v27.mp4`;
review through81.54s:
http://127.0.0.1:8768/storyboard/lab-verse-v02/animatic-through-bright-night.mp4 .
Still inspection and motion notes:
http://127.0.0.1:8768/storyboard/lab-verse-v02/review-board.html .
This revision uses built-in still generation and editorial moves only.
No new Kling job or credit charge; cumulative1784.

## October 10 — v26 headquarters origin verse

User accepted v25, then requested a still-based origin flashback through
“Bright night,” assembled with the existing opening and chorus. Nine new
built-in ImageGen compositions are registered in `shots/shotlist.json` as
`lab2-01` through `lab2-09`, batch `lab-verse-v01`. Direction and later motion
notes: `LAB-VERSE-DIRECTION.md`. Exact prompts and one identical sequence lock
are stored on the canonical shots and under the generated asset folder.

The tank hides Harper's body behind opaque graphite structure. Her face,
shoulders and hands are visible. Ivory/graphite multi-arm service machinery
tends the chamber; the control lattice becomes an irregular living response,
then she manipulates a geometric calculation. A concentration close-up leads
to the massive laboratory ark and increasingly spacious cosmic views. The
ark is separate from her small personal spacecraft. These are composition
drafts with editorial Ken Burns moves, not native character animation.

Recipe: `storyboard-lab-verse-v01.json`. Frames 1550–1958 (end exclusive),
408 frames at 24fps, follow existing phrase starts. The constraint view holds
through the 13-frame vocal gap; later space views cover the small gaps too.
Bright night ends vocally at frame1900; its image holds to the next phrase at
1958 /81.54s. Internal fades are four frames, centered on phrase boundaries.
The eight-frame entry dissolve begins at1550 using a clean outgoing orbit
plate image, avoiding doubled burned lyrics. No zoom blur or shake.

Full current movie: `generated/animatic/A-Right-Little-Something-selected-motion-v26.mp4`.
Opening-through-bright-night playback:
http://127.0.0.1:8768/storyboard/lab-verse-v01/animatic-through-bright-night.mp4 .
Still and motion-note inspection:
http://127.0.0.1:8768/storyboard/lab-verse-v01/review-board.html .
Original full5265-frame timing and master AAC packets are verified on insertion;
the shortened review is1957 frames. Generated verification and proof artifacts
are in the same lab verse folder. V25 is retained. New imagery awaits user
review before paid native motion. No new Kling jobs or credits; cumulative1784.

## October 10 — v25 speed, blur and trail balance

Working movie recipe: `revision-chorus-v05.json`; review:
http://127.0.0.1:8768/storyboard/chorus-revision-v05/ .
The user accepted the v24 footage and orbit route, then requested a slingshot
feel, motion blur/temporal sampling and a much faster bright-trail falloff with
a long faint tail. Only the final orbit effects are revised.

The passes are slightly eccentric (e=0.24). Vis-viva controls relative speed
within each loop, while smooth authored timing connects them and fits the
unchanged 108-frame travel span. Peak/slow relative speed is 2.06×. Sampled
angular momentum changes by only ~0.031% within each loop. These checks apply
to the loops, not a full multi-body itinerary or known real-world masses.

Native Cycles uses a centered 0.65-frame shutter, eight transform key samples
per output frame, 16 motion intervals and 32 ray samples. The heading is
unwrapped for shutter interpolation. The bright white-cyan core follows the
native ship; filaments and sparks are dimmer. Passage-time trail UVs keep
decay consistent when velocity changes. The 2-frame bright decay and 12-frame
faint decay are mixed 92/8%, with a 48-frame cutoff: roughly 11.4% brightness
after 5 frames and 0.54% after 24. See
[BLENDER-ORBIT-DIRECTION.md](BLENDER-ORBIT-DIRECTION.md).

Native source: `generated/storyboard/orbit-blender-v03/hybrid/orbit-hybrid.blend`.
The background plate, other v24 shots, Ken Burns moves, fades and source handles
are retained. V24 remains available. Native render and movie QA precede changing
the current media pointers. No paid generation: cumulative Kling spend 1784,
no pending jobs. Full-film verification records live in
`generated/review/chorus-revision-v05-ledger.json`.

## October 10 — v24 animated scale reveal

Current full animatic:
`generated/animatic/A-Right-Little-Something-selected-motion-v24.mp4`.
Review: http://127.0.0.1:8768/storyboard/chorus-revision-v04/ .
The user approved the v23 direction and requested a Kling replacement for
the remaining scale still, “Show you just how big you are,” at frame 854 / 35.54s.

One six-second 1080p take animates the reviewed `scale-reveal-v02.png`.
Cloud formations and light evolve, Harper moves slightly, and the ship's
platforms, equatorial band, engine ring and thin geodesic field remain coherent
in the reviewed frames. The same editorial Ken Burns opening move is retained.
Source `scale-reveal-motion-v01` is 145 native frames, 1916×1080 at 24fps,
padded to 1920 for the edit. Source frames 25–82 supply the 58-frame lyric span,
with 24 frames before and 63 after; fades consume the existing handles.

Automatic review initially rejected the external still/prompt upload and paid
charge. The user explicitly approved that exact upload and one 48-credit
animation, which was submitted once and collected. Actual charge: 48 credits;
cumulative Kling spend: 1784, no pending jobs. Prompt lock is copied identically
from the existing chorus plan. Recipe: `kling-scale-motion-v01.json`.

V24 is registered in `shots/shotlist.json`; all current media pointers select
it. Original 5265-frame timing, 24fps, 1920×1080 and master AAC packets verified.
The established v23 fades, other shots and Blender orbit remain. V23 is retained.
Native-source review: http://127.0.0.1:8768/storyboard/scale-motion-v01/ .

## October 10 — v23 fades and continuous orbital flight

Working review recipe: `revision-chorus-v03.json`; full animatic:
`generated/animatic/A-Right-Little-Something-selected-motion-v23.mp4`.
Review: http://127.0.0.1:8768/storyboard/chorus-revision-v03/ .

User chose fades as the sequence's default. Zoom blur is reserved for an actual
connected zoom between places. Fades now include inlet-to-portrait,
portrait-to-scale and scale-to-arms coverage. They are centered on the existing
grid; chorus entry remains frame 1046 / 43.54s. Ken Burns pans, the approved
portrait, walking creature, living channels and first orbit source remain.

The final orbit is rebuilt with curvature-matched broad approaches, two full
continuous loops and a smooth transfer. Its luminous history and orbital lines
decay with age, retaining the liked colors, filament lighting, sparks and bloom.
The ship departs before the end so the remaining wake can disappear. The flight
is an authored interpretation informed by NASA's gravity-assist diagrams, not
a physical trajectory solve. See [BLENDER-ORBIT-DIRECTION.md](BLENDER-ORBIT-DIRECTION.md).

Scale reveal remains a still illustration with editorial camera movement;
its animation pass is outstanding. No new paid generation. Cumulative Kling
spend remains 1736 credits, with no pending jobs. V22 is preserved for comparison.
Canonical edit and media pointers move to v23 only after frame-count, resolution,
visual transition and exact master-audio checks pass.

## October 10 — v22 purposeful pans, ecology motion and Blender flight

Current full animatic is
`generated/animatic/A-Right-Little-Something-selected-motion-v22.mp4`.
The camera reference is Ken Burns. Directional, eased image-plane pans open
from the ship onto the vast world, from Harper onto her biospheres, and from
her intervention onto the branching ecological response. The scale insertion
at 35.54s uses a fresh ImageGen illustration with a precise thin-field correction;
the opening footage is no longer reused there. The arms-wide shot stays quiet.

The foreground creature now walks across the bank with visible body travel,
stepping feet and water contact. The key wide is actual Kling animation:
downstream ripples, opening violet fronds and wading creatures. Fronds become
more saturated/opaque than the original still. Working sources are
`creature-walking-v01` and `living-channels-v01`, 145 native frames each at
24fps / 1080p. The former uses source frames 36–70, the latter 25–53;
both retain at least 24 frames of lead/tail. These are agent-reviewed drafts.

The final orbit uses the same clean Kling plate with actual Blender flight
curves and native ship geometry, two tilted flybys, planetary depth occlusion,
colored filament wakes, sparks and bloom. Both loops complete before the
edit ends. Assumed depths and approximate world-position matching remain art
direction. The separate fully native world look study is much simpler than
the painted target and is not the working background. Its editable scene
contains procedural terrain, water, clouds, atmosphere, stars and authored
star rays. See [BLENDER-ORBIT-DIRECTION.md](BLENDER-ORBIT-DIRECTION.md).

Review: http://127.0.0.1:8768/storyboard/chorus-revision-v02/ .
The working full version uses fades; a zoom-blur comparison is retained.
The canonical `activeReviewEdit` is v22, with the versioned edit proposal in
`shots/shotlist.json`. Recipe: `revision-chorus-v02.json`. V21 is preserved.
Verified 761 revision frames and 5,265 full-song frames, 24fps, 1920×1080,
identical original master AAC packets, continuous coverage and exact phrase
starts at 1046 and 1263. Frame-selection QA uses `-reinit_filter 0`: mixed
source color metadata otherwise resets FFmpeg's filter-local frame counter.

The user explicitly approved the two paid ecology uploads after automatic
review requested approval. Both are collected, 48 credits each / 96 actual;
cumulative recorded Kling spend is 1,736. No paid job remains pending.
Ledger: `generated/review/chorus-revision-v02-ledger.json`. New scale art and
its correction used built-in ImageGen; prompts and project-local paths are
saved in the recipe and `scale-field-edit-v02.json`. No Git commit or push.

## October 10 — v21 feedback and transition review

Current full animatic is
`generated/animatic/A-Right-Little-Something-selected-motion-v21.mp4`.
V20 is preserved. The portrait ends at frame 854 / 35.54s, revealing scale
with the accepted opening pullback. The mission has a restrained image-plane
push. New creature-level and wide living-channel stills break up the repeated
coast coverage at 51.12s and give “A right little something” its own reveal at
52.58s. These two compositions remain still-image drafts with camera movement.

Review fades and zoom blurs side by side at
http://127.0.0.1:8768/storyboard/chorus-revision-v01/ . V21 uses the zoom-blur
trial. Transitions are centered on the original boundaries using source
handles; the shore does not hold past the planned chorus entry. The first
orbit take stays; the last uses a new clean Kling pullback with authored route
and tiny ship animation. Both graphics share one exact curve. Kling's camera
move is gentle; the foreground also rotates. See [CHORUS-REVISION.md](CHORUS-REVISION.md).

Both previews have 761 frames. The full animatic retains 5,265 frames, 24fps,
1920×1080, and identical original master AAC packets. The canonical versioned
edit proposal is in `shots/shotlist.json`; the recipe, image prompts and
approximate world-position anchors are in `revision-chorus-v01.json`.
One paid eight-second orbit take cost 64 credits; cumulative recorded Kling
spend is 1,640. It is collected, with no paid job pending. The new ledger is
`generated/review/chorus-revision-v01-ledger.json`. No new Git commit or push.

## October 10 — v20 working motion review

Current full animatic is
`generated/animatic/A-Right-Little-Something-selected-motion-v20.mp4`.
The eight planned shots at frames 737–1549 now have Kling motion working
choices, covering 30.67–64.54s without a still gap. The coast ends at 1045,
and chorus 1 cuts in on the question at frame 1046 / 43.54s. These motion
choices are agent-reviewed drafts; user approval of the stills is preserved
separately. Master audio, 5,265 frames at 24fps, small word-timed lyrics and
earlier accepted opening/planet/hologram are retained. V11–v19 remain local.

| Song frames | Working take |
| --- | --- |
| 737–788 | inlet-v02 |
| 789–911 | starward-portrait-v01 |
| 912–1045 | vr-shore-v02 |
| 1046–1169 | chorus1-01-motion-v02 |
| 1170–1227 | chorus1-02-motion-v01 |
| 1228–1291 | chorus1-03-motion-v02 |
| 1292–1411 | chorus1-04-motion-v01 |
| 1412–1549 | chorus1-05-motion-v01 |

All 12 submitted tasks are collected: eight working takes and four retained
comparisons. Actual charge is 640 credits this run; cumulative recorded Kling
spend is 1,576. No paid task remains pending. Take IDs, prompts, bindings,
charges, source frames, native clean outputs and captured continuity images
are retained. `generated/review/kling-sequence-oct10-manifest.json` is the ledger.

Review full context at http://127.0.0.1:8768/ . Chorus comparisons are at
http://127.0.0.1:8768/storyboard/kling-chorus1-motion-v01/ ; earlier shots at
http://127.0.0.1:8768/storyboard/kling-window-coast-v01/ . Existing still boards
remain available. All new sources retain at least 24 frames / one second on
both sides of their exact edit spans. No retiming or inter-scene blur is baked
into the footage; jump-cut/zoom-blur/dissolve choice awaits editing review.

Observed limits: creature pebble engineering is subtle, so response v02 reads
more as independent ecological activity. Response v01 introduced an internal
cut when dissimilar start/end compositions were forced. Mission v01 changed
attention and added globe graphics; v02 tightened that. The inlet and coast
first attempts introduced unwanted ship/celestial subjects. Scene-only retry
prompts retained the approved landscapes, with unchanged canonical identity
text stored as metadata. See KLING-GENERATION-ORDER.md for these lessons.

Next: review v20 at 30.67–64.54s, choose/adjust the working motion, and test the
chorus transition language using the handles. The next section begins at
frame 1550 / 64.54s, “I’m just a creature of nature.” Large media remain local;
these changes are not a new Git commit or GitHub push.

## October 10 — chorus 1 still exploration

Chorus 1 begins at the question, frame 1046 / 43.54s. User selected imagery
branches B → A → B → A → A at 43.54, 48.71, 51.12, 53.79 and 58.79 seconds,
and requested ImageGen stills first without Blender blocking. See
[CHORUS-1-DIRECTION.md](CHORUS-1-DIRECTION.md) and
`storyboard-chorus1-ideas-v01.json`; canonical proposals are in the shotlist.
Five notes were added at revision 23 with the prior 11 notes preserved.
New chorus sources reserve 24-frame / one-second handles at each end.
Jump-cut/zoom-blur entry and softer overlaps remain alternatives for testing.
These proposals overlap the coast tail from frame 1046; v11 remains the current
full animatic until new images are reviewed. The separate still preview is
at http://127.0.0.1:8768/storyboard/chorus1-ideas-v01/ when built.
The imagery proceeds from living-world projections, through a small water
intervention and independent creature response, to orbital routes and echoes
across different worlds. No new Kling generation is requested.

## Shutdown checkpoint — October 9, animatic v11

The user approved the no-hand/no-window V03 portrait as the keeper and asked
to place all three new stills in the full animatic before shutting down.
V11 is current: `generated/animatic/A-Right-Little-Something-selected-motion-v11.mp4`.
Exactly 433 picture frames at 737–1169 replace the older Blender continuation
and lyric-only coast section. All 5,265 frames, 24 fps, 1920×1080 presentation,
word-timed small bottom lyrics and identical original master AAC packets are
verified. Accepted Kling opening, planet-only take at 581–632 and the rich
star-centered hologram composite at 633–736 are preserved. V10 is retained.

| Current beat | Song frames | Selected material |
| --- | --- | --- |
| space-008 | 737–788 | Static ImageGen V01 narrow alien inlet |
| space-009 | 789–911 | Keeper ImageGen V03, Harper gazing to stars, no hand/glass/hexagons; solid bottom ship rail remains |
| space-011 | 912–1169 | Static ImageGen V01 VR coast, one continuous planned scene through arms/tide/experience |

These are stills in the animatic, not clean motion. `startingFrameSelection`
and `animaticPlacement` record the user-directed stills; `reviewEdits.v11`
records the insertion from v10. `current-media.json`, `current-render.json`,
`current-opening.json` and `project.json` all point to v11. The old separate
cut at frame 854 is retired; `space-010` remains archived. FA38/V01 and rejected
V02 remain available for comparison. Listening notes stay at revision 22:
11 entries, 10 active, one deleted, none addressed; no notes were modified.

No paid generation is pending. Total recorded Kling spend remains 936 credits.
`kling-window-coast-v01.json` is prepared only, with no submitted task IDs:
4s inlet, 7s keeper portrait, 12s continuous shore, native 1080p, no audio,
no automatic cuts, minimum 12-frame handles. The gray-outfit Harper Element
`323570155312565` is bound for both character shots. Estimated cost is 184
credits at the last observed rate; verify the quotation before submission.
The lock block is identical to the canonical register. The coastal gesture
begins around source 0.5s, the tide responds around 2.8s, and the experience
holds from around 6.1s. No staged cuts, avatar growth, headset, ship or HUD.

Next session: review v11 around 30.67–48.71 seconds, then generate the three
clean takes when requested. Collect each submitted task rather than resubmitting
an uncertain outcome. Review actual motion/limbs/tide and place by exact song
frames, preserving master audio. The next unplanned scene is “Do something,”
frame 1170 / 48.71s. See [WINDOW-COAST-DIRECTION.md](WINDOW-COAST-DIRECTION.md)
for all shot reasoning and staged coastal action. Local Oct9 changes are saved
but are not a new Git commit or GitHub push. Large media stay outside Git.

Restart the notes/animatic server from the repository in PowerShell:

```powershell
$taskRoot = 'C:\Users\arneg\OneDrive\Documents\ChatGPT\music-visualization-toolkit'
Start-Process -FilePath "$taskRoot\.venv\Scripts\python.exe" -WorkingDirectory $taskRoot -WindowStyle Hidden -ArgumentList @('tools/listening_review.py', 'projects/a-right-little-something/project.json', '--port', '8768')
```

Open http://127.0.0.1:8768/ for v11 and listening notes, or
http://127.0.0.1:8768/storyboard/window-coast-v01/ for the separate still board.
If the server already responds, reuse it rather than launching another process.
Rebuild the still board with `tools/review_storyboard_stills.py`, then assemble
with `tools/insert_still_storyboard.py ... --version v11`; its repeated run
uses the recorded original v10 source. A media/hash checkpoint is stored at
`generated/review/checkpoint-2026-10-09-v11.json`. No files needed to resume
are kept only in the Codex image-generation output directory.

## Earlier October 9 records (historical)

Latest October 9 continuation: the user accepted `planet-orbit-v01` in v10.
Current portrait draft is V03 / 4FC0: the user requested an edit of FA38
removing the hand/forearm and all glass/hexagon/boundary treatment, keeping
her portrait and solid bottom ship rail. It is registered in
`space-009.startingFrameDraft`, shown in the timed still board and awaits
review. The previously approved FA38 is preserved in `startingFrameSelection`
and linked for comparison. Exact edit prompt is saved in the batch plan.
The user subsequently selected the original close-up still ending FA38.png:
`space-009-starting-frame-v01.png`, shown as “Face at the boundary / v01” in
the review page. V02 is rejected for gum-like field adhesion to her face.
The earlier timed still board used V01; keep the field independent and her face
slightly separated in any future animation. No new image or paid take was
generated for this selection.
The planet take's selection records userSelected=true and draftForReview=false; the
v10 picture/audio are unchanged. New plan `storyboard-window-coast-v01.json`
covers frames 737–1169 with three compositions: a suggested ship-free tidal
inlet for the cramped beat, one boundary close-up from 789 through 911, and
one continuous direct VR shore experience from 912 through 1169. Read
[WINDOW-COAST-DIRECTION.md](WINDOW-COAST-DIRECTION.md) for the action beats,
proposed alien life, projection scale and exact source/handle lengths.
Frame 854 is no longer a cut; old `space-010` is archived in the canonical
register. Listening notes remain revision 22 and are not changed.

Review the new ImageGen stills/timed still board at
http://127.0.0.1:8768/storyboard/window-coast-v01/ . This is explicitly three
static images held to the existing lyrics/master timing, not clean motion.
The full animatic remains v10 while these compositions await review. No paid
generations were submitted for the new batch; cumulative Kling spend remains
936 credits. Proposed eventual native 1080p take lengths are 4s, 7s and 12s.
The next unplanned scene starts at frame 1170, “Do something.”

October 9 clean planet motion: the user reviewed v09, correctly recognized
the still-image camera drift and requested appreciably more motion from Kling.
`kling-planet-cutaway-v01.json` submits one four-second native 1080p take,
`planet-orbit-v01`, with visible orbital terrain/cloud travel and distant
stars. No ship, moons, Harper or display appear in this insert. Cost is 32
credits; cumulative recorded Kling spend is now 936. The task is complete
and no paid task is pending. Animatic v10 replaces the v09 still drift with
this generated take at frames 581–632, source frames 13–64. Native source is
1916×1080, 24 fps, 97 frames, with 12 frames before and 33 after the edit.
The 1920×1080 presentation adds two-pixel side padding without upscaling or
retiming. Sampled edit frames show terrain/cloud travel against an almost
stationary star field, with mountain silhouettes and lighting retained; no
ship, Harper, moons or HUD appears. The user subsequently accepted the take;
the selection now records draftForReview=false and userSelected=true.
The accepted interior hologram, 5,265-frame full duration, small lyrics,
original master AAC packets and listening-note revision 22 are retained.
Review the full animatic at http://127.0.0.1:8768/ around 24.17 seconds; the
four-second source is at `/storyboard/kling-planet-cutaway-v01/`.
V09 preserves the still-drift comparison. Prompt lock remains identical.

Latest October 9 direction: replace `space-006` with a planet-only cutaway.
User found the short ship exterior emphasized style/continuity discontinuity.
V09 now reviews an ImageGen edit with the ship and Harper fully removed,
preserving the established turquoise world, peach clouds and distant nebula.
The editable Blender rig supplies a gentle image-plane camera drift; this is
motion blocking, not a true orbital simulation or final generated take.
Review at http://127.0.0.1:8768/ around 24.17 seconds, with small bottom lyrics.
Exactly song frames 581–632 are replaced; the accepted interior hologram at
633–736 is preserved. Full movie remains 5,265 frames at 24 fps, 1920×1080,
with identical original master AAC packets and unchanged listening notes.
Source motion is 76 frames, with 12-frame handles on each side of the edit.
Starting illustration is 1672×941, projected onto the 1080p draft canvas;
final Kling footage should still be generated natively at 1080p after review.

Plan: `planet-cutaway-v01.json`; rebuild with Blender
`--python tools/build_planet_cutaway.py -- project.json planet-cutaway-v01.json`,
encode the 76 PNGs at 24 fps, and use `tools/insert_selected_motion.py` with
`--shot space-006 --test planet-cutaway-v01 --version v09 --draft`.
The draft is explicitly unapproved in the shot register. Preserve v08 and
the superseded ship experiments for comparison. No new Kling generation has
been submitted; recorded spend remains 904 credits. The next clean prompt
should request slow orbital terrain drift, steady altitude, no ship, no moons,
no fast axial rotation or dramatic zoom; stars stay at astronomical distance.

The following October 9 ship-exterior records are historical and superseded
by this planet-only direction.

October 9 generation: `kling-world-below-v01.json` submits one four-second
native 1080p `space-006` take (32 credits), using starting image v04 with the
smaller Harper. Her gray-outfit Kling Element `323570155312565` contains the
full-body cutout plus the detailed original interior portrait. The approved
prompt reserves the cabin display entirely for a later Blender inset; no
projected star dot, hand-light gathering or hologram is requested. The prompt
lock is unchanged. Keep the full animatic on v08 until this take is reviewed.
Including this take, recorded Kling spend is 904 credits.

This take has completed. Review at
http://127.0.0.1:8768/storyboard/kling-world-below-v01/ . Native source is
1916×1080, 24 fps, 97 frames; the 52-frame edit uses source frames 13–64.
The context movie pads two pixels on each side and cuts directly into the
selected v08 interior display, retaining the song timing and bottom lyrics.
Kling deviated from the prompt: it pushes in rather than widening and adds
cyan glow near Harper's torso despite the no-display instruction. These
deviations await user review; the full animatic remains v08. No task is pending.

October 9 exterior revision: a new `space-006` Blender draft is registered in
`blockingReview`, with the camera across the bow on the other side, both moons
out of frame and the original ship altitude preserved. Harper's hand-raising
anticipation bridges into the selected interior hologram. Review:
http://127.0.0.1:8768/storyboard/world-below-v02/ . It includes one second of
preceding v08 footage and the selected display shot afterwards, with original
song frame timing and bottom lyrics. No paid generation or full-animatic
replacement has happened for this exterior. The next step is to illustrate
the reviewed composition and generate its clean motion. Build source:
`storyboard-world-below-v02.json`; editable Blender scene and renders remain
under ignored generated media. The shared world still contains both moons;
the renderer checks their complete bounds over all 76 source frames.

October 9 current local edit: animatic v08 selects the user-approved larger,
labeled hologram composite over the star-centered Kling performance.
Movie: `generated/animatic/A-Right-Little-Something-selected-motion-v08.mp4`.
Review and add listening notes at http://127.0.0.1:8768/ . It remains 5,265
frames at 24 fps and 1920×1080, with small bottom lyrics and verified identical
master AAC packets. V07 remains available. This local work is not yet a new
GitHub checkpoint.

The hologram stays at song frames 633–736. Its source trim is now 29–132,
showing all five systems while preserving a 12-frame tail. The brighter
masked v03 composite is registered in `space-007.compositeSelection` and
`reviewEdits.v08`; the base Kling take remains recorded in `motionSelection`.
See `hologram-overlay-v03.json` and [HOLOGRAM-DIRECTION.md](HOLOGRAM-DIRECTION.md).
Standalone source/previous-version review: `/storyboard/hologram-overlay-v03/`.
No paid generation was needed.

Blender blocking continues through frame 911 (37.96 seconds). The next
unplanned phrase is “Stretch your arms wide,” followed by “And change the
tide” and “How much can you do with it all?” Listening-note revision 22 and
all existing note anchors remain unchanged; collect new scene direction there.

Latest checkpoint, 2026-10-05: v07 selects the preferred `hologram-star-centered`
redo for frames 633–736. The whole system contracts together and the home star
becomes a point in the wider graph. Full movie:
`generated/animatic/A-Right-Little-Something-selected-motion-v07.mp4`.
Earlier Kling opening continues, with Blender proxy beats at 581–632 and
737–911. The small bottom lyrics and exact master AAC packets are retained;
5265 frames at 24 fps, 1920×1080 presentation. No pending paid tasks. Current
Kling spend is 872 credits; details, alternate tests and next-step reasoning
are in [HOLOGRAM-DIRECTION.md](HOLOGRAM-DIRECTION.md). Git backs up the new
notes, source plans, code and four curated hologram stills, excluding videos,
audio and Blender renders. Remaining task tomorrow: review this selected shot
in context, then continue the rest of the small batch with illustrated
references/animation when ready. Further hologram refinement is optional.

One last comparison after the selection: `hologram-star-centered` starts from
the existing system-level illustration and achieves a more coherent contraction
to a home-star point with neighboring stars. It cost 48 credits and is complete.
The user subsequently favored it, and it is now selected in v07. Nine full
resolution samples show no obvious extra limb/digit, with curled fingers and
the hidden foot limiting complete counts. V06 preserves the prior selection.

First continuation update: five new active notes were blocked in Blender as a
proposal after the checkpoint below. See [STORYBOARD-SPACE-NOTES.md](STORYBOARD-SPACE-NOTES.md)
and `/storyboard/space-notes-v01/` for the timed review. This adds a proposed
revision at frame 581 and continues through frame 911. The accepted v03 edit
source shot records remained intact. The full listening viewer temporarily selected v04,
with Blender proposals inserted at frames 581–911 and the original master
audio packets preserved. The checkpoint note snapshot below is historical; live
listening notes reached revision 22 for this continuation.

2026-10-04. The user accepted animatic v03 as a good working edit and requested
this GitHub checkpoint before continuing. Review locally at
http://127.0.0.1:8768/ (exact-frame viewer: http://127.0.0.1:8767).

## October 4 edit (historical)

`shots/shotlist.json` is authoritative. Four Kling takes cover the first
632 frames / 26.333 seconds. The full animatic has 5265 frames at 24 fps and
1920 × 1080 presentation. Current local movie:
`generated/animatic/A-Right-Little-Something-opening-motion-v03.mp4`.

| Shot | Song frames, inclusive | Current selection |
| --- | --- | --- |
| opening-001 | 1–227 | Space/planet/moons; ship enters and recedes |
| opening-002 | 228–352 | Preferred locked-camera connected-lines portrait |
| opening-003 | 353–542 | One continuous pullback across both up-above phrases |
| opening-005 | 543–632 | Floating interior, hands toward the transparent field |

The former 003/004 cut restarted nearly the same pullback and felt like a
stutter. V03 merges those notes into one take, starting with "Here in orbit
up above" and continuing through "Way up here up above". The original shot
records are preserved under `supersededShots`. Five original listening notes
remain active and unchanged, revision 9. The opening-selection panel provides
shot jumps and review notes; the listening-note anchors retain their original
positions even where the edit has changed.

There is no planned footage beyond this opening yet. The rest of the song
uses a dark review canvas with the same bottom lyrics. V01 and v02 remain
local comparison movies. Generated source clips retain at least half a second
of lead-in and lead-out; no speed changes or master-audio retiming are used.

## Creative direction to carry forward

- Continue the painterly graphic-novel look and established adult Harper:
  curly auburn hair, freckles, gray tee/trousers, bare feet, expressive floating
  performance. Artistic composition takes precedence over exact physical scale.
- Favor Kling for complete illustrated character/scene animation. Keep the
  camera fixed where depth becomes unreliable; avoid troublesome moves rather
  than imposing rigid geometry on every shot.
- Use Blender for composition planning and selective composited effects:
  light, glow, blur and coordinated effects when they improve a Kling shot.
  It remains useful, but the static illustrated actor card is not the chosen
  character-animation workflow.
- Preserve a complete equatorial metal band, upper/lower circular platforms
  and an open aft engine ring. Finish: dark satin metal, continuous amber rims,
  sparse cyan rectangular lamps and cyan engine light.
- The sphere is an ultra-thin transparent technological field, capable of
  displaying/magnifying imagery on its inside. Avoid heavy shiny refractive
  glass. Connected faint cyan geodesic lines are preferred over isolated dots.
  Stable junction dots can accompany lines; localized brightness waves are a
  useful effect reference. Small display-only rotation is optional, restrained.
- Keep two distinct distant moons: larger charcoal volcanic basalt with orange
  fissures, smaller pale icy world with blue fractures. They belong to the
  astronomical background beyond the planet surface, not beside the cabin.
  An upper-right sun motivates reflected illumination; lava may self-emit.

## What worked and what did not

Blender compositions translated surprisingly well into ImageGen starting
frames. Stable ship geometry, orientation, moon identities and appearance
references are valuable planning aids without requiring every generated pixel
to match an exact mesh.

Kling's illustrated motion and character performance were much more appealing
than the native ship plus flat actor card. The native render controlled the
ring/field correctly but was stiff and its metal finish did not exactly match
the illustrations. Keep it as an experiment, not a selected opening take.

Moon depth was poor in some moving shots: they behaved like small nearby balls.
The locked-camera lines test kept them more stable relative to the stars and
was the preferred portrait take. This is not proof that arbitrary camera moves
are solved. The remaining moving pullback still merits depth/field review.

Isolated dots were disliked and could read as stars. The requested rotating-dot
Kling test restored hexagonal lines and did not reliably produce the requested
rotation. Native Blender junctions, lines and traveling brightness worked as
motion graphics, but locking down the entire shot sacrificed the performance.
Use those effects selectively around good animation.

The first nine-second continuous test changed the spacecraft into a different
design, losing the equatorial ring and adding a barrel engine. Supplying the
approved exterior as an ending reference constrained the second take much
better; it is selected in v03. A continuous generation avoids the restart
caused by joining separately generated starting compositions.

## Lyrics and timing

The master is the audio authority. DAWproject timing is used because the song
has many linear tempo ramps; MIDI step events and starting-BPM estimates are
inadequate. The approximately 2.196 ms residual was accepted for the animatic.
Every shot/caption boundary uses the existing frame timing. Preserve the
arranged/performed spelling and typos, audible repeat counts, nine "in" onsets,
"things big now" and "all, all calling".

Default lettering is stored in `production.lyricPresentation`: Bahnschrift,
34 px on 1080p, centered near the bottom, subtle outline/shadow, pale cyan
current-word highlighting. It follows the small word-timed approach from
Monsters Undone. The words are baked into the movie; a small paused lyric readout
also keeps them readable when native player controls cover the bottom of a
small preview. `tools/lyric_overlay.py` preserves frame activation despite
ASS centisecond precision. Font files are machine-local and are not committed.

## Backup and resuming

Git includes code, plans, prompts, authored lyrics, these notes, a small JSON
checkpoint and nine curated PNG references. It excludes all audio, video,
Blender files, render sequences, font copies and bulk generated assets.
Thus this is a production-data/reference backup, not a full media archive.

`checkpoint/manifest.json` maps backed-up timing, transcription and listening
note JSON to its original local paths. `reference-images/manifest.json` maps
the selected stills to their generation-reference paths. Both record SHA-256
checksums. Restore missing files after cloning with:

    python tools/project_checkpoint.py projects/a-right-little-something/project.json --restore

The restore command verifies checksums and keeps every existing local file.
Actual master/DAWproject/video sources must be recovered from a separate media
backup. Generation IDs and prompts survive in the shotlist and plans, but
provider download links may expire. Use `project_checkpoint.py` without
`--restore` to refresh the metadata checkpoint before a later commit.

Next: review the current opening in context, add scene ideas beyond frame 632,
then plan a small next batch. Replan with `tools/shotplan.py --merge` to preserve
creative work; retain identical shared prompt locks, timing-derived frame
counts, and half-second handles. Review an animatic before buying more footage.
The latest continuous-shot tests cost 144 credits; all Kling tests and selected
opening generations so far total 584 credits. No new generation was purchased
for this checkpoint.
