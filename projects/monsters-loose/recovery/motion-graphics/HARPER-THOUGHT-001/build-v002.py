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
rootob=bpy.data.objects.new('Thought bubble - soft head follow',None);s.collection.objects.link(rootob)
bodyob=bpy.data.objects.new('Main cloud - delayed assembly',None);s.collection.objects.link(bodyob);bodyob.parent=rootob
def cloud(name,rx,ry,z,material,center=(0,0),lobes=10):
 n=160;verts=[]
 for depth in (z-.055,z):
  for i in range(n):
   a=2*math.pi*i/n;r=1+.035*math.cos(lobes*a)
   verts.append((center[0]+rx*r*math.cos(a),center[1]+ry*r*math.sin(a),depth))
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
 faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);ob.data.materials.append(material);ob.parent=bodyob
 return ob
cloud('Ink silhouette',2.02,.91,0,ink)
cloud('Ivory face',1.955,.845,.035,paper)
dot_groups=[]
for i,(x,y,r) in enumerate(((-3.38,.50,.065),(-2.98,.59,.105),(-2.51,.48,.17))):
 group=bpy.data.objects.new('Thought bead '+str(i+1),None);s.collection.objects.link(group)
 group.parent=rootob;group.location=(x,y,0);dot_groups.append(group)
 for label,radius,z,material in [('ink',r,0,ink),('paper',r-.022,.035,paper)]:
  ob=cloud('Thought dot '+label+' '+str(i),radius,radius,z,material,(0,0),0);ob.parent=group
font=bpy.data.fonts.load(str(root/'fonts'/'Bangers-Regular.ttf'))
for body,y,size in [('ANOTHER DAY',.24,.79),('IN PARADISE',-.33,.88)]:
 curve=bpy.data.curves.new(body,'FONT');curve.body=body;curve.font=font
 curve.align_x='CENTER';curve.align_y='CENTER';curve.size=size;curve.extrude=.008
 ob=bpy.data.objects.new(body,curve);s.collection.objects.link(ob);ob.parent=bodyob;ob.location=(0,y,.085);ob.data.materials.append(ink)
# Soft head-follow, authored from sampled temple movement with reduced amplitude
# and a few frames of lag. Shared depth keeps the whole thought in one space.
for f,x,y,z,tilt in [(1,2.5,2.55,-.7,-3),(26,2.5,2.55,-.7,-3),
 (52,2.56,2.53,-.65,-2),(78,2.66,2.45,-.61,0),(98,2.70,2.43,-.60,1),(121,2.70,2.43,-.6,1)]:
 rootob.location=(x,y,z);rootob.rotation_euler=(math.radians(-3),math.radians(tilt),math.radians(-2))
 for path in ('location','rotation_euler'):rootob.keyframe_insert(data_path=path,frame=f)
# The chain assembles small-to-large over a restrained 0.6 second interval.
for i,group in enumerate(dot_groups):
 start=14+i*3
 for f,v in [(1,.001),(start,.001),(start+4,1.025),(start+7,1),(99+i*2,1),(105+i*2,.001),(121,.001)]:
  group.scale=(v,)*3;group.keyframe_insert(data_path='scale',frame=f)
for f,scale,x,y,z,tilt in [(1,.001,-.18,-.05,-.25,-8),(22,.001,-.18,-.05,-.25,-8),
 (30,1.025,0,0,.02,2),(36,1,0,0,0,0),(96,1,0,.025,.015,0),
 (104,.96,.05,.06,-.08,3),(114,.001,.14,.12,-.35,9),(121,.001,.14,.12,-.35,9)]:
 bodyob.location=(x,y,z);bodyob.scale=(scale,)*3;bodyob.rotation_euler=(0,math.radians(tilt),0)
 for path in ('location','scale','rotation_euler'):bodyob.keyframe_insert(data_path=path,frame=f)
# Clamp curve handles to prevent overshoot around the hidden holds.
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.handle_left_type='AUTO_CLAMPED';key.handle_right_type='AUTO_CLAMPED'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
s.render.filepath=str(root/'frames-v002'/'bubble-')
s.frame_set(50)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Harper-thought-bubble-v002.blend'))
bpy.ops.render.render(animation=True)

