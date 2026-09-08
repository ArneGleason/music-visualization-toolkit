"""Voice-envelope dial response; reuse verified same-source tracking, not old light."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'fx'
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'frames').mkdir(exist_ok=True)
tracking=json.loads((ROOT/'out/receiver_retimed_review/fx/tracking.json').read_text())
assert tracking['song_frames']==[805,856] and tracking['source_in_frame']==0
source=Path(tracking['source'])
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stems=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
assert len(stems)==1
wave=json.loads((ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())
offset=next(t['offsetSec'] for t in wave['tracks'] if t['id']=='lead-vocal')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(stems[0]),'-ac','1','-af',
 'highpass=f=80,lowpass=f=5000,aresample=12000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4')
times=np.arange(805/24-.25,856/24,1/1000)
rms=[]
for t in times:
    i=round((t-offset)*12000)
    chunk=audio[max(0,i-60):i+61]
    rms.append(float(np.sqrt(np.mean(chunk**2))))
rms=np.array(rms)
# Fixed noise gate avoids amplifying silence; reference percentile keeps speech
# energy strongly visible without flattening all syllables to full output.
floor=10**(-48/20)
reference=max(float(np.quantile(rms[times>=805/24],.95)),floor*2)
target=np.clip((rms-floor)/(reference-floor),0,1)**.75
env=[];value=0.
for x in target:
    tau=.008 if x>value else .065
    value+=(1-np.exp(-.001/tau))*(x-value)
    env.append(value)
env=np.array(env)
cap=cv2.VideoCapture(str(source))
assert cap.get(cv2.CAP_PROP_FPS)==24
yy,xx=np.mgrid[:720,:1280]
mask=((((xx-621)/155)**2+((yy-557)/149)**2<1)&(yy<536)).astype(np.float32)
mask=cv2.GaussianBlur(mask,(0,0),1.4)
def linear(a): return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def display(a):
    a=np.clip(a,0,1)
    return np.where(a<=.0031308,a*12.92,1.055*a**(1/2.4)-.055)
records=[]
for f,record in enumerate(tracking['frames']):
    ok,frame=cap.read(); assert ok
    tracked=cv2.warpPerspective(mask,np.array(record['homography']),(1280,720))
    b,g,r=cv2.split(frame.astype(np.float32)/255)
    tracked*=np.clip((r-b-.12)*4,0,1)
    t=(805+f+.5)/24
    voice=float(np.interp(t,times,env))
    strength=.035+2.8*voice
    rgb=linear(frame[:,:,::-1].astype(np.float32)/255)
    core=rgb*tracked[:,:,None]*strength*.65
    halo=(cv2.GaussianBlur(tracked,(0,0),10)*.18+cv2.GaussianBlur(tracked,(0,0),30)*.10)*strength
    result=(display(rgb+core+halo[:,:,None]*np.array([1.,.46,.10]))*255+.5).astype(np.uint8)[:,:,::-1]
    cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
    records.append(dict(record,voice_envelope=voice,strength=strength))
cap.release()
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),
 '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-an',str(OUT/'receiver_light.mp4')],check=True)
(OUT/'tracking.json').write_text(json.dumps(dict(tracking,driver='lead-vocal RMS amplitude, no drum onset events',
 events=[],stem=str(stems[0]),stem_offset_sec=offset,stem_sha256=hashlib.sha256(stems[0].read_bytes()).hexdigest(),
 rms_window_ms=10,attack_ms=8,release_ms=65,gate_dbfs=-48,reference_rms=reference,frames=records),indent=2))
print('Voice response range:',min(r['voice_envelope'] for r in records),max(r['voice_envelope'] for r in records))
