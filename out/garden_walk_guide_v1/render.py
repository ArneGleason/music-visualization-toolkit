"""Beat-grid choreographed green guide, ahead of the returning walker."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
OUT.mkdir(exist_ok=True);(OUT/'frames').mkdir(exist_ok=True)
cues=json.loads((ROOT/'generated/overlay_cues.json').read_text())
beats=np.array([b['sec']*24 for b in cues['beats']])
y,x=np.mgrid[:720,:1280].astype(np.float32)
def smooth(a):
 a=np.clip(a,0,1);return a*a*(3-2*a)
def flight(sf):
 # Fractional beat phase respects the existing timing grid, not assumed BPM.
 phase=np.interp(sf,beats,np.arange(len(beats)))
 angle=phase*2*np.pi
 progress=(sf-1650)/60
 # Forward travel with an oval beckoning gesture each beat. Always peripheral.
 cx=865+225*progress+42*np.sin(angle-.6)
 cy=235+42*np.cos(angle)+12*np.sin(angle*.5)
 size=5.5+1.5*np.sin(angle-.4)**2
 return cx,cy,size,phase
cap=cv2.VideoCapture(str(ROOT/'out/garden_walk_return_v1/base.mp4'))
cap.set(cv2.CAP_PROP_POS_FRAMES,12)
records=[]
for i,sf in enumerate(range(1650,1710)):
 ok,f=cap.read();assert ok
 pic=f.astype(np.float32)/255
 core=np.zeros((720,1280),np.float32);halo=core.copy()
 for sample in [-.3,.3]:
  cx,cy,size,phase=flight(sf+sample)
  hit=np.exp(-(phase%1)/.23)
  gain=.8+1.7*hit
  for age in range(9):
   px,py,r,_=flight(sf+sample-age*.20)
   distance=(x-px)**2+(y-py)**2
   core+=np.exp(-distance/(2*(r*(1-age*.055))**2))*np.exp(-age*.48)*.34*gain
  distance=(x-cx)**2+(y-cy)**2
  halo+=(np.exp(-distance/(2*19**2))*.22+np.exp(-distance/(2*43**2))*.085)*gain*.5
 # Small foreground-leaf interruptions, not a recovered depth mask. Limit to
 # dark green structure so the guide does not simply paint across the fern.
 gray=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
 dark=1-smooth((gray-.045)/.075)
 green=smooth((pic[:,:,1]-pic[:,:,2]+.005)/.045)
 occlusion=1-.70*cv2.GaussianBlur(dark*green,(0,0),1.8)
 arrival=.4+.6*smooth(i/5)
 result=pic+(core[:,:,None]*np.array([.40,1.,.57])+halo[:,:,None]*np.array([.21,1.,.36]))*occlusion[:,:,None]*arrival
 cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(result*255,0,255).astype(np.uint8))
 records.append({'song_frame':sf,'center':[float(cx),float(cy)],'beat_phase':float(phase),'peak_gain':float(gain)})
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),'-frames:v','60','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(OUT/'clean.mp4')],check=True)
(OUT/'guide.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[1650,1710],'source_frames':[12,72],'source_origin':1638,'guide':'Forward drift with beat-grid oval beckoning gestures, green core, tapered wake, intensity pulses. Peripheral, ahead of walker. Approximate dark-leaf interruption, no solved depth or face relighting.','diagnostics':records},indent=2))
p=ROOT/'out/garden_sequence_v1/render.py';s=p.read_text().replace('garden_sequence_v1','garden_walk_guide_v1')
old="clip={'file':h['output']['base'],'in_sec':12/24,'speed':1}"
assert old in s
s=s.replace(old,"clip={'file':'out/garden_walk_guide_v1/clean.mp4','in_sec':0,'speed':1}")
s=s.replace("'new_walk_fx':False","'new_walk_fx':'beat-grid green guide, already included once in clean'")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'assemble.py')})
