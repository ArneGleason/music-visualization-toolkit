"""Replace the rejected sun approach with the user's escape setup at fixed frames."""
import copy
import json
from pathlib import Path
import shutil

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
register_path=PROJECT/'shots/shotlist.json'
register=load(register_path)
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='robot-ship-so-bright-motion-v01']
assert len(shots)==9
save(OUT/'pre-escape-shot-snapshot.json',shots)
grid={s['id']:(s['startFrame'],s['endFrameExclusive'],s['frames']) for s in shots}
lock=shots[0]['promptLock']
lock=lock.replace('Maintain the original modest portrait framing and opaque tank armor, no added body exposure.',
    'In tank shots maintain the original modest portrait framing and opaque tank armor. In escape-approach shots use modest upper-body framing and the same silver top.')
lock=lock.replace('The chamber stays sealed; human hands, forearms and virtual interfaces remain inside culture fluid behind uninterrupted upper glass, at head level.',
    'In growth-tank shots the chamber stays sealed; human hands, forearms and virtual interfaces remain inside culture fluid behind uninterrupted upper glass, at head level. In escape-approach shots Harper is outside the chamber in a graphite service passage, approaching a bright compact-craft boarding hatch; no tank or fluid around her. The pod exterior design is unresolved until the departure scene.')
for shot in shots:
    shot['batch']='escape-approach-v01'
    shot['promptLock']=lock
    if shot['id']!='lab2-08':
        shutil.copy2(PROJECT/'generated/storyboard/robot-ship-so-bright-motion-v01'/(shot['id']+'.mp4'),OUT/(shot['id']+'.mp4'))
shot=next(s for s in shots if s['id']=='lab2-08')
shot.setdefault('directionHistory',[]).append({k:copy.deepcopy(shot[k]) for k in
    ['description','imagePrompt','startingFrameDraft','motionSelection','cameraMove','motionDirection'] if k in shot})
prior=copy.deepcopy(shot['motionSelection'])
prior.update(userSelected=False,status='User rejected collision-course/too-close-to-sun impression; scene replaced by escape approach')
shot.setdefault('supersededMotionSelections',[]).append(prior)
for test in shot.get('motionTests',[]):
    if test['id']==prior['id']:
        test.update(userSelected=False,status=prior['status'])
shot.pop('motionSelection',None)
shot.pop('motionRef',None)
image='generated/storyboard/escape-approach-v01/lab2-08.png'
shot.update(description='So bright: Harper moves from a dark service passage toward a brightly lit escape-pod boarding hatch',
    sourceDirection='User replaced the sun/ship shot with an escape setup, and explicitly placed pod departure after Bright night in the next scene. Pod design remains undecided.',
    imagePrompt=(OUT/'lab2-08.prompt.txt').read_text(encoding='utf-8'),
    startingFrameDraft=dict(id='lab2-08-escape-approach-v01',image=image,userSelected=False,status='Generated escape approach draft; user review pending'),
    cameraMove=dict(zoom=[1,1.025],panX=[.4,.62],panY=[.5,.5]),
    motionDirection='Harper turns her attention fully toward the lit hatch, then takes one purposeful step toward it. A smooth small camera track follows her shoulder. Keep her face, short curls, silver top and hatch geometry stable. No prominent hand gestures, no robots, no full boarding operation or departure.',
    generationApproach='Reference-based still timing review, followed by one six-second native motion take after approval; source handles24frames each side.',
    motionReview=dict(notes='Narrative still draft replacing rejected sunward course; native escape animation not generated.'))
shot['startingFrameSelection']=copy.deepcopy(shot['startingFrameDraft'])
assert grid=={s['id']:(s['startFrame'],s['endFrameExclusive'],s['frames']) for s in shots}
assert len(set(s['promptLock'] for s in shots))==1

data=load(PROJECT/'generated/animatic/animatic-data.json')
phrase=next(p for p in data['phrases'] if p['startFrame']==1958)
departure=dict(id='escape-001',batch='escape-departure-v01',title='Leaving orbit at the moment',
    description='Harper leaves the original robot laboratory ship in a compact pod; show physical separation and a clear travel direction into open space',
    startPhrase=phrase.get('id'),startFrame=phrase['startFrame'],endFrameExclusive=phrase['endFrameExclusive'],
    frames=phrase['endFrameExclusive']-phrase['startFrame'],lyrics=[phrase['text']],promptLock=lock,
    sourceDirection='User explicitly chose departure after Bright night in the next scene, October10.',
    status='Narrative plan only; pod design undecided; starter frame and motion not generated',
    handles=dict(leadInFrames=24,leadOutFrames=24),cameraMove=dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5]),
    generationApproach='Choose whether to use the established spherical personal spacecraft or a distinct escape pod before generating the exterior departure.',
    motionDirection='Compact pod clears a docking recess in the original ark, separating smoothly into open dark space. Preserve both vessels, avoid collision-course framing; no abrupt banking or warp trail.',
    continuityConstraints=['Original graphite robot ship retained','Harper comes from the bright boarding hatch in lab2-08','Departure follows Bright night','Pod exterior identity remains unresolved'])
