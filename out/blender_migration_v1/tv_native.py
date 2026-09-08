"""Native registered CRT map, live glass and measured flash response."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'orb_native.py').read_text().replace("D=O/'orb'","D=O/'tv'")
code=code.replace('s.frame_end=128','s.frame_end=191').replace('range(1,129)','range(1,192)').replace('n.frame_duration=128','n.frame_duration=191').replace("f'orb_{W}.blend'","f'tv_{W}.blend'")
code=code.replace("colors.extend([((energy if side==0 else 0),(energy if side==1 else 0),0,1)]*4)","colors.extend([(*side,1)]*4)")
code=code.replace('range(fi,fi+11)','range(fi,fi+17)').replace('gain=.85','gain=1.0264').replace('gain*=.22 if 2271+frame-1>=2366 else .45','gain=.3264*.68**age').replace('age<8','age<14').replace('(fi+9,True)','(fi+15,True)')
code=code.replace('(2,2,2,1)','(1,1,1,1)').replace('[(3,2.4),(11,2.9)]','[(2.1,1.0),(6.6,.5)]')
start=code.index('cyan,amber,_=b.split(beam)');end=code.index("s.render.image_settings.file_format",start)
code=code[:start]+'''
# Screen aperture is native geometry, carried as a compositor mask render.
light=b.split(beam)
# Live glass is kept, with only the local CRT darkening used by the approved pass.
# Screen mask comes from a native polygon rendered separately below.
mask_image=b.n.new('CompositorNodeImage')
''' +code[end:]
# Build a fixed-domain shader aperture and use its AOV, not a bitmap mask.
marker="t=bpy.data.node_groups.new('Independent channels native light composite'";at=code.index(marker)
setup='''
from native_nodes import Field
fx=bpy.data.collections.new('FX');s.collection.children.link(fx)
for ob in list(s.collection.objects):
 if ob!=co:s.collection.objects.unlink(ob);fx.objects.link(ob)
mask_collection=bpy.data.collections.new('Aperture');s.collection.children.link(mask_collection)
me=bpy.data.meshes.new('Screen aperture');me.from_pydata([(-8,-4.5,-1),(8,-4.5,-1),(8,4.5,-1),(-8,4.5,-1)],[],[(0,1,2,3)]);ob=bpy.data.objects.new('Screen aperture',me);mask_collection.objects.link(ob);uv=me.uv_layers.new()
for loop,point in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=point
m=bpy.data.materials.new('Native feathered screen aperture');m.use_nodes=True;m.node_tree.nodes.clear();me.materials.append(m);pb=Builder(m.node_tree)
uvn=pb.n.new('ShaderNodeTexCoord');sep=pb.n.new('ShaderNodeSeparateXYZ');pb.plug(uvn.outputs['UV'],sep.inputs[0]);x=Field(pb,sep.outputs[0])*1280;y=(1-Field(pb,sep.outputs[1]))*720
h=json.loads((D/'controls.json').read_text())['inverse'];den=h[2][0]*x+h[2][1]*y+h[2][2];tx=(h[0][0]*x+h[0][1]*y+h[0][2])/den;ty=(h[1][0]*x+h[1][1]*y+h[1][2])/den
edge=(pb.op('ABSOLUTE',(tx-360)/360)**5+pb.op('ABSOLUTE',(ty-360)/360)**5)**.2;mask=((.98-edge)/.19).smooth()
em=pb.n.new('ShaderNodeEmission');pb.plug(mask,em.inputs[0]);out=pb.n.new('ShaderNodeOutputMaterial');pb.plug(em.outputs[0],out.inputs[0])
s.view_layers[0].name='FX';s.view_layers[0].layer_collection.children['Aperture'].exclude=True;layer=s.view_layers.new('Aperture');layer.layer_collection.children['FX'].exclude=True
'''
code=code[:at]+setup+code[at:]
code=code.replace("rl=b.n.new('CompositorNodeRLayers');beam=","rl=b.n.new('CompositorNodeRLayers');rl.layer='FX';beam=")
code=code.replace("mask_image=b.n.new('CompositorNodeImage')",'''mask_image=b.n.new('CompositorNodeRLayers');mask_image.layer='Aperture';mask=b.split(mask_image.outputs['Image'])[0]*.82
out=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear((a*(1-mask*.13)+(1-a*.87)*(1-(-z*255/220).exp())*mask).clamp()) for a,z in zip(pic,light)]),out.inputs['Image'])''')
exec(compile(code,str(O/'orb_native.py'),'exec'))
