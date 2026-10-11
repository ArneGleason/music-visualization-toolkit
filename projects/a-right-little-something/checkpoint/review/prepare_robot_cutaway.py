import copy
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path('tools').resolve()))
from build_chorus_revision import load, save

base = Path('projects/a-right-little-something').resolve()
out = base/'generated/storyboard/lab-robot-cutaway-v01'
assert (out/'lab2-03.png').stat().st_size > 0
register = load(base/'shots/shotlist.json')
shots = [s for s in register['storyboardProposals'] if s.get('batch') == 'lab-silver-motion-v01']
assert len(shots) == 9
register.setdefault('supersededStoryboardProposals', []).extend(copy.deepcopy(shots))
prompt = (out/'lab2-03.prompt.txt').read_text(encoding='utf-8')
lock = (out/'shared-prompt-lock.txt').read_text(encoding='utf-8')
assert prompt.endswith(lock) or prompt.rstrip().endswith(lock.rstrip())
direction = ('Small nonhuman drone rapidly enters data through two projected light manipulators on a large '
             'external holographic display. Luminous cells acknowledge contact with amber pulses. '
             'Robot and display remain outside the sealed tank; Harper and all human anatomy are off camera.')
for shot in shots:
    ident = shot['id']
    shot['batch'] = 'lab-robot-cutaway-v01'
    if ident != 'lab2-03':
        shutil.copy2(base/'generated/storyboard/lab-silver-motion-v01'/(ident+'.mp4'), out/(ident+'.mp4'))
        continue
    shot.setdefault('directionHistory', []).append(dict(version='v30', description=shot['description'],
        image=shot['startingFrameSelection']['image'], motionSelection=copy.deepcopy(shot['motionSelection']),
        userRejected=True, reason='User observed a three-finger hand in native footage and requested a complete robot-only cutaway.'))
    for take in shot['motionTests']:
        if take['id'] == shot['motionSelection']['id']:
            take.update(userRejected=True, status='Rejected by user: hand anatomy defect; entire composition replaced')
    shot.pop('motionSelection', None)
    shot.pop('motionRef', None)
    shot.update(description='Robot-only cutaway beside the growth chamber: a small service drone operates a large luminous external control display with projected light manipulators.',
        motionDirection=direction, generationApproach=direction, imagePrompt=prompt,
        sourceDirection=shot['sourceDirection']+' User correction: replace Harper-hand composition entirely with small robot, luminous panel and holographic manipulators.',
        continuityConstraints='No Harper or human anatomy in this cutaway. Robot and display stay outside uninterrupted tank glass. Controls are holographic light, not physical buttons.',
        cameraMove=dict(zoom=[1.04,1.08], panX=[0.18,0.82], panY=[0.5,0.5]),
        motionReview={'notes':'New robot-only still with editorial move; replacement native animation is prepared for source and budget approval.'})
    selected = dict(id='lab2-03-robot-cutaway-v01', image='generated/storyboard/lab-robot-cutaway-v01/lab2-03.png',
                    userSelected=False, status='New cutaway still for review', generationMode='built-in ImageGen')
    shot['startingFrameDraft'] = copy.deepcopy(selected)
    shot['startingFrameSelection'] = copy.deepcopy(selected)
save(base/'shots/shotlist.json', register)
spec = load(base/'storyboard-lab-silver-motion-v01.json')
spec.update(id='lab-robot-cutaway-v01', output='generated/storyboard/lab-robot-cutaway-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v30.mp4',
    motionShotIds=[s['id'] for s in shots if s['id'] != 'lab2-03'],
    status='Robot control cutaway still replaces rejected hand shot; native replacement approval pending',
    mediaLabel='Kling / Blender / robot control cutaway preview',
    presentation='Eight native lab/ark takes with a new robot-only holographic control cutaway still.',
    continuationNotes='V31 replaces lab2-03 completely with a small robot working projected controls outside the sealed pod. Harper returns in lab2-04. Native replacement is not generated yet. All phrase frames, earlier edits and original master audio are preserved. Six alien biosphere ship design remains a separate reference proposal.',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-robot-cutaway-v01/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/lab-robot-cutaway-v01/lab2-03.png')
save(base/'storyboard-lab-robot-cutaway-v01.json', spec)
motion_prompt = (direction+' Preserve the exact small ivory/graphite drone, chamber ribs and starting composition. '
    'Two slender projected light tendrils make brisk alternating precise taps and short sweeps across luminous cells and rings. '
    'Selected cells give brief amber confirmation pulses and ripple into the next data pattern. '
    'Start motion immediately; keep it active through a central three-second trim. Gentle sensor aiming, stable support feet. '
    'One uninterrupted six-second shot, locked native camera; editorial pan added later. '
    'Keep light manipulators projected, not mechanical finger hands. No physical keycaps, added human, anatomy, cuts, '
    'camera shake, internal fades, text, logos, zoom blur or audio.\n\n'+lock)
save(base/'kling-lab-robot-cutaway-v01.json', dict(status='Prepared for reviewed-source upload and 48-credit approval',
    fps=24, output='generated/kling-tests/lab-robot-cutaway-v01', estimatedCredits=48,
    authorization='New replacement source and prompt prepared; not submitted. Earlier 432-credit batch is complete.',
    shots=[dict(id='lab2-03-robot-motion-v01',shotId='lab2-03',title='Robot holographic control cutaway',
        startFrame=1624,editFrames=74,leadInFrames=24,leadOutFrames=24,model='kling-video-v3_0',duration=6,
        resolution='1080p',imageCount=1,enable_audio=False,prefer_multi_shots=False,tailImage=None,
        firstImage='generated/storyboard/lab-robot-cutaway-v01/lab2-03.png',prompt=motion_prompt,estimatedCredits=48,
        reviewNotes=direction)]))
(out/'motion-prompt.txt').write_text(motion_prompt,encoding='utf-8')
print('Robot cutaway registered at unchanged 1624–1698; native motion prepared, not submitted.')
