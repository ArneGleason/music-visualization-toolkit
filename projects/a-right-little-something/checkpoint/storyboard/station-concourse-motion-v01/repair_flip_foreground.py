"""Remove invented left-edge figures using each locked take's clean first frame."""
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
PLAN=BASE/'kling-station-concourse-v01.json'
plan=json.loads(PLAN.read_text(encoding='utf-8'))
for take in plan['shots']:
    if take['shotId'] not in ('concourse-004','concourse-005'):
        continue
    source=BASE/take['motionRef']
    plate=OUT/(take['shotId']+'-clean-foreground.png')
    final=OUT/(take['shotId']+'-foreground-repaired.mp4')
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-frames:v','1',str(plate)],check=True)
    weight='clip((X-W*0.25)/(W*0.05),0,1)'
    graph=f"[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_expr='A*({weight})+B*(1-({weight}))':shortest=1,format=yuv420p[v]"
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-loop','1','-framerate','24',
        '-i',str(plate),'-filter_complex',graph,'-map','[v]','-an','-frames:v',str(take['nativeFrames']),
        '-c:v','libx264','-preset','fast','-crf','16','-movflags','+faststart',str(final)],check=True)
    take.update(originalMotionRef=take['motionRef'],repairMotionRef=final.relative_to(BASE).as_posix(),
        motionRef=final.relative_to(BASE).as_posix(),
        localRepair='Clean first-frame station plate replaces left25percent with feather to30percent, removing invented foreground figure. Native ship region retained, no translation or retiming.')
PLAN.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print('Repaired unwanted figures in both flip takes without new generation')
