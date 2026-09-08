"""Preserve original light tracking, audio clock and flight; no FX rasters."""
from pathlib import Path
import json,subprocess,numpy as np,hashlib
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'walk'; (D/'plates').mkdir(parents=True,exist_ok=True)
source=R/'clips/raw/forest_walk_track_v6.mp4'
if not (D/'plates/0102.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-frames:v','102',str(D/'plates/%04d.png')],check=True)
code=(R/'out/garden_light_moth_v1/render.py').read_text().split('yy,xx=np.mgrid')[0]
ns={'__file__':str(R/'out/garden_light_moth_v1/render.py')};exec(compile(code,'accepted_audio','exec'),ns)
flightcode=(R/'out/garden_psychedelic_v2/effects.py').read_text().split('def second_light')[0]
exec(compile(flightcode,'accepted_flight','exec'),ns)
old=json.loads((R/'out/garden_ghost_wings_v3/controls.json').read_text()); rows=[]
for record in old[:102]:
    sf=record['song_frame']+.5; t=(sf-1412)/24; voice=min(1,ns['rms'](sf)/ns['ref'])
    gain=(.65+.25*voice+1.9*ns['pulse'](sf,1475,1501))*ns['smooth'](t/.3)
    blobs=[]
    for sample in [-.25,.25]:
        for age in range(6):
            xy=ns['flight'](max(0,t+sample/24-age*.025)); size=(5+2*np.sin(t*1.7)**2)*(1-age*.08)
            blobs.append({'xy':xy.tolist(),'sigma':float(size),'weight':float(np.exp(-age*.7)/2*.6)})
        xy=ns['flight'](t+sample/24)
        for sigma,weight in [(18,.13/2),(45,.055/2)]:blobs.append({'xy':xy.tolist(),'sigma':sigma,'weight':weight})
    rows.append(dict(record,voice=voice,gain=float(gain),blobs=blobs))
assert [v['song_frame'] for v in rows]==list(range(1412,1514))
(D/'controls.json').write_text(json.dumps({'fps':24,'song_frames':[1412,1514],'source_frames':[0,102],'source':str(source.relative_to(R)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':rows},indent=2))
print('Prepared102 original plates and numerical light controls')
