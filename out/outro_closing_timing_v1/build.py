"""Closing editorial timing study. Old A3/B3 stand-ins, not new performances."""
from pathlib import Path
import sys,json,subprocess,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'));sys.path.insert(0,str(ROOT/'tools'))
import cv2
from assembly_timebase import conform_clip
def load(p):
    p=conform_clip(ROOT,{'file':str(ROOT/p),'speed':1},24,prepare=True)['file']
    cap=cv2.VideoCapture(p);fs=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        fs.append(f)
    cap.release();return fs
A=load('clips/outro/A3_kling.mp4');B=load('clips/outro/B3_kling.mp4')
M=load('clips/raw/colony_goodnight_cascade_v6.mp4')
artifact=load('out/outro_B2_afterglow_v1/clean.mp4')
lead=load('out/outro_exchange_fx_v1/preview.mp4')
def smooth(a,b,t):
    u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
def close(f,z,cx=640,cy=350):
    w=1280/z;h=720/z
    x0=np.clip(cx-w/2,0,1280-w);y0=np.clip(cy-h/2,0,720-h)
    return cv2.warpAffine(f,np.float32([[z,0,-x0*z],[0,z,-y0*z]]),(1280,720))
def caption(f,s):
    cv2.rectangle(f,(0,0),(1280,32),(15,15,15),-1)
    cv2.putText(f,s,(16,23),cv2.FONT_HERSHEY_SIMPLEX,.55,(220,220,220),1,cv2.LINE_AA)
    return f
y,x=np.mgrid[:720,:1280].astype(np.float32)
writer=cv2.VideoWriter(str(OUT/'silent.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(1280,720))
assert writer.isOpened()
# Lead-in begins at the accepted A2 discovery line, preserving exact source clock.
for song in range(4362,4854):
    if song<4504:
        f=lead[song-4177].copy()
        label='Accepted lead-in'
    elif song<4557:
        f=close(A[song-4500],1.09+.035*smooth(4504,4557,song),600,345)
        label='TIMING STUDY: older performance / closer framing'
    elif song<4574:
        # Current artifact, isolated from face; a tiny deliberate answering bloom.
        f=cv2.resize(artifact[90+song-4557][455:710,465:835],(1280,720))
        glow=np.exp(-((x-640)/225)**2-((y-360)/240)**2)*.12*math.sin(math.pi*(song-4557)/17)**2
        f=np.clip(f.astype(float)+(255-f)*glow[:,:,None],0,255).astype(np.uint8)
        label='To who? / artifact answers (temporary crop)'
    elif song<4622:
        f=close(A[song-4500],1.125,600,345)
        label='TIMING STUDY: sung phrase / settle'
    elif song<4644:
        f=close(B[song-4500],1.08,640,345)
        label='TIMING STUDY: You first / room-light action pending new take'
    elif song<4671:
        f=A[song-4500].copy()
        # Approximate CRT shutdown on old stand-in screen; no physical hand action.
        off=smooth(4661,4670,song)
        screen=np.exp(-((x-1240)/155)**8-((y-540)/190)**8)
        f=(f*(1-.93*screen[:,:,None]*off)).astype(np.uint8)
        line=np.exp(-((y-525)/(max(1,25*(1-off))))**2-((x-1200)/(max(3,100*(1-off))))**2)*off*(1-off)*2
        f=np.clip(f+line[:,:,None]*np.array([180,230,220]),0,255).astype(np.uint8)
        label='Night / TV shutdown sketch; switch gesture still to generate'
    elif song<4689:
        f=B[song-4500].copy()
        off=smooth(4681,4688,song)
        f=(f*(1-.64*off)).astype(np.uint8)
        label='Night / dim-room sketch; switch gesture still to generate'
    elif song<4782:
        f=M[song-4689].copy() # ONE uninterrupted93-frame moving view.
        iris=1-smooth(4754,4782,song)
        radius=math.hypot(640,360)*iris
        mask=np.clip((radius-np.sqrt((x-640)**2+(y-360)**2))/4,0,1)
        f=(f*mask[:,:,None]).astype(np.uint8)
        label='One continuous Mars night view / iris'
    else:
        f=np.zeros((720,1280,3),np.uint8)
        t=song-4782
        # Layout-only assembling title. Exact approved provenance copy unresolved.
        for j,word in enumerate(['CLOSING','TITLE']):
            a=smooth(j*5,j*5+14,t)
            xx=int(350+j*320+(1-a)*(-90 if j==0 else 90))
            cv2.putText(f,word,(xx,320),cv2.FONT_HERSHEY_SIMPLEX,1.3,tuple(int(c*a) for c in (180,220,245)),2,cv2.LINE_AA)
        a=smooth(12,28,t)
        cv2.putText(f,'Short provenance card - layout placeholder',(290,395),cv2.FONT_HERSHEY_SIMPLEX,.8,tuple(int(c*a) for c in (180,180,180)),1,cv2.LINE_AA)
        label='Proposed 3-second post-music title hold / not final wording'
    f=caption(f,label)
    writer.write(f)
    if song in [4530,4564,4668,4700,4799]:cv2.imwrite(str(OUT/f'check_{song}.jpg'),f)
writer.release()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'silent.mp4'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={4362/24}:end={4782/24},asetpts=PTS-STARTPTS,apad=whole_dur={492/24}[a]','-map','0:v','-map','[a]','-frames:v','492','-t',str(492/24),'-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview.mp4'),'-f','null','-'],check=True)
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(OUT/'preview.mp4')]))
assert p['streams'][0]['nb_read_frames']=='492' and p['streams'][0]['r_frame_rate']=='24/1'
(OUT/'verification.json').write_text(json.dumps({'song_start':4362,'song_end':4782,'post_music_frames':72,'total_frames':492,'fps':24,'mars_source':[0,93],'iris_song':[4754,4782],'artifact_song':[4557,4574],'production_changed':False,'old_A3_B3_origin':4500},indent=2))
print('Closing timing study verified:492frames; no new generations.')
