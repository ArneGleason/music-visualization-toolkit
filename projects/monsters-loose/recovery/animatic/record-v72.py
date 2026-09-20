from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v72-scientist-corrected.mp4'
for s in d['shots']:
 if s['id']=='SCN-010-PRIVATE-PLAN':s.update(source='assets/ANCH-010-A-v002.png',note='Covertly exits laboratory, natural left hand on door; metal right hand at his side. Three-quarter front view makes laterality clear.',status='revised_storyboard_for_review')
 if s['id']=='SCN-010-UNLOCK-ZOO':s.update(source='assets/ANCH-010-B-v002.png',note='Right mechanical hand operates gate lever, natural left holds notebook. Front view with uninterrupted shoulder-to-hand anatomy.',status='revised_storyboard_for_review')
d['current_preview']=preview;d['next_scene_planning'].update(preview=preview,status='revised_storyboards_corrected_right_prosthetic',prompt_record='shots/SCN-010-revised-prompts.json');p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v71**','Current preview: **v72**').replace('recovery/animatic/MonstersLoose-v71-scientist-secret-storyboard.blend','recovery/animatic/MonstersLoose-v72-scientist-corrected.blend').replace('Open the current v71 Blender','Open the current v72 Blender')
s='Latest v72: regenerated Scene10 anchors. A-v002: covert laboratory exit. B-v002: gate release. Both show metal RIGHT hand and natural LEFT, replacing rejected switched/backward hands. Same3223..3379 timing; references only, awaiting animation direction. Built-in image generation, no Kling credits. Prompts: recovery/shots/SCN-010-revised-prompts.json. Review3223.\n\n'+s;p.write_text(s,encoding='utf-8')
