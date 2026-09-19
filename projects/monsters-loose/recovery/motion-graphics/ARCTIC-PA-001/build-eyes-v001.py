import bpy, math
from pathlib import Path
o=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=192
s.render.film_transparent=True;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,1500))
s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1916;s.camera.data.clip_end=3000

def mat(name,col,alpha=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
 out=n.new('ShaderNodeOutputMaterial');e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1)
 if alpha==1:m.node_tree.links.new(e.outputs[0],out.inputs[0])
 else:
  t=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha
  m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(e.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs[0])
 return m
red=mat('Crimson eyes',(0.9,.012,.006));core=mat('Warm red inner iris',(1,.07,.014));black=mat('Vertical dark pupil',(.018,.001,.002))
def shape(name,pts,material,parent):
 me=bpy.data.meshes.new(name);me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update()
 ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.data.materials.append(material);ob.parent=parent
 return ob
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
# Coordinates in the original locked-camera image. Each pair sits in a
# different depth pocket of the cave, away from glass edges and snow.
specs=[(525,355,57,12.5,4.9,28,-12,18),(675,420,46,10,5.2,44,21,24),(444,455,36,8,3.5,60,-24,15)]
for i,(cx,cy,sep,ew,eh,start,advance_x,advance_y) in enumerate(specs):
 head=bpy.data.objects.new('Hidden creature '+str(i+1),None);s.collection.objects.link(head)
 for side in (-1,1):
  eye=bpy.data.objects.new('Eye aperture',None);s.collection.objects.link(eye);eye.parent=head;eye.location=(side*sep/2,0,0)
  # Soft restrained halo: concentric low-opacity disks, no hard outer edge.
  for ring in range(12,0,-1):
   radius=1+ring*.12
   pts=[(math.cos(j*math.tau/48)*ew*radius,math.sin(j*math.tau/48)*eh*radius*1.6,1+(12-ring)*.002) for j in range(48)]
   shape('Soft crimson bloom',pts,mat('Bloom',(.65,.002,.002),.009+(12-ring)*.001),eye)
  pts=[]
  for j in range(64):
   a=j*math.tau/64
   pts.append((ew*math.cos(a),eh*math.sin(a)*abs(math.sin(a))**.35+side*math.cos(a)*.8,2))
  shape('Almond red eye',pts,red,eye)
  pts=[(math.cos(j*math.tau/40)*ew*.42,math.sin(j*math.tau/40)*eh*.82,2.1) for j in range(40)]
  shape('Inner ember',pts,core,eye)
  pts=[(math.cos(j*math.tau/32)*1.05,math.sin(j*math.tau/32)*eh*.90,2.2) for j in range(32)]
  shape('Slit pupil',pts,black,eye)
  for f in range(1,193):
   opened=smooth((f-start)/13)
   eye.scale=(1,max(.001,opened),1);eye.keyframe_insert(data_path='scale',frame=f)
  for ob in list(eye.children):
   for f,hidden in [(0,True),(start-1,True),(start,False)]:
    ob.hide_render=hidden;ob.keyframe_insert(data_path='hide_render',frame=f)
 for f in range(1,193):
  approach=smooth((f-start-14)/130)
  awake=smooth((f-start)/20)
  t=(f-start)/24
  # Slow forward motion grows the pair and its spacing together; staggered
  # lateral/vertical head movement keeps them from reading as synchronized LEDs.
  head.location=(cx-958+advance_x*approach+awake*3.8*math.sin(t*1.5+i),540-cy-advance_y*approach+awake*2.1*math.sin(t*1.1+i*2),0)
  k=1+.38*approach;head.scale=(k,k,k)
  head.rotation_euler.z=math.radians(awake*(1.8*math.sin(t*.9+i)))
  for prop in ('location','scale','rotation_euler'):head.keyframe_insert(data_path=prop,frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for st in layer.strips:
   for bag in st.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/'eyes-frames-v001';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(folder/'eyes-')
s.frame_set(130)
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Arctic-three-monsters-eyes-v001.blend'))
bpy.ops.render.render(animation=True)
