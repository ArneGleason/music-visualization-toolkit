"""Native moving picture panels and a continuous audio-responsive message."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'orb_native.py').read_text().replace("D=O/'orb'","D=O/'meaning'")
code=code.replace('s.frame_end=128','s.frame_end=223').replace('range(1,129)','range(1,224)').replace("f'orb_{W}.blend'","f'meaning_{W}.blend'")
code=code.replace('gain=.85','gain=.8').replace('gain*=.22 if 2271+frame-1>=2366 else .45','gain*=.40')
marker="t=bpy.data.node_groups.new('Independent channels native light composite'"
insertion=code.index(marker)
code=code[:insertion]+'''
# Fixed-domain image plane prevents translated compositor domains clipping a panel.
fx=bpy.data.collections.new('FX');s.collection.children.link(fx)
for ob in list(s.collection.objects):
 if ob!=co:s.collection.objects.unlink(ob);fx.objects.link(ob)
plate_collection=bpy.data.collections.new('Plate');s.collection.children.link(plate_collection)
me=bpy.data.meshes.new('Full canvas');me.from_pydata([(-8,-4.5,-1),(8,-4.5,-1),(8,4.5,-1),(-8,4.5,-1)],[],[(0,1,2,3)])
ob=bpy.data.objects.new('Fixed-domain moving panels',me);plate_collection.objects.link(ob);uv=me.uv_layers.new()
for loop,point in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=point
m=bpy.data.materials.new('Two original performances');m.use_nodes=True;m.node_tree.nodes.clear();me.materials.append(m);pb=Builder(m.node_tree)
from native_nodes import Field
uvn=pb.n.new('ShaderNodeTexCoord');sep=pb.n.new('ShaderNodeSeparateXYZ');pb.plug(uvn.outputs['UV'],sep.inputs[0]);ux=Field(pb,sep.outputs[0]);uy=Field(pb,sep.outputs[1])
rows=json.loads((D/'controls.json').read_text())['frames'];shift=pb.animated('Panel displacement',[row['shift']/1280 for row in rows])
def texture(name,count,start,offset):
 im=bpy.data.images.load(str(D/name/'0001.png'));im.source='SEQUENCE';n=pb.n.new('ShaderNodeTexImage');n.image=im;n.extension='EXTEND';n.image_user.frame_duration=count;n.image_user.frame_start=start;n.image_user.use_auto_refresh=True
 pb.plug(pb.combine([ux-shift+offset,uy,0]),n.inputs['Vector']);return n.outputs['Color']
a=texture('outgoing',168,1,0);z=texture('incoming',95,129,1);color=pb.mix(a,z,pb.op('LESS_THAN',ux,shift),mode='MIX')
em=pb.n.new('ShaderNodeEmission');pb.plug(color,em.inputs[0]);out=pb.n.new('ShaderNodeOutputMaterial');pb.plug(em.outputs[0],out.inputs[0])
s.view_layers[0].name='FX';s.view_layers[0].layer_collection.children['Plate'].exclude=True
layer=s.view_layers.new('Plate');layer.layer_collection.children['FX'].exclude=True
''' +code[insertion:]
start=code.index('im=bpy.data.images.load',code.index(marker));end=code.index("rl=b.n.new('CompositorNodeRLayers')",start)
code=code[:start]+'''
plate=b.n.new('CompositorNodeRLayers');plate.layer='Plate';pic=[b.display(v) for v in b.split(plate.outputs['Image'])]
''' +code[end:]
code=code.replace('(2,2,2,1)','(1.25,1.25,1.25,1)').replace('[(3,2.4),(11,2.9)]','[(2.5,1.6),(9,2.1)]')
code=code.replace("rl=b.n.new('CompositorNodeRLayers');beam=","rl=b.n.new('CompositorNodeRLayers');rl.layer='FX';beam=")
code=code.replace('a+(1-a)*(1-(-z*1.7).exp())','a+z')
exec(compile(code,str(O/'orb_native.py'),'exec'))
