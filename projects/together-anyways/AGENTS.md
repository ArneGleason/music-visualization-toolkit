# Continuing Together Anyways

Read `CONTINUE-HERE.md` before continuing production. `project.json` and
`timeline.json` use project-relative paths. Large media live in ignored
`generated/` directories and travel through the immutable GitHub Release named
in `media-manifest.json`; a Git pull alone does not restore those files.

Restore with `python3 tools/project_media.py restore projects/together-anyways/media-manifest.json`
from the repository root. Do not overwrite local differences without saving them.
Keep accepted timing, previous artwork, review caveats and rejected variants.
Before a machine switch, publish both authored changes and a new media snapshot.

## Character scale references

Use `character-development/supporting-refs-v004/height-register.json` for the
supporting cast's proposed heights and calibration landmarks. Heights remain
proposals until the user approves them. Preserve character identity and subtle
biological traits when changing body proportions or clothing.

Keep clean artwork separately from presentation plates. Add a left-margin
centimeter ruler outside the artwork, with 10 cm ticks, numbers every 50 cm,
and a clearly labeled standing-height marker. Add these graphics deterministically,
not through ImageGen. Standing height excludes hair, hats and carried equipment;
use the messenger's natural digitigrade stance. Posed stature is approximate:
record any stoop/lean allowance rather than claiming the pose measures standing
height. Build group lineups at one shared scale and ground level. The reusable
builder is `tools/cast_references.py`; the register keeps all scale assumptions.

Taffy identity: use `generated/character-development/taffy-front-back-v006.png` directly for future shots. Preserve his portly belly, broad soft torso, full cheeks and large projecting rounded ears. Shot ta-002 v001 drifted slimmer and is superseded by v002; never use that old shot as Taffy's identity authority.

Hand anatomy: humanoid hands have four fingers plus one thumb (five digits total), including the broker. Audit prominent palms and grips before selecting starters. Do not count normally occluded digits as missing, and preserve established subtle biology such as a bifid thumb tip rather than inventing extra whole digits.

Current news direction: the relay news is already playing from Scene5. Use a consistent presenter with a distant elevated surveillance inset of the depot theft, tiny indistinct faces, no recognizable wanted portraits. The partners recognize the event; bystanders cannot instantly identify them.

Adjacent-shot review: compare consecutive cuts containing the same character. Preserve identity but do not copy the same head tilt, facial expression, shoulder angle and body pose into a changed background/composition. Flag the perceptual reset caused by repeated poses; revise the second frame to advance action, gaze, orientation or camera relationship while maintaining screen direction. Intentional cut-ins and justified match cuts are exceptions; a wider change of scale alone is not automatically a defect. Review at playback speed as well as side by side.

Opening geography: begin with a broad high-atmosphere desert-region view (no prominent planet curvature), showing settlement, linked roads and mining/industrial areas. Reuse its recognisable geography/altitude for the later ship climb, failure and return; do not invent the failure cause yet.

Access device continuity: user clarified the horseshoe device is a proximity credential, not a mechanical insertion key. Use ta-013 (Scene2 Shot7) as the device design and hand-relative scale reference; do not force its grip onto a different arm. Anatomically correct wrist/hand and secure grasp take priority; see shots/access-device-reference.txt. Present it near the shaped backward-C jamb receiver from ta-019 with a visible air gap. Preserve the ivory grip, asymmetric metallic casing and red inset; do not shrink it into a belt buckle.

Illustration consistency: user selected ta-003 (Scene1 Shot4, first-run-starters-v003) as the rendering-style reference: realistic illustrated faces, dimensional shading and material detail. Avoid a shift toward cartoon/princess-like facial proportions or simplified cel shading, especially Harper in close views. Maintain each shot’s acting and camera angle rather than copying the reference pose.

Motion direction: user rejected ambient micro-movement as the default for this caper. Most shots need a readable objective, physical action, reaction and changed end pose/position at natural speed. Reserve lingering for motivated beats. Put the primary action inside the musical edit, not only in discarded handles. Camera movement supports actor intent; it cannot substitute for story action. Review motion at speed and adjacent cuts, not only sample frames. Keep each video prompt confined to its current action, avoiding future plot context that may be enacted prematurely.

