import bpy
from pathlib import Path
p=Path('projects/a-right-little-something').resolve()
bpy.ops.wm.open_mainfile(filepath=str(p/'generated/storyboard/opening-v02/opening-storyboard-v01.blend'))
print('SCENES',[(s.name,len(s.objects)) for s in bpy.data.scenes])
s=next(s for s in bpy.data.scenes if s.name.startswith('opening-004'))
s.frame_set(13)
for o in s.objects:
 if o.type in ['MESH','CURVE','CAMERA','EMPTY']:
  print(o.name, o.type,tuple(round(v,3) for v in o.matrix_world.translation),[m.name for m in o.data.materials] if o.type in ['MESH','CURVE'] else '')
