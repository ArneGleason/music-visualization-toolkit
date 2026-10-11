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
assert register['activeReviewEdit']=='v53'
shot=next(s for s in register['storyboardProposals'] if s['id']=='departure-002')
prompt=(OUT/'undocking.prompt.txt').read_text(encoding='utf-8')
assert shot['promptLock'] in prompt
image=(OUT/'undocking.png').relative_to(BASE).as_posix()
shot['description']='Exterior from open space looking back toward the berth. The ship is already clear and turned toward camera, with Harper at the user-preferred larger scale, visibly floating weightless inside in her gray long-sleeved coverall, both complete shoes and her whole body clear of the metal band. Station and disconnected gantry recede behind it in depth. Camera retreats into the bigger sky until the station becomes a tiny point.'
shot['motionDirection']='Ship departs gently toward camera in depth, not sideways past a parallel gantry. Keep exactly one outer equatorial structural band and no internal cockpit ring or railing. Preserve entry point, single aft engine ring and upper/lower technical plates from the original empty-ship reference. Harper floats gently with bent knees, never standing; preserve both complete shoes with clearance above the band. Slight three-quarter angle keeps the aft ring behind and clear of her. Camera provides the large pullback; native action still pending.'
shot['imagePrompt']=prompt
shot['referenceRole']='Ship continuity reference for matching the intro; user-selected ship design, larger Harper adjustment pending review'
register.setdefault('continuityReferences',{})['personalSphereShip']={'id':'sphere-ship-continuity-v01','image':image,'geometrySource':'generated/storyboard/departure-discovery-v01/undocking.png','scaleSource':'generated/storyboard/departure-discovery-v04/larger-harper-scale-source.png','boardItemId':'departure-v04-undocking','userSelectedDesign':True,'useFor':'Match selected intro shots to the middle-sequence ship design when that revision is undertaken.','invariants':['Single outer equatorial band; no internal cockpit ring','One aft engine ring and entry port','Original upper/lower technical plates and transparent cyan-grid sphere','Larger adult Harper scale, floating rather than standing'],'scope':'Reference saved now; intro footage not revised in this turn.'}
register['departureDiscoverySequence']['shipContinuityReference']='sphere-ship-continuity-v01'
shot['storyboardSegments'][0]['image']=image
with Image.open(OUT/'undocking.png') as im:
    shot['startingFrameDraft'].update(id='departure-v04-undocking',image=image,nativeWidth=im.width,nativeHeight=im.height,userSelected=False)
shot['startingFrameSelection']=copy.deepcopy(shot['startingFrameDraft'])
save(BASE/'shots/shotlist.json',register)
save(OUT/'undocking.actual-generation.json',dict(tool='built-in ImageGen',attempts=1,source='C:/Users/arneg/.codex/generated_images/01a12b1a-e36e-7740-980d-0dfad1557d1f/exec-e84f2fc8-8059-422f-9490-aa9b313e0916.png',sha256=hashlib.sha256((OUT/'undocking.png').read_bytes()).hexdigest(),qa='Larger head and torso scale restored from the user-preferred first floating draft; both knees tucked and shoes visible. Ship geometry retained.'))
options=read(OLD/'review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v53.mp4',continuationNotes='V54 restores larger floating Harper and marks this ship design as the continuity reference for future intro matching. V53 timing unchanged. No Kling spending.')
save(OUT/'review-options.json',options)
timing=read(OLD/'timing-check.json')
timing['segments']=[seg for s in register['storyboardProposals'] if s.get('batch')=='departure-discovery-v01' for seg in s['storyboardSegments']]
save(OUT/'timing-check.json',timing)
(OUT/'build.py').write_text((OLD/'build.py').read_text(encoding='utf-8').replace('selected-motion-v50.mp4','selected-motion-v53.mp4'),encoding='utf-8')
finish=(OLD/'finish.py').read_text(encoding='utf-8').replace('V51','V54').replace('v51','v54').replace('equal to V50','equal to V53').replace('departure-discovery-v01/board/index.html','departure-discovery-v04/board/index.html')
finish=finish.replace("'Selected text plan; stills and motion not generated.'","'Generated stills timed in V53; user review pending. Native action not yet generated.'")
finish=finish.replace("note['resolution']=shots[sid]['motionReview']['notes']", "note['resolution']=shots[sid]['motionReview']['notes']\n        if sid=='departure-002':\n            note['text']='Departure / Bigger sky: forward departure with Harper\\n\\n'+shots[sid]['description']+'\\nStaging: '+shots[sid]['motionDirection']+'\\nFrames 2665–2805; V54 still preview, review pending.'")
(OUT/'finish.py').write_text(finish,encoding='utf-8')
gallery=read(OLD/'gallery-manifest.json')
for item in gallery:
    if item['id']=='undocking':
        item.update(src='../undocking.png',prompt=prompt,title='SHIP CONTINUITY REFERENCE — larger floating Harper')
    else:
        item['src']='../../departure-discovery-v01/'+item['output']
save(OUT/'gallery-manifest.json',gallery)
save(OUT/'gallery-options.json',{**read(OLD/'gallery-options.json'),'title':'Departure and jungle discovery — V54 stills'})
(OUT/'board').mkdir(exist_ok=True)
print('Registered departure correction; V51 timing preserved')
