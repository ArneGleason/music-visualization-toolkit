"""Reblock approved gantry imagery as walk, consideration, resumed walk."""
import copy
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v48'
save(OUT/'pre-revision-shotlist.json',r)
beats={(b['bar'],b['beat']):b['frame'] for b in read(BASE/'generated/animatic/animatic-data.json')['beats']}
start,consider,resume,end=beats[(40,1)],beats[(41,2)],beats[(41,4)],2595
assert (start,consider,resume,end)==(2425,2507,2539,2595)
shots={s['id']:s for s in r['storyboardProposals']}
continuation=copy.deepcopy(shots['concourse-010'])
for k in ['revisionHistory','stillRevisionHistory','motionTests','animaticPlacement']:
    continuation.pop(k,None)
continuation.update(id='concourse-013',sourceNoteId='concourse-013-direction-oct11')
r['storyboardProposals'].append(continuation)
for s in r['storyboardProposals']:
    if s.get('batch')=='station-concourse-v04':
        s['batch']='station-concourse-v05'
rows=[(shots['concourse-010'],start,consider,'Walk toward the ship',
    'Use the approved original gantry view. Harper walks naturally toward the ship for the longer opening beat, then eases into a brief stop midway along the gantry. Camera stays fixed or makes one very slow continuous move; preserve ship and station geometry.'),
    (shots['concourse-012'],consider,resume,'Pause and size it up',
    'Cut earlier to the approved entrance POV looking back toward Harper and the station. She has stopped to consider: small assessing eye movement, quiet practical approval, relaxed face, no big smile. Her gaze settles and she resolves to continue.'),
    (continuation,resume,end,'Continue along the gantry',
    'Return to the SAME wide camera and SAME native walking take at its later continuation, not the beginning. Harper resumes from the exact position where she stopped and walks the remaining distance toward the entrance. Keep her visible and outside through the end; no interior reveal. Carry purposeful walking motion into the next transition.')]
for s,a,z,title,direction in rows:
    s.setdefault('revisionHistory',[]).append(copy.deepcopy({k:v for k,v in s.items() if k!='revisionHistory'}))
    s.update(title=title,startFrame=a,endFrameExclusive=z,frames=z-a,startSeconds=(a-1)/24,endSeconds=(z-1)/24,
        timingBasis='DAWproject bar40 beat1 / bar41 beat2 / bar41 beat4, then existing next-vocal boundary2595.',
        description=direction,motionDirection=direction,status='Approved still; revised walk-consider-walk timing draft')
    s['startingFrameDraft']['userSelected']=True
    s['startingFrameDraft']['status']='User-approved image reused for revised blocking'
    for key in ['motionSelection','motionRef','videoPrompt']:
        s.pop(key,None)
continuation['motionContinuity']={'sameNativeTakeAs':'concourse-010','resumeAfter':'concourse-012','requireLaterSourceFrames':True,'noLoopOrReset':True}
seq=r['concourseSequence']
seq.setdefault('directionHistory',[]).append(dict(stage='V48 stills approved; motion pacing revised',sourceDirection=seq['sourceDirection']))
seq.update(status='V49 walk, consideration close-up, resumed walk',
    sourceDirection='User approves both stills. Longer walk down gantry, cut to her expression stopped sizing it up, then return to her continuing toward the entrance so movement covers the long scene. Move expression earlier, not as the final moment.',
    stillReview='http://127.0.0.1:8768/storyboard/station-concourse-v05/')
save(BASE/'shots/shotlist.json',r)
options=read(OUT.parent/'station-concourse-v04/review-options.json')
options.update(id='station-concourse-v05',output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v48.mp4',
    presentation='Approved stills reblocked as walk, consider, resumed walk; new movement is not yet generated.',
    mediaLabel='Gantry walk / consider / continue',
    continuationNotes='V49 reblocks approved gantry stills at2425–2595: walk82frames, consideration32frames, resumed walk56frames. Use two sequential selections from one continuous wide native take around the close-up; never loop the approach. This is a still timing preview. No new generation or spending. Original audio/full timing retained.')
save(OUT/'review-options.json',options)
save(OUT/'motion-plan.json',dict(status='Prepared direction only; not submitted',
    wideTake=dict(sharedBy=['concourse-010','concourse-013'],durationSeconds=10,
        sourceSelectionsOneBasedInclusive=[[25,106],[139,194]],
        sourcePauseCoveredByCloseup=[107,138],
        direction='One uninterrupted locked or very slowly moving wide gantry take. Walk, pause32frames, resume from that same spot. Remain outside and visible. Keep ship and station geometry fixed; no generated cuts.'),
    closeup=dict(shot='concourse-012',durationSeconds=4,sourceSelectionOneBasedInclusive=[25,56],
        direction='Approved entrance POV. Still considering the ship, subtle assessing eyes and restrained positive decision. Remains stopped; no broad smile, speaking or lip sync.'),
    currentPreview='Held approved stills only; does not demonstrate the intended walking',newPaidJobs=0))
print('Registered 82 / 32 / 56 frame walk-consider-walk pattern')
