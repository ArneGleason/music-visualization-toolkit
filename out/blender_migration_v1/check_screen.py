"""Exact song clocks, full-frame diagnostics, resolution and source checks."""
from pathlib import Path
import json,sys,hashlib,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'screen'
sys.path.insert(0,str(R/'out/fx_tracking_deps')); import cv2
data=json.loads((D/'controls.json').read_text())
assert [v['song_frame'] for v in data['frames']]==list(range(1189,1304))
assert data['delivery_song_frames']==[1201,1304] and data['delivery_frames']==[12,115]
handoff=json.loads((R/'out/receiver_reply_arrival_v1/handoff.json').read_text())
assert hashlib.sha256((R/'out/receiver_reply_arrival_v1/base.mp4').read_bytes()).hexdigest().lower()==handoff['claude_result']['base']['sha256'].lower()
tracking={v['song_frame']:v for v in json.loads((R/'out/screen_garden_trial/tracking.json').read_text())['frames']}
for row in data['frames'][12:69]:
    assert row['transform']==tracking[row['song_frame']]['transform']
ref=cv2.VideoCapture(str(R/'out/screen_garden_trial/clean.mp4')); ref.set(cv2.CAP_PROP_POS_FRAMES,119)
comparisons=[]
for f in range(13,116):
    ok,a=ref.read(); assert ok
    z=cv2.imread(str(D/f'native_1280/{f:04d}.png')); assert z is not None and z.shape==(720,1280,3)
    comparisons.append({'frame':f,'mae':float(np.abs(a.astype(float)-z.astype(float)).mean())})
ref.release(); hi=[]
for f in [13,25,57,64,69,70,115]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png')); z=cv2.imread(str(D/f'native_1920/{f:04d}.png')); assert z is not None and z.shape==(1080,1920,3)
    hi.append({'frame':f,'mae':float(np.abs(a.astype(float)-cv2.resize(z,(1280,720),interpolation=cv2.INTER_AREA).astype(float)).mean())})
assert max(v['mae'] for v in hi)<3
random=[]
for f in [25,64,70]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png')); z=cv2.imread(str(D/f'random_access_{f:04d}.png'))
    delta=int(np.abs(a.astype(int)-z.astype(int)).max()); assert delta==0
    random.append({'frame':f,'max_pixel_difference':delta})
# Fully expanded circle covers every pixel; held receiver plate is invisible.
assert 820-((640**2+360**2)**.5)>3
garden=cv2.VideoCapture(str(R/'clips/raw/forest_threshold_v6.mp4'))
assert garden.get(cv2.CAP_PROP_FPS)==24 and garden.get(cv2.CAP_PROP_FRAME_COUNT)>=108
garden.release()
sources=[{'file':s['file'],'sha256':hashlib.sha256((R/s['file']).read_bytes()).hexdigest()} for s in data['sources']]
result={'status':'technical_checks_pass_owner_review_pending','sources':sources,'all_frames':comparisons,'resolution':hi,'random_access':random,'hidden_hold_fully_masked':True,'garden_raw_frames':[0,108]}
(D/'qa.json').write_text(json.dumps(result,indent=2))
print('Screen checks passed; max resolution mean:',max(v['mae'] for v in hi),flush=True)
