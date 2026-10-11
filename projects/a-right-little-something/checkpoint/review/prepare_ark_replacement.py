import copy
from pathlib import Path
import shutil
import sys
from PIL import Image

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/ark-replacement-v01'
lock=(out/'shared-prompt-lock.txt').read_text(encoding='utf-8').strip()
directions={
 'lab2-06':('Headquarters ark reveal','Start a measured camera pullback immediately, revealing the six lateral biosphere layout from the forward cyan laboratory galleries. Tiny stable ship glide, faint field-ring shimmer, small parallax between hull and distant stars. Keep habitats terrain-scale; no growing plants or rearranging pods.'),
 'lab2-07':('Dark aft-quarter glide','Measured lateral ark travel through near-black space. Maintain the aft-quarter viewpoint with restrained depth parallax. Cyan field ring stays open and stable, amber outlines remain small. No roll, sudden turn, exhaust or star streaks. Movement begins immediately for the brief phrase.'),
 'lab2-08':('Starward illumination','Camera pans gently toward the warm star at upper-right while the ark drifts out through lower-left, producing a light-and-dust interlude. Illustrated bloom breathes subtly with softly moving dust; retain detailed light, no optical flare circles or exposure washout.'),
 'lab2-09':('Luminous vastness','Slow camera pullback with layered cyan/violet nebula parallax. The tiny six-pod ark glides steadily toward the distant stars, retaining its silhouette and soft aft field ring. Calm continuous motion through the final hold; no accelerated departure or stretching ship.')}
moves={
 'lab2-06':dict(zoom=[1.15,1.035],panX=[0.55,0.5],panY=[0.5,0.5]),
 'lab2-07':dict(zoom=[1.05,1.02],panX=[0.35,0.65],panY=[0.5,0.5]),
 'lab2-08':dict(zoom=[1.12,1.03],panX=[0.15,0.8],panY=[0.45,0.45]),
 'lab2-09':dict(zoom=[1.09,1.015],panX=[0.6,0.45],panY=[0.5,0.5])}
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-robot-motion-v01']
assert len(shots)==9
for ident in directions:
    assert (out/(ident+'.png')).stat().st_size>0
    prompt=(out/(ident+'.prompt.txt')).read_text(encoding='utf-8')
    assert prompt.rstrip().endswith(lock)
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
plan_shots=[]
for shot in shots:
    ident=shot['id']
    shot['batch']='ark-replacement-v01'
    shot['promptLock']=lock
    if ident not in directions:
        shutil.copy2(base/'generated/storyboard/lab-robot-motion-v01'/(ident+'.mp4'),out/(ident+'.mp4'))
        continue
    label,direction=directions[ident]
    shot.setdefault('directionHistory',[]).append(dict(version='v32',description=shot['description'],
        image=shot['startingFrameSelection']['image'],motionSelection=copy.deepcopy(shot['motionSelection']),
        reason='User approved six lateral biopod field-drive ark v04 and requested replacement exterior shots.'))
    shot.setdefault('supersededMotionSelections',[]).append(copy.deepcopy(shot['motionSelection']))
    shot.pop('motionSelection',None)
    shot.pop('motionRef',None)
    image=out/(ident+'.png')
    size=Image.open(image).size
    selected=dict(id='ark-'+ident+'-start-v01',image=image.relative_to(base).as_posix(),userSelected=False,
        status='New v04 ark starting-frame draft for user review',generationMode='built-in ImageGen',
        nativeWidth=size[0],nativeHeight=size[1],label=label)
    shot.update(description=label+' using the approved six-pod field-drive ark.',
        imagePrompt=(out/(ident+'.prompt.txt')).read_text(encoding='utf-8'),
        sourceDirection=shot['sourceDirection']+' User accepted v04 ark architecture, muted habitat colors and small flora; replacement stills requested before Kling go-ahead.',
        startingFrameDraft=copy.deepcopy(selected),startingFrameSelection=copy.deepcopy(selected),
        cameraMove=moves[ident],motionDirection=direction,generationApproach=direction,
        continuityConstraints='Match headquarters ark v04: six lateral pods, fixed physical biome order, tiny flora/broad terrain, same hull/arms/culture galleries and vertical cyan field-drive ring.',
        motionReview={'notes':'New ark starting still with editorial move; native Kling footage not yet authorized or generated. '+direction})
    motion_prompt=(direction+' Preserve the exact approved starting-frame vessel, six-pod geometry and muted terrain habitats. '
        'One uninterrupted six-second illustrated shot, immediate sustained motion, no internal cuts or fades. '
        'No extra ship, duplicate/vanishing pods, deforming hull, physical rocket plume, human figure, text, logos, '
        'camera shake, zoom blur or generated audio.\n\n'+lock)
    plan_shots.append(dict(id=ident+'-ark-motion-v01',shotId=ident,title=shot['title'],startFrame=shot['startFrame'],
        editFrames=shot['frames'],leadInFrames=24,leadOutFrames=24,model='kling-video-v3_0',duration=6,resolution='1080p',
        imageCount=1,enable_audio=False,prefer_multi_shots=False,tailImage=None,firstImage=selected['image'],
        prompt=motion_prompt,estimatedCredits=48,reviewNotes=direction))
save(base/'shots/shotlist.json',register)
spec=load(base/'storyboard-lab-robot-motion-v01.json')
spec.update(id='ark-replacement-v01',output='generated/storyboard/ark-replacement-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v32.mp4',
    useMotion=True,motionShotIds=[s['id'] for s in shots if s['id'] not in directions],cameraMoves={},
    draftForReview=True,status='Four new ark starting frames in phrase slots; user still review before Kling go-ahead',
    mediaLabel='Kling / Blender / new biopod ark still preview',
    presentation='Five native lab takes followed by four new six-biopod field-drive ark stills with purposeful editorial movement.',
    continuationNotes='V33 replaces only the four old ark exterior compositions with new v04 design starter-frame drafts. Five native lab takes, including robot cutaway, remain. All phrase timing, fades, schematic dissolve and original master audio are retained. Kling directions prepared; no replacement video submitted until user go-ahead after still review.',
    reviewUrl='http://127.0.0.1:8768/storyboard/ark-replacement-v01/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/ark-replacement-v01/review-board.html')
save(base/'storyboard-ark-replacement-v01.json',spec)
save(base/'kling-ark-replacement-v01.json',dict(status='Starting frames and directions prepared; user explicitly requested still review before video go-ahead',
    fps=24,output='generated/kling-tests/ark-replacement-v01',estimatedCredits=192,
    authorization='No video upload, generation or new credit charge authorized yet for these four replacement takes.',shots=plan_shots))
save(out/'shot-directions.json',dict(promptLock=lock,shots=[dict(id=s['id'],title=s['title'],startFrame=s['startFrame'],
    endFrameExclusive=s['endFrameExclusive'],frames=s['frames'],image=s['startingFrameDraft']['image'],
    direction=s['motionDirection'],motionPrompt=next(p['prompt'] for p in plan_shots if p['shotId']==s['id'])) for s in shots if s['id'] in directions]))
print('Four new ark stills registered; video directions prepared; no Kling submissions.')
