import bpy,json,math
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
root=Path('C:/Users/arneg/OneDrive/Documents/ChatGPT/music-visualization-toolkit/projects/a-right-little-something/generated/storyboard/hologram-overlay-v02')
bpy.ops.wm.open_mainfile(filepath=str(root/'hologram-overlay-v02.blend'))
s=bpy.context.scene;tracking=json.loads((root/'tracking.json').read_text());errors=[];counts={};planes=set();belt_count=0;moving=0
for frame in (101,113,125,144):
 s.frame_set(frame);bpy.context.view_layer.update()
 for name,rows in tracking['systems'].items():
  r=next(r for r in rows if r['frame']==frame);obj=bpy.data.objects['SYSTEM / '+name];p=world_to_camera_view(s,s.camera,obj.matrix_world.translation)
  errors.append(math.dist(r['pixel'],[p.x*1920,(1-p.y)*1080]));counts[name]=obj['planet_count']
for obj in s.objects:
 if '/ orbital plane ' in obj.name:planes.add(tuple(round(x,3) for x in obj.rotation_euler))
 if '/ asteroid belt ' in obj.name and obj.type=='MESH':belt_count+=len(obj.data.vertices)//6
 if '/ planet ' in obj.name and obj.type=='MESH' and '/ moon ' not in obj.name:
  s.frame_set(125);a=obj.location.copy();s.frame_set(144);moving+=math.dist(a,obj.location)>.0001
assert max(errors)<.01,errors
assert sorted(counts.values())==[2,3,4,5,6],counts
assert len(planes)>10 and belt_count==460 and moving==20,(len(planes),belt_count,moving)
d={'maxProjectionResidualPx':max(errors),'planetCounts':counts,'distinctOrbitalPlanes':len(planes),'asteroidParticles':belt_count,'movingPlanets':moving,'scope':'Registration against measured roots, baked orbital motion and contents; depth remains artist-assigned'}
(root/'scene-checks.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
