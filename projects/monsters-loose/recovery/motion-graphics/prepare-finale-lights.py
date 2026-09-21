import json
from pathlib import Path
import numpy as np
from PIL import Image
o=Path(__file__).resolve().parent/'OUTRO-LIGHTS-001'
guesses={0:[(595,146),(646,155),(688,123),(706,113),(716,122),(818,137),(872,145)],85:[(594,144),(643,155),(685,124),(701,114),(713,123),(813,138),(867,146)],170:[(591,145),(636,158),(676,127),(693,117),(705,127),(800,140),(850,150)],255:[(588,147),(630,159),(669,133),(683,122),(695,130),(786,143),(832,152)],339:[(584,148),(627,159),(665,135),(676,123),(688,131),(775,145),(818,154)]}
tracks=[[] for _ in range(7)]
for f,points in guesses.items():
 a=np.array(Image.open(o/('finale-plain-'+str(f)+'.png'))).astype(float)
 for i,(x,y) in enumerate(points):
  patch=a[y-5:y+6,x-5:x+6];yy,xx=np.mgrid[y-5:y+6,x-5:x+6];score=np.maximum(0,patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2])-20)**2
  score*=np.exp(-((xx-x)**2+(yy-y)**2)/12)
  if score.sum()>100:x=float((score*xx).sum()/score.sum());y=float((score*yy).sum()/score.sum())
  tracks[i].append([f,round(x,2),round(y,2)])
anchors=[[t[0][1],t[0][2],2.8,3.1,t] for t in tracks]
(o/'finale-anchors.json').write_text(json.dumps(anchors,indent=2))
print('Seven beacons tracked at five crane positions')