assert not any(s['id']==departure['id'] for s in register['storyboardProposals'])
register['storyboardProposals'].append(departure)
save(register_path,register)

spec=load(PROJECT/'storyboard-robot-ship-so-bright-motion-v01.json')
spec.update(id='escape-approach-v01',output='generated/storyboard/escape-approach-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v35.mp4',
    motionShotIds=[s['id'] for s in shots if s['id']!='lab2-08'],
    presentation='Original robot ship exteriors with a new interior escape-approach intercut at So bright.',
    mediaLabel='Kling / Blender / Harper escape-approach still draft',
    continuationNotes='V36 replaces only So bright with Harper approaching a lit escape-pod hatch, preserving its31frame slot and surrounding native footage. Bright night remains the original ark exterior. Departure is planned for Leaving orbit at1958 after Bright night; pod design undecided. Exact timings, fades and master audio retained.',
    status='Escape approach still in phrase timing review; no new native motion yet',
    reviewUrl='http://127.0.0.1:8768/storyboard/escape-approach-v01/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/escape-approach-v01/lab2-08.png')
save(PROJECT/'storyboard-escape-approach-v01.json',spec)

take=copy.deepcopy(load(PROJECT/'kling-robot-ship-so-bright-v01.json')['shots'][0])
take.update(id='lab2-08-escape-approach-motion-v01',firstImage=image,
    prompt='''Harper is outside the growth tank in a dark service passage, approaching the brightly lit compact-craft boarding hatch. She turns her gaze and shoulders fully toward the hatch and takes one measured purposeful step toward its threshold. Movement begins immediately; this is a quiet urgent escape setup, not a long walk or chase. Camera tracks smoothly a small distance with her upper body, maintaining the hatch destination on the right. Short curly auburn hair moves subtly; preserve her freckled adult face, hazel eyes and opaque silver halter top. Her hands stay naturally low and mostly outside framing, no finger gestures or touching a panel. The open hatch, seat and small cabin recess remain fixed and believable; warm light spills softly onto the graphite passage and her curls, cyan/amber lights steady. Do not show a launch or departure, close the hatch, add robots, pursuers or alarms, change clothing, add exposed anatomy, or reveal/redesign the full pod hull. Six seconds of continuous restrained action, no cuts, dissolves, zoom blur, shake, text or audio.\n\n'''+lock,
    reviewNotes='Harper makes one readable step toward the bright hatch; choose a clear early window for the31frame So bright slot. Pod departure follows Bright night, in a separate planned scene.')
save(PROJECT/'kling-escape-approach-v01.json',dict(status='Prepared; awaiting timed-still review and explicit approval for one48credit take',
    fps=24,output='generated/kling-tests/escape-approach-v01',reviewOutput='generated/storyboard/escape-approach-motion-v01',estimatedCredits=48,
    authorization=None,shots=[take]))
project_path=PROJECT/'project.json'
project=load(project_path)
project['production']['labVerseReview']=spec['reviewUrl']
project['production']['escapeSetup']=dict(approachShot='lab2-08',departureShot='escape-001',departureStartFrame=1958,
    timingDecision='User chose after Bright night',podDesign='Undecided; boarding shot hides full exterior',status='Approach still generated; departure planned')
save(project_path,project)
g=load(OUT/'generation-input.json')
g.update(status='First attempt succeeded; timed-still draft pending user review',
    originalGeneratedFile='C:/Users/arneg/.codex/generated_images/01a125f7-d729-7f60-8997-758a2cbdca4d/exec-dc607724-6887-4a8c-a671-482a0ebdcd68.png',
    reviewNotes='Freckled adult Harper and silver halter visible in dark passage. Lit boarding hatch, seat and instruments read clearly. Human hands and full craft exterior are offscreen. No tank/fluid; bright/dark contrast supplies phrase meaning.',boardRevision=73)
save(OUT/'generation-input.json',g)
save(OUT/'review-manifest.json',[
    dict(index=1,id='escape-approach',title='So bright — Harper approaches the hatch',src='lab2-08.png',href='lab2-08.png',output='lab2-08.png'),
    dict(index=2,id='harper-lab-identity',title='Harper identity and silver lab costume',src='../lab-silver-v01/lab2-05.png',href='../lab-silver-v01/lab2-05.png',output='../lab-silver-v01/lab2-05.png')])
save(OUT/'review-options.json',dict(preset='detail-review',showCaptions=True,minTileWidth=480,title='So bright — escape setup'))
cancel_path=PROJECT/'generated/storyboard/robot-ship-so-bright-v02/generation-input.json'
cancel=load(cancel_path)
cancel['status']='Superseded before generation; user changed So bright to escape approach. No image or video job submitted.'
save(cancel_path,cancel)
print('Escape approach registered at1838–1869; departure plan at1958–2010; eight native chunks preserved')
