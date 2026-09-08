"""Tracked internal artifact light, peripheral motes and local optical afterglow."""
from pathlib import Path
import hashlib,json,subprocess,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'));sys.path.insert(0,str(ROOT/'tools'))
import cv2
from assembly_timebase import conform_clip
original=ROOT/'out/outro_exchange_fx_v1/b_selected.mp4'
source=conform_clip(ROOT,{'file':str(original),'speed':1},24,prepare=True)['file']
cap=cv2.VideoCapture(source);frames=[]
while True:
    ok,im=cap.read()
    if not ok:break
    frames.append(im)
cap.release();N=len(frames);assert N==191
for folder in ['optical','lights']:(OUT/folder).mkdir(exist_ok=True)
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'out/outro_B2_v2/guide.wav'),'-ac','1','-ar','24000','-f','f32le','-'])
audio=np.frombuffer(pcm,dtype='<f4')
energy=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(N)])
# Local line normalization, not the much louder other speaker's whole-window peak.
energy=np.clip(energy/max(np.percentile(np.r_[energy[11:42],energy[80:111],energy[141:184]],90),1e-6),0,1)
def smooth(a,b,x):
    p=np.clip((x-a)/(b-a),0,1);return p*p*(3-2*p)
gate=np.maximum.reduce([smooth(a-5,a,np.arange(N))*(1-smooth(b-1,b+4,np.arange(N))) for a,b in [(11,42),(80,111),(141,184)]])
energy*=gate
for i in range(1,N):energy[i]=max(energy[i],energy[i-1]*.85)
# Incremental sparse tracking confined to artifact, forward/backward validated.
centers=[np.array([650.,576.],np.float32)]; failures=[]
for i in range(1,N):
    if i==111:
        centers.append(np.array([650.,576.],np.float32))
        continue  # Offscreen take change, never optical-flow across unrelated takes.
    prev=cv2.cvtColor(frames[i-1],cv2.COLOR_BGR2GRAY);cur=cv2.cvtColor(frames[i],cv2.COLOR_BGR2GRAY)
    m=np.zeros_like(prev);cx,cy=centers[-1];cv2.ellipse(m,(int(cx),int(cy)),(43,67),0,0,360,255,-1)
    pts=cv2.goodFeaturesToTrack(prev,60,.02,4,mask=m)
    if pts is None:raise RuntimeError('No artifact features')
    nxt,st,_=cv2.calcOpticalFlowPyrLK(prev,cur,pts,None,winSize=(21,21),maxLevel=2)
    back,bst,_=cv2.calcOpticalFlowPyrLK(cur,prev,nxt,None,winSize=(21,21),maxLevel=2)
    good=(st.ravel()>0)&(bst.ravel()>0)&(np.linalg.norm(back-pts,axis=2).ravel()<1)
    if good.sum()<4:raise RuntimeError(f'Artifact track lost {i}')
    delta=np.median((nxt-pts).reshape(-1,2)[good],axis=0)
    if np.linalg.norm(delta)>40:raise RuntimeError(f'Unreasonable artifact motion {i}: {delta}')
    centers.append(centers[-1]+delta)
y,x=np.mgrid[:720,:1280].astype(np.float32)
rng=np.random.default_rng(917)
particles=[(rng.uniform(0,1),rng.uniform(2.3,4.2),rng.uniform(0,math.tau),rng.uniform(.8,1.8),rng.choice([-1,1])) for _ in range(38)]
records=[]
for i,f in enumerate(frames):
    t=(i+155)/24;cx,cy=centers[i];v=float(energy[i]);pic=f.astype(np.float32)/255
    dx=x-cx;dy=y-cy;dist=np.sqrt(dx*dx+dy*dy)
    # No optical displacement on face, hands or specimen. Only nearby peripheral air.
    inner=1-np.exp(-((dx/83)**6+(dy/108)**6))
    region=np.exp(-((dx/245)**2+(dy/200)**2))*inner*smooth(355,415,y)
    displacement=np.sin(dist*.055-t*3.4)*(.9+2.3*v)*region
    mx=x+displacement*dx/np.maximum(dist,1);my=y+displacement*dy/np.maximum(dist,1)
    warped=cv2.remap(f,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(str(OUT/'optical'/f'{i:03}.png'),warped)
    b,g,r=cv2.split(pic)
    # Source-derived luminous internal structure, with tracked tapered shell aperture.
    roi=np.exp(-((dx/48)**6+(dy/81)**6))*(1-smooth(cy+56,cy+79,y))
    warm=np.clip((r-b-.045)*7,0,1)*np.clip((g-b-.015)*9,0,1)*roi
    theta=np.arctan2(dy,dx)
    sweep=.65+.35*np.exp(-np.mod(t*2.3-theta,math.tau)/1.1)
    core=cv2.GaussianBlur(warm,(0,0),.75)*sweep*(.65+2.1*v)
    emitted=core[:,:,None]*np.array([.10,.55,1.],np.float32)
    emitted+=cv2.GaussianBlur(emitted,(0,0),5)*1.0+cv2.GaussianBlur(emitted,(0,0),17)*.70
    # A soft practical spill on the low hands/suit, well below the face.
    spill=np.exp(-.5*((dx/80)**2+(dy/85)**2))*(.02+.10*v)
    emitted+=spill[:,:,None]*np.array([.17,.45,.80],np.float32)
    motes=np.zeros_like(emitted)
    for j,(phase,life,angle,size,side) in enumerate(particles):
        age=(t/life+phase)%1
        # Begin around the specimen, curl outward as they rise, fade before face height.
        px=cx+side*(25+165*age)+35*math.sin(age*math.tau+angle)*age
        py=cy-15-200*age+12*math.sin(age*math.tau*1.3+angle)
        fade=math.sin(math.pi*age)**1.4*(.4+.7*v)
        color=np.array([1.,.56,.80] if j%3 else [.88,.93,1.],np.float32)
        cv2.circle(motes,(int(px),int(py)),max(1,int(size)),tuple(float(c*fade) for c in color),-1,cv2.LINE_AA)
    emitted+=motes*1.2+cv2.GaussianBlur(motes,(0,0),3)*3+cv2.GaussianBlur(motes,(0,0),9)*1.7
    emitted*=smooth(340,390,y)[:,:,None]
    # Additive delta computed as soft screen light to avoid clipping opaque white.
    delta=(1-pic)*(1-np.exp(-emitted))
    cv2.imwrite(str(OUT/'lights'/f'{i:03}.png'),np.clip(delta*255,0,255).astype(np.uint8))
    if i in [67,77,88,96]:
        preview=np.clip(warped.astype(np.float32)+delta*255,0,255).astype(np.uint8)
        cv2.imwrite(str(OUT/f'check_{i:03}.jpg'),preview)
    records.append({'source_frame':i,'song_frame':4320+i,'center':centers[i].tolist(),'voice_envelope':v})
(OUT/'settings.json').write_text(json.dumps({'source':source,'frames':N,'fps':24,'song_origin':4320,'tracking':'artifact local sparse optical flow, forward/backward rejection, translation only','driver':'90percentile own three reply windows, gated with release; not speaker-separated','records':records},indent=2))
print('Afterglow layers ready',flush=True)
