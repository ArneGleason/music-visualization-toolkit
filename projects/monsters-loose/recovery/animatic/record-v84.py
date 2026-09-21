from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v84-next-scene-storyboard.mp4'
new=json.loads((r/'animatic/scene12-storyboard-records.json').read_text())
for s in new:s['source']=s['source'].replace('animatic/../','')
d['shots']=[s for s in d['shots'] if not s['id'].startswith('SCN-012-')]+new
d['scene11_production']=d['next_scene_planning']
d['next_scene_planning']={'scene':12,'title':'No way! Yes way!','start_frame':3775,'end_frame_exclusive':4126,'duration_frames':351,'status':'storyboard_for_review','preview':preview,'note':'Existing two storyboard anchors exposed for collaborative shot planning. No new generated footage.'}
d['current_preview']=preview
d['production_priority']='Flesh out remaining scenes first; defer fixes including kid eye-roll until later, subject to remaining generation credits.'
p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'shots/SCN-006-kid-eyeroll.md';p.write_text(p.read_text()+'\n## September20 resumed production\nKeep the nice-looking existing take as a placeholder. Eye-roll action remains earmarked for the later fixes pass; flesh out all remaining scenes before spending remaining credits on revisions.\n')
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v83**','Current preview: **v84**').replace('recovery/animatic/MonstersLoose-v83-cyclops-turbulence.blend','recovery/animatic/MonstersLoose-v84-next-scene-storyboard.blend').replace('Open the current v83 Blender','Open the current v84 Blender');p.write_text('Latest v84: Scene12 storyboard extension, frames3775..4125 (14.625seconds). Two existing anchors: keeper/child exchange, then escape as spectacle. Approved footage through3774 preserved. Flesh out remaining scenes before deferred fixes; kid eye-roll remains a placeholder. No new generation credits.\n\n'+s,encoding='utf-8')
p=Path('projects/monsters-loose/HANDOFF.md');p.write_text('# Current working state\n\nv84 extends the approved v83 edit through Scene12 as a two-shot storyboard, ending4125. Next step: review and choreograph the keeper/child exchange and escape spectacle. Scenes through11 remain approved. Defer kid eye-roll and other fixes until the remaining video is fleshed out, then prioritize by available credits. Media remains external; see inventory.json.\n')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
