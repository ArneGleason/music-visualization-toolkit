"""Save v038 story notes without moving any frame boundary."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
src=P/'shots/rest-of-song-v024/proposal.json';backup=N/'proposal-before.json'
if not backup.exists():backup.write_text(src.read_text())
q=json.loads(backup.read_text())
changes={
'S07-SH01':('Approaching the crossing','From an oblique service-lane angle, Harper and Taffy move toward the open entrance still some distance ahead. Machinery and the guard establish the crossing; the following closer view finds them further along the approach.','Entirely different camera angle from Shot2; distant entrance and small pair with room to advance. Avoid a near-identical head-on composition with inconsistent door scale.'),
'S08-SH01':('Together, then','In the remote dark salvage nook Harper offers the fake jewel; the scrapper studies it with recognition while Taffy watches. His four separate arms remain anatomically clear, two per side.','Preserve accepted dark trade setup; use approved scrapper identity and S08SH02 anatomy, exactly four arms.'),
'S09-SH02':('Lucky to find this','Harper and Taffy look around the old cabin, examining its fittings by portable light. Their delight comes from discovering the ship and its possibilities, not from handling the regulator.','Cabin exploration with useful space and existing fittings; no cartridge handling or installation.'),
'S09-SH03':('A fine find together','They explore the cockpit and adjoining cabin. Harper tries the feel of the dormant flight controls while Taffy looks around with growing enthusiasm; they share their good fortune.','Change viewpoint and body poses from Shot2. Two side-by-side seats; unpowered cockpit and portable illumination. No cartridge repair.'),
'S09-SH04':('True?','A quick curious glance at an old cockpit gauge or control: a small discovery beat as they size up their lucky find.','Brief close exploration/reaction insert, no loose regulator connector or repair failure.'),
'S09-SH05':('A little higher','Harper reaches toward an overhead ventilation latch or inspection cover. Taffy raises their portable light a little higher to help her see.','Different task from cartridge repair; natural supported reach, coherent cabin geography.'),
'S09-SH06':('On the upbeat','Now introduce the regulator for the first time: they steady it at the repair bay and try a few coordinated taps on its sticky locking collar. On the final tap it starts to slip.','Retain existing frame. This is the first cartridge-handling beat, leading directly to its loss, rather than the end of a long installation sequence.'),
'S10-SH01':('No retrieving that','The closing maintenance door slams on the trapped regulator, buckling its casing and destroying its connector. Harper and Taffy recoil, see it is ruined and decide to find a replacement. They are alone; the scrapper is not present.','Remove scrapper from background only. Preserve closing door, trapped part and partners. Next shot establishes the unattended donor vehicle.'),
'S13-SH04':('The compromise fails','The substitute starts to malfunction and the warning returns. Taffy turns his attention back to the device while Harper reacts at the controls; thrust falters and the descent begins.','Retain accepted wide frame showing both actors and the module.'),
'S14-SH01':('A sliding landing','The ship hurtles down, makes hard ground contact and skids for a considerable distance under its remaining momentum. Cut to the interior while it is still sliding, before the final impact or breakthrough is shown explicitly.','Retain accepted higher approach starter. Use lead-in for descent, then fast ground slide. Do not force a visible cave collapse into this short exterior shot.'),
'S14-SH02':('Still together','Carry the sliding vibration into the dusty cabin; the final jolt and dust can imply the impact and breakthrough off screen. Taffy is slumped with eyes closed. Harper shoves his shoulder and he stirs; both have survived. The next wide shot reveals where they came to rest.','Retain accepted starter. Stage the rousing beat after the final jolt; preserve the wreck orientation established by Shot3.')}
for s in q['shots']:
 if s['id'] in changes:
  s['title'],s['action'],s['camera']=changes[s['id']];s['reviewOverlay']=s['action']
 s['status']='starter_review_v038'
for s in q['scenes']:
 if s['id']=='S09':s['purpose']='Explore the lucky find together, then a brief first repair attempt loses the needed part.'
q['status']='starter_review_v038';q['note']='v038: different approach angle, scrapper anatomy, ship exploration before brief cartridge handling, partners alone at crush, retained slide/crash direction. 39shots, timing unchanged.'
assert [(x['startFrame'],x['endFrameExclusive']) for x in q['shots']]==[(x['startFrame'],x['endFrameExclusive']) for x in json.loads(backup.read_text())['shots']]
assert len(q['shots'])==39 and sum(x['frames'] for x in q['shots'])==3234
for f in [src,N/'proposal.json']:f.write_text(json.dumps(q,indent=2)+'\n')
lines=['# Scene and shot directions v038','','39 planned shots, all v037 timing retained. These notes capture user review; detailed motion direction will be refined next. No Kling generation or animatic rebuild.','','## Review decisions','','- Revised images: S07SH01, S08SH01, S09SH02–05, S10SH01.','- S09SH06 first introduces cartridge handling; SH07 loses it; S10SH01 crushes it with only the partners present.','- Retain the current S12SH07 demolition reference match and SH07B cockpit prep. User described the revised reference match as better; no revert requested.','- S13SH04: Taffy turns attention back to the malfunctioning module.','- S14SH01: ground contact and sustained slide; cut to interior before explicit final crash/breakthrough. SH03 reveals the resting wreck and subterranean setting.','- Mechanical reference remains archived v036/S09-SH05.png, even though current S09SH05 now depicts an overhead task.','','## Shot directions','']
for scene in q['scenes']:
 lines += ['## '+scene['id']+' · '+scene['name'],'',scene['purpose'],'']
 for s in q['shots']:
  if s['sceneId']!=scene['id']:continue
  lines += ['### '+s['id']+' · '+s['title'],'',f"Frames {s['startFrame']}–{s['endFrameExclusive']} · {s['frames']}f / {s['frames']/24:.3f}s · {', '.join(s['indexes'])}",'',s['action'],'','Framing: '+s['camera'],'']
(N/'scene-and-shot-directions.md').write_text('\n'.join(lines)+'\n')
print('39 shots; all boundaries unchanged; direction notes saved.')
