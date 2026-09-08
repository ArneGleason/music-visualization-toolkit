"""Original plate extraction and tracking/control data only; no FX rendering."""
from pathlib import Path
import json,sys,subprocess
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
def extract(name,source,first,count):
    d=O/name;d.mkdir(exist_ok=True);p=d/'plates';p.mkdir(exist_ok=True)
    if not (p/f'{count:04d}.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-vf',f'trim=start_frame={first}:end_frame={first+count},setpts=PTS-STARTPTS','-frames:v',str(count),str(p/'%04d.png')],check=True)
    return d
track=json.loads((R/'out/receiver_voice_review/fx/tracking.json').read_text())
d=extract('receiver',Path(track['source']),0,51)
for row in track['frames']:row['inverse']=np.linalg.inv(np.array(row['homography'])).tolist()
(d/'controls.json').write_text(json.dumps(track,indent=2))
d=extract('specimen',R/'out/lipsync_followup_review_v1/specimen_combined.mp4',12,106)
old=json.loads((R/'out/specimen_signal_v1/recipe.json').read_text())['diagnostics']
y,x=np.mgrid[:720,:1280].astype(float)
def smooth(a):
    a=np.clip(a,0,1);return a*a*(3-2*a)
records=[]
for i in range(106):
    f=cv2.imread(str(d/f'plates/{i+1:04d}.png')).astype(float)/255;b,g,r=cv2.split(f)
    roi=np.exp(-(((x-829)/74)**6+((y-239)/93)**6))
    warm=np.clip((g-b-.035)*12,0,1)*np.clip((r-b-.09)*9,0,1)*np.clip((g-.48)*5,0,1)*(1-smooth((r-g-.19)/.09))*roi
    neutral=1-smooth((np.maximum.reduce([r,g,b])-np.minimum.reduce([r,g,b])-.035)/.065)
    visible=1-cv2.GaussianBlur(neutral*smooth((y-265)/30)*smooth((g-.27)/.12),(0,0),1.2)
    warm*=visible;mass=warm.sum()
    records.append({'song_frame':2016+i,'vocal_envelope':old[i]['vocal_envelope'],'cx':float((warm*x).sum()/max(mass,1e-6)),'cy':float((warm*y).sum()/max(mass,1e-6))})
(d/'controls.json').write_text(json.dumps({'frames':records,'song_frames':[2016,2122],'source':'out/lipsync_followup_review_v1/specimen_combined.mp4','source_frames':[12,118]},indent=2))
print('Original plates and tracked controls ready. No external FX layers created.')
