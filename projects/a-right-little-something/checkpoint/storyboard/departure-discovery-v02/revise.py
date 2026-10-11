"""Register the user's front-facing departure correction and reuse exact timing."""
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image

OUT=Path(__file__).resolve().parent
OLD=OUT.with_name('departure-discovery-v01')
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v51'
shot=next(s for s in register['storyboardProposals'] if s['id']=='departure-002')
prompt=(OUT/'undocking.prompt.txt').read_text(encoding='utf-8')
assert shot['promptLock'] in prompt
image=(OUT/'undocking.png').relative_to(BASE).as_posix()
shot['description']='Exterior from open space looking back toward the berth. The ship is already clear and turned toward camera, with Harper visibly inside at the controls. Station and disconnected gantry recede behind it in depth. Camera retreats into the bigger sky until the station becomes a tiny point.'
shot['motionDirection']='Ship departs gently toward camera in depth, not sideways past a parallel gantry. Keep compact personal-craft scale grounded by visible Harper. Slight three-quarter angle keeps the aft ring behind and clear of her. Camera provides the large pullback; native action still pending.'
shot['imagePrompt']=prompt
shot['storyboardSegments'][0]['image']=image
with Image.open(OUT/'undocking.png') as im:
    shot['startingFrameDraft'].update(id='departure-v02-undocking',image=image,nativeWidth=im.width,nativeHeight=im.height,userSelected=False)
shot['startingFrameSelection']=copy.deepcopy(shot['startingFrameDraft'])
save(BASE/'shots/shotlist.json',register)
save(OUT/'undocking.actual-generation.json',dict(tool='built-in ImageGen',attempts=1,source='C:/Users/arneg/.codex/generated_images/01a12b1a-e36e-7740-980d-0dfad1557d1f/exec-90ff0933-5c7a-432a-9eb6-23cb5f9b9ea5.png',sha256=hashlib.sha256((OUT/'undocking.png').read_bytes()).hexdigest(),qa='Harper visible; station behind at smaller apparent scale; sphere presented front three-quarter. Sphere is about 77% of image height rather than requested 48%, but depth separates station and craft.'))
options=read(OLD/'review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v51.mp4',continuationNotes='V52 replaces departure-002 first still with a front three-quarter view, visible Harper and station receding behind. Exact V51 timing retained. No Kling spending.')
save(OUT/'review-options.json',options)
timing=read(OLD/'timing-check.json')
timing['segments']=[seg for s in register['storyboardProposals'] if s.get('batch')=='departure-discovery-v01' for seg in s['storyboardSegments']]
save(OUT/'timing-check.json',timing)
(OUT/'build.py').write_text((OLD/'build.py').read_text(encoding='utf-8').replace('selected-motion-v50.mp4','selected-motion-v51.mp4'),encoding='utf-8')
finish=(OLD/'finish.py').read_text(encoding='utf-8').replace('V51','V52').replace('v51','v52').replace('equal to V50','equal to V51').replace('departure-discovery-v01/board/index.html','departure-discovery-v02/board/index.html')
finish=finish.replace("'Selected text plan; stills and motion not generated.'","'Generated stills timed in V51; user review pending. Native action not yet generated.'")
finish=finish.replace("note['resolution']=shots[sid]['motionReview']['notes']", "note['resolution']=shots[sid]['motionReview']['notes']\n        if sid=='departure-002':\n            note['text']='Departure / Bigger sky: forward departure with Harper\\n\\n'+shots[sid]['description']+'\\nStaging: '+shots[sid]['motionDirection']+'\\nFrames 2665–2805; V52 still preview, review pending.'")
(OUT/'finish.py').write_text(finish,encoding='utf-8')
gallery=read(OLD/'gallery-manifest.json')
for item in gallery:
    if item['id']=='undocking':
        item.update(src='../undocking.png',prompt=prompt,title='Toward camera — Harper aboard, station behind')
    else:
        item['src']='../../departure-discovery-v01/'+item['output']
save(OUT/'gallery-manifest.json',gallery)
save(OUT/'gallery-options.json',read(OLD/'gallery-options.json'))
(OUT/'board').mkdir(exist_ok=True)
print('Registered departure correction; V51 timing preserved')
