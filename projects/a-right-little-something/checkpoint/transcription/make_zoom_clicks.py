import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import load_project
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import whisper,numpy as np,librosa
from scipy.io import wavfile
offset=p['vocalOrigin']['masterSeconds'];a=117.5;z=123.0
y=whisper.load_audio(p['sources']['lead'])[int((a-offset)*16000):int((z-offset)*16000)]
y=y/max(1,float(np.max(np.abs(y)))/.7)
cues=json.loads((b/'lyrics/zoom-cues.json').read_text())['cues']
for rate,name in [(1,'zoom-nine-cues.wav'),(.5,'zoom-nine-cues-half-speed.wav')]:
 vocal=y if rate==1 else librosa.effects.time_stretch(y,rate=rate)
 ticks=np.zeros_like(vocal)
 for c in cues:
  at=round((c['masterSeconds']-a)/rate*16000);n=480
  tick=.25*np.sin(np.arange(n)/16000*2*np.pi*1800)*np.hanning(n)
  ticks[at:at+n]+=tick
 stereo=np.stack([vocal,vocal*.6+ticks],axis=1)
 wavfile.write(str(b/'generated/animatic'/name),16000,(np.clip(stereo,-1,1)*32767).astype(np.int16))
print('Made normal and half-speed vocal/click checks; crop starts at master 117.5 seconds')
