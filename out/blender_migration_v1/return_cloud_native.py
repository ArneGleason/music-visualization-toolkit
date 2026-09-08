"""Native coherent-color accelerating return and final settling, raw plates only."""
from pathlib import Path
import re
O=Path(__file__).resolve().parent;R=O.parents[1]
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
import random
from mathutils import Vector
s.render.engine='BLENDER_EEVEE';cam.type='PERSP';cam.lens=22.5;cam.sensor_width=36
time=b.animated('Song time',[v['song_frame']/24 for v in rows]);env=b.animated('Music energy',[v['env'] for v in rows]);gate=b.animated('Room return only',[v['base_fx'] for v in rows])
roi=(-((x-638)/65)**6-((y-583)/90)**6).exp();warm=((r-blue-8/255)/(45/255)).clamp()*((g-blue-3/255)/(35/255)).clamp()*roi*(.6+1.5*env)*gate
mask=(1-(-((x-640)/270)**6-((y-400)/390)**6).exp())*(((y-345)/125).smooth()+.4*(1-((y-250)/110).smooth())*b.op('GREATER_THAN',b.op('ABSOLUTE',x-640),500))
pattern=(.5+.5*b.op('SINE',x*.013+y*.010-time*.7+1.1*b.op('SINE',y*.009+time*.3)))**5
shade=b.op('MINIMUM',.7,b.op('MAXIMUM',.15,(r+g+blue)/3*255/140))*mask*pattern*.65*gate
for name,field in [('Warm',warm),('Room',shade)]:
 av=s.view_layers[0].aovs.add();av.name=name;av.type='VALUE';node=b.n.new('ShaderNodeOutputAOV');node.aov_name=name;b.plug(field,node.inputs['Value'])
em=b.n.new('ShaderNodeEmission');b.plug(tex.outputs['Color'],em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
base_collection=bpy.data.collections.new('Base');s.collection.children.link(base_collection)
for obj in list(s.collection.objects):
 if obj!=co:s.collection.objects.unlink(obj);base_collection.objects.link(obj)
close=False;N=2400;sc=s
def smooth(a,b,t):v=max(0,min(1,(t-a)/(b-a)));return v*v*(3-2*v)
def project(x,y,z):return ((x-.5)*16*(10-z)/10,(.5-y)*9*(10-z)/10,z)
legacy=(R/'out/outro_particle_continuity_v1/render.py').read_text();cloud=legacy[legacy.index('rng=random.Random'):legacy.index("tree=bpy.data.node_groups.new")];cloud=re.sub(r'\bout\b','particle_output',cloud)
exec(compile(cloud,'accepted_native_particle_continuity','exec'))
cloud_collection=bpy.data.collections.new('Cloud');s.collection.children.link(cloud_collection)
for obj in list(s.collection.objects):
 if obj!=co:s.collection.objects.unlink(obj);cloud_collection.objects.link(obj)
s.view_layers[0].name='Base';s.view_layers[0].layer_collection.children['Cloud'].exclude=True;layer=s.view_layers.new('Cloud');layer.layer_collection.children['Base'].exclude=True
t=bpy.data.node_groups.new('Native room and returning cloud','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
base=b.n.new('CompositorNodeRLayers');base.layer='Base';cloud=b.n.new('CompositorNodeRLayers');cloud.layer='Cloud'
warm=Field(b,base.outputs['Warm'])+Field(b,b.blur(base.outputs['Warm'],5,W))+Field(b,b.blur(base.outputs['Warm'],16,W))*.7;room=Field(b,base.outputs['Room'])
pic=[b.display(v) for v in b.split(base.outputs['Image'])];energy=[warm*c/255+room*z/255 for c,z in zip([255,145,35],[85,48,80])]
picture=b.combine([b.linear((a+(1-a)*(1-(-e).exp())).clamp()) for a,e in zip(pic,energy)])
light=b.mix(cloud.outputs['Image'],b.mix(b.blur(cloud.outputs['Image'],3,W),(2,2,2,1),mode='MULTIPLY'));light=b.mix(light,b.mix(b.blur(cloud.outputs['Image'],10,W),(1.2,1.2,1.2,1),mode='MULTIPLY'))
end=b.n.new('NodeGroupOutput');b.plug(b.mix(picture,light),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.frame_set(1);s.render.filepath=str(out/'0001.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/f'return_cloud_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
