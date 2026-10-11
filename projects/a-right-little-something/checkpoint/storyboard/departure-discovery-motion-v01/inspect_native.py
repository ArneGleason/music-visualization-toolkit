"""Record provider receipts, probe outputs and extract useful native frames."""
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
PLAN=BASE/'kling-departure-discovery-v01.json'
plan=json.loads(PLAN.read_text(encoding='utf-8'))
credit_total=0
ready=[]
for take in plan['shots']:
    folder=BASE/plan['output']/take['id']
    submission=folder/'submission.json'
    if not submission.exists():
        continue
    receipt=json.loads(submission.read_text(encoding='utf-8'))
    body=receipt.get('body',{})
    take.update(generationId=body.get('generationId'),actualCredits=body.get('creditsConsumed',0))
    credit_total+=take['actualCredits']
    source=BASE/take['repairMotionRef'] if take.get('repairMotionRef') else next(folder.glob('*-clean.mp4'),None)
    if not source:
        continue
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_streams','-of','json',str(source)]))['streams'][0]
    assert info['height']==1080 and info['r_frame_rate']=='24/1'
    lead=take.get('sourceEditStartFrame',25)-1
    assert int(info['nb_frames'])>=lead+take['editFrames']+24
    samples=([25,65,106,139,165,194] if take['shotId']=='concourse-010' else [1,lead+1,lead+max(1,take['editFrames']//2),lead+take['editFrames']])
    expression='+'.join(f'eq(n\\,{n-1})' for n in samples)
    image=OUT/(take['shotId']+('-repaired-samples.jpg' if take.get('repairMotionRef') else '-native-samples.jpg'))
    if not image.exists():
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-vf',
            f'select={expression},scale=640:360,tile=2x{4 if len(samples)>4 else 2}','-frames:v','1','-q:v','2',str(image)],check=True)
    take.update(collectionStatus='Collected clean native output',motionRef=source.relative_to(BASE).as_posix(),
                nativeWidth=info['width'],nativeHeight=info['height'],nativeFrames=int(info['nb_frames']),qaSampleFrames=samples)
    ready.append(take['shotId'])
plan.update(actualCredits=credit_total,confirmedCumulativeKlingCredits=plan['priorConfirmedCumulativeCredits']+credit_total,
            paidJobsPending=len(ready)!=len(plan['shots']),collectedShotIds=ready)
assert credit_total<=plan['approvedCredits'], 'Provider charge exceeds approved budget'
PLAN.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print('Collected',len(ready),'of',len(plan['shots']),'confirmed credits',credit_total,'cumulative',plan['priorConfirmedCumulativeCredits']+credit_total)
print('Ready:',', '.join(ready))
