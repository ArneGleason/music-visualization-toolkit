"""Timing, source hashes, all-frame diagnostics and resolution comparison."""
from pathlib import Path
import json,gzip,hashlib,sys,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'message'
sys.path.insert(0,str(R/'out/fx_tracking_deps')); import cv2
data=json.loads((D/'controls.json').read_text())
h=json.loads((R/'out/receiver_reply_arrival_v1/handoff.json').read_text())
actual=hashlib.sha256((R/h['output']['base']).read_bytes()).hexdigest()
assert actual.lower()==h['claude_result']['base']['sha256'].lower()
assert [v['song_frame'] for v in data['frames']]==list(range(971,1201))
with gzip.open(D/'paths.json.gz','rt') as f:paths=json.load(f)
old=json.loads((R/'out/rosette_duet_trial/choreography.json').read_text())['frames']; center_errors=[]
for i,row in enumerate(old):
    for side,state in enumerate(row['sprites']):
        if state is None:continue
        p=next(p for p in paths[i][1] if p['kind']=='sprite' and p['side']==side)
        center_errors.append(float(np.linalg.norm(np.array(p['xy']).mean(axis=0)-state['center'])))
assert max(center_errors)<1e-5
references=[cv2.VideoCapture(str(R/'out/rosette_duet_trial/preview.mp4')),cv2.VideoCapture(str(R/'out/receiver_now_v3/clean.mp4'))]
comparisons=[]
for i in range(230):
    ok,ref=references[0 if i<111 else 1].read(); assert ok
    native=cv2.imread(str(D/f'native_1280/{i+1:04d}.png')); assert native is not None and native.shape==(720,1280,3)
    # First old reference contains captions and a prior display transform.
    # Exclude subtitle area there; these differences are not a parity gate.
    crop=560 if i<111 else 720; delta=np.abs(native[:crop].astype(float)-ref[:crop].astype(float))
    comparisons.append({'frame':i+1,'mae':float(delta.mean()),'p99':float(np.quantile(delta,.99))})
for cap in references:cap.release()
hi=[]
for f in [1,70,100,112,155,211,230]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png')); z=cv2.imread(str(D/f'native_1920/{f:04d}.png')); assert z is not None
    delta=np.abs(a.astype(float)-cv2.resize(z,(1280,720),interpolation=cv2.INTER_AREA).astype(float)); hi.append({'frame':f,'mae':float(delta.mean()),'p99':float(np.quantile(delta,.99))})
random_access=[]
for f in [70,211]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png')); z=cv2.imread(str(D/f'random_access_{f:04d}.png')); assert z is not None
    maximum=int(np.abs(a.astype(int)-z.astype(int)).max()); random_access.append({'frame':f,'pixel_max_difference':maximum}); assert maximum==0, 'Saved-scene/sequential mismatch'
assert max(v['mae'] for v in hi)<3, 'Resolution comparison needs investigation'
result={'status':'technical_diagnostics_not_owner_approval','source_hash_pass':True,'random_access':random_access,'max_sprite_center_error_px':max(center_errors),'all_frames':comparisons,'resolution':hi,'max_mean':max(v['mae'] for v in comparisons),'max_resolution_mean':max(v['mae'] for v in hi)}
(D/'qa.json').write_text(json.dumps(result,indent=2)); print(json.dumps({k:v for k,v in result.items() if k!='all_frames'},indent=2))
