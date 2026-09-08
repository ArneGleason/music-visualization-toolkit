"""Native additive line meshes with independent audio and finite persistence."""
import bpy,sys,json,gzip,math,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O));from native_nodes import Builder
D=O/'orb';args=sys.argv[sys.argv.index('--')+1:];W=int(args[0]);dest=D/f'native_{W}';dest.mkdir(exist_ok=True)
with gzip.open(D/'segments.json.gz','rt') as f:geometry=json.load(f)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.transparent_max_bounces=128
s.render.resolution_x=W;s.render.resolution_y=W*9//16;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=128
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.film_transparent=True
cam=bpy.data.cameras.new('Normalized optical camera');co=bpy.data.objects.new('Camera',cam);s.collection.objects.link(co);co.location=(0,0,20);cam.type='ORTHO';cam.ortho_scale=16;s.camera=co
for fi,segments in enumerate(geometry):
 if not segments:continue
 verts=[];faces=[];colors=[]
 for j,(p,q,width,energy,side) in enumerate(segments):
  p=np.array(p);q=np.array(q);delta=q-p;length=np.linalg.norm(delta)
  if length<1e-5:continue
  norm=np.array([-delta[1],delta[0]])/length*width*.5;k=len(verts)
  for point in [p+norm,q+norm,q-norm,p-norm]:verts.append(((point[0]-640)/80,(360-point[1])/80,fi*.01+j*.0000001))
  faces.append((k,k+1,k+2,k+3));colors.extend([((energy if side==0 else 0),(energy if side==1 else 0),0,1)]*4)
 me=bpy.data.meshes.new(f'Native beam {fi+1}');me.from_pydata(verts,[],faces);attr=me.color_attributes.new(name='Channel energy',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',np.array(colors,dtype=np.float32).ravel())
 m=bpy.data.materials.new(me.name);m.use_nodes=True;m.node_tree.nodes.clear();b=Builder(m.node_tree);vc=b.n.new('ShaderNodeVertexColor');vc.layer_name='Channel energy'
 em=b.n.new('ShaderNodeEmission');b.plug(vc.outputs['Color'],em.inputs[0]);gain=.85
 for frame in range(fi,fi+11):
  age=frame-fi-1
  if age==0:gain=.85
  elif age>0:gain*=.22 if 2271+frame-1>=2366 else .45
  em.inputs[1].default_value=gain if 0<=age<8 else 0;em.inputs[1].keyframe_insert('default_value',frame=frame)
 tr=b.n.new('ShaderNodeBsdfTransparent');add=b.n.new('ShaderNodeAddShader');b.plug(em.outputs[0],add.inputs[0]);b.plug(tr.outputs[0],add.inputs[1]);out=b.n.new('ShaderNodeOutputMaterial');b.plug(add.outputs[0],out.inputs[0]);me.materials.append(m)
 ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob)
 for frame,hide in [(0,True),(fi+1,False),(fi+9,True)]:ob.hide_render=hide;ob.keyframe_insert('hide_render',frame=frame)
t=bpy.data.node_groups.new('Independent channels native light composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
im=bpy.data.images.load(str(D/'plates/0001.png'));im.source='SEQUENCE';n=b.n.new('CompositorNodeImage');n.image=im;n.frame_start=1;n.frame_duration=128;n.use_auto_refresh=True
size=b.n.new('CompositorNodeScale');size.inputs['Type'].default_value='Render Size';b.plug(n.outputs[0],size.inputs[0]);pic=[b.display(v) for v in b.split(size.outputs[0])]
rl=b.n.new('CompositorNodeRLayers');beam=b.mix(rl.outputs['Image'],(2,2,2,1),mode='MULTIPLY')
for sigma,gain in [(3,2.4),(11,2.9)]:beam=b.mix(beam,b.mix(b.blur(rl.outputs['Image'],sigma,W),(gain,gain,gain,1),mode='MULTIPLY'))
cyan,amber,_=b.split(beam);light=[cyan*a+amber*z for a,z in zip([.2,.8,1],[1,.5,.1])]
out=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear((a+(1-a)*(1-(-z*1.7).exp())).clamp()) for a,z in zip(pic,light)]),out.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.frame_set(1);s.render.filepath=str(dest/'0001.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/f'orb_{W}.blend'))
selected=list(map(int,args[1].split(','))) if len(args)>1 else range(1,129)
for f in selected:s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
