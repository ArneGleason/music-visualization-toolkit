from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[2]
p=r/'shots/shotlist.json';backup=r/'shots/shotlist-pre-countdown-v61.json'
if not backup.exists():shutil.copy2(p,backup)
d=json.loads(p.read_text(encoding='utf-8'))
s=next(s for s in d['shots'] if s['id']=='SCN-008-COUNTDOWN-COUNT4')
s.update(source='motion-graphics/COUNTDOWN-EDIT-002/count4-timed-v001.mp4',media_type='video',status='assembled_for_review',effects_record='motion-graphics/COUNTDOWN-EDIT-002/selections.json',note='Generated cyclops tentacle down-strike, compressed to11frames; Blender contact jolt and short radial impact strokes.')
d['countdown_production'].update(preview='animatic/MonstersLoose-v61-countdown-punches.mp4',blender='animatic/MonstersLoose-v61-countdown-punches.blend',credits=312,numbers=['5','4','3','2'],number_treatment='Ten-frame large central punch, overshoot and fast exit. User explicitly excludes1.',revision_note='User requested moving arm impact instead of still four. One5second Kling take,40additional credits.')
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
