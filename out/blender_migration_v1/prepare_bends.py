"""Extract accepted untreated performances; retain their exact resolved clocks."""
from pathlib import Path
import json, subprocess, sys
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'bends'
sys.path.insert(0,str(R/'tools'))
from assembly_sources import load_decisions, resolve_clip
from assembly_timebase import conform_clip
(D/'plates').mkdir(parents=True,exist_ok=True)
edl=json.loads((R/'out/swimmer_chorus_review_v1/shotlist.json').read_text())
records=[]; offset=0
for ident in ['s045','s046']:
    shot=next(s for s in edl['shots'] if s['id']==ident)
    clip=conform_clip(R,resolve_clip(R,shot,24,load_decisions(R)),24,prepare=False)
    first=round(clip['in_sec']*24); count=shot['frames']
    if not (D/'plates'/f'{offset+count:04d}.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/clip['file']),'-vf',f'trim=start_frame={first}:end_frame={first+count},setpts=PTS-STARTPTS','-frames:v',str(count),'-start_number',str(offset+1),str(D/'plates/%04d.png')],check=True)
    records.append({'id':ident,'source':clip['file'],'source_frames':[first,first+count],'delivery_frames':[offset,offset+count]}); offset+=count
assert offset==137
(D/'controls.json').write_text(json.dumps({'song_frames':[3505,3642],'fps':24,'sources':records,'frames':[{'song_frame':3505+i} for i in range(137)],'persistence_decay':.78,'persistence_frames':32},indent=2))

