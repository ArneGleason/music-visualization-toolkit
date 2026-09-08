"""Native artifact crop, continuous depth motes and green dancer."""
from pathlib import Path
import re
O=Path(__file__).resolve().parent;R=O.parents[1]
code=(O/'afterglow_native.py').read_text()
needle="s.render.engine='BLENDER_EEVEE'"
code=code.replace(needle,needle+'''
x=445+x*400/1280;y=475+y*225/720
b.plug(b.combine([x/1280,1-y/720,0]),tex.inputs['Vector'])
cam.type='PERSP';cam.lens=22.5;cam.sensor_width=36
''')
# Isolated close insert did not use the room projector or old screen-space motes.
code=code.replace("('Motes',motes),('Room',room)","('Motes',[0,0,0]),('Room',[0,0,0])")
# Strengthen the source-derived warm internal structure, as in the accepted insert.
code=code.replace('core=warm*sweep*(.65+2.1*voice)','core=warm*sweep*(.65+2.1*voice)')
code=code.replace('b.blur(rl.outputs[\'Core\'],.75,W)',"b.blur(rl.outputs['Core'],.75,W*3.2)").replace("b.blur(rl.outputs['Core'],5,W)","b.blur(rl.outputs['Core'],5,W*3.2)").replace("b.blur(rl.outputs['Core'],17,W)","b.blur(rl.outputs['Core'],17,W*3.2)")
marker="t=bpy.data.node_groups.new('Native afterglow light composite'";at=code.index(marker)
legacy=(R/'out/outro_particle_continuity_v1/render.py').read_text();cloud=legacy[legacy.index('rng=random.Random'):legacy.index("tree=bpy.data.node_groups.new")]
cloud=re.sub(r'\bout\b','particle_output',cloud)
insertion='''
from mathutils import Vector
base_collection=bpy.data.collections.new('Base');s.collection.children.link(base_collection)
for obj in list(s.collection.objects):
 if obj!=co:s.collection.objects.unlink(obj);base_collection.objects.link(obj)
close=True;N=128;sc=s
def smooth(a,b,t):
 v=max(0,min(1,(t-a)/(b-a)));return v*v*(3-2*v)
def project(x,y,z):return ((x-.5)*16*(10-z)/10,(.5-y)*9*(10-z)/10,z)
'''+cloud+'''
cloud_collection=bpy.data.collections.new('Cloud');s.collection.children.link(cloud_collection)
for obj in list(s.collection.objects):
 if obj!=co:s.collection.objects.unlink(obj);cloud_collection.objects.link(obj)
s.view_layers[0].name='Base';s.view_layers[0].layer_collection.children['Cloud'].exclude=True
layer=s.view_layers.new('Cloud');layer.layer_collection.children['Base'].exclude=True
'''
code=code[:at]+insertion+code[at:]
code=code.replace("rl=b.n.new('CompositorNodeRLayers')","rl=b.n.new('CompositorNodeRLayers');rl.layer='Base'")
at=code.index("s.render.image_settings.file_format='PNG'")
code=code[:at]+'''
cloud_render=b.n.new('CompositorNodeRLayers');cloud_render.layer='Cloud';glare=b.n.new('CompositorNodeGlare');glare.inputs['Type'].default_value='Fog Glow';glare.inputs['Quality'].default_value='High';glare.inputs['Threshold'].default_value=.06;glare.inputs['Strength'].default_value=2.4;glare.inputs['Size'].default_value=.25;b.plug(cloud_render.outputs['Image'],glare.inputs['Image'])
red=b.op('MAXIMUM',0,b.linear(delta[0].clamp())-b.linear(delta[2].clamp()))*5
artifact=b.combine([red*c for c in [1,.5,.085]])
artifact=b.mix(artifact,b.mix(b.blur(artifact,10,W),(1.5,1.5,1.5,1),mode='MULTIPLY'))
base_result=b.mix(rl.outputs['Image'],artifact)
cloud_light=b.mix(cloud_render.outputs['Image'],b.mix(b.blur(cloud_render.outputs['Image'],3,W),(2,2,2,1),mode='MULTIPLY'))
cloud_light=b.mix(cloud_light,b.mix(b.blur(cloud_render.outputs['Image'],10,W),(2,2,2,1),mode='MULTIPLY'))
b.plug(b.mix(base_result,cloud_light),outnode.inputs['Image'])
''' +code[at:]
exec(compile(code,str(O/'afterglow_native.py'),'exec'))
