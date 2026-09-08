"""Native Blender existing-emission selection and vocal-linked bloom."""
from pathlib import Path
import bpy,json,sys
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent/'probe';O.mkdir(exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
W=int(args[0]) if args else 1280
frames=[int(x) for x in args[1].split(',')] if len(args)>1 else list(range(1,193))
out=O/f'native_{W}';out.mkdir(exist_ok=True)
data=json.loads((R/'out/probe_voice_trial/tracking.json').read_text())['frames']
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8
s.render.resolution_x=W;s.render.resolution_y=W*9//16;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=192
s.view_settings.view_transform='Standard';s.view_settings.look='None'
s.world=bpy.data.worlds.new('Black');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
cam=bpy.data.cameras.new('Screen plane camera');co=bpy.data.objects.new('Camera',cam);s.collection.objects.link(co);co.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=16;s.camera=co
bpy.ops.mesh.primitive_plane_add(size=2);plane=bpy.context.object;plane.scale=(8,4.5,1)
m=bpy.data.materials.new('Native luminance / gold selection');m.use_nodes=True;plane.data.materials.append(m)
n=m.node_tree.nodes;n.clear();l=m.node_tree.links
def op(kind,*vals):
    z=n.new('ShaderNodeMath');z.operation=kind
    for i,v in enumerate(vals):
        if isinstance(v,(int,float)):z.inputs[i].default_value=v
        else:l.new(v,z.inputs[i])
    return z.outputs[0]
def clamp(v):return op('MINIMUM',1,op('MAXIMUM',0,v))
def animated(name,key,index=None):
    z=n.new('ShaderNodeValue');z.label=name
    for f,r in enumerate(data,1):
        z.outputs[0].default_value=r[key] if index is None else r[key][index]
        z.outputs[0].keyframe_insert('default_value',frame=f)
    return z.outputs[0]
cx=animated('Tracked nozzle X','nozzle_xy',0);cy=animated('Tracked nozzle Y','nozzle_xy',1)
uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0])
x=op('MULTIPLY',sep.outputs[0],1280);y=op('MULTIPLY',op('SUBTRACT',1,sep.outputs[1]),720)
tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'clips/raw/signal_crossing_space_v6.mp4'));tex.image.source='MOVIE';tex.image_user.frame_duration=192;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True
l.new(uv.outputs['UV'],tex.inputs['Vector'])
rgbnode=n.new('ShaderNodeSeparateColor');l.new(tex.outputs['Color'],rgbnode.inputs[0]);channels=[]
for v in list(rgbnode.outputs)[:3]:
    gate=op('GREATER_THAN',v,.0031308)
    channels.append(op('ADD',op('MULTIPLY',op('MULTIPLY',v,12.92),op('SUBTRACT',1,gate)),op('MULTIPLY',op('SUBTRACT',op('MULTIPLY',op('POWER',v,1/2.4),1.055),.055),gate)))
r,g,b=channels
gold=op('MULTIPLY',clamp(op('DIVIDE',op('SUBTRACT',g,.38),.40)),op('MULTIPLY',clamp(op('MULTIPLY',op('SUBTRACT',op('SUBTRACT',r,b),.12),3)),clamp(op('MULTIPLY',op('SUBTRACT',op('SUBTRACT',g,b),.08),4))))
dist=op('DIVIDE',op('SUBTRACT',y,cy),38)
corridor=op('MULTIPLY',op('EXPONENT',op('MULTIPLY',op('MULTIPLY',dist,dist),-1)),clamp(op('DIVIDE',op('ADD',op('SUBTRACT',x,cx),12),22)))
mask=op('MULTIPLY',gold,corridor)
em=n.new('ShaderNodeEmission');l.new(mask,em.inputs[0]);mo=n.new('ShaderNodeOutputMaterial');l.new(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native source-aware additive glow','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t
n=t.nodes;l=t.links
plate=n.new('CompositorNodeImage');plate.image=bpy.data.images.load(str(O/'plates/0001.png'));plate.image.source='SEQUENCE'
plate.frame_duration=192;plate.frame_start=1;plate.use_auto_refresh=True
scale=n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';l.new(plate.outputs['Image'],scale.inputs['Image'])
render=n.new('CompositorNodeRLayers')
def blur(inp,sigma):
    z=n.new('CompositorNodeBlur');z.inputs['Size'].default_value=(sigma*3*W/1280,)*2;l.new(inp,z.inputs['Image']);return z.outputs[0]
def mix(a,b,factor=1,mode='ADD'):
    z=n.new('ShaderNodeMix');z.data_type='RGBA';z.blend_type=mode;z.clamp_result=False;z.inputs[0].default_value=factor
    for value,sock in [(a,z.inputs[6]),(b,z.inputs[7])]:
        if isinstance(value,tuple):sock.default_value=value
        else:l.new(value,sock)
    return z.outputs[2]
mask=blur(render.outputs['Image'],1)
core=mix(scale.outputs[0],mask,1,'MULTIPLY')
halo=mix(mix(blur(mask,7),(.32,.32,.32,1),1,'MULTIPLY'),mix(blur(mask,22),(.16,.16,.16,1),1,'MULTIPLY'))
halo=mix(halo,(1,.53,.13,1),1,'MULTIPLY')
light=mix(mix(core,(2.4,2.4,2.4,1),1,'MULTIPLY'),halo)
drive=n.new('ShaderNodeMix');drive.data_type='RGBA';drive.blend_type='MULTIPLY';drive.inputs[0].default_value=1
l.new(light,drive.inputs[6])
for f,row in enumerate(data,1):
    a=row['vocal_envelope'];drive.inputs[7].default_value=(a,a,a,1);drive.inputs[7].keyframe_insert('default_value',frame=f)
end=n.new('NodeGroupOutput');l.new(mix(scale.outputs[0],drive.outputs[2]),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(O/f'probe_{W}.blend'))
for f in frames:
    s.frame_set(f)
    s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
