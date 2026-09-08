"""Record selected native frame ranges for the later 1080 delivery, without rendering."""
from pathlib import Path
import json
O=Path(__file__).resolve().parent;R=O.parents[1]
edl=json.loads((O/'full_native_review_draft.json').read_text());groups={}
for shot in edl['shots']:
 p=Path(shot['clip']['file']);p=p if p.is_absolute() else R/p
 if not p.is_relative_to(O):continue
 family=p.parent.name;start=round(shot['clip'].get('in_sec',0)*24);end=start+shot['frames']
 if family=='message' and p.name=='performance_clean.mp4':start=max(0,start-60);end=max(0,end-60)
 offset=12 if family=='screen' else 0
 item=groups.setdefault(family,{'scene':str((O/family/f'{family}_1920.blend').relative_to(R)).replace('\\','/'),'blender_frame_ranges_end_exclusive':[],'cuts':[]})
 item['blender_frame_ranges_end_exclusive'].append([start+1+offset,end+1+offset]);item['cuts'].append(shot['id'])
for item in groups.values():
 merged=[]
 for a,z in sorted(item['blender_frame_ranges_end_exclusive']):
  if merged and a<=merged[-1][1]:merged[-1][1]=max(z,merged[-1][1])
  else:merged.append([a,z])
 item['blender_frame_ranges_end_exclusive']=merged
plan={'status':'planning_only_not_upscaled_or_mastered','resolution':[1920,1080],'fps':24,'native_scenes':groups,'assembly':'Rebuild native FX caches at target resolution, remap cache spans in Blender, render lyrics and review numbers at target resolution. Do not upscale the 720 composite. Preserve all song-frame and source-frame clocks.','video_upscale':'Future selected-span source-video upscale replaces only raw plates. No external upscale or mastering was invoked.','exceptions':['Message performance cache has60untreated source frames before the native effect. Preserve this through native VSE source segments.','Screen transition cache begins at native scene frame13.','Probe output has an unused internal gap; only listed ranges are seen.','Do not overwrite720preview caches with1080media or reinterpret their source offsets.']}
(O/'resolution_delivery_plan.json').write_text(json.dumps(plan,indent=2))
