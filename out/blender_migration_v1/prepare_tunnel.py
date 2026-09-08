"""Copy accepted radial tracks and sample guitar as numerical data, not pixels."""
from pathlib import Path
import json,subprocess,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'tunnel';(D/'plates').mkdir(parents=True,exist_ok=True)
data=json.loads((R/'out/tunnel_arrival_o01/controls.json').read_text())
old=json.loads((R/'out/musical_contour_tunnel_analog/tracking.json').read_text())
local=json.loads((R/'projects/rivers-of-mars/project.local.json').read_text());paths=list(Path(local['sources']['stems']).glob('*Guitar*restored.wav'));assert len(paths)==1
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-af','highpass=f=90,lowpass=f=1800,aresample=8000','-f','f32le','-'])
guitar=np.frombuffer(raw,'<f4');go=old['guitar_offset'];first,end=data['song_frames'];norm=max(float(np.quantile(np.abs(guitar[int((first/24-go)*8000):int((end/24-go)*8000)]),.97)),1e-5)
for i,row in enumerate(data['frames']):
    t=(first+i)/24
    signal=np.interp((t-go-.064+np.arange(512)/8000)*8000,np.arange(len(guitar)),guitar)/norm
    row['signal']=(np.tanh(signal*1.35+.14*signal**2)*np.sin(np.arange(512)*np.pi/512)**2).tolist()
data['source']='clips/raw/telescope_time_tunnel_v6.mp4';data['source_frames']=[0,57]
if not (D/'plates/0057.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/data['source']),'-frames:v','57',str(D/'plates/%04d.png')],check=True)
(D/'controls.json').write_text(json.dumps(data))
