"""Staging audition: provisional reply, listening still, continuous vocal thread."""
import json,subprocess,sys,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(a,**kw): subprocess.run([str(x) for x in a],check=True,cwd=ROOT,**kw)
def ease(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)
(OUT/'frames').mkdir(exist_ok=True)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem),'-af',f'atrim=start={2658/24-.178348}:duration={223/24},asetpts=PTS-STARTPTS','-ac','1','-ar','24000','-f','f32le','-']),np.float32)
env=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(223)])
env=np.clip(env/max(np.percentile(env,90),1e-5),0,1)
cap=cv2.VideoCapture(str(ROOT/'out/astronaut_reply_v1/base.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,12)
listener=cv2.VideoCapture(str(ROOT/'clips/raw/duet_call_response_sync_v6.mp4'))
listener.set(cv2.CAP_PROP_POS_MSEC,3000);ok,still=listener.read();assert ok;listener.release()
# Extract only the stable astronomer side before the generated scene morphs.
h,w=still.shape[:2];plate=still[int(h*.04):int(h*.52),:int(w*.48)]
plate=cv2.resize(plate,(1280,720));cv2.imwrite(str(OUT/'listener_still.jpg'),plate)
trail=np.zeros((720,1280,3),np.float32)
for i,sf in enumerate(range(2658,2881)):
    if sf<2812:
        ok,pic=cap.read();assert ok
    else:
        z=1+.035*(sf-2812)/69
        pic=cv2.warpAffine(plate,np.array([[z,0,640*(1-z)],[0,z,360*(1-z)]],np.float32),(1280,720),borderMode=cv2.BORDER_REFLECT)
    energy=np.zeros_like(trail)
    if sf>=2748:
        t=(sf-2748)/24;u=np.linspace(0,1,400)
        growth=ease((sf-2748)/22)
        if sf<2812:
            x=1080-1160*u*growth
            y=550-65*np.sin(u*np.pi)+25*np.sin(u*5+t)*growth
        else:
            arrival=ease((sf-2812)/25)
            x=1350-(1060+100*arrival)*u
            y=525+75*np.sin(u*np.pi)+20*np.sin(u*5+t)
        window=audio[i*1000:i*1000+1000]
        wave=np.interp(u,np.linspace(0,1,len(window)),window)
        wave=np.tanh(wave*5)
        y+=wave*(12+30*env[i])*np.sin(u*np.pi)
        # Analog dwell and moving scan head, cyan leading and amber echo.
        for j in range(len(u)-1):
            dwell=1/(1+abs(y[j+1]-y[j])*.10)
            scan=.45+.55*np.exp(-((u[j]-t*.4)%1)*3)
            strength=(.6+env[i]*1.2)*dwell*scan*growth
            a=tuple(np.rint([x[j],y[j]]).astype(int));b=tuple(np.rint([x[j+1],y[j+1]]).astype(int))
            cv2.line(energy,a,b,(strength,strength*.78,strength*.20),2,cv2.LINE_AA)
            cv2.line(energy,(a[0]+12,a[1]+12),(b[0]+12,b[1]+12),(strength*.12,strength*.45,strength*.95),1,cv2.LINE_AA)
        fade=1-ease((sf-2868)/13)
        energy*=fade
    trail=trail*.55+energy*.65
    glow=trail*1.1+cv2.GaussianBlur(trail,(0,0),3)*1.6+cv2.GaussianBlur(trail,(0,0),12)*2.8
    result=np.clip(pic.astype(np.float32)/255+glow,0,1)
    cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.uint8(result*255))
cap.release()
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','223','-an','-c:v','libx264','-crf','17',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/lipsync_followup_review_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/lipsync_followup_review_v1/overlay_cues.json').read_text())
for ident,start,end,lyric in [('meaning_reply_test',2658,2812,'Sometimes. Not always. Meaning leaves thread.'),('meaning_listener_test',2812,2881,'Words leave words.')]:
    s=copy.deepcopy(edl['shots'][-1]);s.update(id=ident,setup=ident,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start,lyric=lyric,clip={'file':'out/meaning_thread_trial_v1/clean.mp4','in_sec':(start-2658)/24,'speed':1})
    edl['shots'].append(s);cues['shots'].append({'id':ident,'setup':ident,'section':'meaning_exchange','start':start,'end':end,'lyric':lyric})
edl['duration_sec']=cues['duration_sec']=2881/24;cues['frames']=2881
for name,d in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(d,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"meaning_thread_trial_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2620','--end','2880','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2620/24}:end={2881/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','261','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'REVIEW.md').write_text('''# Meaning thread staging test

Preview2620..2881: approved question and meant insert, then proposed reply and listener.
No generation, no production changes. Astronaut uses original reply base12..166 as an explicitly provisional performance, NOT verified lip sync for these words. Listener is a still extracted at3seconds from the left half of original duet, with a3.5percent procedural push. No looping or slowed footage. Stills are deliberate placeholders.
Thread starts2748, cyan with amber echo, vocal amplitude and waveform driven at the actual song clock. Crosses picture cut2812 and fades before2881. Flat lyrics/master once.
Judge exchange structure and musical-thread concept. Performance replacement and final tracking/occlusion remain pending. Not an approved delivery.
''')
print('Meaning thread audition ready.',flush=True)
