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
