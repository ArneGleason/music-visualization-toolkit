"""Continue accepted numerical sprite state; extract only original video plates."""
from pathlib import Path
import json,gzip,subprocess,shutil,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'screen'
(D/'plates').mkdir(parents=True,exist_ok=True); (D/'screen_plates').mkdir(exist_ok=True)
def extract(file,first,last,destination):
    if (destination/f'{last-first:04d}.png').exists():return
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/file),'-vf',f'trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS','-frames:v',str(last-first),str(destination/'%04d.png')],check=True)
extract('out/receiver_reply_arrival_v1/base.mp4',119,188,D/'plates')
extract('clips/raw/interference_bloom_v6.mp4',0,103,D/'screen_plates')
# The hidden receiver plate holds after the screen completely fills the frame.
for f in range(70,116):shutil.copyfile(D/'plates/0069.png',D/'plates'/f'{f:04d}.png')
old={v['song_frame']:v for v in json.loads((R/'out/receiver_now_v3/tracking.json').read_text())['frames']}
tracks={v['song_frame']:v for v in json.loads((R/'out/screen_garden_trial/tracking.json').read_text())['frames']}
code='# Retain the tested audio'+(O/'prepare_message.py').read_text().split('# Retain the tested audio',1)[1].split('rows=[]; geometry=[]',1)[0]
exec(compile(code,str(O/'prepare_message.py'),'exec'))
# Warm the actual phase-folded oscillator, not a new approximate circle.
for sf in range(971,1189):
    ns['current_transform']=np.array(old[sf]['transform']) if sf in old else np.eye(2,3)
    for sub in range(2):
        for sprite in sprites:sprite.render(sf+(sub+.5)/2)
rows=[]; geometry=[]
for sf in range(1189,1304):
    record=(old if sf<1201 else tracks).get(sf,tracks[1257]); matrix=np.array(record['transform']); ns['current_transform']=matrix
    rows.append({'song_frame':sf,'voice':record['voice'] if sf<1258 else 0,'receiver':sf<1258,'inverse':np.linalg.inv(np.vstack((matrix,[0,0,1]))).tolist(),'transform':matrix.tolist()})
    subs=[]
    for sub in range(2):
        at=sf+(sub+.5)/2; paths=[]
        for sprite in sprites:
            p=sprite.render(at)
            if sf<1258 and p:paths.append(p)
        if sf<1258:paths+=hardware(at,matrix,record['voice'])
        subs.append(paths)
    geometry.append(subs)
with gzip.open(D/'paths.json.gz','wt') as f:json.dump(geometry,f)
(D/'controls.json').write_text(json.dumps({'fps':24,'song_frames':[1189,1304],'delivery_song_frames':[1201,1304],'delivery_frames':[12,115],'frames':rows,'sources':[{'file':'out/receiver_reply_arrival_v1/base.mp4','source_frames':[119,188],'song_frames':[1189,1258],'hidden_hold_after':1258},{'file':'clips/raw/interference_bloom_v6.mp4','source_frames':[0,103],'song_frames':[1201,1304]}],'screen_crop':[380,100,520,520]},indent=2))
print('Screen continuation prepared,115 scene frames including12 history frames.')
