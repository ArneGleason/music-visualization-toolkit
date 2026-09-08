"""Preserve exact per-take controls, including the longer revised overhead shot."""
from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
for name,ref in [('swim043','out/swimmer_cutaway_v2/fx/s043'),('swim044','out/swimmer_fx_full/s044'),('swim047','out/swimmer_fx_full/s047')]:
    d=O/name;(d/'plates').mkdir(parents=True,exist_ok=True)
    data=json.loads((R/ref/'controls.json').read_text());n=len(data['frames']);start=round(data['source']['in_sec']*24)
    if not (d/f'plates/{n:04d}.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/data['source']['file']),'-vf',f'trim=start_frame={start}:end_frame={start+n},setpts=PTS-STARTPTS','-frames:v',str(n),str(d/'plates/%04d.png')],check=True)
    data['reference']=ref
    (d/'controls.json').write_text(json.dumps(data,indent=2))
