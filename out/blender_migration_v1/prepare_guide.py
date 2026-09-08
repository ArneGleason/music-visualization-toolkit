"""Numeric beat-grid trajectories; all light fields are rendered in Blender."""
from pathlib import Path
import json,math,subprocess,bisect
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'guide'
(D/'plates').mkdir(parents=True,exist_ok=True)
if not (D/'plates/0060.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'out/garden_walk_return_v1/base.mp4'),'-vf','trim=start_frame=12:end_frame=72,setpts=PTS-STARTPTS','-frames:v','60',str(D/'plates/%04d.png')],check=True)
beats=[v['sec']*24 for v in json.loads((R/'generated/overlay_cues.json').read_text())['beats']]
def flight(sf):
    i=max(0,min(len(beats)-2,bisect.bisect_right(beats,sf)-1));phase=i+(sf-beats[i])/(beats[i+1]-beats[i]);a=phase*math.tau
    return [865+225*(sf-1650)/60+42*math.sin(a-.6),235+42*math.cos(a)+12*math.sin(a*.5),5.5+1.5*math.sin(a-.4)**2,phase]
rows=[]
for sf in range(1650,1710):
    rows.append({'song_frame':sf,'samples':[{'head':flight(sf+s),'tail':[flight(sf+s-age*.20) for age in range(9)]} for s in [-.3,.3]]})
(D/'controls.json').write_text(json.dumps({'frames':rows,'song_frames':[1650,1710],'source':'out/garden_walk_return_v1/base.mp4','source_frames':[12,72]},indent=2))
