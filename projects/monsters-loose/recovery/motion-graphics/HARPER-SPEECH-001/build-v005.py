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

def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
for i,(lines,start,end) in enumerate([(['EVERY HABITAT','HAS ITS WONDERS.'],13,60),(['THE LAB','MIXES THINGS UP.'],93,140)]):
 cx,cy,sx,sy,tilt=[(1.62,3.66,1,1,-.5),(1.94,3.49,1.02,1.02,-1.0)][i]
 words_by_line=[]
 for line in lines:
  row=[]
  for text in line.split():
   cu=bpy.data.curves.new(text,'FONT');cu.body=text;cu.font=font;cu.align_x='LEFT';cu.align_y='CENTER';cu.size=1
   ob=bpy.data.objects.new(text,cu);s.collection.objects.link(ob);cu.materials.append(ink);bpy.context.view_layer.update();row.append((ob,ob.dimensions.x))
  words_by_line.append(row)
 first_width=words_by_line[0][0][1]
 full_width=sum(w for ob,w in words_by_line[0])+.18
 initial_sx=max(.34,(first_width+.9)/6.3)
 def shape(f):
  gx=smooth((f-start-2)/7);gy=smooth((f-start-8)/10)
  settle=.01*math.sin(math.pi*(f-start-20)/8) if start+20<=f<=start+28 else 0
  ax=(initial_sx+(sx-initial_sx)*gx)*(1+settle);ay=(.56+(sy-.56)*gy)*(1+settle)
  dx=.025*math.sin(f*.06);dy=.018*math.sin(f*.045)
  # Keep the body clear of Harper; tail alone follows her authored head motion.
  hx=-.15*max(0,min(1,(f-48)/96));hy=-.10*max(0,min(1,(f-24)/96))
  tip=(-2.38+hx,2.18+hy)
  pts=[]
  for x,y in points:
   w=max(0,1-math.hypot(x+4,y+1.48)/2.05)**1.5
   px=cx+dx+x*ax;py=cy+dy+y*ay
   px+=(tip[0]-(cx+dx-4*ax))*w;py+=(tip[1]-(cy+dy-1.48*ay))*w
   pts.append((px,py))
  return pts,cx+dx,cy+dy,gx,gy
 n=len(points)
 def verts(f,ribbon=False):
  pts,*_=shape(f)
  if not ribbon:return [(x,y,0) for x,y in pts]
  outer=[];inner=[]
  for j,(x,y) in enumerate(pts):
   prev=pts[(j-1)%n];nxt=pts[(j+1)%n];tx=nxt[0]-prev[0];ty=nxt[1]-prev[1];ln=max(.001,math.hypot(tx,ty));nx=-ty/ln;ny=tx/ln
   width=.036*(1+.22*math.sin(j*2*math.pi/n*3+.7)+.12*math.sin(j*2*math.pi/n*7+1.3))
   outer.append((x+nx*width,y+ny*width,.025));inner.append((x-nx*width,y-ny*width,.025))
  return outer+inner
 for name,material,ribbon in [('Ivory expanding balloon',paper,False),('Weighted continuous outline',ink,True)]:
  me=bpy.data.meshes.new(name);me.from_pydata(verts(start,ribbon),[],[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)] if ribbon else [tuple(range(n))]);me.update()
  ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);me.materials.append(material);visible(ob,start,end)
  ob.shape_key_add(name='Basis');ob.data.shape_keys.use_relative=False
  for f in range(1,145):
   key=ob.shape_key_add(name='frame%03d'%f);key.interpolation='KEY_LINEAR'
   for v,co in zip(key.data,verts(f,ribbon)):v.co=co
   ob.data.shape_keys.eval_time=key.frame;ob.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)
 for li,row in enumerate(words_by_line):
  total=sum(w for ob,w in row)+.18*(len(row)-1);offset=-total/2
  for wi,(ob,w) in enumerate(row):
   arrival=start+(2+wi*6 if li==0 else 12+wi*4);visible(ob,arrival,end)
   for f in range(1,145):
    pts,bx,by,gx,gy=shape(f)
    xx=(-first_width/2+(offset+first_width/2)*gx) if li==0 and wi==0 else offset
    ob.location=(bx+xx,by+(.31*gy if li==0 else -.38),.07);ob.keyframe_insert(data_path='location',frame=f)
   offset+=w+.18
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:
      if cu.data_path!='hide_render':k.interpolation='LINEAR'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'frames-v005/bubble-')
(o/'frames-v005').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Harper-speech-v005.blend'));bpy.ops.render.render(animation=True)
