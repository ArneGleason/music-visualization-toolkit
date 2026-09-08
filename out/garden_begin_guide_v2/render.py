"""The established green guide celebrates arrival at the responding garden."""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
beats=np.array([b['sec']*24 for b in json.loads((ROOT/'generated/overlay_cues.json').read_text())['beats']])
def smooth(v):
 v=np.clip(v,0,1);return v*v*(3-2*v)
def position(sf):
 t=sf-1786
 phase=np.interp(sf,beats,np.arange(len(beats)))
 local_phase=phase-np.interp(1798,beats,np.arange(len(beats)))
 a=local_phase*2*np.pi
 landing=smooth(t/13)
 # Right-hand arrival, a delighted oval dance, then a small upward flourish.
 cx=1120*(1-landing)+(877+47*np.sin(a))*landing
 cy=(340-95*landing)+landing*43*np.cos(a)
 leap=np.exp(-((sf-1828)/4.5)**2)
 cy-=55*leap
 size=6.2+1.3*landing+.9*leap
 return cx,cy,size,phase,leap
def guide(pic,sf,x,y,protection):
 core=np.zeros(x.shape,np.float32);halo=core.copy()
 for sample in (-.30,.30):
  cx,cy,size,phase,leap=position(sf+sample)
  gain=.95+1.5*np.exp(-(phase%1)/.23)+.7*leap
  for age in range(9):
   px,py,r,_,_=position(sf+sample-age*.22)
   d=(x-px)**2+(y-py)**2
   core+=np.exp(-d/(2*(r*(1-age*.055))**2))*np.exp(-age*.48)*.34*gain
  d=(x-cx)**2+(y-cy)**2
  halo+=(np.exp(-d/(2*19**2))*.22+np.exp(-d/(2*43**2))*.085)*gain*.5
 arrival=.55+.45*smooth((sf-1786)/4)
 return pic+(core[:,:,None]*np.array([.40,1.,.57])+halo[:,:,None]*np.array([.21,1.,.36]))*protection[:,:,None]*arrival
p=ROOT/'out/garden_begin_light_v1/render.py'
s=p.read_text().replace('garden_begin_light_v1','garden_begin_guide_v2')
old='result=pic+(core+bloom)*protection[:,:,None]'
assert old in s
s=s.replace(old,old+'\n result=guide(result,sf,x,y,protection)')
s=s.replace("'method':'Source-colour", "'guide':'Same green core, wake and beat pulses as approved walk. Arrives from right, excited oval dance, upward flourish on begin, kept away from face.','method':'Source-colour")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py'),'guide':guide})
