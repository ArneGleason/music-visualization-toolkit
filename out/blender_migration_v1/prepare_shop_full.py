"""Preserve the approved alien-head hoop geometry and exact exit clock."""
import json,gzip,math
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'shop_full';D.mkdir(exist_ok=True)
records=json.loads((R/'out/shop_wide_synced_v5/recipe.json').read_text())['diagnostics'];geometry=[]
theta=np.linspace(0,2*np.pi,384,endpoint=False)
def sm(t):t=np.clip(t,0,1);return t*t*(3-2*t)
for rec in records:
 sf=rec['song_frame'];level=rec['vocal_level'];a=np.clip((sf-2424)/6,0,1)**1.8;zoom=1280/(1280+(800/1.2-1280)*a);cx=(382-520*a)*zoom;cy=(262-(64/1.2)*a)*zoom;radius=88*zoom;segments=[]
 if sf<2433:
  fade=sm((sf-2399+2)/5)*(1-sm((sf-2427)/5))
  for side in range(2):
   phase=(sf-2399)*.105+side*np.pi/2;rr=radius*(1+.07*level*np.sin(theta*5+phase));px=rr*np.cos(theta);py=rr*np.sin(theta)
   xx=cx+px*.90;yy=cy+py*(.60 if side==0 else .87)+px*(.25 if side==0 else -.25)
   for j in range(len(theta)):
    q=(j+1)%len(theta);val=(.3+1.1*level)*fade*(.35+.65*np.exp(-np.mod(theta[j]-phase,2*np.pi)/1.7))
    segments.append([[float(xx[j]),float(yy[j])],[float(xx[q]),float(yy[q])],2,float(val),1-side])
 geometry.append(segments)
with gzip.open(D/'segments.json.gz','wt') as f:json.dump(geometry,f)
(D/'controls.json').write_text(json.dumps({'song_frames':[2399,2484],'effect_clear':2433,'frames':records},indent=2))
