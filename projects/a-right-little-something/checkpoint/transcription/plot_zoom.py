import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import load_project
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import whisper,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
fig,axes=plt.subplots(4,1,figsize=(18,11),sharex=True)
for role,ax,sp in [('lead',axes[0],axes[1]),('leadRenaissance',axes[2],axes[3])]:
 offset=p['vocalOrigin']['masterSeconds']; a=119.3-offset; z=122-offset
 y=whisper.load_audio(p['sources'][role])[int(a*16000):int(z*16000)]
 t=np.arange(len(y))/16000+119.3
 ax.plot(t,y,lw=.35);ax.set_title(role);ax.grid()
 f,tt,s=signal.spectrogram(y,16000,nperseg=256,noverlap=224)
 sp.pcolormesh(tt+119.3,f,10*np.log10(s+1e-12),vmin=-100,vmax=-45,shading='auto');sp.set_ylim(0,5000);sp.grid()
 for x in [119.8,120.0,120.2,120.4,120.6,120.8,121.0,121.2,121.4,121.6]:ax.axvline(x,c='red',alpha=.2);sp.axvline(x,c='red',alpha=.2)
axes[-1].set_xticks(np.arange(119.3,122,.1));axes[-1].tick_params(axis='x',rotation=70)
fig.tight_layout();fig.savefig(b/'generated/transcription/zoom-waveform.png',dpi=150)
