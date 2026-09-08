"""Inspect native scenes and image dependencies for the autonomous pass."""
from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent;R=O.parents[1];results=[]
families=sorted(d.name for d in O.iterdir() if d.is_dir() and (d/f'{d.name}_1280.blend').exists() and d.name!='shop_optics')
for family in families:
 for width in [1280,1920]:
  scene_file=O/family/f'{family}_{width}.blend'
  if not scene_file.exists():continue
  bpy.ops.wm.open_mainfile(filepath=str(scene_file));s=bpy.context.scene;issues=[];images=[]
  for image in bpy.data.images:
   if image.name in ['Render Result','Viewer Node']:continue
   if image.source=='GENERATED':issues.append('Generated pixel buffer: '+image.name);continue
   p=Path(bpy.path.abspath(image.filepath)).resolve();images.append(str(p))
   allowed=p.is_relative_to((O/family).resolve()) or (family in ('scope','world') and p.is_relative_to((R/'codex/out').resolve())) or (family=='shop_full' and p.is_relative_to((O/'shop_optics').resolve())) or (family=='probe' and p==(R/'clips/raw/signal_crossing_space_v6.mp4').resolve())
   if not allowed:issues.append('Review source provenance: '+str(p))
   if not p.exists():issues.append('Missing image: '+str(p))
  if (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)!=(width,width*9//16,100):issues.append('Resolution mismatch')
  if s.render.fps!=24 or s.render.fps_base!=1:issues.append('FPS mismatch')
  if s.sequence_editor and len(s.sequence_editor.strips):
   for strip in s.sequence_editor.strips:
    if strip.type=='SCENE':continue
    if strip.type=='MOVIE' and family=='aerial' and Path(bpy.path.abspath(strip.filepath)).resolve()==(R/'out/opening_aerial_flow_v1/base.mp4').resolve():images.append(bpy.path.abspath(strip.filepath));continue
    issues.append('Inspect sequence strip '+strip.name)
  results.append({'family':family,'width':width,'file':str(scene_file),'frames':[s.frame_start,s.frame_end],'images':images,'issues':issues})
(O/'autonomous_blend_audit.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'scenes':len(results),'issues':[r for r in results if r['issues']]},indent=2))
