import bpy,math
from pathlib import Path
r=Path(r"C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913");o=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=144;s.render.film_transparent=True
s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.show_specular_highlight=False;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,20));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=19.16

def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
ink=mat('Warm ink',(.024,.032,.029));paper=mat('Ivory paper',(.94,.88,.69))
font=bpy.data.fonts.load(str(r/'motion-graphics/HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf'))
def mesh(n,vs,ma,parent,z):
 me=bpy.data.meshes.new(n);me.from_pydata([(x,y,z) for x,y in vs],[],[tuple(range(len(vs)))]);me.update();ob=bpy.data.objects.new(n,me);s.collection.objects.link(ob);ob.parent=parent;ob.data.materials.append(ma);return ob
for i,(lines,start,end) in enumerate([(['EVERY HABITAT','HAS ITS WONDERS.'],13,60),(['WE BRING','THEM HERE.'],61,92),(['THE LAB','MIXES THINGS UP.'],93,140)]):
 group=bpy.data.objects.new('Speech beat '+str(i+1),None);s.collection.objects.link(group);group.location=(1.62,3.66,0)
 # Tail toward mouth; rounded balloon remains clear of face and main beast.
 mesh('Tail ink',[(-2.45,-.35),(-4.0,-1.48),(-1.65,-.70)],ink,group,.005)
 mesh('Tail ivory',[(-2.40,-.31),(-3.85,-1.36),(-1.72,-.64)],paper,group,.015)
 for name,rx,ry,z,ma in [('Balloon ink',3.45,1.12,.02,ink),('Balloon paper',3.39,1.06,.03,paper)]:
  mesh(name,[(rx*math.cos(a*2*math.pi/128),ry*math.sin(a*2*math.pi/128)) for a in range(128)],ma,group,z)
 for line,y in zip(lines,[.34,-.36]):
  cu=bpy.data.curves.new(line,'FONT');cu.body=line;cu.font=font;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=1.0
  ob=bpy.data.objects.new(line,cu);s.collection.objects.link(ob);ob.parent=group;ob.location=(0,y,.06);ob.data.materials.append(ink)
 for f,sc,dz,tilt in [(1,.001,-.15,-4),(start,.001,-.15,-4),(start+4,1.025,.03,1),(start+7,1,0,0),(end-5,1,0,0),(end,.001,-.12,3),(144,.001,-.12,3)]:
  group.scale=(sc,)*3;group.rotation_euler=(0,math.radians(tilt),0);group.location=(1.62-.035*f/144,3.66-.04*f/144,dz)
  for prop in ['scale','rotation_euler','location']:group.keyframe_insert(data_path=prop,frame=f)
for a in bpy.data.actions:
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'frames/bubble-');s.frame_set(35)
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Harper-speech-v001.blend'));bpy.ops.render.render(animation=True)

