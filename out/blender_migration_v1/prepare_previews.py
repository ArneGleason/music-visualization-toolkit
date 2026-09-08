from pathlib import Path
import json
O=Path(__file__).resolve().parent;R=O.parents[1]
d=json.loads((R/'out/swirl_tail_review_v1/shotlist.json').read_text())
for s in d['shots']:
    if s['id']=='opening_need_landscape':s['clip']['file']='out/blender_migration_v1/aerial/native_clean.mp4'
    elif s['id'] in ['s009','s011']:s['clip']['file']='out/blender_migration_v1/probe/native_clean.mp4'
(O/'preview_shotlist.json').write_text(json.dumps(d,indent=2))
