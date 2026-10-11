import bpy,json,math
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
root=Path('C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit/projects/a-right-little-something/generated/storyboard/hologram-overlay-v01')
bpy.ops.wm.open_mainfile(filepath=str(root/'hologram-overlay-v01.blend'))
s=bpy.context.scene;data=json.loads((root/'tracking.json').read_text());errors=[]
for frame in (101,113,125,144):
 s.frame_set(frame);bpy.context.view_layer.update()
 for name,rows in data['systems'].items():
  row=next(r for r in rows if r['frame']==frame);obj=bpy.data.objects['SYSTEM / '+name]
  p=world_to_camera_view(s,s.camera,obj.matrix_world.translation)
  errors.append(math.dist(row['pixel'],[p.x*1920,(1-p.y)*1080]))
assert max(errors)<.01,errors
(root/'projection-check.json').write_text(json.dumps({'samples':len(errors),'maximumProjectionResidualPx':max(errors),'scope':'Root projection against measured image points, not accuracy of the tracking or depth assumptions'},indent=2)+'\n')
print('Projected source-point registration:',max(errors),'px over',len(errors),'samples')
