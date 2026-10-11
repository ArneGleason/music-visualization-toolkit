"""Register two checked ejection takes without changing the canonical frame grid."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--interior-start',type=int,default=25)
parser.add_argument('--exterior-start',type=int,default=25)
parser.add_argument('--interior-notes',required=True)
parser.add_argument('--exterior-notes',required=True)
args=parser.parse_args()

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_streams','-of','json',str(path)]))['streams'][0]

plan_path=PROJECT/'kling-escape-ejection-v01.json'
plan=load(plan_path)
register_path=PROJECT/'shots/shotlist.json'
register=load(register_path)
shots=sorted([s for s in register['storyboardProposals'] if s.get('batch')=='escape-ejection-v01'],key=lambda s:s['startFrame'])
assert len(shots)==11 and register['activeReviewEdit']=='v38'
save(OUT/'pre-motion-shot-snapshot.json',shots)
target=PROJECT/'generated/storyboard/escape-ejection-motion-v01'
target.mkdir(parents=True,exist_ok=True)
selections=[]
for shot in shots:
    shot['batch']='escape-ejection-motion-v01'
    if shot['id'].startswith('lab2-'):
        shutil.copy2(OUT/(shot['id']+'.mp4'),target/(shot['id']+'.mp4'))
        continue
    take=next(t for t in plan['shots'] if t['shotId']==shot['id'])
    folder=PROJECT/plan['output']/take['id']
    result=load(folder/'result.json')['body']
    assert result['status'] in ['SUCCEED','SUCCEEDED','SUCCESS','COMPLETED'],result['status']
    submission=load(folder/'submission.json')['body']
    native=next(folder.glob('*-clean.mp4'),None) or next(folder.glob('*.mp4'))
    info=probe(native)
    source_start=args.interior_start if shot['id']=='escape-001' else args.exterior_start
    notes=args.interior_notes if shot['id']=='escape-001' else args.exterior_notes
    lead=source_start-1
    frames=int(info['nb_frames'])
    assert info['r_frame_rate']=='24/1' and info['height']==1080 and info['width']<=1920
    assert lead>=24 and frames-lead-shot['frames']>=24
    selection=dict(id=take['id'],motionRef=native.relative_to(PROJECT).as_posix(),
        sourceFrames=frames,nativeWidth=info['width'],nativeHeight=info['height'],fps=24,
        credits=submission['creditsConsumed'],generationId=submission['generationId'],
        plan=plan_path.relative_to(PROJECT).as_posix(),sourceEditStartFrame=source_start,
        editFrames=shot['frames'],leadInFrames=lead,availableLeadOutFrames=frames-lead-shot['frames'],
        status='Agent reviewed native draft; user playback pending',userSelected=False,draftForReview=True,
        reviewNotes=notes,retimed=False)
    shot.setdefault('motionTests',[]).append(copy.deepcopy(selection))
    shot['motionSelection']=selection
    shot['motionRef']=selection['motionRef']
    shot['motionReview']=dict(notes=notes)
    shot['cameraMove']=dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5])
    shot['generationApproach']='User-approved native Kling take collected, sampled and inserted with24sourceframes minimum each side; no retiming or additional editorial camera movement.'
    shot['status']='Checked native ejection draft; user playback pending'
    shot['handles'].update(status='Native source handles verified')
    for field in ['startingFrameDraft','startingFrameSelection']:
        shot[field].update(userSelected=True,status='User approved starter frame and prompt for Kling upload')
    take.update(sourceEditStartFrame=source_start,reviewNotes=notes,status='Completed and collected; agent QA recorded; user playback pending')
    selections.append(dict(shotId=shot['id'],sourceProbe=info,selection=selection))
assert len({s['promptLock'] for s in shots})==1
save(register_path,register)
spec=load(PROJECT/'storyboard-escape-ejection-v01.json')
spec.update(id='escape-ejection-motion-v01',output='generated/storyboard/escape-ejection-motion-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v38.mp4',
    motionShotIds=[s['id'] for s in shots],
    presentation='Accepted robot-lab footage followed by native secured-cabin release and exterior pod departure, in the full song.',
    mediaLabel='Kling / Blender / native escape sequence',
    continuationNotes='V39 replaces two escape stills with native Kling footage at1897–2010 and2010–2105. Interior starts1:19; exterior1:23.71. Nine previous prepared native chunks are reused. Native action and limitations recorded in shot notes. Exact timing, fades and original master audio preserved. Next channel begins2105.',
    status='Both new native clips collected and checked; full animatic user review pending',
    reviewUrl='http://127.0.0.1:8768/?v=v39')
spec.setdefault('cameraMoves',{}).update({sid:dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5]) for sid in ['escape-001','escape-002']})
save(PROJECT/'storyboard-escape-ejection-motion-v01.json',spec)
plan.update(status='Both approved takes completed and collected; native QA recorded; user playback pending',
    actualCredits=112,confirmedCumulativeKlingCredits=2472,
    reviewTitle='Escape pod — interior release and exterior departure',
    reviewSummary='User-approved eight-second interior and six-second exterior takes,1080p,112credits total. Exact edit windows follow the canonical grid with one-second minimum source handles. No retiming.')
save(plan_path,plan)
save(target/'source-verification.json',dict(selections=selections,paidCredits=112,
    confirmedCumulativeKlingCredits=2472,startFrame=1897,endFrameExclusive=2105,retimed=False))
project_path=PROJECT/'project.json'
project=load(project_path)
project['production']['escapeSetup'].update(status='Two native departure takes completed and checked; V39 playback pending',
    motionReview=spec['reviewUrl'],nativeMotionPlan='kling-escape-ejection-v01.json',confirmedCumulativeKlingCredits=2472)
save(project_path,project)
print('Two native shots registered with verified source handles; nine prior chunks preserved')
