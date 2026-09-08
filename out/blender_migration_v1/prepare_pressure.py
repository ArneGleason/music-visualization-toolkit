from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'pressure'
(D/'plates').mkdir(parents=True,exist_ok=True)
data=json.loads((R/'out/message_into_rockets_v3/fx/controls.json').read_text());data['frames']=data['diagnostics']
if not (D/'plates/0069.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/data['source']['file']),'-vf','trim=start_frame=42:end_frame=111,setpts=PTS-STARTPTS','-frames:v','69',str(D/'plates/%04d.png')],check=True)
(D/'controls.json').write_text(json.dumps(data,indent=2))
