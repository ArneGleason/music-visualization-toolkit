"""Two vocal-driven messenger hoops form a projected 3D blossom and spin."""
import json,sys,subprocess,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
(OUT/'frames').mkdir(exist_ok=True)
def smooth(v):
    v=np.clip(v,0,1);return v*v*(3-2*v)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem),'-af',
    f'atrim=start={2265/24-.178348}:duration=7,asetpts=PTS-STARTPTS,highpass=f=80,lowpass=f=1500',
    '-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
norm=max(float(np.quantile(np.abs(audio),.94)),.001)
angle=np.linspace(0,2*np.pi,512,endpoint=False)
phase=np.arange(512)/512
trail=[np.zeros((720,1280),np.float32) for _ in range(2)]
period=40.;level=0.;radial=np.zeros(512)
cap=cv2.VideoCapture(str(ROOT/'clips/raw/mars_domes_wide_v6.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,12)
records=[]
for i,sf in enumerate(range(2271,2399)):
    ok,f=cap.read();assert ok
    center=round((sf-2265)/24*8000)
    chunk=audio[max(0,center-256):center+256].astype(float);chunk-=chunk.mean()
    rms=float(np.sqrt(np.mean(chunk**2)));level=max(min(1,rms/norm*2),level*.72)
    corr=np.correlate(chunk,chunk,'full')[len(chunk)-1:]
    candidates=np.arange(22,90);scores=corr[candidates]/(len(chunk)-candidates)
    peaks=np.flatnonzero((scores[1:-1]>scores[:-2])&(scores[1:-1]>=scores[2:]))+1
    if len(peaks) and rms>.002:period=.8*period+.2*candidates[peaks[np.argmax(scores[peaks])]]
    lo=max(1,center-int(period));hi=min(len(audio)-1,center+int(period))
    cross=np.flatnonzero((audio[lo-1:hi-1]<=0)&(audio[lo:hi]>0))+lo
    origin=cross[np.argmin(abs(cross-center))] if len(cross) else center
    wave=sum(np.interp(origin+(phase+k)*period,np.arange(len(audio)),audio) for k in [-1,0,1])/(3*norm)
    radial=.55*radial+.45*np.tanh(np.abs(wave)*1.8)
    light=np.zeros((720,1280,3),np.float32)
    formation=smooth((sf-2330)/34)
    spin=smooth((sf-2364)/35)*np.pi*1.65
    for side,(entry,color) in enumerate([(2308,np.array([1.,.80,.20])),(2315,np.array([.10,.50,1.]))]):
        if sf<entry:continue
        arrival=smooth((sf-entry)/28)
        progress=(sf-entry)/24
        cx=(180 if side==0 else 1100)*(1-arrival)+640*arrival
        cy=260+(1-arrival)*95*np.sin(progress*4+side*np.pi)
        radius=(24+125*arrival+34*formation)*(1+.09*level)
        radius_vector=radius*(1+(.08+.17*formation)*radial+.16*formation*np.sin(5*angle+side*.5))
        theta=angle+progress*.4
        px=radius_vector*np.cos(theta);py=radius_vector*np.sin(theta)
        # Perpendicular loop planes share one center, forming a world in depth.
        tilt=(.28 if side==0 else 1.25)*formation
        xyz=np.stack([px,py*np.cos(tilt),py*np.sin(tilt)],axis=1)
        yaw=spin+.45*formation
        rot=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
        xyz=xyz@rot.T
        pitch=.18+.24*formation
        rot=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]])
        xyz=xyz@rot.T
        perspective=850/(850-xyz[:,2])
        xy=xyz[:,:2]*perspective[:,None]+np.array([cx,cy])
        energy=np.zeros((720,1280),np.float32)
        fade=smooth((sf-entry)/5)
        for j in range(512):
            q=(j+1)%512;distance=np.linalg.norm(xy[q]-xy[j]);dwell=1/(1+distance*.16)
            scan=.6+.4*np.exp(-np.mod(progress*3-angle[j],2*np.pi)/1.3)
            depth=.68+.32*(xyz[j,2]/max(radius,1)+1)/2
            intensity=(.65+1.05*level)*fade*dwell*scan*depth
            cv2.line(energy,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[q]).astype(int)),float(intensity),2 if xyz[j,2]<0 else 3,cv2.LINE_AA)
        trail[side]=trail[side]*.48+energy*.70
        beam=trail[side]*1.8+cv2.GaussianBlur(trail[side],(0,0),3)*2+cv2.GaussianBlur(trail[side],(0,0),10)*2.3
        light+=beam[:,:,None]*color
    pic=f.astype(np.float32)/255
    result=pic+(1-pic)*(1-np.exp(-light*1.7))
    cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(result*255,0,255).astype(np.uint8))
    records.append({'song_frame':sf,'vocal_level':level,'formation':float(formation),'spin_radians':float(spin)})
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','128','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/next_mars_sequence_v1/shotlist.json').read_text());cues=json.loads((ROOT/'out/next_mars_sequence_v1/overlay_cues.json').read_text())
edl['shots'][-1]['clip']={'file':'out/colony_world_blossom_v1/clean.mp4','in_sec':0,'speed':1}
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2233','--end','2398','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={2233/24}:end={2399/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','166','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[2271,2399],'source_frames':[12,140],'preview_song_frames':[2233,2399],'method':'Two phase-folded vocal radial traces approach on curved paths, assemble in perpendicular3D planes into a five-lobed world blossom, rotate on spin. Perspective projection, depth intensity, dwell weighting, circulating beam peak, persistence and bloom. Screen-positioned floating objects, not tracked physical set objects.','entries':[2308,2315],'formation':[2330,2364],'spin':[2364,2399],'stem_offset_seconds':.178348,'diagnostics':records,'mastering':False},indent=2))
print('World blossom preview ready.')
