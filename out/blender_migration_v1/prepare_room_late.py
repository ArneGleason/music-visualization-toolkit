"""Late room appearances with accepted hold and source-frame mapping."""
from pathlib import Path
import json,shutil
O=Path(__file__).resolve().parent;D=O/'room_late';(D/'plates').mkdir(parents=True,exist_ok=True)
data=json.loads((O/'afterglow_b2/controls.json').read_text());rows=[]
for song in [*range(4400,4431),*range(4449,4516)]:
 index=min(song-4320,190);row=dict(data['frames'][index]);row['song_frame']=song;rows.append(row)
 shutil.copy2(O/'afterglow_b2/plates'/f'{index+1:04d}.png',D/'plates'/f'{len(rows):04d}.png')
data['frames']=rows;(D/'controls.json').write_text(json.dumps(data,indent=2))
