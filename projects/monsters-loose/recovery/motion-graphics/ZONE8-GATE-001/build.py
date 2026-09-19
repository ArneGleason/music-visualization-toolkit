import bpy,math,json,random
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
timing=json.loads((o/'timing.json').read_text());hits=timing['impact_source_frames_one_based']
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24
s.frame_start=1;s.frame_end=72;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,1200));cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1245;cam.data.clip_end=2400
def mat(name,col,alpha=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
 e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1);out=n.new('ShaderNodeOutputMaterial')
 if alpha==1:m.node_tree.links.new(e.outputs[0],out.inputs[0])
 else:
  tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha
  m.node_tree.links.new(tr.outputs[0],mix.inputs[1]);m.node_tree.links.new(e.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs[0])
 return m
def mesh(name,pts,faces,m):
 me=bpy.data.meshes.new(name);me.from_pydata(pts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.data.materials.append(m);return ob
m=mat('Painted steel gate',(1,1,1));tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(r/'assets/SCN-003-zone8-gate-v001.png'))
m.node_tree.links.new(tex.outputs['Color'],next(n for n in m.node_tree.nodes if n.type=='EMISSION').inputs[0])
cols,rows=160,90
pts=[(-640+x*1280/cols,-360+y*720/rows,0) for y in range(rows+1) for x in range(cols+1)]
faces=[]
for y in range(rows):
 for x in range(cols):
  a=y*(cols+1)+x;faces.append((a,a+1,a+cols+2,a+cols+1))
ob=mesh('Gate leaves and reactive foliage',pts,faces,m);uv=ob.data.uv_layers.new()
for p in ob.data.polygons:
 for li in p.loop_indices:
  v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=((v.x+640)/1280,(v.y+360)/720)
ob.shape_key_add(name='Basis')
def impulse(f,delay=0):
 return sum(math.exp(-(f-h-delay)/3.5)*math.cos((f-h-delay)*2.15) for h in hits if f>=h+delay)
def clamp(v):return max(0,min(1,v))
for f in range(1,73):
 k=ob.shape_key_add(name='Rigid leaf recoil %03d'%f)
 kick=impulse(f);leaf=impulse(f,2)
 for v,(x,y,z) in zip(k.data,pts):
  px=x+640;py=360-y
  # Broad near-rigid panels rotate a fraction around stationary outer hinges.
  left_edge=220-35*(py/720);right_edge=1080+40*(py/720)
  mask=clamp((px-left_edge)/24)*clamp((right_edge-px)/24)*clamp((685-py)/16)
  hinge=clamp(1-abs(px-645)/440)
  side=-1 if px<645 else 1
  v.co.x+=mask*hinge*side*6.0*kick
  v.co.y+=mask*hinge*2.3*kick
  latch=math.exp(-(((px-640)/170)**4+((py-398)/30)**4))
  v.co.x+=latch*2.8*impulse(f,1)
  foliage=mask*clamp((350-py)/80)
  v.co.y+=foliage*1.8*leaf*math.sin(px*.035)
 for at,value in [(f-1,0),(f,1),(f+1,0)]:k.value=value;k.keyframe_insert(data_path='value',frame=at)
 cam.location.x=2.5*kick;cam.location.y=1.6*impulse(f,1)
 cam.rotation_euler.z=math.radians(.14*kick)
 for prop in ('location','rotation_euler'):cam.keyframe_insert(data_path=prop,frame=f)
random.seed(8)
dust=mat('Amber dust',(.38,.25,.12),.20);fine=mat('Small falling grit',(.62,.40,.18),.60)
for h in hits:
 for j in range(25):
  ground=j<16
  px=random.uniform(300,1050) if ground else random.choice([270,620,800,1080])+random.uniform(-25,25)
  py=random.uniform(660,682) if ground else random.choice([390,165,470])
  size=random.uniform(2,7) if ground else random.uniform(.7,1.8)
  vertices=[(math.cos(a*math.tau/9)*size,math.sin(a*math.tau/9)*size*.55,0) for a in range(9)]
  p=mesh('Impact dust puff' if ground else 'Latch grit',vertices,[tuple(range(9))],dust if ground else fine)
  vx=random.uniform(-2,2);vy=random.uniform(2,4) if ground else random.uniform(-.2,.6)
  for f in range(1,73):
   age=f-h
   p.hide_render=not(0<=age<16);p.keyframe_insert(data_path='hide_render',frame=f)
   a=max(0,age);p.location=(px-640+vx*a,360-py+vy*a-.13*a*a,4)
   sc=(1+a*.15)*max(.01,1-a/17) if ground else max(.01,1-a/17)
   p.scale=(sc,sc,sc)
   for prop in ('location','scale'):p.keyframe_insert(data_path=prop,frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/'frames';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.filepath=str(folder/'gate-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Zone8-gate-rattle-v001.blend'))
bpy.ops.render.render(animation=True)
