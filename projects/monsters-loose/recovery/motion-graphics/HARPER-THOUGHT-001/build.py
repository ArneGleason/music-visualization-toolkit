import bpy, math, pathlib
from mathutils import Vector
root=pathlib.Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=121
s.render.film_transparent=True
s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=False;s.display.shading.show_cavity=False
s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=False
s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,20))
s.camera=bpy.context.object;s.camera.data.lens=50;s.camera.data.sensor_width=36
s.camera.data.sensor_fit='HORIZONTAL'
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
ink=mat('Warm black ink',(.024,.032,.029));paper=mat('Warm ivory paper',(.94,.88,.69))
rootob=bpy.data.objects.new('Thought bubble - spatial anchor',None);s.collection.objects.link(rootob)
def cloud(name,rx,ry,z,material,center=(0,0),lobes=10):
 n=160;verts=[]
 for depth in (z-.055,z):
  for i in range(n):
   a=2*math.pi*i/n;r=1+.035*math.cos(lobes*a)
   verts.append((center[0]+rx*r*math.cos(a),center[1]+ry*r*math.sin(a),depth))
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
 faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);ob.data.materials.append(material);ob.parent=rootob
 return ob
cloud('Ink silhouette',2.02,.91,0,ink)
cloud('Ivory face',1.955,.845,.035,paper)
for i,(x,y,r) in enumerate(((-2.32,-.20,.075),(-2.16,-.30,.12),(-1.95,-.34,.18))):
 cloud('Thought dot ink '+str(i),r,r,0,ink,(x,y),0)
 cloud('Thought dot paper '+str(i),r-.025,r-.025,.035,paper,(x,y),0)
font=bpy.data.fonts.load(str(root/'fonts'/'Bangers-Regular.ttf'))
for body,y,size in [('ANOTHER DAY',.24,.79),('IN PARADISE',-.33,.88)]:
 curve=bpy.data.curves.new(body,'FONT');curve.body=body;curve.font=font
 curve.align_x='CENTER';curve.align_y='CENTER';curve.size=size;curve.extrude=.008
 ob=bpy.data.objects.new(body,curve);s.collection.objects.link(ob);ob.parent=rootob;ob.location=(0,y,.085);ob.data.materials.append(ink)
# A small depth approach and damped tilt, with restrained settling and retreat.
keys=[(1,.001,1.2,2.28,-.8,-16),(14,.001,1.2,2.28,-.8,-16),
 (21,1.045,1.2,2.38,.05,5),(28,1,1.2,2.38,0,-3),
 (76,1.015,1.16,2.42,.06,-1),(92,1.025,1.14,2.43,.08,0),
 (102,.96,1.15,2.48,-.1,5),(112,.001,1.2,2.57,-1,17),(121,.001,1.2,2.57,-1,17)]
for f,scale,x,y,z,tilt in keys:
 rootob.location=(x,y,z);rootob.scale=(scale,)*3
 rootob.rotation_euler=(math.radians(-4),math.radians(tilt),math.radians(-2))
 for path in ('location','scale','rotation_euler'):rootob.keyframe_insert(data_path=path,frame=f)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
s.render.filepath=str(root/'frames'/'bubble-')
s.frame_set(50)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Harper-thought-bubble-v001.blend'))
bpy.ops.render.render(animation=True)

