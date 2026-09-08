"""A vocal-responsive souvenir signal becomes a peripheral window reflection."""
import json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
(OUT/'frames').mkdir(exist_ok=True)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem),'-af',
 f'atrim=start={2399/24-.178348}:duration={85/24},asetpts=PTS-STARTPTS',
 '-ac','1','-ar','24000','-f','f32le','-']),dtype=np.float32)
rms=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(85)])
norm=max(float(np.quantile(rms,.9)),.001)
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
cap=cv2.VideoCapture(str(ROOT/'out/shop_snap_test_v2/clean.mp4'))
theta=np.linspace(0,2*np.pi,384,endpoint=False)
y,x=np.mgrid[:720,:1280].astype(np.float32)
trail=np.zeros((720,1280,3),np.float32);level=0;records=[]
for i,sf in enumerate(range(2399,2484)):
 ok,frame=cap.read();assert ok
 level=max(min(1,float(rms[i]/norm)),level*.70)
 change=smooth((sf-2424)/12)
 cx=210*(1-change)+145*change;cy=325*(1-change)+389*change
 radius=52*(1-change)+83*change
 # Stylized signal/reflection handoff, not a physical 3D surface reconstruction.
 light=np.zeros_like(trail)
 fade=smooth((sf-2399+2)/5)*(1-smooth((sf-2472)/11))
 flicker=1 if sf<2459 else (.45+.55*abs(np.sin((sf-2459)*1.9)))
 for side,color in enumerate([np.array([.10,.55,1.]),np.array([1.,.80,.20])]):
  phase=(sf-2399)*.105+side*np.pi/2
  rr=radius*(1+.07*level*np.sin(theta*5+phase))
  px=rr*np.cos(theta);py=rr*np.sin(theta)
  horizontal=.90*(1-change)+.32*change
  xx=cx+px*horizontal
  yy=cy+py*(.60 if side==0 else .87)+px*(.25 if side==0 else -.25)
  energy=np.zeros((720,1280),np.float32)
  for j in range(len(theta)):
   q=(j+1)%len(theta)
   scan=.35+.65*np.exp(-np.mod(theta[j]-phase,2*np.pi)/1.7)
   val=(.3+1.1*level)*fade*flicker*scan
   cv2.line(energy,(round(xx[j]),round(yy[j])),(round(xx[q]),round(yy[q])),float(val),2,cv2.LINE_AA)
  light+=energy[:,:,None]*color
 trail=trail*.38+light*.8
 glow=trail*1.1+cv2.GaussianBlur(trail,(0,0),3)*2.0+cv2.GaussianBlur(trail,(0,0),12)*2.5
 blur=float(np.exp(-.5*((sf-2430.5)/1.25)**2))
 if blur>.02:
  streaks=[]
  for scale in np.linspace(1-.20*blur,1+.20*blur,13):
   streaks.append(cv2.remap(glow,((x-640)/scale+640).astype(np.float32),((y-270)/scale+270).astype(np.float32),cv2.INTER_LINEAR))
  glow=cv2.GaussianBlur(np.mean(streaks,axis=0),(0,0),max(.1,9*blur))
 # Effect stays left of the actor; no face illumination or full-frame flash.
 pic=frame.astype(np.float32)/255
 result=pic+(1-pic)*(1-np.exp(-glow*1.5))
 cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(result*255,0,255).astype(np.uint8))
 records.append({'song_frame':sf,'vocal_level':level,'reflection_mix':float(change),'fade':float(fade)})
cap.release()
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),'-frames:v','85','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(OUT/'clean.mp4')],check=True)
p=ROOT/'out/shop_reply_review_v1/render.py'
s=p.read_text().replace('clips/raw/counterfeit_parade_v6.mp4','out/shop_signal_test_v1/clean.mp4')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[2399,2484],
 'preview_song_frames':[2330,2484],'base':'out/shop_snap_test_v2/clean.mp4',
 'driver':'restored lead vocal RMS, placement+.178348seconds applied once',
 'method':'Amber/cyan globe traces morph into peripheral window reflection; continuous phase and envelope across source switch, blur follows punch; final flicker and release.',
 'continuity':'Motif callback to preceding world, not literal phase-matched continuation of its geometry.',
 'limitations':'Authored screen-space placement, no solved optical reflection or camera track.',
 'lip_sync_applied':False,'production_merged':False,'diagnostics':records},indent=2))
