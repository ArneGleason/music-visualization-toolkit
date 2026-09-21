import bpy,json,warnings,sys
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
p=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(p/'MonstersUndone-v94.blend'))
s=bpy.context.scene;s.frame_set(1);factor=1.5
paths=set()
for st in s.sequence_editor.strips:
 if hasattr(st,'transform'):
  for key in ['offset_x','offset_y']:
   paths.add(st.transform.path_from_id(key));setattr(st.transform,key,getattr(st.transform,key)*factor)
  if st.type in ['MOVIE','IMAGE']:
   for key in ['scale_x','scale_y']:
    paths.add(st.transform.path_from_id(key));setattr(st.transform,key,getattr(st.transform,key)*factor)
 if st.type=='TEXT':
  paths.add(st.path_from_id('font_size'));st.font_size*=factor
# Scale animated pixel coordinates and media zoom keys as well as static values.
a=s.animation_data.action if s.animation_data else None
if a:
 curves=[]
 for layer in a.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:curves.extend(bag.fcurves)
 for fc in curves:
  if fc.data_path in paths:
   for k in fc.keyframe_points:
    k.co.y*=factor;k.handle_left.y*=factor;k.handle_right.y*=factor
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.ffmpeg.constant_rate_factor='PERC_LOSSLESS';s.render.ffmpeg.ffmpeg_preset='GOOD'
s.render.filepath=str(p/'MonstersUndone-v94-master-1080p-render.mp4')
s.name='Monsters Undone v94 1080p master';s.frame_start=1;s.frame_end=5290
bpy.ops.wm.save_as_mainfile(filepath=str(p/'MonstersUndone-v94-master-1080p.blend'))
if '--check' in sys.argv:
 for f in [504,2541,3130,5285]:
  s.frame_start=f;s.frame_end=f;s.render.filepath=str(p/f'master-check-{f}.mp4');bpy.ops.render.render(animation=True)
else:bpy.ops.render.render(animation=True)
