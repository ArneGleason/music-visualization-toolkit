from pathlib import Path
import subprocess,json,math
import numpy as np
from scipy.ndimage import map_coordinates
O=Path(__file__).resolve().parent;R=O.parents[1];W,H=1280,720
Y,X=np.mgrid[:H,:W].astype(np.float32)
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
src=R/'motion-graphics/SCENE11-POLISH-001/smoke-b-polished-v001.mp4'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3)
enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(O/'smoke-b-turbulence-v001.mp4')],stdin=subprocess.PIPE)
rng=np.random.default_rng(73)
eddies=[(rng.uniform(670,1120),rng.uniform(150,575),rng.uniform(38,85),rng.uniform(0,6.28),rng.choice([-1,1])) for _ in range(16)]
for f,frame in enumerate(frames):
 t=f/24;gain=float(smooth(8,23,f)*(1-smooth(34,50,f)))
 # A soft envelope keeps the door and keyhole architecture stable.
 mask=np.exp(-(((X-900)/300)**4+((Y-365)/320)**4))*smooth(530,680,X)
 dx=np.zeros_like(X);dy=np.zeros_like(Y)
 for cx,cy,r,phase,spin in eddies:
  cx+=24*math.sin(t*2.2+phase);cy+=18*math.cos(t*1.7+phase)-f*.45
  u=(X-cx)/r;v=(Y-cy)/r;fall=np.exp(-(u*u+v*v)*1.6)
  pulse=.75+.25*math.sin(t*3+phase)
  dx+=-v*fall*spin*32*pulse;dy+=u*fall*spin*32*pulse
 # Fine travelling ripples break up the broader rotating displacement.
 dx+=4*np.sin(X/23+Y/37-t*6)*np.cos(Y/51+t*2)
 dy+=4*np.cos(Y/25-X/43-t*5)*np.sin(X/57+t*2.6)
 # Gradually anchor the single eye while the surrounding vapor still curls.
 eye=np.exp(-(((X-900)/75)**2+((Y-245)/65)**2)*2)
 mask*=1-.70*eye*smooth(28,43,f)
 dx*=mask*gain;dy*=mask*gain
 coords=[np.clip(Y+dy,0,H-1),np.clip(X+dx,0,W-1)]
 im=np.stack([map_coordinates(frame[:,:,c],coords,order=1,mode='nearest') for c in range(3)],axis=2) if gain else frame
 enc.stdin.write(im.astype(np.uint8).tobytes())
enc.stdin.close();assert enc.wait()==0
(O/'settings.json').write_text(json.dumps({'source':str(src),'frames':51,'fps':24,'effect':'16 drifting local vortices plus fine evolving turbulence; invisible displacement only','envelope_local':[8,23,34,50],'final_frame':'zero displacement; approved clear reveal','unchanged':'all other shots'},indent=2))
print('smoke turbulence complete')
