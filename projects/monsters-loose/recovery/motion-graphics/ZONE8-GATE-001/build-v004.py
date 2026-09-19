import bpy,math,json,random
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
timing=json.loads((o/'timing-v004.json').read_text());hits=timing['impact_source_frames_one_based']
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
 fade=clamp((timing['mechanical_stop_source_frame']-f)/3)
 return fade*sum(strength*math.exp(-(f-h-delay)/1.6)*math.cos((f-h-delay)*2.15) for h,strength in zip(hits,timing['impact_strengths']) if f>=h+delay)
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
# Broad, textured translucent billows plus ballistic grit. Impacts unchanged.
def cloud_material(name,col):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();lk=m.node_tree.links
 uv=n.new('ShaderNodeTexCoord')
 dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(.5,.5,0);lk.new(uv.outputs['UV'],dist.inputs[0])
 edge=n.new('ShaderNodeValToRGB');edge.color_ramp.elements[0].position=.06;edge.color_ramp.elements[0].color=(1,1,1,1);edge.color_ramp.elements[1].position=.5;edge.color_ramp.elements[1].color=(0,0,0,1);lk.new(dist.outputs['Value'],edge.inputs[0])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.72;lk.new(uv.outputs['UV'],noise.inputs['Vector'])
 density=n.new('ShaderNodeValToRGB');density.color_ramp.elements[0].position=.25;density.color_ramp.elements[0].color=(.12,.12,.12,1);density.color_ramp.elements[1].position=.72;lk.new(noise.outputs['Fac'],density.inputs[0])
 mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';lk.new(edge.outputs[0],mul.inputs[0]);lk.new(density.outputs[0],mul.inputs[1])
 opacity=n.new('ShaderNodeMath');opacity.operation='MULTIPLY';lk.new(mul.outputs[0],opacity.inputs[0])
 e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1)
 tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');lk.new(opacity.outputs[0],mix.inputs[0]);lk.new(tr.outputs[0],mix.inputs[1]);lk.new(e.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');lk.new(mix.outputs[0],out.inputs[0])
 return m,opacity.inputs[1]
fine=mat('Amber airborne grit',(.66,.44,.23),.8)
for hi,(h,strength) in enumerate(zip(hits,timing['impact_strengths'])):
 for j in range(14):
  ground=j<10
  px=300+(j/9)*730+random.uniform(-22,22) if ground else random.choice([265,640,1060])+random.uniform(-18,18)
  py=random.uniform(654,680) if ground else random.choice([390,470,165])
  radius=random.uniform(50,85) if ground else random.uniform(28,48)
  col=random.choice([(.34,.27,.19),(.46,.35,.23),(.27,.24,.19)])
  material,alpha=cloud_material('Textured dust billow %d %d'%(hi,j),col)
  p=mesh('Ground billow' if ground else 'Hinge dust burst',[(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],[(0,1,2,3)],material)
  u=p.data.uv_layers.new()
  for poly in p.data.polygons:
   for li in poly.loop_indices:
    v=p.data.vertices[p.data.loops[li].vertex_index].co;u.data[li].uv=((v.x+1)/2,(v.y+1)/2)
  vx=random.uniform(-2,2);vy=random.uniform(2,4) if ground else random.uniform(-.3,1.5);phase=random.uniform(0,6.28)
  life=random.randint(32,43)
  for f in range(1,73):
   age=f-h;a=max(0,age);active=0<=age<life
   p.hide_render=not active;p.keyframe_insert(data_path='hide_render',frame=f)
   grow=.35+1.5*(1-math.exp(-a/9))
   p.location=(px-640+vx*a+math.sin(a*.12+phase)*a*.22,360-py+vy*a,5+hi*.3+j*.01)
   p.scale=(radius*grow*1.35,radius*grow*.72,1);p.rotation_euler.z=math.sin(phase)*.15+a*.004
   # Very quick impact bloom; cloud persists after mechanical motion stops.
   alpha.default_value=(.72+.22*strength)*min(1,(a+1)/3)*max(0,1-a/life)**.65 if active else 0
   alpha.keyframe_insert(data_path='default_value',frame=f)
   for prop in ('location','scale','rotation_euler'):p.keyframe_insert(data_path=prop,frame=f)
 for j in range(65):
  ground=j<45;px=random.uniform(270,1090);py=random.uniform(654,679) if ground else random.choice([165,390,470])+random.uniform(-15,15)
  size=random.uniform(1.2,3.3)
  vertices=[(math.cos(a*math.tau/5)*size,math.sin(a*math.tau/5)*size*.65,0) for a in range(5)]
  p=mesh('Thrown grit',vertices,[tuple(range(5))],fine)
  vx=random.uniform(-3.5,3.5);vy=random.uniform(3,7) if ground else random.uniform(-1,3);life=random.randint(14,28)
  for f in range(1,73):
   age=f-h;a=max(0,age);p.hide_render=not(0<=age<life);p.keyframe_insert(data_path='hide_render',frame=f)
   p.location=(px-640+vx*a,360-py+vy*a-.18*a*a,9);sc=max(.05,1-a/life);p.scale=(sc,sc,sc)
   for prop in ('location','scale'):p.keyframe_insert(data_path=prop,frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/'frames-v004';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.filepath=str(folder/'gate-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Zone8-gate-rattle-v004.blend'))
bpy.ops.render.render(animation=True)
