from pathlib import Path
import json,sys,hashlib,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'walk'
sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
data=json.loads((D/'controls.json').read_text());assert [r['song_frame'] for r in data['frames']]==list(range(1412,1514))
assert hashlib.sha256((R/data['source']).read_bytes()).hexdigest()==data['source_sha256']
old=json.loads((R/'out/garden_ghost_wings_v3/controls.json').read_text())[:102]
assert all(a['center']==b['center'] and a['visibility']==b['visibility'] and a['source_frame']==i for i,(a,b) in enumerate(zip(data['frames'],old)))
comparison=[]
for f in range(1,103):
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png'));z=cv2.imread(str(R/f'out/garden_ghost_wings_v3/walk/frames/{f-1:04d}.png'))
    assert a is not None and z is not None and a.shape==z.shape==(720,1280,3)
    comparison.append({'frame':f,'mae':float(np.abs(a.astype(float)-z.astype(float)).mean())})
hi=[]
for f in [1,25,40,65,78,102]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png'));z=cv2.imread(str(D/f'native_1920/{f:04d}.png'));assert z is not None and z.shape==(1080,1920,3)
    hi.append({'frame':f,'mae':float(np.abs(a.astype(float)-cv2.resize(z,(1280,720),interpolation=cv2.INTER_AREA).astype(float)).mean())})
assert max(v['mae'] for v in hi)<3
random=[]
for f in [40,78]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png'));z=cv2.imread(str(D/f'random_access_{f:04d}.png'));delta=int(np.abs(a.astype(int)-z.astype(int)).max());assert delta==0
    random.append({'frame':f,'max_pixel_difference':delta})
(D/'qa.json').write_text(json.dumps({'status':'technical_checks_pass_owner_review_pending','all_frames':comparison,'resolution':hi,'random_access':random,'source_hash_pass':True,'tracking_pass':True},indent=2))
print('QA passed. Max mean reference/resolution difference:',max(v['mae'] for v in comparison),max(v['mae'] for v in hi))
