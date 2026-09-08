"""Extract untreated source frames and copy accepted numerical music controls."""
from pathlib import Path
import json, subprocess
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'birds'
(D/'plates').mkdir(parents=True,exist_ok=True)
old=json.loads((R/'out/garden_birds_fx_v2/recipe.json').read_text())
if not (D/'plates/0076.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/old['source']),'-frames:v','76',str(D/'plates/%04d.png')],check=True)
(D/'controls.json').write_text(json.dumps({'frames':old['diagnostics'],'source':old['source'],'song_frames':[1710,1786]},indent=2))
