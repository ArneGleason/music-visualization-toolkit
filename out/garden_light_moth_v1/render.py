import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
def pulse(f,on,off):return smooth((f-on)/3)*(1-smooth((f-off)/9))
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'));assert len(stem)==1
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem[0]),'-ac','1','-ar','12000','-f','f32le','-']),dtype='<f4')
def rms(sf):
 i=round((sf/24-.178348)*12000);a=audio[i-120:i+121];return float(np.sqrt(np.mean(a*a)))
ref=max(np.quantile([rms(f) for f in range(1412,1569)],.9),.001)
yy,xx=np.mgrid[:720,:1280]
records=[];last=np.array([890.,205.]);velocity=np.zeros(2)
for name,start,end in [('walk',1412,1514),('moth',1514,1569)]:
 folder=OUT/name;folder.mkdir(exist_ok=True);(folder/'frames').mkdir(exist_ok=True)
 file='forest_walk_track_v6.mp4' if name=='walk' else 'forest_fauna_moth_v6.mp4'
 cap=cv2.VideoCapture(str(ROOT/'clips/raw'/file));assert cap.get(cv2.CAP_PROP_FPS)==24
 for i,sf in enumerate(range(start,end)):
  ok,frame=cap.read();assert ok
  pic=frame.astype(np.float32)/255;b,g,r=cv2.split(pic)
  voice=min(1,rms(sf+.5)/ref)
  if name=='walk':
   # Isolate the existing luminous green source, not general foliage saturation.
   score=np.maximum(0,g-(r+b)*.5)*g
   score*=((g>.66)&(g>r*1.04)&(g>b*1.1)&(yy>100)&(yy<335))
   score=cv2.GaussianBlur(score,(0,0),3)
   predicted=last+velocity
   if i:score*=np.exp(-((xx-predicted[0])**2+(yy-predicted[1])**2)/(2*95**2))
   _,peak,_,loc=cv2.minMaxLoc(score)
   visible=peak>.004 and (i==0 or np.linalg.norm(np.array(loc)-last)<100)
   center=np.array(loc,dtype=float) if visible else last.copy()
   velocity=.5*velocity+.5*(center-last) if visible else velocity*.8
   last=center
   d=(xx-center[0])**2+(yy-center[1])**2
   accent=pulse(sf+.5,1475,1501)
   visibility=float(np.clip((peak-.004)/.012,0,1)) if visible else 0.
   strength=((.2+.32*voice)+2.3*accent)*visibility
   glow=(np.exp(-d/(2*5**2))*.45+np.exp(-d/(2*17**2))*.22+
         np.exp(-d/(2*42**2))*.095)*strength
   result=np.clip(pic+glow[:,:,None]*np.array([.30,1.,.65]),0,1)
   rec={'song_frame':sf,'source_frame':i,'center':center.tolist(),'confidence':peak,'visibility':visibility,'accent':float(accent)}
  else:
   # Frame-local warm-translucent wing matte follows wing deformation. No static
   # mask or glow over the pink thistle. Retain vein contrast in the core.
   matte=np.clip((np.minimum(r,g)-.46)*4,0,1)*np.clip((r-b+.04)*3,0,1)
   matte*=((yy<425)&(xx>70)&(xx<1210))
   matte=cv2.GaussianBlur(matte,(0,0),1.5)
   breath=pulse(sf+.5,1524,1553)
   strength=.08+.18*voice+.30*breath
   glow=cv2.GaussianBlur(matte,(0,0),6)*.26+cv2.GaussianBlur(matte,(0,0),22)*.30
   result=np.clip(pic+pic*matte[:,:,None]*strength*.20+
       glow[:,:,None]*np.array([.43,.79,1.])*strength,0,1)
   rec={'song_frame':sf,'source_frame':i,'voice':voice,'breath':float(breath)}
  cv2.imwrite(str(folder/'frames'/f'{i:04d}.png'),np.rint(result*255).astype(np.uint8));records.append(rec)
 cap.release()
 run(['ffmpeg','-v','error','-y','-framerate','24','-i',folder/'frames/%04d.png','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',folder/'clean.mp4'])
(OUT/'controls.json').write_text(json.dumps(records,indent=2))
edl=json.loads((ROOT/'out/screen_garden_trial/shotlist.json').read_text());cues=json.loads((ROOT/'out/screen_garden_trial/overlay_cues.json').read_text())
for name,setup,start,end in [('walk','forest_walk_track',1412,1514),('moth','forest_fauna_moth',1514,1569)]:
 shot=dict(edl['shots'][-1]);shot.update(id='garden_'+name,setup=setup,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start,
 clip={'file':f'out/garden_light_moth_v1/{name}/clean.mp4','in_sec':0,'speed':1})
 edl['shots'].append(shot);cue=dict(cues['shots'][-1]);cue.update(id=shot['id'],setup=setup,start=start,end=end);cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=1569/24;cues['frames']=1569
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'blender.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy',
 '--start','1374','--end','1568','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=57.25:end=65.375,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','195','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Walk/moth preview ready, song1374..1569.')
