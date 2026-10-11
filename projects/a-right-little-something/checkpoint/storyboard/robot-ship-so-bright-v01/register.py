"""Restore the user's original ship choice and register one unanimated draft."""
import copy
import json
from pathlib import Path
import shutil

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

register_path=PROJECT/'shots/shotlist.json'
register=load(register_path)
previous=load(PROJECT/'generated/storyboard/lab-robot-motion-v01/shot-directions.json')
old={s['id']:s for s in previous['shots']}
active=[s for s in register['storyboardProposals'] if s['id'] in old]
save(OUT/'pre-reversion-shot-snapshot.json',active)
before_grid={s['id']:(s['startFrame'],s['endFrameExclusive'],s['frames']) for s in active}
keys=['description','promptLock','sourceDirection','generationApproach','motionDirection','cameraMove',
      'startingFrameDraft','startingFrameSelection','motionSelection','motionRef','imagePrompt','continuityConstraints']
for shot in active:
    if shot['id'] in ['lab2-06','lab2-07','lab2-08','lab2-09']:
        history=dict(batch=shot['batch'],reason='User reverted to original graphite robot headquarters design; biopod designs shelved',
            **{k:copy.deepcopy(shot[k]) for k in keys if k in shot})
        shot.setdefault('directionHistory',[]).append(history)
        for key in keys:
            if key in old[shot['id']]:
                shot[key]=copy.deepcopy(old[shot['id']][key])
            else:
                shot.pop(key,None)
        if 'blenderModelDevelopment' in shot:
            shot['blenderModelDevelopment']['status']='Shelved experiment; user returned to original robot ship design'
    shot['batch']='robot-ship-so-bright-v01'
    shot['promptLock']=previous['promptLock']
    if shot['id']!='lab2-08':
        shutil.copy2(PROJECT/'generated/storyboard/lab-robot-motion-v01'/(shot['id']+'.mp4'),OUT/(shot['id']+'.mp4'))

shot=next(s for s in active if s['id']=='lab2-08')
shot.setdefault('supersededMotionSelections',[]).append(dict(copy.deepcopy(shot['motionSelection']),
    userSelected=False,status='User rejected distracting starward luminous streaks; replace shot'))
for test in shot.get('motionTests',[]):
    if test.get('id')=='lab2-08-motion-v01':
        test.update(userSelected=False,status='User rejected distracting starward luminous streaks')
shot.pop('motionSelection',None)
shot.pop('motionRef',None)
image='generated/storyboard/robot-ship-so-bright-v01/lab2-08.png'
prompt=(OUT/'lab2-08.prompt.txt').read_text(encoding='utf-8')
shot.update(description='So bright: original graphite laboratory ark rim-lit beneath the curved limb of a large warm sun, with open space between them',
    imagePrompt=prompt,startingFrameDraft=dict(id='lab2-08-original-ship-v02',image=image,userSelected=False,
        status='Generated redesigned draft; user review pending'),
    cameraMove=dict(zoom=[1.0,1.035],panX=[.5,.64],panY=[.5,.45]),
    motionDirection='Slow smooth starward pan, subtle ship drift and gentle solar surface motion. Warm rimlight and cyan galleries remain stable. No luminous streaks, beams, trails, flare spokes, exposure pumping or geometry changes.',
    motionReview=dict(notes='Old streaked take rejected. New sun-dominant starter frame with editorial pan; native replacement not generated.'),
    generationApproach='Reference-based ImageGen still, then one six-second silent 1080p Kling replacement after review; preserve 24-frame source handles.')
shot['startingFrameSelection']=copy.deepcopy(shot['startingFrameDraft'])
assert before_grid=={s['id']:(s['startFrame'],s['endFrameExclusive'],s['frames']) for s in active}
assert len(set(s['promptLock'] for s in active))==1,'Original shared lock must remain identical'
save(register_path,register)

