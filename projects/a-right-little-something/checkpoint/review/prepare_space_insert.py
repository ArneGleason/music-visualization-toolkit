import copy
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-verse-v02']
assert len(shots)==9
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
out=base/'generated/storyboard/lab-motion-v01'
out.mkdir(exist_ok=True)
records={x['id']:x for x in load(base/'generated/storyboard/lab-space-motion-v01/sources.json')}
notes={
 'lab2-06':'Native hull/light motion is restrained; existing editorial opening move supplies a clear reveal. Sampled hull, galleries and spars remain coherent.',
 'lab2-07':'Actual lateral ship travel and camera drift through dark sky, distinct from the preceding reveal. Sampled hull remains coherent.',
 'lab2-08':'Late source window follows the camera toward the bright star; ship slips almost completely outside lower-left, breaking repeated hull compositions. Kling adds two long illustrated star streaks; inspect in context.',
 'lab2-09':'Tiny ark crosses richly painted broad nebula, with faint native drift; a restrained editorial opening move maintains the vast-space ending.'}
for shot in shots:
    ident=shot['id']
    shot['batch']='lab-motion-v01'
    if ident not in notes:
        shutil.copy2(base/'generated/storyboard/lab-verse-v02'/(ident+'.mp4'),out/(ident+'.mp4'))
        shot['status']='Accepted still retained; lab native animation paused after provider guideline rejection'
        continue
    take=records[ident+'-motion-v01']
    lead={'lab2-06':24,'lab2-07':45,'lab2-08':85,'lab2-09':24}[ident]
    assert lead>=24 and 145-lead-shot['frames']>=24
    selected=dict(take,plan='kling-lab-space-motion-v01.json',status='Agent checked native draft',
       userSelected=False,draftForReview=True,sourceEditStartFrame=lead+1,editFrames=shot['frames'],
       leadInFrames=lead,availableLeadOutFrames=145-lead-shot['frames'],reviewNotes=notes[ident])
    shot.setdefault('motionTests',[]).append(selected)
    shot['motionSelection']=copy.deepcopy(selected)
    shot['motionRef']=take['motionRef']
    shot['motionReview']={'notes':notes[ident]}
save(base/'shots/shotlist.json',register)
spec=load(base/'storyboard-lab-verse-v02.json')
spec.update(id='lab-motion-v01',output='generated/storyboard/lab-motion-v01',
 sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v28.mp4',useMotion=True,
 motionShotIds=list(notes),draftForReview=False,status='Four native exterior takes; five lab stills pending provider-compatible treatment',
 mediaLabel='Kling / Blender / native laboratory ark exteriors / five lab stills',
 presentation='Four native Kling ark exterior takes replace their accepted stills; five lab shots remain accepted stills following provider rejection of the first tank request.',
 continuationNotes='V29 retains v28 schematic fade and original master/grid, inserts four native ark takes into phrase-timed lab verse. So bright uses late source86–116 for a star/dust interlude between ship views. Five tank scenes remain accepted stills; first tank animation rejected by Kling guidelines, fully clothed treatment decision pending. No further generation without resolving the lab content and reviewing revised imagery.',
 cameraMoves={'lab2-07':dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5]),
              'lab2-08':dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5])},
 reviewUrl='http://127.0.0.1:8768/storyboard/lab-motion-v01/animatic-through-bright-night.mp4')
save(base/'storyboard-lab-motion-v01.json',spec)
space=load(base/'kling-lab-space-motion-v01.json')
space.update(status='Four jobs completed and collected; agent QA passed, user motion review pending',actualCredits=192)
save(base/'kling-lab-space-motion-v01.json',space)
save(out/'generation-ledger.json',dict(priorCredits=1784,newConfirmedCredits=192,cumulativeConfirmedCredits=1976,
 approvedMaximum=432,remainingUnspentApprovalBudget=240,
 failedLabAttempt='First tank submission400content-guideline error, no generationId or credit field returned',
 completedJobs=list(records),pendingJobs=[],labDecisionPending=True))
print('Prepared four native inserts; >=24frame handles each side, five accepted stills cached.')
