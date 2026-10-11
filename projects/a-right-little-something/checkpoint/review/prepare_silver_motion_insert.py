import copy
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-silver-v01']
assert len(shots)==9
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
out=base/'generated/storyboard/lab-silver-motion-v01'
out.mkdir(exist_ok=True)
records={x['shotId']:x for x in load(out/'sources.json')}
assert set(records)=={f'lab2-{i:02d}' for i in range(1,6)}
notes={
 'lab2-01':'Actual eye/face expression and floating hair/bubble motion inside the sealed silver-swimwear tank. Kling also introduces external ivory service arms at the right edge, consistent with the following caretaker reveal. Editorial pan retained.',
 'lab2-02':'Actual caretaker service-arm motion and floating Harper in the growth chamber; opaque lower armor and silver swimwear retained. Editorial reveal retained.',
 'lab2-03':'Restrained finger and internal lattice motion, drifting hair and bubbles, with robot at external control. Raised hand remains inside uninterrupted upper chamber glass; silver wardrobe retained.',
 'lab2-04':'Actual finger/ring calculation inside culture fluid, face tracks gesture, uninterrupted glass and silver wardrobe retained.',
 'lab2-05':'Actual concentrating expression and living curls/fluid with geometric glints; brief phrase coverage selected from central source.'}
for shot in shots:
    ident=shot['id']
    shot['batch']='lab-silver-motion-v01'
    for key in ('startingFrameDraft','startingFrameSelection'):
        shot[key].update(userSelected=True,status='User approved silver wardrobe source for Kling upload')
    if ident not in records:
        shutil.copy2(base/'generated/storyboard/lab-silver-v01'/(ident+'.mp4'),out/(ident+'.mp4'))
        continue
    take=records[ident]
    lead=42 if ident=='lab2-05' else 24
    assert lead>=24 and take['sourceFrames']-lead-shot['frames']>=24
    selected=dict(take,plan='kling-lab-silver-motion-v01.json',status='Agent reviewed native draft',
        userSelected=False,draftForReview=True,sourceEditStartFrame=lead+1,editFrames=shot['frames'],
        leadInFrames=lead,availableLeadOutFrames=take['sourceFrames']-lead-shot['frames'],reviewNotes=notes[ident])
    shot.setdefault('motionTests',[]).append(selected)
    shot['motionSelection']=copy.deepcopy(selected)
    shot['motionRef']=take['motionRef']
    shot['motionReview']={'notes':notes[ident]}
save(base/'shots/shotlist.json',register)
spec=load(base/'storyboard-lab-silver-v01.json')
spec.update(id='lab-silver-motion-v01',output='generated/storyboard/lab-silver-motion-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v29.mp4',
    useMotion=True,motionShotIds=[s['id'] for s in shots],draftForReview=True,
    status='Nine native lab/ark shots assembled; user motion playback pending',
    mediaLabel='Kling / Blender / nine native lab and ark shots',
    presentation='Five native silver-swimwear laboratory takes and four native ark exterior takes, with purposeful editorial moves and phrase-centered fades.',
    continuationNotes='V30 replaces all five remaining lab stills with approved-budget native Kling takes. All nine lab/ark shots now have native motion. Sealed upper tank, silver bikini and internal hand/interface geography retained. V28 schematic tail dissolve, earlier Kling/Blender footage, original master AAC and5265frame grid preserved. So bright remains a star-pan interlude between ark views.',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-silver-motion-v01/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/lab-silver-v01/review-board.html')
save(base/'storyboard-lab-silver-motion-v01.json',spec)
plan=load(base/'kling-lab-silver-motion-v01.json')
plan.update(status='Five approved silver lab takes completed and collected; agent motion QA done, user playback pending',actualCredits=240)
save(base/'kling-lab-silver-motion-v01.json',plan)
save(out/'generation-ledger.json',dict(priorCredits=1784,exteriorCredits=192,labCredits=240,
    newCredits=432,cumulativeConfirmedCredits=2216,approvedMaximum=432,pendingJobs=[],completedLabJobs=[x['id'] for x in records.values()]))
print('Prepared all9 native shots; four unchanged exterior clips cached;432newcredits total.')
