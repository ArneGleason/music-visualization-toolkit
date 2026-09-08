"""Existing singing-tail review plus a vocal-driven floating phosphor rosette."""
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
edl=json.loads((ROOT/'out/astronaut_reply_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/astronaut_reply_review/overlay_cues.json').read_text())
s=next(s for s in edl['shots'] if s['id']=='s012');s.update(end_sec=1082/24,dur_sec=171/24,frames=171)
next(c for c in cues['shots'] if c['id']=='s012')['end']=1082
edl['duration_sec']=cues['duration_sec']=1082/24;cues['frames']=1082
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','971','--end','1081','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
# Guide already aligned: source0 maps to song899. No extra stem offset.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'out/astronaut_reply_v1/guide.wav'),'-af','highpass=f=80,lowpass=f=1500,aresample=8000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4');norm=max(np.quantile(np.abs(audio),.95),.001)
cap=cv2.VideoCapture(str(OUT/'raw.mp4'));assert cap.get(cv2.CAP_PROP_FPS)==24
(OUT/'frames').mkdir(exist_ok=True)
period=40.;trail=np.zeros((720,1280),np.float32);records=[]
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def center(t):
    anchors=[(-.2,180,445),(.25,270,320),(.80,330,270),(1.12,215,375),(1.55,320,420),(2.2,240,285)]
    for a,b in zip(anchors,anchors[1:]):
        if t<=b[0]:
            q=smooth((t-a[0])/(b[0]-a[0]));return np.array(a[1:])*(1-q)+np.array(b[1:])*q
    return np.array(anchors[-1][1:])
for f in range(111):
    ok,frame=cap.read();assert ok
    song=(971+f+.5)/24;t=song-1030/24
    energy=np.zeros((720,1280),np.float32)
    if t>-.16:
        i=round((song-899/24)*8000);chunk=audio[i-512:i+512].astype(float);chunk-=chunk.mean()
        amplitude=float(np.sqrt(np.mean(chunk*chunk)))
        corr=np.correlate(chunk,chunk,'full')[len(chunk)-1:]
        candidates=np.arange(22,90);scores=corr[candidates]/(len(chunk)-candidates)
        peaks=np.flatnonzero((scores[1:-1]>scores[:-2])&(scores[1:-1]>=scores[2:]))+1
        if len(peaks) and amplitude>.002:
            lag=candidates[peaks[np.argmax(scores[peaks])]];period=.8*period+.2*lag
        lo=max(1,i-int(period));hi=min(len(audio)-1,i+int(period))
        crossings=np.flatnonzero((audio[lo-1:hi-1]<=0)&(audio[lo:hi]>0))+lo
        origin=crossings[np.argmin(abs(crossings-i))] if len(crossings) else i
        phase=np.arange(256)/256
        folded=sum(np.interp(origin+(phase+k)*period,np.arange(len(audio)),audio) for k in [-1,0,1])/(3*norm)
        radial=12+28*np.tanh(np.abs(folded)*1.65)
        radial=(radial+np.roll(radial,1)+np.roll(radial,-1))/3
        angle=np.linspace(0,2*np.pi,768,endpoint=False)
        radius=np.tile(radial,3)
        xy=center(t)+np.stack([np.cos(angle+.35*t)*radius,np.sin(angle+.35*t)*radius*.82],axis=1)
        activation=smooth((t+.16)/.25)
        level=activation*(.45+.85*min(1,amplitude/norm))
        for j in range(len(xy)):
            q=(j+1)%len(xy)
            speed=np.linalg.norm(xy[q]-xy[j]);dwell=1/(1+speed*.45)
            sweep=.72+.28*((j/768-t*.7)%1)
            cv2.line(energy,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[q]).astype(int)),float(level*dwell*sweep),1,cv2.LINE_AA)
        energy=cv2.GaussianBlur(energy,(0,0),.6)
        records.append({'song_frame':971+f,'center':center(t).tolist(),'rms':amplitude,'period_samples':period})
    trail=trail*.44+energy
    light=trail*2.6+cv2.GaussianBlur(trail,(0,0),3)*3.3+cv2.GaussianBlur(trail,(0,0),10)*4
    rgb=frame.astype(np.float32)/255
    # Screen-add cyan phosphor, preserved original plate, no camera shake/grade.
    result=np.clip(rgb+light[:,:,None]*np.array([1.,.85,.32]),0,1)
    cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),np.rint(result*255).astype(np.uint8))
cap.release()
for name,inputargs in [('preview',['-framerate','24','-i',OUT/'frames/%04d.png']),('without_fx',['-i',OUT/'raw.mp4'])]:
 run(['ffmpeg','-v','error','-y',*inputargs,'-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=40.458333333333:end=45.083333333333,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','111','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/f'{name}.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'sprite.json').write_text(json.dumps({'driver':'phase-folded rectified vocal waveform, three cycles per revolution; adapted from scope Rosette','guide_song_origin':899,'rosette_song_start':1030,'records':records},indent=2))
print('Existing take extended through1082;111-frame rosette trial ready.')
