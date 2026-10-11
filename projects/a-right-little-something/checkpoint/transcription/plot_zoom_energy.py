import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import load_project
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import whisper,numpy as np
from scipy import signal,ndimage
from PIL import Image,ImageDraw,ImageFont
im=Image.new('RGB',(2000,1000),'white');d=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
left,right=110,1960
def x(t):return left+(t-119.3)/2.7*(right-left)
results=[]
for role,top in [('lead',50),('leadRenaissance',520)]:
 offset=p['vocalOrigin']['masterSeconds'];a=119.3-offset;z=122-offset
 y=whisper.load_audio(p['sources'][role])[int(a*16000):int(z*16000)]
 band=signal.sosfiltfilt(signal.butter(4,[500,4000],btype='bandpass',fs=16000,output='sos'),y)
 env=np.sqrt(ndimage.uniform_filter1d(band*band,160))[::16]
 env/=env.max();t=np.arange(len(env))/1000+119.3
 peaks,_=signal.find_peaks(env,distance=80,prominence=.08)
 results.append(dict(role=role,peaks=[dict(time=float(t[i]),amplitude=float(env[i])) for i in peaks]))
 d.text((left,top),role+' — 500–4000 Hz energy; 10 ms RMS',fill='black',font=font)
 for tick in np.arange(119.3,122,.1):
  xx=x(tick);d.line([(xx,top+35),(xx,top+360)],fill='#dddddd');d.text((xx-15,top+365),f'{tick:.1f}',fill='black',font=font)
 d.line([(x(tt),top+350-ee*300) for tt,ee in zip(t,env)],fill='#005588',width=2)
 for i in peaks:
  xx=x(t[i]);yy=top+350-env[i]*300
  d.ellipse((xx-4,yy-4,xx+4,yy+4),fill='red');d.text((xx-22,yy-25),f'{t[i]:.3f}',fill='red',font=font)
im.save(b/'generated/transcription/zoom-energy.png')
(b/'generated/transcription/zoom-energy-peaks.json').write_text(json.dumps(results,indent=2))
print(results)
