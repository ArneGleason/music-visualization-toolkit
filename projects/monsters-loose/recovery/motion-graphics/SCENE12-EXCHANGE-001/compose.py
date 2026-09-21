from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image,ImageFilter
O=Path(__file__).resolve().parent;R=O.parents[1];W,H=1280,720

def read(name):
 p=R/f'video-tests/KLING-SCENE12-{name.upper()}-001/KLING-SCENE12-{name.upper()}-001-01.mp4'
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','scale=1280:720','-f','rawvideo','-pix_fmt','rgb24','-']);return np.frombuffer(b,np.uint8).reshape(-1,H,W,3)
no=read('no');yes=read('yes')
def zoom(im,z,cx,cy):
 return im.transform((W,H),Image.Transform.AFFINE,(1/z,0,cx-W/(2*z),0,1/z,cy-H/(2*z)),Image.Resampling.BICUBIC)
enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(O/'exchange-composite-v001.mp4')],stdin=subprocess.PIPE)
for f in range(108):
 if f<40:im=Image.fromarray(no[round(28+f*1.05)])
 elif f<48:
  q=(f-40)/7;q=q*q*(3-2*q);z=2.15-1.15*q;cx=W*(.33+.17*q);cy=H*.50
  frame=Image.fromarray(yes[12+f-40]);amount=.14*np.sin(np.pi*(f-39)/9)
  ims=[np.array(zoom(frame,z*(1+amount*t),cx,cy),dtype=np.float32) for t in np.linspace(-.5,.5,9)]
  im=Image.fromarray(np.uint8(np.clip(np.mean(ims,axis=0),0,255))).filter(ImageFilter.GaussianBlur(3*np.sin(np.pi*(f-39)/9)))
  if f<43:im=Image.blend(Image.fromarray(no[70+f-40]).filter(ImageFilter.GaussianBlur(4)),im,(f-39)/4)
 else:im=Image.fromarray(yes[20+f-48])
 bubble=Image.open(O/f'bubbles/bubble-{f+1:04d}.png').convert('RGBA')
 # Brief opacity ramps soften starts and remove the kid balloon before the move.
 opacity=1
 for a,b in [(0,38),(48,95)]:
  if a<=f<=b:opacity=min(1,(f-a+1)/3,(b-f+1)/3)
 bubble.putalpha(bubble.getchannel('A').point(lambda v:round(v*opacity)))
 im=Image.alpha_composite(im.convert('RGBA'),bubble).convert('RGB');enc.stdin.write(np.array(im).tobytes())
enc.stdin.close();assert enc.wait()==0
(O/'selections.json').write_text(json.dumps({'fps':24,'start':3775,'end_exclusive':3883,'duration_frames':108,'kid_source_frames':[28,69],'blur_pullback_master':[3815,3823],'Harper_source_frames':[12,79],'bubble_word_onsets':[3775,3782,3823,3835],'audio':'original song only; generated dialogue discarded','credits_consumed':120},indent=2))
