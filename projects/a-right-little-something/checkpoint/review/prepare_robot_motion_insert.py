import copy
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/lab-robot-motion-v01'
take=load(out/'source.json')
notes=(out/'native-qa.txt').read_text(encoding='utf-8').strip()
assert notes
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-robot-cutaway-v01']
assert len(shots)==9
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
for shot in shots:
    ident=shot['id']
    shot['batch']='lab-robot-motion-v01'
    if ident!='lab2-03':
        shutil.copy2(base/'generated/storyboard/lab-robot-cutaway-v01'/(ident+'.mp4'),out/(ident+'.mp4'))
        continue
    lead=24
    assert take['sourceFrames']-lead-shot['frames']>=24
    selected=dict(take,plan='kling-lab-robot-cutaway-v01.json',status='Agent reviewed native robot cutaway draft',
        userSelected=False,draftForReview=True,sourceEditStartFrame=lead+1,editFrames=shot['frames'],
        leadInFrames=lead,availableLeadOutFrames=take['sourceFrames']-lead-shot['frames'],reviewNotes=notes)
    shot.setdefault('motionTests',[]).append(selected)
    shot['motionSelection']=copy.deepcopy(selected)
    shot['motionRef']=take['motionRef']
    shot['motionReview']={'notes':notes}
    for key in ('startingFrameDraft','startingFrameSelection'):
        shot[key].update(userSelected=True,status='User approved robot cutaway starting still for replacement Kling upload')
save(base/'shots/shotlist.json',register)
spec=load(base/'storyboard-lab-robot-cutaway-v01.json')
spec.update(id='lab-robot-motion-v01',output='generated/storyboard/lab-robot-motion-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v31.mp4',
    useMotion=True,motionShotIds=[s['id'] for s in shots],draftForReview=True,
    status='Native robot cutaway replaces rejected Harper hand; user playback pending',
    mediaLabel='Kling / Blender / native robot control cutaway',
    presentation='Nine native lab/ark takes with robot-only holographic control cutaway before returning to Harper.',
    continuationNotes='V32 replaces the robot cutaway still with its approved48credit native Kling animation at exact1624–1698frames. All earlier footage, source handles, phrase fades, master audio and5265frame grid are retained. Alien biosphere ark design remains a separate reference, not yet regenerated in the four exterior clips.',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-robot-motion-v01/animatic-through-bright-night.mp4')
save(base/'storyboard-lab-robot-motion-v01.json',spec)
plan=load(base/'kling-lab-robot-cutaway-v01.json')
plan.update(status='Approved native robot take completed, collected and agent reviewed; user playback pending',actualCredits=take['credits'])
save(base/'kling-lab-robot-cutaway-v01.json',plan)
save(out/'generation-ledger.json',dict(priorCredits=2216,newCredits=take['credits'],cumulativeConfirmedCredits=2216+take['credits'],pendingJobs=[]))
print('Native robot cutaway registered; eight unchanged shot chunks reused.')
