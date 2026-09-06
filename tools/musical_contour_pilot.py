"""One tracked telescope ring, guitar contour and drum-driven radial kicks."""
import json
import math
import pathlib
import sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
import numpy as np
from tracked_light_pilot import run, linear, display
OUT=ROOT/'out/musical_contour_tunnel'
ANALOG='--analog' in sys.argv
if ANALOG:
    OUT=ROOT/'out/musical_contour_tunnel_analog'


def analog_beam(frame, scale, signal, kick, f, history):
    """Ring-local phosphor memory: old traces move with the tracked rim."""
    theta=np.arange(512)*math.tau/512
    sec=f/24
    noise=(.48*np.sin(theta*37+sec*19)+.3*np.sin(theta*83-sec*31)
           +.22*np.sin(theta*131+sec*43))*(1+.35*math.sin(sec*5))
    offset=signal*15+kick*16+noise
    slope=(np.roll(offset,-1)-np.roll(offset,1))/(2*math.tau/512*174*scale)
    dwell=1/np.sqrt(1+slope*slope)
    # Clockwise head, sharp leading edge and one continuous long decay behind it.
    age=(sec*.65+.13-theta/math.tau)%1
    scan=.20+.80*np.exp(-age/.38)
    history.append((offset.copy(),dwell.copy(),scan.copy()))
    del history[:-6]
    # 2x spatial supersampling; temporal persistence below is a separate effect.
    yy,xx=np.mgrid[:1440,:2560].astype(np.float32)
    x=(xx+.5)/2-630; y=((yy+.5)/2-315)*174/172
    radius=np.hypot(x,y)
    index=(np.arctan2(y,x)%math.tau)*512/math.tau
    lo=index.astype(np.int32)%512; frac=index-lo
    def interp(v): return v[lo]*(1-frac)+v[(lo+1)%512]*frac
    beam=np.zeros_like(radius)
    for j,(old,weight,sweep) in enumerate(reversed(history)):
        memory=math.exp(-j/(24*.075))
        if j==0: memory=1.
        else: memory*=.24
        dw=interp(weight)
        distance=(radius-(174*scale+interp(old)))*dw
        width=.45+.85*dw
        intensity=interp(sweep)*(.12+.88*dw)
        core=np.exp(-.5*(distance/width)**2)
        halo=.22*np.exp(-.5*(distance/(2.4+dw*1.5))**2)+.035*np.exp(-.5*(distance/9)**2)
        beam+=memory*intensity*(core+halo)
    beam=cv2.resize(beam,(1280,720),interpolation=cv2.INTER_AREA)
    rgb=linear(frame[:,:,::-1].astype(np.float32)/255)
    rgb+=beam[:,:,None]*np.array([.38,.92,.64],np.float32)*1.05
    return (display(rgb)*255+.5).astype(np.uint8)[:,:,::-1]


