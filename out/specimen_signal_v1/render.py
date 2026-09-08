"""Vocal-driven internal specimen light with moving source-colour masks."""
import json,sys,subprocess,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
(OUT/'frames').mkdir(exist_ok=True)
def smooth(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem),
    '-af',f'atrim=start={2016/24-.178348}:duration={106/24},asetpts=PTS-STARTPTS',
    '-ac','1','-ar','24000','-f','f32le','-']),dtype=np.float32)
energy=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(106)])
energy=np.clip(energy/max(np.percentile(energy,90),1e-6),0,1)
for i in range(1,106):energy[i]=max(energy[i],energy[i-1]*.68)
cap=cv2.VideoCapture(str(ROOT/'out/specimen_discovery_v1/base.mp4'))
cap.set(cv2.CAP_PROP_POS_FRAMES,12)
y,x=np.mgrid[:720,:1280].astype(np.float32)
records=[]
for i,sf in enumerate(range(2016,2122)):
    ok,f=cap.read();assert ok
    pic=f.astype(np.float32)/255;b,g,r=cv2.split(pic)
    # Restricted prop region; only its warm luminous internal structure seeds light.
    roi=np.exp(-(((x-829)/74)**6+((y-239)/93)**6))
    warm=np.clip((g-b-.035)*12,0,1)*np.clip((r-b-.09)*9,0,1)
    warm*=np.clip((g-.48)*5,0,1)*(1-smooth((r-g-.19)/.09))*roi
    # Silver foreground gloves are neutral; exclude their silhouette and bloom spill.
    neutral=(1-smooth((np.maximum.reduce([r,g,b])-np.minimum.reduce([r,g,b])-.035)/.065))
    glove=neutral*smooth((y-265)/30)*smooth((g-.27)/.12)
    visible=1-cv2.GaussianBlur(glove,(0,0),1.2)
    warm*=visible
    mass=float(warm.sum())
    cx=float((warm*x).sum()/max(mass,1e-6));cy=float((warm*y).sum()/max(mass,1e-6))
    # Moving highlight coordinates derived anew from the visible prop each frame.
    theta=np.arctan2(y-cy,x-cx)
    phase=(sf-2065)*.24
    sweep=np.exp(-np.mod(phase-theta,2*np.pi)/.85)
    acquired=smooth((sf-2062)/8)
    response=.13+.42*energy[i]+acquired*(.30+1.05*energy[i])
    punctuation=np.exp(-((sf-2087)/5)**2)*.45
    settle=1-.38*smooth((sf-2111)/10)
    signal=cv2.GaussianBlur(warm,(0,0),.8)*(response+punctuation)*settle*(.6+acquired*.8*sweep)
    core=signal[:,:,None]*np.array([.18,.62,1.],np.float32)
    bloom=cv2.GaussianBlur(core,(0,0),4)*.9+cv2.GaussianBlur(core,(0,0),11)*.65
    # Keep effect inside/near prop and away from face. No full-object outline.
    confinement=np.exp(-(((x-829)/84)**6+((y-239)/104)**6))*visible
    emitted=(core+bloom)*confinement[:,:,None]
    result=pic+(1-pic)*(1-np.exp(-emitted*1.25))
    cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(result*255,0,255).astype(np.uint8))
    records.append({'song_frame':sf,'vocal_envelope':float(energy[i]),'mask_mass':mass,'visible_light_centroid':[cx,cy]})
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','106','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/specimen_discovery_review_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/specimen_discovery_review_v1/overlay_cues.json').read_text())
shot=next(s for s in edl['shots'] if s['id']=='exchange_listener_audition')
shot['clip']={'file':'out/specimen_signal_v1/clean.mp4','in_sec':0,'speed':1}
shot['description']='Vocal-reactive internal spiral activation; stronger on discovery hold, no lip sync.'
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','1973','--end','2198','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={1973/24}:end={2199/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','226','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[2016,2122],'source':'out/specimen_discovery_v1/base.mp4','source_frames':[12,118],'source_origin':2004,'preview_song_frames':[1973,2199],'method':'Per-frame warm structure masks and centroid-following circulating highlight; vocal RMS attack/release, acquisition2062..2070, fuller2087 response. Neutral foreground glove exclusion. Approximate colour-based occlusion, not a solved3D track or manual roto.','vocal_stem':str(stem),'stem_offset_seconds':.178348,'mastering':False,'handles_rendered':0,'diagnostics':records},indent=2))
print('Specimen activation preview ready.')
