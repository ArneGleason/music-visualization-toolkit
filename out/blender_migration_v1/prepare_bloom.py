"""Preserve accepted lip-sync plate and above-head conductor's exact numerical path."""
from pathlib import Path
import json,subprocess,runpy
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'bloom'
(D/'plates').mkdir(parents=True,exist_ok=True)
if not (D/'plates/0068.png').exists():
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'out/garden_bloom_synced_v5/plate24.mp4'),'-vf','trim=start_frame=66:end_frame=134,setpts=PTS-STARTPTS','-frames:v','68',str(D/'plates/%04d.png')],check=True)
position=runpy.run_path(str(R/'out/garden_guide_conductor_v4/guide.py'))['position']
def point(sf):return [float(v) for v in position(sf)]
rows=[{'song_frame':sf,'samples':[{'head':point(sf+s),'tail':[point(sf+s-age*.32) for age in range(12)]} for s in [-.3,.3]]} for sf in range(1786,1854)]
(D/'controls.json').write_text(json.dumps({'frames':rows,'song_frames':[1786,1854],'source':'out/garden_bloom_synced_v5/plate24.mp4','source_frames':[66,134]},indent=2))
