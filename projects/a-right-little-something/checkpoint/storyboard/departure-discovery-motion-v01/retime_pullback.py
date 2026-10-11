"""Use only the clean post-flare native pullback with an immediate ease-out."""
import json
import math
from pathlib import Path
import subprocess
from PIL import Image

OUT=Path(__file__).resolve().parent;BASE=OUT.parents[2]
plan_path=BASE/'kling-departure-discovery-v01.json'
plan=json.loads(plan_path.read_text(encoding='utf-8'))
take=next(t for t in plan['shots'] if t['shotId']=='departure-002')
source=BASE/take['motionRef']
destination=OUT/'departure-retimed-clean.mp4'
width,height=1920,1080;size=width*height*3
decoder=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-vf','trim=start_frame=72:end_frame=193,setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-frames:v','140','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(destination)],stdin=subprocess.PIPE)
def next_image():
    raw=decoder.stdout.read(size)
    assert len(raw)==size
    return Image.frombytes('RGB',(width,height),raw)
lo=next_image();hi=next_image();index=0;mapping=[]
try:
    for n in range(140):
        position=120*(1-(1-n/139)**3)
        low=min(119,math.floor(position))
        while index<low:
            lo=hi;hi=next_image();index+=1
        weight=min(1,max(0,position-index))
        encoder.stdin.write(Image.blend(lo,hi,weight).tobytes())
        mapping.append(dict(editFrame=n+1,nativeSourceFrame=round(position+73,6)))
finally:
    encoder.stdin.close();decoder.stdout.close()
assert encoder.wait()==0;assert decoder.wait()==0
take.update(editMotionRef=destination.relative_to(BASE).as_posix(),sourceEditStartFrame=1,sourceSelectionNote='Native73–193 retimed to140frames with cubic ease-out; skips unwanted early flare and accelerates departure immediately. Adjacent-frame blends smooth the slow distant tail; no added image translation or cross-shot dissolve.',retime=dict(nativeStartFrame=73,nativeEndFrameInclusive=193,outputFrames=140,curve='source=73+120*(1-(1-outputIndex/139)^3)',frameBlending=True),availableLeadOutFrames=0)
take['placements'][0]['sourceEditStartFrame']=1
plan_path.write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'pullback-frame-map.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
print('Retimed clean native73–193 to140frames; first motion immediate, easing into distance')
