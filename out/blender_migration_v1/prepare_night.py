"""Original night plate and exact existing music controls, no raster effects."""
import subprocess,json,math,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'night';(D/'plates').mkdir(parents=True,exist_ok=True)
if not (D/'plates/0072.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'clips/raw/colony_goodnight_cascade_v6.mp4'),'-vf','fps=24','-frames:v','72',str(D/'plates/%04d.png')],check=True)
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'audio/song.wav'),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
env=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(4782)]);env=np.clip(env/(np.percentile(env[4362:4782],85)+1e-8),0,1)
beats=[v for bar in json.loads((R/'analysis/beatmap.json').read_text())['bars'] for v in bar['beats']]
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def beat(t):return max([math.exp(-max(0,t-q)/.17)*smooth((t-q+.04)/.04) for q in beats if -.04<=t-q<.9]+[0])
rows=[{'song_frame':sf,'env':float(env[sf]),'beat':beat(sf/24),'sub_beats':[beat((sf+dt)/24) for dt in np.linspace(-.4,.4,9)]} for sf in range(4710,4782)]
(D/'controls.json').write_text(json.dumps({'frames':rows},indent=2))
