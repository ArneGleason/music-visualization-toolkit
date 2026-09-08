"""Continuous two-ring message above a genuine two-panel push transition."""
import json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
def smooth(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
def stem_audio(pattern):
    p=next(Path(local['sources']['stems']).glob(pattern))
    a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af',f'atrim=start={2658/24-.178348}:duration={223/24},asetpts=PTS-STARTPTS,highpass=f=80,lowpass=f=1500','-ac','1','-ar','24000','-f','f32le','-']),np.float32)
    return a,max(float(np.quantile(np.abs(a),.94)),.001)
drivers=[stem_audio('*Lead Vocal*restored.wav'),stem_audio('*Guitar*restored.wav')]
colors=[np.array([1.,.8,.2]),np.array([.1,.5,1.])]
angle=np.linspace(0,2*np.pi,384,endpoint=False)
rng=np.random.default_rng(72)
marks=rng.normal(size=(30,3));marks/=np.linalg.norm(marks,axis=1)[:,None];marks*=rng.uniform(.15,.70,(30,1))
trail=np.zeros((720,1280,3),np.float32)
cap=cv2.VideoCapture(str(ROOT/'out/astronaut_reply_v1/base.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,12)
listener=cv2.imread(str(ROOT/'out/meaning_thread_trial_v1/listener_still.jpg'));assert listener is not None
(OUT/'frames').mkdir(exist_ok=True)
records=[]
def pose(sf):
    travel=smooth((sf-2748)/88)
    center=np.array([1000-720*travel,465+98*np.sin(np.pi*travel)])
    radius=102-14*np.sin(np.pi*travel)
    return center,radius
for i,sf in enumerate(range(2658,2881)):
    shift=round(1280*smooth((sf-2786)/40))
    if shift<1280:
        ok,old=cap.read();assert ok
    incoming=listener
    picture=np.zeros((720,1280,3),np.uint8)
    if shift<1280:picture[:,shift:]=old[:,:1280-shift]
    if shift>0:picture[:,:shift]=incoming[:,1280-shift:]
    # Both full frames translate right. The message is a separate continuous layer.
    center,radius=pose(sf);t=(sf-2658)/24
    yaw=.55+t*.58;pitch=.36+.15*np.sin(t*.9)
    ry=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
    rx=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]])
    rotation=rx@ry
    def project(xyz):
        p=xyz@rotation.T
        return p[:,:2]*(850/(850-p[:,2]))[:,None]+center,p[:,2]
    light=np.zeros_like(trail);levels=[]
    entrance=smooth((sf-2658)/18)
    for side,((audio,norm),color) in enumerate(zip(drivers,colors)):
        chunk=audio[i*1000:(i+1)*1000]
        level=min(1,float(np.sqrt(np.mean(chunk**2)))/norm*2);levels.append(level)
        wave=np.tanh(np.interp(np.linspace(0,999,384),np.arange(len(chunk)),chunk)/norm*1.4)
        theta=angle+t*.35
        radial=radius*(1+.10*level+.13*wave+.035*np.sin(5*theta+t))
        px=radial*np.cos(theta);py=radial*np.sin(theta)
        warp=radius*(.11*wave+.045*np.sin(3*theta-t))*level
        tilt=.28 if side==0 else 1.25
        xyz=np.stack([px,py*np.cos(tilt)-warp*np.sin(tilt),py*np.sin(tilt)+warp*np.cos(tilt)],axis=1)
        xy,depth=project(xyz)
        beam=np.zeros((720,1280),np.float32)
        for j in range(384):
            k=(j+1)%384;distance=np.linalg.norm(xy[j]-xy[k])
            dwell=1/(1+distance*.14)
            scan=.65+.45*np.exp(-((t*2-angle[j])%(2*np.pi))/1.1)
            value=(.8+level*.9)*dwell*scan*(.8+.2*depth[j]/radius)*entrance
            cv2.line(beam,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[k]).astype(int)),float(value),2,cv2.LINE_AA)
        light+=beam[:,:,None]*color
    # Sparse non-letter marks: paired bars, small branches, dots within the volume.
    for k,mark in enumerate(marks):
        leak=k<10 and sf>=2755+k*3
        if leak:
            birth=2755+k*3;age=(sf-birth)/24
            if age>2.1:continue
            birth_center,birth_r=pose(birth)
            pos=birth_center+np.array([65+age*55,20+np.sin(k)*25+age*24])
            opacity=(1-age/2.1)**1.5*.8
            size=3
        else:
            xyz=mark*radius*(1+.08*levels[k%2])+np.array([np.sin(t+k)*3,np.cos(t*1.3+k)*3,0])
            points,depth=project(xyz[None,:]);pos=points[0]
            opacity=(.35+.35*levels[k%2])*(.8+.2*depth[0]/radius)*entrance
            size=4+(k%3)
        color=colors[k%2]*opacity
        point=tuple(np.rint(pos).astype(int))
        if k%3==0:cv2.circle(light,point,2,tuple(color),-1,cv2.LINE_AA)
        else:
            a=(point[0]-size,point[1]-size//2);b=(point[0]+size,point[1]+size//2)
            cv2.line(light,a,b,tuple(color),1,cv2.LINE_AA)
            if k%3==1:cv2.line(light,(a[0],a[1]+4),(b[0],b[1]+4),tuple(color),1,cv2.LINE_AA)
            else:cv2.line(light,point,(point[0]+size,point[1]-size),tuple(color),1,cv2.LINE_AA)
    trail=trail*.40+light*.8
    glow=trail*1.25+cv2.GaussianBlur(trail,(0,0),2.5)*1.6+cv2.GaussianBlur(trail,(0,0),9)*2.1
    result=np.clip(picture.astype(np.float32)/255+glow,0,1)
    cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.uint8(result*255))
    records.append({'song_frame':sf,'panel_shift_right_pixels':shift,'object_center':center.tolist(),'radius':radius,'vocal_level':levels[0],'guitar_level':levels[1]})
cap.release()
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','223','-an','-c:v','libx264','-crf','16',OUT/'clean.mp4'])
# Reuse the tested lyric and approved lead-in assembly, changing only the audition picture.
edl=json.loads((ROOT/'out/meaning_thread_trial_v1/shotlist.json').read_text())
for s in edl['shots']:
    if s['id'] in ['meaning_reply_test','meaning_listener_test']:
        s['clip']['file']='out/meaning_orb_pass_v2/clean.mp4'
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_bytes((ROOT/'out/meaning_thread_trial_v1/overlay_cues.json').read_bytes())
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"meaning_orb_pass_v2"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2620','--end','2880','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2620/24}:end={2881/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','261','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'choreography.json').write_text(json.dumps({'status':'movement_test_owner_review_pending','preview_frames':[2620,2881],'push_frames':[2786,2826],'travel_frames':[2748,2836],'records':records},indent=2))
print('Two-ring message pass ready.',flush=True)
