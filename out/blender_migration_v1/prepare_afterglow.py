"""Original room performances and already-verified artifact tracks."""
import json,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1]
for family,folder,offset in [('afterglow_b1','outro_B1_afterglow_v1',0),('afterglow_b2','outro_B2_afterglow_v1',155)]:
 D=O/family;(D/'plates').mkdir(parents=True,exist_ok=True);cfg=json.loads((R/'out'/folder/'settings.json').read_text())
 (D/'controls.json').write_text(json.dumps({'source':cfg['source'],'time_offset':offset,'frames':cfg['records']},indent=2))
 if not (D/'plates/0191.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',cfg['source'],str(D/'plates/%04d.png')],check=True)
