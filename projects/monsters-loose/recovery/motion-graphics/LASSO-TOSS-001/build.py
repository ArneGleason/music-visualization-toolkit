import bpy,math,json
from pathlib import Path
o=Path(__file__).resolve().parent;cfg=json.loads((o/'tracks.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=97;s.render.film_transparent=True
s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.show_specular_highlight=False;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1916;s.camera.data.clip_end=2000

def interp(rows,f):
 for a,b in zip(rows,rows[1:]):
  if a[0]<=f<=b[0]:
   t=(f-a[0])/(b[0]-a[0]);return [x+(y-x)*t for x,y in zip(a[1:],b[1:])]
 return rows[0][1:] if f<rows[0][0] else rows[-1][1:]
def points(f,part):
 hx,hy=interp(cfg['hand_keys'],f);wx,wy=interp(cfg['coil_keys'],f)
 # Loop hangs to the left/below glove. One release, then exits screen left.
 t=max(0,(f-cfg['release_frame'])/11);g=min(1,t)
 if t==0:cx,cy=hx-73*.707,hy+103*.707
 else:
  a,b=interp(cfg['hand_keys'],cfg['release_frame']);cx=a-73*.707-640*t;cy=b+103*.707-140*t+55*t*t
 rx=73+48*g;ry=103-57*g
 knot=(cx+rx*.707,cy-ry*.707)
 if part=='loop':return [(cx+rx*math.cos(-math.pi/4+2*math.pi*i/160),cy+ry*math.sin(-math.pi/4+2*math.pi*i/160)) for i in range(161)]
 # Slack lead starts at held coils, passes below torso, joins loop knot.
 end=knot; sag=max(30,110*(1-g))
 a=(wx-10,wy+12);b=(wx-55,wy+100*(1-g));c=(end[0]+65,end[1]+sag)
 return [tuple((1-u)**3*a[k]+3*(1-u)**2*u*b[k]+3*(1-u)*u*u*c[k]+u**3*end[k] for k in (0,1)) for u in [i/100 for i in range(101)]]
def verts(f,part,width,z,braid=False):
 pts=points(f,part);v=[]
 for side in (-1,1):
  for i,(x,y) in enumerate(pts):
   a=pts[max(0,i-1)];b=pts[min(len(pts)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];ln=max(.001,math.hypot(dx,dy));shift=(1.5*math.sin(i*1.5) if braid else 0)+side*width
   v.append((x-dy/ln*shift-958,540-y-dx/ln*shift,z))
 return v
for part in ('lead','loop'):
 for name,col,width,z,braid in [('Ink',(.025,.018,.009),5,0,False),('Hemp',(.55,.29,.095),3.6,.02,False),('Lit braid',(.88,.60,.28),.9,.04,True)]:
  mat=bpy.data.materials.new(part+name);mat.diffuse_color=(*col,1);n=len(points(0,part));me=bpy.data.meshes.new(part+name);me.from_pydata(verts(0,part,width,z,braid),[],[(i,i+1,i+1+n,i+n) for i in range(n-1)]);me.materials.append(mat)
  ob=bpy.data.objects.new(part+name,me);s.collection.objects.link(ob);ob.shape_key_add(name='Basis');me.shape_keys.use_relative=False
  for f in range(97):
   key=ob.shape_key_add(name='source%03d'%f);key.interpolation='KEY_LINEAR'
   for v,co in zip(key.data,verts(f,part,width,z,braid)):v.co=co
   me.shape_keys.eval_time=key.frame;me.shape_keys.keyframe_insert(data_path='eval_time',frame=f+1)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
(o/'overlay').mkdir(exist_ok=True);s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'overlay/rope-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Lasso-toss-v001.blend'));bpy.ops.render.render(animation=True)
