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
# One hand-shaped contour; the curved tail is part of the same perimeter.
segments=[((-3.12,-.30),(-3.40,.18),(-3.06,.73),(-2.35,.90)),((-2.35,.90),(-1.37,1.20),(.77,1.14),(2.25,.94)),((2.25,.94),(3.04,.83),(3.47,.39),(3.36,-.12)),((3.36,-.12),(3.30,-.64),(2.73,-.96),(1.87,-1.00)),((1.87,-1.00),(.54,-1.10),(-.89,-1.03),(-1.85,-.88)),((-1.85,-.88),(-2.12,-1.51),(-3.20,-1.49),(-4.00,-1.48)),((-4.00,-1.48),(-3.35,-1.43),(-2.86,-1.21),(-2.79,-.61)),((-2.79,-.61),(-2.94,-.52),(-3.05,-.42),(-3.12,-.30))]
points=[]
for a,b,c,d in segments:
 for j in range(24):
  t=j/24;points.append(tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in (0,1)))
def visible(ob,first,last):
 for f,v in [(1,True),(first-1,True),(first,False),(last,False),(last+1,True)]:ob.hide_render=v;ob.keyframe_insert(data_path='hide_render',frame=f)
for i,(lines,start,end) in enumerate([(['EVERY HABITAT','HAS ITS WONDERS.'],13,60),(['WE BRING','THEM HERE.'],61,92),(['THE LAB','MIXES THINGS UP.'],93,140)]):
 group=bpy.data.objects.new('Speech beat '+str(i+1),None);s.collection.objects.link(group)
 me=bpy.data.meshes.new('Continuous balloon');me.from_pydata([(x,y,0) for x,y in points],[],[tuple(range(len(points)))]);me.update();ob=bpy.data.objects.new('Ivory continuous balloon',me);s.collection.objects.link(ob);ob.parent=group;ob.data.materials.append(paper);visible(ob,start,end)
 cu=bpy.data.curves.new('Single uninterrupted ink perimeter','CURVE');cu.dimensions='3D';cu.bevel_depth=.026;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for v,(x,y) in zip(sp.points,points):v.co=(x,y,.022,1)
 sp.use_cyclic_u=True;ob=bpy.data.objects.new('Ink outline including curved tail',cu);s.collection.objects.link(ob);ob.parent=group;ob.data.materials.append(ink);visible(ob,start,end)
 wi=0
 for line,y in zip(lines,[.31,-.38]):
  words=[]
  for word in line.split():
   cu=bpy.data.curves.new(word,'FONT');cu.body=word;cu.font=font;cu.align_x='LEFT';cu.align_y='CENTER';cu.size=1.0
   ob=bpy.data.objects.new(word,cu);s.collection.objects.link(ob);ob.parent=group;ob.data.materials.append(ink);bpy.context.view_layer.update();words.append((ob,ob.dimensions.x))
  total=sum(w for _,w in words)+.18*(len(words)-1);x=-total/2
  for ob,w in words:
   ob.location=(x,y,.065);arrival=start+2+wi*2;visible(ob,arrival,end)
   for f,k in [(arrival,.99),(arrival+3,1)]:ob.scale=(k,k,k);ob.keyframe_insert(data_path='scale',frame=f)
   x+=w+.18;wi+=1
 lastword=start+2+(wi-1)*2
 # Already near final size. A short drift away from speaker, then a tiny final-word settle.
 for f,sc,dx,dy in [(start,1.035,-.11,-.04),(start+6,1.009,0,0),(lastword+1,1.017,.008,0),(lastword+7,1,0,0),(end-4,1,0,0),(end,.995,.045,.015)]:
  group.scale=(sc,)*3;group.location=(1.62+dx,3.66+dy,0)
  for prop in ['scale','location']:group.keyframe_insert(data_path=prop,frame=f)
for a in bpy.data.actions:
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:
      if cu.data_path!='hide_render':k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'frames-v003/bubble-');s.frame_set(35)
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Harper-speech-v003.blend'));bpy.ops.render.render(animation=True)