Broker/companion dynamic: user wants the single shoulder companion to be the brains, quietly whispering instructions; the broker provides muscle, charisma and intimidation. Show cause and effect (whisper → boss order → minion reaction), not merely two characters looking at one another. New S01SH04 replaces the partners' planning two-shot; S01SH07 remains the later wider guard-blocking shot.

Transition review: prefer considering a crossfade for elapsed time or major scene/location changes; use short fades when pace matters, and direct cuts for continuous action. User-approved trials use12frames for full and6frames for quick fades at24fps. Preserve musical timing and selected source starts; use actual source handles, never freeze missing handles.

Approved scrapper identity: use `generated/world-development/port-ship-v031/scrapper.png` directly. Kind ant-like head with small beak, compound eyes, antennae, four arms and two bare clawed legs; tarnished metallic-knit sleeveless top and separate worn teal wrap skirt (no pants), canvas belt with three advanced powered repair tools. Preserve this six-limb biology and wardrobe; earlier human/reptilian and knitted-shorts versions are superseded. Height164cm excludes antennae and remains a design-scale proposal.

Approved ship identity: Harrier motorhome v035 exteriors (`generated/world-development/port-ship-v035/ship-front.png`, `ship-rear.png`) with v034 interiors (`cabin-forward.png`, `cockpit-reverse.png`, `cabin-grounded.png`). Preserve swollen ivory/teal hull, short wings, single fin, paired intakes, four side vector nozzles, side-by-side cockpit, snub nose forming fixed recessed forward radar bowl, and three missing machinery covers. Use unpowered grounded lighting for hidden salvage scenes. Earlier pre-Harrier ship art is historical, not geometry authority.

Remainder story direction (v037 review): scrapper hideaway is a remote, dark, unpatrolled rear salvage recess, not an exposed security walkway. Donor mechanic is a separate ordinary worker leaving an open donor vehicle; scrapper is not the person the partners hide from. Preserve the archived v036 S09SH05 repair housing through installation and failure (current v038 S09SH05 is now an overhead exploration task). Cartridge must be trapped and visibly crushed by a powered closing mechanism, not merely dropped. No cushion/comfort-object business in S11SH05.

Port sabotage: the scrapper's previously planted maintenance helper assists Harper through the infrastructure. Taffy is lookout; Harper's “Don't turn it off” addresses the system, not Taffy reaching for a plug. Keep the clearance-trigger circuit live. Use the v037 directions for the added cockpit preparation cut and wider failure reaction.

Ending: crash near the mine breaks into an ancestral underground city of the scrapper's beaked ant species. A monumental ancient four-armed beaked-ant statue establishes that link. Taffy shines a flashlight up; surrounding dormant systems begin to activate. Keep the purpose unresolved. Match approach, resting wreck and portal geography across S14; preserve actual aircraft intake versus entry door.

Scene9 pacing (v038): Shots2–4 explore the ship, Shot5 is a separate overhead inspection/lighting task, Shot6 first introduces regulator handling and Shot7 loses it. Do not restore the long cartridge installation sequence. Scrapper is absent from S10SH01 crushing; only Harper and Taffy witness it. Scene14 direction: approach, ground contact and sustained slide; cut inside before explicit final impact/breakthrough, reveal resting underground wreck in Shot3.

Direction pass v039: Scene9 local control lamps can wake on True, before full ship startup in S10SH05. Original cartridge is pried loose in S09SH06 and lost; Taffy's attempted release switch crushes it in S10SH01. S11SH03B supplies a visible troubled reaction after the arrest. Onboard planning is S11SH06 at a horizontal tabletop, composition distinct from port terminals. S12SH04 introduces guard suspicion and Taffy's warning, SH05 covert withdrawal. Proposed wipes into S10SH02, S10SH04 and S12SH01 distinguish omitted travel. See v039 full acting/direction notes.

S12SH04 direction refinement v040: the guard initially faces their general direction but has NOT noticed them; turns and wanders away on another route. Taffy notices him and warns Harper. Avoid sustained eye contact, suspicion, pursuit or confrontation.

Camera direction (Scene8 v048 approval): user prefers more purposeful camera travel, especially in longer-duration shots. Alternate fixed compositions with motivated dolly, lateral, boom or tilt moves when useful; tie movement to exploration, action and attention rather than continuous generic drift. Preserve expressive acting and clear objectives as the primary storytelling. Retain established likeness; avoid gratuitous reverse-angle face reconstruction.
