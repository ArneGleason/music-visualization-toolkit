"""Extract original plates and numerical wing-contour particles only."""
from pathlib import Path
import json,gzip,subprocess,hashlib,sys,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'moth';(D/'plates').mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
source=R/'clips/raw/forest_fauna_moth_v6.mp4'
if not (D/'plates/0055.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-frames:v','55',str(D/'plates/%04d.png')],check=True)
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
yy,xx=np.mgrid[:720,:1280]
code=(R/'out/garden_ghost_wings_v3/ghost_wings.py').read_text().split(' glow=layer*1.4')[0]
code=code.replace('layer=np.zeros((720,1280,3),np.float32)','layer=[]')
needle='   cv2.circle(layer,tuple(np.rint(p).astype(int)),1 if j%5 else 2,tuple(float(x*level) for x in color),-1,cv2.LINE_AA)'
assert needle in code
code=code.replace(needle,"   layer.append({'xy':p.tolist(),'radius':1 if j%5 else 2,'rgb':[float(x*level) for x in color[::-1]]})")+' return layer\n'
ns={'np':np,'cv2':cv2,'smooth':smooth,'xx':xx,'yy':yy};exec(compile(code,'accepted_contour_math','exec'),ns)
rows=json.loads((R/'out/garden_ghost_wings_v3/controls.json').read_text())[102:];assert len(rows)==55
paths=[]
for i,row in enumerate(rows):
    pic=cv2.imread(str(D/f'plates/{i+1:04d}.png')).astype(np.float32)/255
    paths.append(ns['ghost_wings']([],pic,row['song_frame']+.5))
with gzip.open(D/'particles.json.gz','wt') as f:json.dump(paths,f)
(D/'controls.json').write_text(json.dumps({'fps':24,'song_frames':[1514,1569],'source_frames':[0,55],'source':str(source.relative_to(R)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':rows},indent=2))
print('Prepared55 moth frames and numerical particle contours')
