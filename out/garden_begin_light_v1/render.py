"""Seed-lantern light propagation and word-timed arrival, existing motion."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
OUT.mkdir(exist_ok=True);(OUT/'frames').mkdir(exist_ok=True)
y,x=np.mgrid[:720,:1280].astype(np.float32)
def smooth(a):
 a=np.clip(a,0,1);return a*a*(3-2*a)
# Source is nearly frontal, with small natural movement. Actual source colour
# supplies the moving light masks; depth ordering is authored, not a 3D solve.
depth=np.clip(np.maximum(np.abs(x-640)/620,(y-230)/480),0,1)
body=1-smooth((np.sqrt(((x-640)/125)**2+((y-415)/330)**2)-.92)/.25)
face=np.exp(-(((x-640)/92)**4+((y-182)/83)**4))
protection=1-np.maximum(body,face)
pods=[(193,320,24),(270,320,23),(310,265,13),(287,365,16),
 (355,393,31),(283,423,29),(355,485,27),(402,540,22),
 (342,581,32),(250,632,30),(149,680,30),(79,550,40),(24,456,31)]
pod_region=np.zeros_like(x)
for cx,cy,rad in pods:
 for px in (cx,1280-cx):
  pod_region=np.maximum(pod_region,np.exp(-(((x-px)/rad)**4+((y-cy)/(rad*1.25))**4)))
cap=cv2.VideoCapture(str(ROOT/'clips/raw/forest_awakening_frontal_v6.mp4'))
records=[]
for i,sf in enumerate(range(1786,1841)):
 ok,f=cap.read();assert ok
 pic=f.astype(np.float32)/255;b,g,r=cv2.split(pic)
 warm=np.clip((r-b-.06)*4,0,1)*np.clip((r-.32)*3,0,1)
 pink=np.clip((r-g-.06)*4,0,1)*np.clip((b-g-.025)*5,0,1)*np.clip((r-.34)*3,0,1)
 far=(1-smooth((np.abs(x-640)-150)/100))*(1-smooth((y-380)/70))
 warm*=np.maximum(pod_region,far*np.clip((r-.62)*4,0,1)*.5)*protection
 pink*=protection
 # Distant lights respond first; the wave arrives at the nearest pods on begin.
 arrival=1790+38*depth
 wave=np.exp(-((sf-arrival)/6.5)**2)
 begin=smooth((sf-1825)/3)*(1-smooth((sf-1831)/10))
 invitation=smooth((sf-1786)/8)
 gain=(.10*invitation+.85*wave+.95*begin)
 seed=cv2.GaussianBlur(warm,(0,0),1.1)*gain
 flowers=cv2.GaussianBlur(pink,(0,0),1.2)*(.40*wave+.60*begin)
 core=seed[:,:,None]*np.array([.22,.60,1.],np.float32)+flowers[:,:,None]*np.array([.82,.43,.78],np.float32)
 bloom=cv2.GaussianBlur(core,(0,0),7)*.75+cv2.GaussianBlur(core,(0,0),23)*.50
 # Leave likeness/suit untouched by synthetic spill; keep light localized.
 result=pic+(core+bloom)*protection[:,:,None]
 cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(result*255,0,255).astype(np.uint8))
 records.append({'song_frame':sf,'begin_envelope':float(begin),'mean_wave':float(wave.mean())})
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','55','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/garden_walk_guide_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/garden_walk_guide_v1/overlay_cues.json').read_text())
shot=dict(edl['shots'][-1]);shot.update(id='garden_begin_light_audition',setup='forest_awakening_frontal',start_sec=1786/24,end_sec=1841/24,dur_sec=55/24,frames=55,lyric='for the song to begin.',description='Garden lantern light wave arrives on begin, then releases.',prompt='',still='Frontal garden, woman and glowing seed lanterns.',clip={'file':'out/garden_begin_light_v1/clean.mp4','in_sec':0,'speed':1})
edl['shots'].append(shot);cues['shots'].append({'id':shot['id'],'setup':shot['setup'],'section':'scene-04','start':1786,'end':1841,'lyric':shot['lyric']})
edl['duration_sec']=cues['duration_sec']=1841/24;cues['frames']=1841
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','1710','--end','1840','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex','[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=71.25:end=76.708333333333,asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','131','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[1786,1841],'source_frames':[0,55],'source':'clips/raw/forest_awakening_frontal_v6.mp4','preview_song_frames':[1710,1841],'preview_frames':131,'begin_frame':1828,'method':'Source-colour lantern/flower masks, authored distant-to-near light wave, broad begin envelope and release. Existing generated emission retained. Approximate spatial grouping, not solved 3D geometry.','mastering':False,'audio':'master once; source audio discarded','processed_handles':0,'diagnostics':records},indent=2))
print('Garden begin preview complete:131frames, bird then garden response.')
