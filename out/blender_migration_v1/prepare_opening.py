"""Prepare original opening footage, never the old review containing overlays."""
from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'opening'
(D/'plates').mkdir(parents=True,exist_ok=True)
if not (D/'plates/0086.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'clips/raw/obs_dome_open_v6.mp4'),'-frames:v','86',str(D/'plates/%04d.png')],check=True)
(D/'controls.json').write_text(json.dumps({'frames':[{'song_frame':i} for i in range(86)],'song_frames':[0,86],'source':'clips/raw/obs_dome_open_v6.mp4'},indent=2))
