"""Local FX trial: vocal energy modulates existing gold probe signal."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(a,**kw): subprocess.run([str(x) for x in a],check=True,cwd=ROOT,**kw)
source=ROOT/'clips/raw/signal_crossing_space_v6.mp4'
cap=cv2.VideoCapture(str(source));assert cap.get(cv2.CAP_PROP_FPS)==24
ok,first=cap.read();assert ok
gray=cv2.cvtColor(first,cv2.COLOR_BGR2GRAY)
region=np.zeros(gray.shape,np.uint8);region[335:403,350:422]=255
points=cv2.goodFeaturesToTrack(gray,80,.01,3,mask=region)
assert points is not None and len(points)>=6
origin=np.array([430.,375.]);prev=gray
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'));assert len(stem)==1
wave=json.loads((ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())
offset=next(t['offsetSec'] for t in wave['tracks'] if t['id']=='lead-vocal')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(stem[0]),'-ac','1','-af','highpass=f=80,lowpass=f=5000,aresample=12000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4')
rms=[]
for f in range(192):
    i=round(((719+f+.5)/24-offset)*12000)
    rms.append(float(np.sqrt(np.mean(audio[i-120:i+121]**2))))
floor=10**(-48/20);ref=max(np.quantile(rms,.94),floor*2)
targets=np.clip((np.array(rms)-floor)/(ref-floor),0,1)**.75
env=[];v=0
for x in targets:
    tau=.012 if x>v else .075
    v+=(1-np.exp(-1/24/tau))*(x-v);env.append(v)
yy,xx=np.mgrid[:720,:1280]
(OUT/'frames').mkdir(exist_ok=True)
records=[]
def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def display(a):
    a=np.clip(a,0,1)
    return np.where(a<=.0031308,a*12.92,1.055*a**(1/2.4)-.055)
for f in range(192):
    if f==0:frame=first
    else:
        ok,frame=cap.read();assert ok
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if f:
        moved,status,_=cv2.calcOpticalFlowPyrLK(prev,gray,points,None,winSize=(21,21),maxLevel=3)
        back,st,_=cv2.calcOpticalFlowPyrLK(gray,prev,moved,None,winSize=(21,21),maxLevel=3)
        good=(status.ravel()>0)&(st.ravel()>0)&(np.linalg.norm(back-points,axis=2).ravel()<1)
        assert good.sum()>=6, f'Track lost {f}'
        delta=np.median((moved-points)[good,0,:],axis=0)
        assert np.linalg.norm(delta)<8
        origin+=delta;points=moved[good]
    x,y=origin
    rgb=frame[:,:,::-1].astype(np.float32)/255
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    # Extract existing yellow emission, exclude rust-red planet and dark space.
    gold=np.clip((g-.38)/.40,0,1)*np.clip((r-b-.12)*3,0,1)*np.clip((g-b-.08)*4,0,1)
    corridor=np.exp(-((yy-y)/38)**2)*np.clip((xx-x+12)/22,0,1)
    mask=cv2.GaussianBlur((gold*corridor).astype(np.float32),(0,0),1.0)
    # Only modulate light already present. When native beam extinguishes, FX dies.
    pulse=env[f]
    core=linear(rgb)*mask[:,:,None]*(2.4*pulse)
    halo=(cv2.GaussianBlur(mask,(0,0),7)*.32+cv2.GaussianBlur(mask,(0,0),22)*.16)*pulse
    result=(display(linear(rgb)+core+halo[:,:,None]*np.array([1.,.53,.13]))*255+.5).astype(np.uint8)[:,:,::-1]
    cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
    records.append({'source_frame':f,'song_frame':719+f,'vocal_envelope':pulse,'nozzle_xy':origin.tolist(),'track_points':len(points),'mask_sum':float(mask.sum())})
    prev=gray
cap.release()
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',OUT/'clean.mp4'])
(OUT/'tracking.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'song_origin':719,'driver':'lead-vocal RMS','stem_offset_seconds':offset,'frames':records},indent=2))
edl=json.loads((ROOT/'out/receiver_voice_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/receiver_voice_review/overlay_cues.json').read_text())
for shot in edl['shots']:
    if shot['id'] in ('s009','s011'):
        shot['clip']['file']='out/probe_voice_trial/clean.mp4'
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','719','--end','910','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=29.958333333333:end=37.958333333333,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','192','-c:v','libx264','-crf','17','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Probe vocal trial rendered. Min tracked points:',min(r['track_points'] for r in records))
