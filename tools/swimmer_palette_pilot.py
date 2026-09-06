"""Two matched palette trials on a tracked subset of surface swimmers."""
import json
import pathlib
import sys
import math
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
import numpy as np
from tracked_light_pilot import run,linear,display
OUT=ROOT/'out/swimmer_palette_pilot'
SHOT=sys.argv[sys.argv.index('--shot')+1] if '--shot' in sys.argv else 's044'
FULL='--full' in sys.argv
if FULL: OUT=ROOT/'out/swimmer_fx_full'/SHOT


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name in ('cyan','violet'): (OUT/name).mkdir(exist_ok=True)
    cues=json.loads((ROOT/'generated/overlay_cues.json').read_text())
    cue=next(s for s in cues['shots'] if s['id']==SHOT)
    first=cue['start']; count=48
    shot=next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots'] if s['id']==SHOT)
    if FULL:
        first=round(shot['start_sec']*24); count=round(shot['end_sec']*24)-first
    overhead=shot['setup']=='basin_kaleidoscope_top'
    assert shot['clip']['speed']==1
    local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
    paths=list(pathlib.Path(local['sources']['stems']).glob('*Drum Kit*restored.wav')); assert len(paths)==1
    raw=run(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-af',
        'highpass=f=100,lowpass=f=2800,aresample=8000','-f','f32le','-'])
    audio=np.frombuffer(raw,'<f4')
    tracks=json.loads((ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())['tracks']
    offset=next(t['offsetSec'] for t in tracks if t['id']=='drums')
    times=np.arange(first/24,(first+count)/24,1/192)
    rms=[]
    for t in times:
        i=int((t-offset)*8000); rms.append(np.sqrt(np.mean(audio[i-80:i+1]**2)))
    rms=np.array(rms); onset=np.maximum(rms-np.roll(rms,4),0); onset[:4]=0
    candidates=[i for i in range(1,len(onset)-1) if onset[i]>onset[i-1] and onset[i]>=onset[i+1]
                and times[i]>first/24+.4 and times[i]<(first+count)/24-.2]
    chosen=[]
    for i in sorted(candidates,key=lambda i:onset[i],reverse=True):
        if all(abs(times[i]-times[j])>.55 for j in chosen): chosen.append(i)
        if len(chosen)==(4 if FULL else 2): break
    events=[float(times[i]) for i in sorted(chosen)]
    cap=cv2.VideoCapture(str(ROOT/shot['clip']['file']))
    cap.set(cv2.CAP_PROP_POS_FRAMES,round(shot['clip']['in_sec']*24))
    # Torso anchors and local ellipses; not full-body segmentation.
    anchors=[(640,310,45,22,.30),(445,407,55,24,.15),(835,412,55,24,.15),(625,533,70,30,0.)]
    if overhead: anchors=[]
    yy,xx=np.mgrid[:720,:1280]
    colors={'cyan':np.array([.10,.70,.85]),'violet':np.array([.57,.24,.88])}
    if FULL: colors.pop('cyan')
    for name,c in colors.items(): colors[name]=c*(.52/np.dot(c,[.2126,.7152,.0722]))
    previous=None; state=[]; records=[]
    for f in range(count):
        ok,frame=cap.read(); assert ok
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if previous is None:
            for x,y,rx,ry,lead in anchors:
                roi=(((xx-x)/rx)**2+((yy-y)/ry)**2<1).astype(np.uint8)*255
                p=cv2.goodFeaturesToTrack(gray,45,.012,4,mask=roi)
                assert p is not None and len(p)>=6
                state.append([p.copy(),p.copy()])
        core=np.zeros((720,1280),np.float32); rec=[]
        lum=linear(frame[:,:,::-1].astype(np.float32)/255).mean(axis=2)
        for k,(x,y,rx,ry,lead) in enumerate(anchors):
            original,p=state[k]
            if previous is not None:
                q,status,_=cv2.calcOpticalFlowPyrLK(previous,gray,p,None,winSize=(25,25),maxLevel=3)
                back,bs,_=cv2.calcOpticalFlowPyrLK(gray,previous,q,None,winSize=(25,25),maxLevel=3)
                good=(status.ravel()>0)&(bs.ravel()>0)&(np.linalg.norm(back-p,axis=2).ravel()<1.)
                original=original[good]; p=q[good]
            assert len(p)>=5,(f,k,'track lost')
            movement=np.median(p[:,0]-original[:,0],axis=0)
            state[k]=[original,p]
            cx,cy=np.array([x,y])+movement
            mask=np.exp(-2*(((xx-cx)/rx)**2+((yy-cy)/ry)**2)).astype(np.float32)
            t=(first+f+.5)/24
            pulse=sum((1-math.exp(-(t-(hit-lead))/.025))*math.exp(-(t-(hit-lead))/.14)
                      for hit in events if 0<t-(hit-lead)<.65)
            # Current reflections drive detail, not a flat glowing torso silhouette.
            highlights=np.clip((lum-.07)/.32,0,1)**1.3
            core+=mask*highlights*pulse*1.9
            rec.append({'centre':[float(cx),float(cy)],'points':len(p),'pulse':pulse})
        if overhead:
            # Current-frame silver selection within the pool; no individual IDs.
            rgb=frame[:,:,::-1].astype(np.float32)/255
            silver=np.clip((rgb.min(axis=2)-.24)/.45,0,1)
            silver*=np.clip(1-(rgb.max(axis=2)-rgb.min(axis=2))/.25,0,1)
            rr=np.sqrt(((xx-640)/450)**2+((yy-350)/300)**2)
            region=np.clip((1-rr)/.13,0,1)*np.clip((rr-.10)/.08,0,1)
            angle=np.arctan2(yy-350,xx-640)
            t=(first+f+.5)/24
            pulsemap=np.zeros_like(core)
            for j,hit in enumerate(events):
                # Opposed sectors sweep together, then the ensemble answers.
                lead=.30*(1+np.cos(2*angle-j*math.pi/2))/2
                age=t-hit+lead
                response=(1-np.exp(-np.maximum(age,0)/.025))*np.exp(-np.maximum(age,0)/.14)
                pulsemap+=np.where((age>0)&(age<.65),response,0)
            core=region*silver*pulsemap*1.9
            rec=[{'selected_pixels':int(np.sum(region*silver>.1))}]
        halo=cv2.GaussianBlur(core,(0,0),6)*.75+cv2.GaussianBlur(core,(0,0),17)*.30
        base=linear(frame[:,:,::-1].astype(np.float32)/255)
        for name,color in colors.items():
            glow=core[:,:,None]*np.array([.88,.92,1.])*1.1+halo[:,:,None]*color
            result=(display(base+glow)*255+.5).astype(np.uint8)[:,:,::-1]
            cv2.imwrite(str(OUT/name/f'{f:04d}.png'),result)
        if f in (0,count//2,count-1):
            check=frame.copy()
            for item,(_,_,rx,ry,_) in zip(rec,anchors):
                cv2.ellipse(check,tuple(np.round(item['centre']).astype(int)),(rx,ry),0,0,360,(0,255,0),1)
            cv2.imwrite(str(OUT/f'track_{f:04d}.jpg'),check)
        records.append({'song_frame':first+f,'groups':rec}); previous=gray
    cap.release()
    for name in colors:
        run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/name/'%04d.png'),
             '-ss',str(first/24),'-i',str(ROOT/'audio/song.wav'),'-t',str(count/24),
             '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
             '-movflags','+faststart',str(OUT/(name+'.mp4'))])
        if FULL:
            run(['ffmpeg','-y','-v','error','-i',str(OUT/(name+'.mp4')),'-map','0:v:0','-c:v','copy','-an',str(OUT/'clean.mp4')])
    (OUT/'controls.json').write_text(json.dumps({'shot':SHOT,'song_frames':[first,first+count],
        'full':FULL,'overhead':overhead,'shotlist_frames_field':shot['frames'],
        'events':events,'source':shot['clip'],'stem_offset':offset,'frames':records,
        'palette_linear_rgb':{n:c.tolist() for n,c in colors.items()},
        'limitations':('current-frame silver selection in authored pool region; no individual tracks' if overhead else 'translation-only torso tracks; no limb/face segmentation'),
        'timing_mismatch':FULL and count!=shot['frames']},indent=2))
    print('DONE:', SHOT, count, 'frames', ', '.join(colors))


if __name__=='__main__': main()
