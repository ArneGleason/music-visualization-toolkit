import bpy, math, json
from pathlib import Path
o=Path(__file__).resolve().parent
cfg=json.loads((o/'tracks.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=cfg['frames'];s.render.film_transparent=True
s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.show_specular_highlight=False;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1916;s.camera.data.clip_end=2000

def track(f):
 rows=cfg['ellipse_keys']
 for a,b in zip(rows,rows[1:]):
  if a[0]<=f<=b[0]:
   t=(f-a[0])/(b[0]-a[0]);return [x+(y-x)*t for x,y in zip(a[1:],b[1:])]
 return rows[0][1:] if f<rows[0][0] else rows[-1][1:]

def verts(f,accent):
 cx,cy,rx,ry,angle=track(f);angle=math.radians(angle)
 # Two short pressure-tapered ink strokes orbit just outside the loop.
 phase=(f-12)*.12+accent*math.pi
 strength=min(1,max(0,(f-6)/8),max(0,(84-f)/12))
 out=[]
 for side in (-1,1):
  for j in range(33):
   t=j/32;a=phase+t*.48
   w=1.7*math.sin(math.pi*t)**.65*strength
   x=(rx+12+side*w)*math.cos(a);y=(ry+10+side*w)*math.sin(a)
   px=cx+x*math.cos(angle)-y*math.sin(angle);py=cy+x*math.sin(angle)+y*math.cos(angle)
   out.append((px-958,540-py,.1))
 return out
m=bpy.data.materials.new('Warm pale comic motion accents');m.diffuse_color=(.72,.62,.40,1)
for i in range(2):
 me=bpy.data.meshes.new('Tapered arc');me.from_pydata(verts(1,i),[],[(j,j+1,j+34,j+33) for j in range(32)]);me.materials.append(m)
 ob=bpy.data.objects.new('Traveling motion accent '+str(i),me);s.collection.objects.link(ob);ob.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for f in range(1,cfg['frames']+1):
  key=ob.shape_key_add(name='frame%03d'%f);key.interpolation='KEY_LINEAR'
  for v,co in zip(key.data,verts(f,i)):v.co=co
  me.shape_keys.eval_time=key.frame;me.shape_keys.keyframe_insert(data_path='eval_time',frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
(o/'overlay').mkdir(exist_ok=True);s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'overlay/motion-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Lasso-prop-motion-v001.blend'));bpy.ops.render.render(animation=True)
