from pathlib import Path
import json,subprocess,numpy as np
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');o=Path(__file__).resolve().parent
src=r/'video-tests/KLING-TOUR-003/KLING-TOUR-003-01.mp4'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),np.uint8).reshape(-1,540,960,3)
anchors=[[(0,448,6),(70,449,12),(144,449,18)],[(0,497,24),(70,497,31),(144,496,38)],[(0,139,10),(12,148,18),(70,183,50),(130,210,78),(144,216,84)],[(0,770,9),(12,763,15),(70,731,49),(130,702,76),(144,696,81)],[(0,193,53),(12,200,60),(70,223,88),(130,244,111),(144,249,116)]]
tracks={};visibility={}
for i,keys in enumerate(anchors):
 rows=[];vis=[]
 for f,im in enumerate(a):
  x=int(round(np.interp(f,[k[0] for k in keys],[k[1] for k in keys])));y=int(round(np.interp(f,[k[0] for k in keys],[k[2] for k in keys])))
  x0=max(0,x-9);y0=max(0,y-6);patch=im[y0:min(540,y+7),x0:min(960,x+10)].astype(float)
  score=patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2]);yy,xx=np.unravel_index(score.argmax(),score.shape)
  visible=float(score.max()>55)
  if visible:x=x0+int(xx);y=y0+int(yy)
  bg=np.median(np.concatenate([patch[0],patch[-1],patch[:,0],patch[:,-1]]),axis=0)/255
  rows.append([x,y,bg.tolist()]);vis.append(visible)
 tracks[str(i)]=rows;visibility[str(i)]=vis
(o/'tracks.json').write_text(json.dumps(tracks),encoding='utf-8');(o/'visibility.json').write_text(json.dumps(visibility),encoding='utf-8')
s=(r/'motion-graphics/SWAMP-LIGHTS-001/build.py').read_text()
s=s.replace("tracks=json.loads((o/'tracks.json').read_text())","tracks=json.loads((o/'tracks.json').read_text())\nvisibility=json.loads((o/'visibility.json').read_text())")
s=s.replace('s.frame_end=227','s.frame_end=145').replace('master=f-1+1293','master=f-1+1495').replace('p=math.exp(-.5*(d/3.4)**2)','visible=visibility[str(i)][f-1]\n  ma.default_value=.94*visible;ma.keyframe_insert(data_path=\'default_value\',frame=f)\n  p=math.exp(-.5*(d/3.4)**2)*visible').replace('(ca,.08+.92*p)','(ca,(.08+.92*p)*visible)').replace('Swamp-lights-v001.blend','Tour-lights-v001.blend')
(o/'build.py').write_text(s,encoding='utf-8')
print('Tracked five red lights over',len(a),'frames; visibility gating', {k:sum(v) for k,v in visibility.items()})
