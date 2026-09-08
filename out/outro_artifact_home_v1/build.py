"""Shot8 atmosphere returns to artifact; independent supersampled emission layer."""
from pathlib import Path
import sys, math, subprocess, json
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
SOURCE=ROOT/'out/outro_additive_green_v1/preview_numbered.mp4'
W,H=1280,720; SCALE=2
rng=np.random.default_rng(9821)
particles=[]
for j in range(180):
    # Keep initial atmosphere around shoulders and room, not over face.
    sx=rng.uniform(.09,.36) if j%2 else rng.uniform(.66,.94)
    sy=rng.uniform(.36,.90)
    particles.append((sx,sy,rng.uniform(.015,.15),rng.uniform(.72,.98),rng.uniform(-1,1),rng.uniform(.6,1.5)))
def ease(a,b,t):
    u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
def effect(frame):
    total=np.zeros((H*SCALE,W*SCALE,3),np.float32)
    for sub in [-.375,-.125,.125,.375]:
        u=np.clip((frame+sub)/21,0,1)
        layer=np.zeros_like(total)
        for j,(sx,sy,start,end,turn,weight) in enumerate(particles):
            p=ease(start,end,u)
            # Curved, inward paths end inside the artifact, not in front of the face.
            xx=(1-p)*sx+p*.498+math.sin(p*math.pi)*turn*.065
            yy=(1-p)*sy+p*.806+math.sin(p*math.pi)*.09
            fade=1-ease(.81,1,p)
            shimmer=.8+.2*math.sin(j*1.3+u*3)
            color=np.array([.18,.055,.30] if j%3 else [.22,.13,.07])*weight*fade*shimmer
            radius=max(1,round(SCALE*(.6+weight*.65)*(1-.45*p)))
            cv2.circle(layer,(round(xx*W*SCALE),round(yy*H*SCALE)),radius,tuple(float(v) for v in color),-1,cv2.LINE_AA)
        # Glints with broad colored atmospheric glow, all strictly additive.
        layer+=cv2.GaussianBlur(layer,(0,0),3*SCALE)*2.1
        layer+=cv2.GaussianBlur(layer,(0,0),16*SCALE)*2.8
        total+=layer/4
    return cv2.resize(total,(W,H),interpolation=cv2.INTER_AREA)
def add(f,e):
    b=f.astype(np.float32)/255
    linear=np.where(b<=.04045,b/12.92,((b+.055)/1.055)**2.4)+e
    rgb=np.where(linear<=.0031308,linear*12.92,1.055*np.maximum(linear,0)**(1/2.4)-.055)
    out=np.clip(rgb*255,0,255).astype(np.uint8)
    assert np.all(out.astype(int)>=f.astype(int)-1)
    return out
cap=cv2.VideoCapture(str(SOURCE));cap.set(cv2.CAP_PROP_POS_FRAMES,260)
writer=cv2.VideoWriter(str(OUT/'shot8_silent.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(W,H))
for i in range(22):
    ok,f=cap.read();assert ok
    e=effect(i);e[:92]=0
    f=add(f,e)
    cv2.rectangle(f,(0,38),(1185,66),(12,12,12),-1)
    cv2.putText(f,'Atmosphere returns to artifact / lip sync still unresolved',(16,57),cv2.FONT_HERSHEY_SIMPLEX,.51,(170,210,240),1,cv2.LINE_AA)
    writer.write(f)
    if i in [0,7,14,21]:cv2.imwrite(str(OUT/f'check_{i:02}.jpg'),f)
writer.release();cap.release()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(SOURCE),'-i',str(OUT/'shot8_silent.mp4'),'-filter_complex','[0:v]trim=end_frame=260,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=282,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
print('Shot8 replaced, same timing and master audio. 2x spatial / four shutter samples.')
