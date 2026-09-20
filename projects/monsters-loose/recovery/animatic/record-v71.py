from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v71-scientist-secret-storyboard.mp4'
for s in d['shots']:
 if s['id'].startswith('SCN-009'):s.update(status='user_approved',approval_note='User approved completed v70 sequence: Awesome. That is fabulous.')
for id,a,b,asset,note in [('SCN-010-PRIVATE-PLAN',3223,3301,'ANCH-010-A-v001.png','Scientist slips away to master enclosure controls; looks back as he opens cabinet.'),('SCN-010-UNLOCK-ZOO',3301,3379,'ANCH-010-B-v001.png','Mechanical hand draws master release lever; warning lamps and enclosure opening. Provisional hardware differs from companion frame; match when developing final shots.')]:
 if not any(s['id']==id for s in d['shots']):d['shots'].append(dict(id=id,start_frame=a,end_frame_exclusive=b,source='assets/'+asset,source_in_frame=0,media_type='image',status='storyboard_for_review',note=note))
d['scene9_production']=dict(d['next_scene_planning'],status='user_approved')
d['next_scene_planning']=dict(scene='SCN-010',start_frame=3223,end_frame_exclusive=3379,duration_frames=156,preview=preview,status='storyboard_for_shot_planning',credits=0)
d['current_preview']=preview;p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v70**, through master frame3222','Current preview: **v71**, through master frame3378').replace('recovery/animatic/MonstersLoose-v70-scene9-performances.blend','recovery/animatic/MonstersLoose-v71-scientist-secret-storyboard.blend').replace('Open the current v70 Blender','Open the current v71 Blender')
s='Latest v71: preview extended through Scene10, The Scientist\'s Secret, frames3223..3379 exclusive (156frames /6.5seconds). Existing storyboards: private plan3223..3301, unlock zoo3301..3379. Music/lyrics retained. Provisional control hardware needs matching during shot development. No new generated footage or credits. User approved v70 Scene9. Review3200 for lead-in.\n\n'+s;p.write_text(s,encoding='utf-8')
