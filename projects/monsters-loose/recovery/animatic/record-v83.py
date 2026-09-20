from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v83-cyclops-turbulence.mp4'
for s in d['shots']:
 if s['id'] in ['SCN-011-GROW-A','SCN-011-GROW-B']:s['status']='user_approved'
 if s['id']=='SCN-011-SMOKE-B':
  s.update(source='motion-graphics/SCENE11-SMOKE-003/smoke-b-turbulence-v001.mp4',status='motion_graphics_for_review',effects_record='motion-graphics/SCENE11-SMOKE-003/settings.json',note='Approved cloud/focus reveal plus 16 drifting local vortex displacements and fine travelling turbulence. Eases to zero by final frame3774. No visible particle sprites; timing unchanged.')
d['current_preview']=preview;d['next_scene_planning'].update(preview=preview,status='cyclops_turbulence_for_review');p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v82**','Current preview: **v83**').replace('recovery/animatic/MonstersLoose-v82-insect-impact.blend','recovery/animatic/MonstersLoose-v83-cyclops-turbulence.blend').replace('Open the current v82 Blender','Open the current v83 Blender');p.write_text('Latest v83: localized swirling displacement and fine turbulence through the Cyclops vapor reveal, settling to zero at final frame3774. Approved insect v82 and lizard effects preserved. Timing unchanged; no generation credits. Review3718. Reproducible effects: recovery/motion-graphics/SCENE11-SMOKE-003/build.py.\n\n'+s,encoding='utf-8')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
