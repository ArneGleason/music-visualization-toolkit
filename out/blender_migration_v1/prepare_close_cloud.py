"""Continuous artifact insert uses original frames23..107, never a baked plate."""
import json,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'close_cloud';(D/'plates').mkdir(parents=True,exist_ok=True)
cfg=json.loads((O/'afterglow_b2/controls.json').read_text());cfg['frames']=cfg['frames'][23:107];cfg['song_frames']=[4538,4622]
(D/'controls.json').write_text(json.dumps(cfg,indent=2))
if not (D/'plates/0084.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',cfg['source'],'-vf','trim=start_frame=23:end_frame=107,setpts=PTS-STARTPTS',str(D/'plates/%04d.png')],check=True)
