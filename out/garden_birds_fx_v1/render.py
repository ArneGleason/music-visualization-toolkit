"""Lantern response and chrome glints, isolated phrase-timed bird audition."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
OUT.mkdir(exist_ok=True);(OUT/'frames').mkdir(exist_ok=True)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stems=Path(local['sources']['stems'])
def audio(pattern):
 paths=list(stems.glob(pattern));assert len(paths)==1,(pattern,paths)
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-ar','12000','-f','f32le','-'])
 return np.frombuffer(data,dtype='<f4')
voice=audio('*Lead Vocal*restored.wav');drums=audio('*Drum Kit*restored.wav')
def levels(a):
 vals=[]
 for sf in range(1700,1786):
  i=round((sf/24-.178348)*12000);part=a[max(0,i-120):i+121]
  vals.append(float(np.sqrt(np.mean(part*part))))
 return np.asarray(vals)/max(np.quantile(vals,.9),.001)
v=levels(voice);d=levels(drums)
def smooth(a):
 a=np.clip(a,0,1);return a*a*(3-2*a)
y,x=np.mgrid[:720,:1280].astype(np.float32)
lamps=[(556,14,50,70),(774,130,48,64),(520,209,50,80),(733,275,57,78),(669,392,38,64),(609,468,60,78),(678,563,45,66)]
cap=cv2.VideoCapture(str(ROOT/'clips/raw/forest_fauna_birds_v6.mp4'))
state=0.;previous=None;records=[]
for i,sf in enumerate(range(1710,1786)):
 ok,f=cap.read();assert ok
 pic=f.astype(np.float32)/255;b,g,r=cv2.split(pic)
 gray=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY);hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
 beat=min(d[i+10],1.4);state+= (beat-state)*(.62 if beat>state else .22)
 voice_level=min(v[i+10],1.3)
 woke=smooth((sf-1739)/4)*(1-smooth((sf-1752)/13))
 settle=1-.55*smooth((sf-1768)/14)
 warm=np.clip((r-b-.08)*4,0,1)*np.clip((r-.2)*2.8,0,1)
 all_lamps=np.zeros_like(r);core=np.zeros_like(pic)
 for j,(cx,cy,rx,ry) in enumerate(lamps):
  region=np.exp(-(((x-cx)/rx)**4+((y-cy)/ry)**4))
  matte=warm*region
  all_lamps=np.maximum(all_lamps,region)
  # Small staggered acknowledgement flows down the hanging cluster on woke.
  arrival=1741+j*1.4
  ack=np.exp(-((sf-arrival)/4.8)**2)
  gain=(.14+.36*state+.10*voice_level+.75*ack)*settle
  local=cv2.GaussianBlur(matte,(0,0),1.3)*gain
  core+=local[:,:,None]*np.array([.12,.43,1.],np.float32)
 bloom=cv2.GaussianBlur(core,(0,0),8)*.58+cv2.GaussianBlur(core,(0,0),24)*.28
 # Chrome selection follows the moving highlight itself. Motion gating avoids
 # coloring still water/foliage; soft color masks avoid hard tracked outlines.
 if previous is None:
  motion=np.ones_like(r)
 else:
  diff=cv2.absdiff(gray,previous).astype(np.float32)/255
  motion=np.clip(cv2.GaussianBlur(diff,(0,0),4)*18,0,1)
 previous=gray
 silver=np.clip((1-hsv[:,:,1].astype(np.float32)/100),0,1)*np.clip((r-.32)*3,0,1)
 silver*=1-np.clip(all_lamps*1.5,0,1)
 area=(x>175)&(x<1100)&(y>130)&(y<705)
 silver*=area*(.28+.72*motion)
 glint=cv2.GaussianBlur(silver,(0,0),.75)*(.16+.32*state+.40*woke)*settle
 pearl=glint[:,:,None]*np.array([1.,.74,.86],np.float32)
 pearl+=cv2.GaussianBlur(pearl,(0,0),4)*.8
 result=np.clip((pic+core+bloom+pearl)*255,0,255).astype(np.uint8)
 cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),result)
 records.append({'song_frame':sf,'drum':float(state),'voice':float(voice_level),'woke':float(woke),'settle':float(settle)})
def run(a,**kw):subprocess.run([str(q) for q in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','76','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/garden_waking_v3/shotlist.json').read_text());cues=json.loads((ROOT/'out/garden_waking_v3/overlay_cues.json').read_text())
shot=dict(edl['shots'][-1]);shot.update(id='garden_birds_fx_audition',setup='forest_fauna_birds',start_sec=1710/24,end_sec=1786/24,dur_sec=76/24,frames=76,clip={'file':'out/garden_birds_fx_v1/clean.mp4','in_sec':0,'speed':1})
shot.update(lyric='And whatever woke is waiting',description='Chrome hummingbirds hovering at warm hanging seed lanterns; musical light response.',prompt='',still='Chrome hummingbirds at seed lanterns. Existing motion plate, not a generation prompt.')
shot.pop('start_barbeat',None)
cue=dict(cues['shots'][-1]);cue.update(id=shot['id'],setup=shot['setup'],start=1710,end=1786,lyric='And whatever woke is waiting')
# Isolated test only. Do not invent coverage for the pending walking cut.
edl['shots']=[shot];cues['shots']=[cue];edl['duration_sec']=cues['duration_sec']=1786/24;cues['frames']=1786
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','1710','--end','1785','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex','[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=71.25:end=74.416666666667,asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','76','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[1710,1786],'source_frames':[0,76],'source':'clips/raw/forest_fauna_birds_v6.mp4','fx':'Warm localized lamp pulses and pearl/violet chrome highlights; drum energy plus word-timed woke cascade, release on waiting. Image-derived masks, not full object/3D tracking.','mastering':False,'processed_handles':0,'diagnostics':records},indent=2))
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Bird audition complete,76frames, exact master timing.')
