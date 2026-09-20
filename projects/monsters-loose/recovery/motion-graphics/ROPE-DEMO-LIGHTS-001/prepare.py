import json,subprocess
import numpy as np
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
source=r/'video-tests/KLING-ROPE-DEMO-001/KLING-ROPE-DEMO-001-01.mp4'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vf','scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape(-1,540,960,3)
seeds=[(95,9),(217,80),(424,55),(602,161),(755,89)];tracks={};vis={}
for i,(sx,sy) in enumerate(seeds):
 rows=[];visible=[]
 for im in a:
  x0=max(0,sx-7);y0=max(0,sy-7);roi=im[y0:sy+8,x0:sx+8].astype(float);score=roi[:,:,0]-np.maximum(roi[:,:,1],roi[:,:,2]);yy,xx=np.unravel_index(score.argmax(),score.shape);x=x0+int(xx);y=y0+int(yy)
  mask=np.indices((21,21));rad=(mask[1]-10)**2+(mask[0]-10)**2
  # Background sampling offset below top-edge beacon if needed.
  cy=max(10,y);patch=im[cy-10:cy+11,x-10:x+11].astype(float)/255
  bg=np.median(patch[(rad>=49)&(rad<=100)],axis=0).tolist()
  rows.append([x,y,bg]);visible.append(1 if score.max()>40 else 0)
 tracks[str(i)]=rows;vis[str(i)]=visible
(o/'tracks.json').write_text(json.dumps(tracks));(o/'visibility.json').write_text(json.dumps(vis))
print('Frames',len(a),'visible counts',{k:sum(v) for k,v in vis.items()})