spec=load(PROJECT/'storyboard-lab-robot-motion-v01.json')
spec.update(id='robot-ship-so-bright-v01',output='generated/storyboard/robot-ship-so-bright-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v33.mp4',
    motionShotIds=[s['id'] for s in active if s['id']!='lab2-08'],cameraMoves={'lab2-07':spec['cameraMoves']['lab2-07']},
    presentation='Original robot headquarters ship restored; So bright replaced by a redesigned sunlit starter-frame draft.',
    mediaLabel='Kling / Blender / original robot ship with So bright still draft',
    continuationNotes='V34 restores the original robot ship motion for lab2-06/07/09 and retains five native lab takes. Only So bright is a new sun-dominant still draft, without starward streaks. Exact phrase frame grid, fades, schematic dissolve and original master audio retained. One replacement Kling take prepared, not submitted.',
    status='Original ship restored; redesigned So bright still in timing review before paid motion',
    reviewUrl='http://127.0.0.1:8768/storyboard/robot-ship-so-bright-v01/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/robot-ship-so-bright-v01/lab2-08.png')
save(PROJECT/'storyboard-robot-ship-so-bright-v01.json',spec)

prior_plan=load(PROJECT/'kling-lab-space-motion-v01.json')
take=copy.deepcopy(next(t for t in prior_plan['shots'] if t['shotId']=='lab2-08'))
lock='PROMPT LOCK:'+take['prompt'].split('\n\nPROMPT LOCK:')[1]
take.update(id='lab2-08-original-ship-motion-v02',firstImage=image,
    prompt='''So bright: original laboratory ark beneath the warm curved limb of the sun. Begin a gentle smooth camera pan toward the upper-right sun immediately; the complete unchanged ship glides subtly toward the right and slightly slips down-left in the camera frame. Solar surface has slow restrained granular convection; the diffuse corona moves gently close to the star limb. The visual action is illumination: steady gold rimlight grazes the graphite hull while cyan culture galleries show faint internal activity. Preserve clear star surface detail, dark space, the exact ship geometry and all service spars. No streams or lines connecting the ship and sun, no luminous streaks, beams, flare spokes, ribbons, trails, warp effects, added exhaust or high-speed travel. No pulsing/strobing bloom or exposure washout. Motion is restrained and continuous from the first frame. One uninterrupted six-second shot with no internal cuts or dissolves, no text and no audio.\n\n'''+lock,
    reviewNotes='Redesigned sun-dominant interlude. Track toward the star without new streaks. Keep whole ship coherent, preserve subtle illumination and intentional motion.')
save(PROJECT/'kling-robot-ship-so-bright-v01.json',dict(status='Prepared; awaiting reviewed still/animatic and explicit 48-credit video approval',
    fps=24,output='generated/kling-tests/robot-ship-so-bright-v01',reviewOutput='generated/storyboard/robot-ship-so-bright-motion-v01',
    estimatedCredits=48,authorization=None,shots=[take]))

project_path=PROJECT/'project.json'
project=load(project_path)
model=project['production']['headquartersArkModel']
model['status']='Shelved experiment; user chose original graphite submarine-like robot laboratory ship'
model['poseTransferExperiment']['status']='Experiment reviewed; user chose original ship instead'
project['production']['headquartersShipDesignSelection']=dict(reference='generated/storyboard/lab-verse-v01/lab2-06.png',
    status='User returned to original robot headquarters ship',changedOn='2026-10-10',
    notes='Retain original exterior motion except replace So bright without starward streaks.')
project['production']['labVerseReview']=spec['reviewUrl']
for ref in project['visualReferences']:
    if ref['id'].startswith('headquarters-alien-biopod-ark'):
        ref['currentUse']=False
        ref['supersededReason']='User returned to original robot headquarters ship'
save(project_path,project)
save(OUT/'review-manifest.json',[
    dict(index=1,id='original-ship-reference',title='Original robot ship — design reference',src='../lab-verse-v01/lab2-06.png',href='../lab-verse-v01/lab2-06.png',output='../lab-verse-v01/lab2-06.png'),
    dict(index=2,id='old-so-bright',title='Previous So bright — distracting streaks',src='../lab-verse-v01/lab2-08.png',href='../lab-verse-v01/lab2-08.png',output='../lab-verse-v01/lab2-08.png'),
    dict(index=3,id='new-so-bright',title='New So bright — sun and rimlight',src='lab2-08.png',href='lab2-08.png',output='lab2-08.png')])
save(OUT/'review-options.json',dict(preset='detail-review',showCaptions=True,minTileWidth=480,title='Original robot ship — revised So bright',contactSheetColumns=3,contactSheetThumb=480,contactSheetOutput='so-bright-overview.png'))
print('Original ship restored in canonical development; eight unchanged motion chunks copied; new still and paid plan prepared')
