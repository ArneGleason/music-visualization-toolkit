"""Native Gaussian tracked lights, no external raster FX. Blender5.2."""
from pathlib import Path
import bpy,json,sys,math
O=Path(__file__).resolve().parent/'aerial'
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
W=int(args[0]) if args else 1280
frames=[int(i) for i in args[1].split(',')] if len(args)>1 else list(range(1,78))
out=O/f'native_{W}';out.mkdir(exist_ok=True)
d=json.loads((O/'controls.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16
s.render.resolution_x=W;s.render.resolution_y=W*9//16;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=77
s.view_settings.view_transform='AgX';s.view_settings.look='None'
s.world=bpy.data.worlds.new('Black');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
cam=bpy.data.cameras.new('Normalized camera');co=bpy.data.objects.new('Camera',cam);s.collection.objects.link(co);co.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=16;s.camera=co
bpy.ops.mesh.primitive_plane_add(size=2)
plane=bpy.context.object;plane.name='Continuous analytic light field';plane.scale=(8,4.5,1)
m=bpy.data.materials.new('Tracked Gaussian lights, native shader');m.use_nodes=True;plane.data.materials.append(m)
n=m.node_tree.nodes;n.clear();l=m.node_tree.links
def op(kind,*inputs):
    z=n.new('ShaderNodeMath');z.operation=kind
    for i,v in enumerate(inputs):
        if isinstance(v,(float,int)):z.inputs[i].default_value=v
        else:l.new(v,z.inputs[i])
    return z.outputs[0]
def value(name,values):
    v=n.new('ShaderNodeValue');v.label=name
    for f,x in enumerate(values,1):v.outputs[0].default_value=float(x);v.outputs[0].keyframe_insert('default_value',frame=f)
    return v.outputs[0]
uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0])
x=op('MULTIPLY',sep.outputs['X'],1280);y=op('MULTIPLY',op('SUBTRACT',1,sep.outputs['Y']),720)
rgb=[0,0,0]
for k in range(3):
    cx=value(f'Anchor{k} X',[p[k][0] for p in d['positions']]);cy=value(f'Anchor{k} Y',[p[k][1] for p in d['positions']])
    dx=op('SUBTRACT',x,cx);dy=op('SUBTRACT',y,cy)
    r2=op('ADD',op('MULTIPLY',dx,dx),op('MULTIPLY',dy,dy))
    shape=0
    for radius,weight in ([(1.65,1),(7,.17),(15,.025)] if k==0 else [(1.4,1),(4.4,.2)]):
        shape=op('ADD',shape,op('MULTIPLY',op('EXPONENT',op('DIVIDE',r2,-2*radius*radius)),weight))
    strength=[]
    for j in range(77):
        gate=min(1,j/7,(76-j)/8);vis=max(0,min(1,(d['valid_until'][k]-j)/6))
        strength.append(gate*vis*(.025+.9*d['strengths'][j] if k==0 else .025+.36*d['energy'][j]**2))
    amp=value(f'Anchor{k} exact song driver',strength)
    color=[110,240,65] if k==0 else ([245,184,105] if k==1 else [135,214,190])
    for c in range(3):rgb[c]=op('ADD',rgb[c],op('MULTIPLY',op('MULTIPLY',shape,amp),color[c]/255))
# Decode the legacy sRGB-authored light palette, without importing raster layers.
# Continuous subpixel signal deliberately replaces 8-bit truncation.
combine=n.new('ShaderNodeCombineXYZ')
for c,v in enumerate(rgb):
    low=op('DIVIDE',v,12.92);high=op('POWER',op('DIVIDE',op('ADD',v,.055),1.055),2.4)
    gate=op('GREATER_THAN',v,.04045)
    linear=op('ADD',op('MULTIPLY',low,op('SUBTRACT',1,gate)),op('MULTIPLY',high,gate))
    l.new(linear,combine.inputs[c])
em=n.new('ShaderNodeEmission');l.new(combine.outputs[0],em.inputs[0]);mo=n.new('ShaderNodeOutputMaterial');l.new(em.outputs[0],mo.inputs[0])
# Preserve the approved sequence-editor color path, now with a native scene
# strip instead of externally generated light PNGs.
s.view_settings.view_transform='Standard'
parent=bpy.data.scenes.new('Aerial native assembly')
parent.render.engine='CYCLES';parent.cycles.samples=16
parent.render.resolution_x=W;parent.render.resolution_y=W*9//16
parent.render.resolution_percentage=100;parent.render.fps=24
parent.frame_start=1;parent.frame_end=77
parent.view_settings.view_transform='AgX';parent.view_settings.look='None'
strips=parent.sequence_editor_create().strips
p=strips.new_movie(name='Original untreated footage',filepath=str(O.parents[2]/d['plate']),channel=1,frame_start=1)
p.frame_final_duration=77;p.transform.scale_x=p.transform.scale_y=W/1280
fx=strips.new_scene(name='Native tracked lights',scene=s,channel=2,frame_start=1)
fx.blend_type='ADD';fx.blend_alpha=.85;fx.frame_final_duration=77
parent.render.image_settings.file_format='PNG';parent.render.image_settings.color_mode='RGB'
parent.render.filepath=str(out)+'/'
bpy.context.window.scene=parent
bpy.ops.wm.save_as_mainfile(filepath=str(O/f'aerial_{W}.blend'))
for f in frames:
    parent.frame_set(f);parent.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True,scene=parent.name)
