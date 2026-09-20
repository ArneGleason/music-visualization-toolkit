import bpy,math
from pathlib import Path
r=Path(r"C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913");o=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=121;s.render.film_transparent=True
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

# One continuous shape: expand its body while the tail stays attached near Harper.
def visible(ob,first,last=111):
 for f,v in [(1,True),(first-1,True),(first,False),(last,False),(last+1,True)]:
  ob.hide_render=v;ob.keyframe_insert(data_path='hide_render',frame=f)
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def growth(f):
 g=smooth((f-46)/12)
 # Very restrained settling after the last word, no large bounce.
 settle=.014*math.sin(math.pi*max(0,min(1,(f-58)/8))) if 58<=f<=66 else 0
 return g,settle
def shape(f):
 g,b= growth(f);sx=.34+(.72-.34)*g;sy=.44+(.98-.44)*g
 cx=-2.48+.20*g;cy=3.68-.03*g
 drift=.018*math.sin(f*.07)
 cy+=drift
 # Mouth moves downward slightly as she leans back, stronger follow at tail tip.
 dy=-.32*smooth((f-40)/50)
 tip=(-4.00+.04*smooth((f-40)/50),1.61+dy)
 pts=[]
 for x,y in points:
  w=max(0,1-math.hypot(x+4,y+1.48)/2.05)**1.5
  px=cx+x*sx*(1+b);py=cy+y*sy*(1+b)
  px+=(tip[0]-(cx-4*sx*(1+b)))*w;py+=(tip[1]-(cy-1.48*sy*(1+b)))*w
  pts.append((px,py))
 return pts,cx,cy,g
n=len(points)
def verts(f,ribbon=False):
 pts,*_=shape(f)
 if not ribbon:return [(x,y,0) for x,y in pts]
 outer=[];inner=[]
 for j,(x,y) in enumerate(pts):
  prev=pts[(j-1)%n];nxt=pts[(j+1)%n];tx=nxt[0]-prev[0];ty=nxt[1]-prev[1];ln=max(.001,math.hypot(tx,ty));nx=-ty/ln;ny=tx/ln
  width=.031*(1+.22*math.sin(j*2*math.pi/n*3+.7)+.12*math.sin(j*2*math.pi/n*7+1.3))
  outer.append((x+nx*width,y+ny*width,.025));inner.append((x-nx*width,y-ny*width,.025))
 return outer+inner
for name,material,ribbon in [('Ivory expanding balloon',paper,False),('Natural weighted continuous outline',ink,True)]:
 me=bpy.data.meshes.new(name);me.from_pydata(verts(29,ribbon),[],[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)] if ribbon else [tuple(range(n))]);me.update()
 ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);me.materials.append(material);visible(ob,29)
 ob.shape_key_add(name='Basis')
 # Absolute shape keys interpolate one coherent contour, including its curved tail.
 ob.data.shape_keys.use_relative=False
 for f in range(1,122):
  key=ob.shape_key_add(name='frame%03d'%f)
  key.interpolation='KEY_LINEAR'
  for v,co in zip(key.data,verts(f,ribbon)):v.co=co
  ob.data.shape_keys.eval_time=key.frame;ob.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)

def word(text,size):
 cu=bpy.data.curves.new(text,'FONT');cu.body=text;cu.font=font;cu.align_x='LEFT';cu.align_y='CENTER';cu.size=size
 ob=bpy.data.objects.new(text,cu);s.collection.objects.link(ob);cu.materials.append(ink);bpy.context.view_layer.update();return ob,ob.dimensions.x
sorry,sw=word('SORRY.',.78);visible(sorry,31)
for f in range(1,122):
 pts,cx,cy,g=shape(f);sorry.location=(cx-sw/2,cy+.59*g,.07);sorry.keyframe_insert(data_path='location',frame=f)
for line,yy,arrivals in [("I'M NOT ON",0,[52,54,56]),('THE MENU.',-.59,[58,60])]:
 words=[word(w,.78) for w in line.split()];total=sum(w for ob,w in words)+.13*(len(words)-1);offset=-total/2
 for (ob,w),arrival in zip(words,arrivals):
  visible(ob,arrival)
  for f in range(1,122):
   pts,cx,cy,g=shape(f);ob.location=(cx+offset,cy+yy,.07);ob.keyframe_insert(data_path='location',frame=f)
  offset+=w+.13
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:
      if cu.data_path!='hide_render':k.interpolation='LINEAR'
folder=o/'overlay';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(folder/'bubble-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Aquarium-speech-v001.blend'));bpy.ops.render.render(animation=True)
