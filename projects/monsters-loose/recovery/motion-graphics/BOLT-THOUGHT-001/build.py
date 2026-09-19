import bpy, math, pathlib
from mathutils import Vector
root=pathlib.Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=241
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
cloud('Ink silhouette',1.25,.65,0,ink)
cloud('Ivory face',1.185,.585,.035,paper)
dot_groups=[]
for i,(x,y,r) in enumerate(((-2.32,.40,.065),(-1.96,.49,.105),(-1.60,.38,.17))):
 group=bpy.data.objects.new('Thought bead '+str(i+1),None);s.collection.objects.link(group)
 group.parent=rootob;group.location=(x,y,0);dot_groups.append(group)
 for label,radius,z,material in [('ink',r,0,ink),('paper',r-.022,.035,paper)]:
  ob=cloud('Thought dot '+label+' '+str(i),radius,radius,z,material,(0,0),0);ob.parent=group
font=bpy.data.fonts.load(str(root.parent/'HARPER-THOUGHT-001'/'fonts'/'Bangers-Regular.ttf'))
for body,y,size in [('OH MY',0,1.0)]:
 curve=bpy.data.curves.new(body,'FONT');curve.body=body;curve.font=font
 curve.align_x='CENTER';curve.align_y='CENTER';curve.size=size;curve.extrude=.008
 ob=bpy.data.objects.new(body,curve);s.collection.objects.link(ob);ob.parent=bodyob;ob.location=(0,y,.085);ob.data.materials.append(ink)
# Shared placement stays fixed; each link gets a separate amount of head follow.
rootob.location=(3.1,2.3,-.7)
rootob.rotation_euler=(math.radians(-3),math.radians(-3),math.radians(-2))
cloud_follow=bpy.data.objects.new('Cloud follow - 25 percent, 8 frame lag',None)
s.collection.objects.link(cloud_follow);cloud_follow.parent=rootob;bodyob.parent=cloud_follow
# Authored head displacement from the same sampled footage used in v002.
head_keys=[(1,0,0,0),(48,0,0,0),(64,.02,-.025,0),(82,.04,-.055,0),(121,.04,-.055,0)]
for ob,weight,lag in [(dot_groups[0],1.0,0),(dot_groups[1],.65,3),
                      (dot_groups[2],.42,5),(cloud_follow,.25,8)]:
 base=ob.location.copy()
 ob['head_follow_weight']=weight;ob['head_follow_delay_frames']=lag
 ob.location=base;ob.keyframe_insert(data_path='location',frame=1)
 for frame,dx,dy,dz in head_keys:
  ob.location=base+Vector((dx*weight,dy*weight,dz*weight))
  ob.keyframe_insert(data_path='location',frame=min(frame+lag,121))
# The chain assembles small-to-large over a restrained 0.6 second interval.
for i,group in enumerate(dot_groups):
 start=42+i*3
 for f,v in [(1,.001),(start,.001),(start+4,1.025),(start+7,1),(99+i*2,1),(105+i*2,.001),(121,.001)]:
  group.scale=(v,)*3;group.keyframe_insert(data_path='scale',frame=f)
for f,scale,x,y,z,tilt in [(1,.001,-.18,-.05,-.25,-8),(50,.001,-.18,-.05,-.25,-8),
 (55,1.025,0,0,.02,2),(61,1,0,0,0,0),(96,1,0,.025,.015,0),
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
s.render.filepath=str(root/'frames'/'bubble-')
s.frame_set(50)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Bolt-oh-my-v001.blend'))
bpy.ops.render.render(animation=True)