def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'frames').mkdir(exist_ok=True)
    cues=json.loads((ROOT/'generated/overlay_cues.json').read_text())
    cue=next(s for s in cues['shots'] if s['id']=='s056')
    first=cue['start']; count=min(48,cue['end']-first)
    shot=next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots'] if s['id']=='s056')
    assert shot['clip']['speed']==1
    cap=cv2.VideoCapture(str(ROOT/shot['clip']['file']))
    cap.set(cv2.CAP_PROP_POS_FRAMES,round(shot['clip']['in_sec']*24))
    local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
    tracks=json.loads((ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())['tracks']
    def stem(name,track):
        paths=list(pathlib.Path(local['sources']['stems']).glob('*'+name+'*restored.wav'))
        assert len(paths)==1,(name,paths)
        raw=run(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-af',
                 'highpass=f=90,lowpass=f=1800,aresample=8000','-f','f32le','-'])
        data=np.frombuffer(raw,'<f4'); offset=next(t['offsetSec'] for t in tracks if t['id']==track)
        return data,offset
    guitar,go=stem('Guitar','guitar'); drums,do=stem('Drum Kit','drums')
    ts=np.arange(first/24-.5,(first+count)/24,1/192)
    envelope=[]
    for t in ts:
        i=int((t-do)*8000); envelope.append(np.sqrt(np.mean(drums[i-80:i+1]**2)))
    envelope=np.array(envelope); onset=np.maximum(envelope-np.roll(envelope,4),0); onset[:4]=0
    chosen=[]
    for i in np.argsort(onset)[::-1]:
        if onset[i]<np.quantile(onset,.90): break
        if all(abs(ts[i]-ts[j])>.3 for j in chosen): chosen.append(int(i))
    events=[(float(ts[i]),float(onset[i]/max(onset.max(),1e-6))) for i in sorted(chosen)]
    start=int((first/24-go)*8000); stop=int(((first+count)/24-go)*8000)
    norm=max(float(np.quantile(np.abs(guitar[start:stop]),.97)),1e-5)
    theta=np.linspace(0,math.tau,512,endpoint=False)
    circle=np.column_stack((630+174*np.cos(theta),315+172*np.sin(theta))).astype(np.float32)
    previous=None; records=[]; history=[]
    for f in range(count):
        ok,frame=cap.read(); assert ok
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if previous is None:
            yy,xx=np.mgrid[:720,:1280]; r=np.hypot(xx-630,yy-315)
            region=((r>153)&(r<193)).astype(np.uint8)*255
            points=cv2.goodFeaturesToTrack(gray,140,.008,5,mask=region)
            original=points.copy()
        else:
            moved,status,_=cv2.calcOpticalFlowPyrLK(previous,gray,points,None,winSize=(31,31),maxLevel=3)
            back,bs,_=cv2.calcOpticalFlowPyrLK(gray,previous,moved,None,winSize=(31,31),maxLevel=3)
            good=(status.ravel()>0)&(bs.ravel()>0)&(np.linalg.norm(back-points,axis=2).ravel()<1.2)
            points=moved[good]; original=original[good]
        assert len(points)>=10,f'Lost ring at {f}'
        # The central star is stationary in this excerpt. Constrain the fit to
        # that observed vanishing point; an unconstrained fit drifts sideways
        # when only one arc retains features.
        pivot=np.array([630.,315.])
        ratios=np.linalg.norm(points[:,0]-pivot,axis=1)/np.linalg.norm(original[:,0]-pivot,axis=1)
        scale=float(np.median(ratios))
        matrix=np.array([[scale,0,630*(1-scale)],[0,scale,315*(1-scale)]],np.float64)
        inliers=(np.abs(ratios-scale)<.06).astype(np.uint8)[:,None]
        assert inliers.sum()>=8
        baseline=cv2.transform(circle[None],matrix)[0]
        centre=cv2.transform(np.array([[[630.,315.]]],np.float32),matrix)[0,0]
        normal=baseline-centre; normal/=np.linalg.norm(normal,axis=1)[:,None]
        t=(first+f+.5)/24
        # Trailing audio window, softly periodic at the seam; no invented note data.
        indices=(t-go-.064+np.arange(512)/8000)*8000
        signal=np.interp(indices,np.arange(len(guitar)),guitar)/norm
        if ANALOG:
            # Asymmetric soft saturation adds harmonic character to the visual
            # drive only. Soundtrack remains unchanged.
            signal=np.tanh(1.35*signal+.14*signal*signal)
            signal-=signal.mean()
            signal*=np.sin(theta/2)**2
        else:
            signal=np.tanh(signal)*np.sin(theta/2)**2
        kick=sum(v*(1-math.exp(-(t-e)/.018))*math.exp(-(t-e)/.14) for e,v in events if 0<t-e<.7)
        contour=baseline+normal*(signal*15+kick*16)[:,None]
        ink=np.zeros_like(frame)
        cv2.polylines(ink,[np.round(contour*4).astype(np.int32)],True,(208,244,225),8,cv2.LINE_AA,shift=2)
        # A drawn contour with restrained halo, not a duplicate brass rim.
        result=np.clip(frame.astype(np.float32)+ink*.92+cv2.GaussianBlur(ink,(0,0),2)*.25,0,255).astype(np.uint8)
        if ANALOG:
            result=analog_beam(frame,scale,signal,kick,f,history)
        cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
        error=np.linalg.norm(cv2.transform(original,matrix)-points,axis=2).ravel()[inliers.ravel()>0]
        records.append({'song_frame':first+f,'inliers':int(inliers.sum()),'median_error_px':float(np.median(error)),
                        'matrix':matrix.tolist(),'kick':kick,'radius_px':float(np.linalg.norm(baseline-centre,axis=1).mean())})
        if f in (0,24,count-1):
            check=frame.copy(); cv2.polylines(check,[baseline.astype(np.int32)],True,(0,255,0),1)
            cv2.imwrite(str(OUT/f'track_{f:04d}.jpg'),check)
        previous=gray
    cap.release()
    run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/'frames/%04d.png'),'-ss',str(first/24),
         '-i',str(ROOT/'audio/song.wav'),'-t',str(count/24),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','256k','-movflags','+faststart',str(OUT/'musical_contour.mp4')])
    (OUT/'tracking.json').write_text(json.dumps({'shot':'s056','song_frames':[first,first+count],
        'source':shot['clip'],'events':events,'guitar_offset':go,'drum_offset':do,
        'analog':ANALOG,'analog_settings':{'scan_hz':.65,'tail_floor':.20,
            'persistence_seconds':.075,'history_frames':6,'supersampling':2,
            'noise':'deterministic modulated harmonics, visual only',
            'dwell':'inverse local path speed','memory_space':'tracked ring local'},
        'method':'local optical flow and similarity fit, not camera solve','frames':records},indent=2))
    print('DONE',len(records),'frames')


if __name__=='__main__': main()
