"""Measure distinct vowel-energy attacks; never space repeated words evenly."""
import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import load_project,MusicalGrid
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import whisper,numpy as np
from scipy import signal,ndimage
offset=p['vocalOrigin']['masterSeconds']; start=119.3
peak_times=[119.898,120.341,120.482,120.670,120.839,120.989,121.174,121.340,121.514]
valley_windows=[(119.60,119.74),(120.18,120.28),(120.36,120.43),(120.55,120.63),(120.72,120.79),(120.88,120.94),(121.08,121.14),(121.23,121.30),(121.40,121.47)]
measurements={}
for role in ['lead','leadRenaissance']:
 y=whisper.load_audio(p['sources'][role])[int((start-offset)*16000):int((122-offset)*16000)]
 band=signal.sosfiltfilt(signal.butter(4,[500,4000],btype='bandpass',fs=16000,output='sos'),y)
 energy=np.sqrt(ndimage.uniform_filter1d(band*band,320))
 result=[]
 for peak,(a,z) in zip(peak_times,valley_windows):
  lo,hi=int((a-start)*16000),int((z-start)*16000)
  valley=lo+int(np.argmin(energy[lo:hi])); end=int((peak-start)*16000)
  threshold=energy[valley]+.2*(energy[end]-energy[valley])
  attack=valley+int(np.flatnonzero(energy[valley:end+1]>=threshold)[0])
  result.append(dict(valley=start+valley/16000,attack=start+attack/16000,peak=peak))
 measurements[role]=result
grid=MusicalGrid(json.loads((b/p['timing']['beatmap']).read_text(encoding='utf-8')))
cues=[]
for i,(original,clean) in enumerate(zip(measurements['lead'],measurements['leadRenaissance'])):
 # Original performance is authoritative; processed stem is a cross-check.
 t=original['attack']; frame=round(grid.sec(grid.position(t))*p['render']['fps'])+1
 cues.append(dict(index=i+1,text='in',masterSeconds=t,sourceSeconds=t-offset,
                  musicalPosition=grid.position(t).text(),frame=frame,
                  frameSeconds=(frame-1)/p['render']['fps'],frameErrorMs=((frame-1)/p['render']['fps']-t)*1000,
                  processedAttackSeconds=clean['attack'],crossCheckDifferenceMs=(clean['attack']-t)*1000,
                  boundaryWindowSeconds=[original['valley'],t],vowelPeakSeconds=original['peak'],
                  basis='original lead 500–4000 Hz, 20 ms RMS, first 20% attack above local minimum; spectrogram/processed-stem cross-check',
                  reviewStatus='acoustic cue candidate; verify with audible pulse preview'))
doc=dict(lyric='Hit zoom. Zoom '+', '.join(['in']*9)+' to see far',fps=p['render']['fps'],
         onsetDefinition='vowel-energy attack; coarticulated word boundaries are not sample-exact',cues=cues,measurements=measurements)
(b/'lyrics/zoom-cues.json').write_text(json.dumps(doc,indent=2),encoding='utf-8')
print(json.dumps(cues,indent=2))
