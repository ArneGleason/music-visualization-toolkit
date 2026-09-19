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
 cx,cy,sx,sy,tilt=[(1.62,3.66,1,1,-.5),(1.08,3.30,.84,.97,1.1),(1.94,3.49,1.02,1.02,-1.0)][i]
 weights=[max(0,1-math.hypot(x+4,y+1.48)/2.05)**1.5 for x,y in points]
 # Each layout moves independently; tail tip remains near the speaker.
 tipdx=-2.38-(cx-4*sx);tipdy=2.18-(cy-1.48*sy)
 pts=[(x*sx+tipdx*w,y*sy+tipdy*w) for (x,y),w in zip(points,weights)]
 def deform_mesh(name,verts,faces,material,ws):
  me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.parent=group;ob.data.materials.append(material);visible(ob,start,end)
  ob.shape_key_add(name='Basis')
  for axis,label in [(0,'Tail follows head horizontally'),(1,'Tail follows head vertically')]:
   key=ob.shape_key_add(name=label);key.slider_min=-1;key.slider_max=1
   for v,w in zip(key.data,ws):v.co[axis]+=.70*w
   for frame,dx,dy in [(1,0,0),(24,.05,.02),(48,.12,-.035),(72,.06,-.09),(96,-.09,-.13),(120,-.13,-.10),(144,-.15,-.10)]:
    key.value=(dx,dy)[axis];key.keyframe_insert(data_path='value',frame=frame)
  return ob
 deform_mesh('Ivory continuous balloon',[(x,y,0) for x,y in pts],[tuple(range(len(pts)))],paper,weights)
 # Ribbon outline: variable pen pressure, heavier lower curves, gently imperfect edge.
 outer=[];inner=[];n=len(pts)
 for j,(x,y) in enumerate(pts):
  prev=pts[(j-1)%n];nxt=pts[(j+1)%n];tx=nxt[0]-prev[0];ty=nxt[1]-prev[1];ln=max(.001,math.hypot(tx,ty));nx=-ty/ln;ny=tx/ln
  width=.044*(1+.22*math.sin(j*2*math.pi/n*3+.7)+.12*math.sin(j*2*math.pi/n*7+1.3))
  outer.append((x+nx*width,y+ny*width,.025));inner.append((x-nx*width,y-ny*width,.025))
 deform_mesh('Pressure-varied continuous ink',outer+inner,[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],ink,weights+weights)
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
  group.scale=(sc,)*3;group.location=(cx+dx,cy+dy,0)
  for prop in ['scale','location']:group.keyframe_insert(data_path=prop,frame=f)
 # A delayed, lighter body response plus very small ambient drift and tilt.
 drift=bpy.data.objects.new('Ambient and delayed head follow '+str(i+1),None);s.collection.objects.link(drift);group.parent=drift
 for f in range(1,145,4):
  phase=(f-1)/24
  h=max(0,(f-7)/144)
  drift.location=(.027*math.sin(phase*1.05+i*.5)-.022*h,.018*math.sin(phase*.83+i*.7)-.016*h,.025*math.sin(phase*.60+i))
  drift.rotation_euler=(math.radians(.35*math.sin(phase*.70)),math.radians(.55*math.sin(phase*.65+i)),math.radians(tilt+.18*math.sin(phase*.8)))
  for prop in ['location','rotation_euler']:drift.keyframe_insert(data_path=prop,frame=f)
for a in bpy.data.actions:
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:
      if cu.data_path!='hide_render':k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(o/'frames-v004/bubble-');s.frame_set(35)
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Harper-speech-v004.blend'));bpy.ops.render.render(animation=True)
