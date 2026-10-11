"""Promote a reviewed collected replacement into the existing phrase grid."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--source-start-frame',type=int,default=25)
parser.add_argument('--review-notes',required=True)
args=parser.parse_args()
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
plan_path=PROJECT/'kling-escape-approach-v01.json'
plan=load(plan_path)
take=plan['shots'][0]
folder=PROJECT/plan['output']/take['id']
result=load(folder/'result.json')['body']
assert result['status'] in ['SUCCEED','SUCCEEDED','SUCCESS','COMPLETED'],result['status']
native=next(folder.glob('*-clean.mp4'),None) or next(folder.glob('*.mp4'))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(native)]))['streams'][0]
frames=int(probe['nb_frames'])
lead=args.source_start_frame-1
assert probe['r_frame_rate']=='24/1'
assert probe['height']==1080 and probe['width']<=1920
assert lead>=24 and frames-lead-31>=24
selection=dict(id=take['id'],motionRef=native.relative_to(PROJECT).as_posix(),sourceFrames=frames,
    nativeWidth=probe['width'],fps=24,credits=48,generationId=plan['generationId'],
    plan=plan_path.relative_to(PROJECT).as_posix(),status='Agent checked native replacement; user playback pending',
    userSelected=False,draftForReview=True,sourceEditStartFrame=args.source_start_frame,
    editFrames=31,leadInFrames=lead,availableLeadOutFrames=frames-lead-31,reviewNotes=args.review_notes)
register_path=PROJECT/'shots/shotlist.json'
register=load(register_path)
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='escape-approach-v01']
assert len(shots)==9
target=PROJECT/'generated/storyboard/escape-approach-motion-v01'
target.mkdir(parents=True,exist_ok=True)
for shot in shots:
    shot['batch']='escape-approach-motion-v01'
    if shot['id']=='lab2-08':
        shot.setdefault('motionTests',[]).append(copy.deepcopy(selection))
        shot['motionSelection']=selection
        shot['motionRef']=selection['motionRef']
        shot['cameraMove']=dict(zoom=[1,1],panX=[.5,.5],panY=[.5,.5])
        shot['motionReview']=dict(notes=args.review_notes)
        shot['motionDirection']=take['prompt']
    else:
        shutil.copy2(OUT/(shot['id']+'.mp4'),target/(shot['id']+'.mp4'))
save(register_path,register)
spec=load(PROJECT/'storyboard-escape-approach-v01.json')
spec.update(id='escape-approach-motion-v01',output='generated/storyboard/escape-approach-motion-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v36.mp4',
    motionShotIds=[s['id'] for s in shots],
    presentation='So bright now intercuts native Harper movement toward the escape hatch, amid the original robot ship exteriors.',
    mediaLabel='Kling / Blender / native Harper escape approach',
    continuationNotes='V37 keeps eight prior native lab/ark takes; only So bright changes to native Harper escape-approach motion. Bright night remains the exterior pause; pod departure is planned at1958after Bright night with design undecided. Exact phrase grid, fades, schematic dissolve and original master audio retained.',
    status='All nine lab/ark shots animated; So bright is an escape setup, user playback pending',
    reviewUrl='http://127.0.0.1:8768/storyboard/escape-approach-motion-v01/animatic-through-bright-night.mp4')
save(PROJECT/'storyboard-escape-approach-motion-v01.json',spec)
plan.update(status='Requested 48-credit escape-approach take completed and collected; agent QA passed; user playback pending',actualCredits=48,
    sourceEditStartFrame=args.source_start_frame,reviewNotes=args.review_notes)
save(plan_path,plan)
save(target/'source-verification.json',dict(nativeSource=selection['motionRef'],sourceProbe=probe,selection=selection,
    editFrames=31,startFrame=1838,endFrameExclusive=1869,paidCredits=48,retimed=False))
project_path=PROJECT/'project.json'
project=load(project_path)
project['production']['labVerseReview']=spec['reviewUrl']
project['production']['escapeSetup']['status']='Native approach animated; departure planned, pod design undecided'
save(project_path,project)
print('Native replacement registered with source handles; eight unchanged chunks copied')
