from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913')
p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v82-insect-impact.mp4'
for s in d['shots']:
 if s['id'] in ['SCN-011-SHRINK-B','SCN-011-SMOKE-B']:s['status']='user_approved'
 if s['id'] in ['SCN-011-GROW-A','SCN-011-GROW-B']:
  name=s['id'].replace('SCN-011-','').lower()
  s.update(source=f'motion-graphics/SCENE11-INSECT-002/{name}-polished-v001.mp4',status='motion_graphics_for_review',effects_record='motion-graphics/SCENE11-INSECT-002/settings.json',note='Stronger rapid growth zoom blur carries 27 frames across cut; 43 percent local expansion and 11 percent push inside; amplified beam recoil, 110 dust puffs and 80 debris flecks outside. Timing unchanged.')
d['current_preview']=preview;d['next_scene_planning'].update(preview=preview,status='insect_motion_graphics_revision_for_review');p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v81**','Current preview: **v82**').replace('recovery/animatic/MonstersLoose-v81-transformation-polish.blend','recovery/animatic/MonstersLoose-v82-insect-impact.blend').replace('Open the current v81 Blender','Open the current v82 Blender');p.write_text('Latest v82: stronger insect rapid-growth blur continuing across the cut, amplified enclosure recoil, dust and debris. Approved lizard roar and Cyclops reveal preserved. No generation credits; shot timing unchanged. Review from frame3508. Reproducible effects: recovery/motion-graphics/SCENE11-INSECT-002/build.py.\n\n'+s,encoding='utf-8')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
