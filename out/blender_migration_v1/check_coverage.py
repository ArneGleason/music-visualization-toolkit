"""Verify reference coverage, without claiming its baked effects are native."""
from pathlib import Path
from fractions import Fraction
from concurrent.futures import ThreadPoolExecutor
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
data=json.loads((O/'migration_register.json').read_text())
paths=sorted(set(s['selected_reference'] for s in data['shots']))
def probe(p):
    f=R/p
    if not f.is_file():return p,{'error':'missing source'}
    raw=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,r_frame_rate,avg_frame_rate','-of','json',str(f)])
    return p,json.loads(raw)['streams'][0]
with ThreadPoolExecutor(max_workers=4) as pool:info=dict(pool.map(probe,paths))
checks=[]
for shot in data['shots']:
    meta=info[shot['selected_reference']]
    a,b=shot['song_frames'];first=shot['source_start_frame'];end=first+b-a
    valid='error' not in meta and Fraction(meta['r_frame_rate'])==24 and int(meta['nb_frames'])>=end and first>=0
    checks.append({'id':shot['id'],'song_frames':[a,b],'source_frames':[first,end],
                   'coverage_ok':valid,'metadata':meta})
(O/'coverage.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'checked':len(checks),'failures':[c for c in checks if not c['coverage_ok']]},indent=2))
