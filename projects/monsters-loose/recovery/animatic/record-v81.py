from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v81-transformation-polish.mp4'
notes={'SHRINK-B':'Tracked19px roar refraction starts3492, full strength3494 through3514.','GROW-A':'Soft localized32percent expansion plus6.5percent anchored push reinforces growth; no hard cutout.','GROW-B':'Localized beam/mesh impact shakes, amber dust and falling grit at five collapse beats.','SMOKE-B':'Cloud hold and localized18px blur fading to original sharpness on final frame3774; softens abrupt creature appearance.'}
for s in d['shots']:
 name=s['id'].replace('SCN-011-','')
 if s['id'].startswith('SCN-011') and name in notes:
  s['pre_polish_source']=s['source'];s.update(source=f'motion-graphics/SCENE11-POLISH-001/{name.lower()}-polished-v001.mp4',status='motion_graphics_for_review',effects_record='motion-graphics/SCENE11-POLISH-001/settings.json',note=notes[name])
d['current_preview']=preview;d['next_scene_planning'].update(preview=preview,status='motion_graphics_polish_for_review');p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v80**','Current preview: **v81**').replace('recovery/animatic/MonstersLoose-v80-vapor-cyclops.blend','recovery/animatic/MonstersLoose-v81-transformation-polish.blend').replace('Open the current v80 Blender','Open the current v81 Blender');p.write_text('Latest v81: motion polish only, no generation credits. Tiny-lizard roar full by3494; insect local growth expansion/push; localized collapse recoil/dust/grit; Cyclops cloud/blur reveal sharp on3774. Timings unchanged. Reproducible video effects in recovery/motion-graphics/SCENE11-POLISH-001/build.py (NumPy/SciPy/Pillow), assembled in Blender. Review3488.\n\n'+s,encoding='utf-8')
