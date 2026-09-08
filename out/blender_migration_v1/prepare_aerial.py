from pathlib import Path
import json, subprocess
import numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'aerial'; D.mkdir(exist_ok=True)
track=json.loads((R/'out/opening_aerial_glimmer_v1/tracking.json').read_text())
pos=np.array(track['positions']); valid=[76]*3
for k in range(3):
    for n in range(1,77):
        if np.array_equal(pos[n:,k],np.tile(pos[n-1,k],(77-n,1))):
            valid[k]=n-1;break
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'audio/song.wav'),'-f','f32le','-ac','1','-ar','24000','-'])
a=np.frombuffer(pcm,dtype='<f4')
e=np.array([np.sqrt(np.mean(a[(205+i)*1000:(206+i)*1000]**2)) for i in range(77)])
e=np.convolve(e,[.2,.6,.2],mode='same');e=np.clip(e/(np.percentile(e,90)+1e-9),0,1)
track.update(energy=e.tolist(),valid_until=valid,song_frames=[205,282],plate='out/opening_aerial_flow_v1/base.mp4')
(D/'controls.json').write_text(json.dumps(track,indent=2))
for name,src in [('plates',track['plate']),('reference','out/opening_aerial_glimmer_v1/clean.mp4')]:
    dest=D/name;dest.mkdir(exist_ok=True)
    if not (dest/'0077.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/src),'-frames:v','77','-fps_mode','passthrough',str(dest/'%04d.png')],check=True)
print('Read-only timing/track transfer and original/reference frame extraction complete',valid)
