"""Native radial refraction, chromatic split, spirographs and phosphor trails.

Only untreated plates are image inputs. Geometry carries deterministic points;
the saved Blender scene holds its full animation and persistence.
"""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
import numpy as np
s.cycles.samples=16; s.cycles.transparent_max_bounces=64
def sm(v):
    v=max(0,min(1,v)); return v*v*(3-2*v)
def controls(sf):
    build=sm((sf-3505)/56); fade=1-sm((sf-3618)/19)
    bend=math.exp(-((sf-3574)/11)**2); mind=math.exp(-((sf-3604)/13)**2)
    return build,fade,bend,mind
values=[controls(v['song_frame']) for v in rows]
build,fade,bend,mind=[b.animated(name,[v[j] for v in values]) for j,name in enumerate(['Buildup','Release','Bends','Mind'])]
time=b.animated('Song-local time',[(v['song_frame']-3505)/24 for v in rows])
dx=x-640; dy=y-270; rad=(dx*dx+(dy*1.1)**2)**.5+.001
face=(-((dx/175)**4+((y-280)/220)**4)).exp()
edge=(-((rad-310)/250)**2).exp()*(1-face)*((620-y)/90).clamp()
wave=b.op('SINE',rad/45-time*4)*(2+6*build+34*bend+54*mind)*fade*edge
split=edge*(1.2*build+9*bend+17*mind)*fade
def reflect(v,last):
    return last-b.op('ABSOLUTE',b.op('FLOORED_MODULO',v,2*last)-last)
for channel,sign in enumerate([-1,0,1]):
    samplex=reflect(x+dx/rad*(wave+sign*split),1279)
    sampley=reflect(y+dy/rad*(wave*.65+sign*split),719)
    # Blender displacement is inverse mapping, opposite to cv2 remap offsets.
    for name,value in [(f'DX{channel}',x-samplex),(f'DY{channel}',sampley-y)]:
        av=s.view_layers[0].aovs.add(); av.name=name; av.type='VALUE'
        node=b.n.new('ShaderNodeOutputAOV'); node.aov_name=name
        b.plug(value*W/1280,node.inputs['Value'])
em=b.n.new('ShaderNodeEmission'); em.inputs[0].default_value=(0,0,0,1)
outmat=b.n.new('ShaderNodeOutputMaterial'); b.plug(em.outputs[0],outmat.inputs[0])
# Optical plane is behind additive light geometry, whose surface is transparent.
plane.location.z=-.1
theta=np.arange(1100)*math.tau/1099
seeds=np.random.default_rng(91).random((320,5))
for fi,row in enumerate(rows):
    sf=row['song_frame']; t=(sf-3505)/24; bu,fa,be,mi=values[fi]
    strength=(.08+.30*bu+1.1*be+1.8*mi)*fa
    if strength<1e-8:continue
    radius=190+120*bu+150*mi
    verts=[]; faces=[]; colors=[]
    def polygon(points,color):
        j=len(verts)
        for px,py in points:
            mask=(1-.98*math.exp(-(((px-640)/175)**4+((py-280)/220)**4)))*max(0,min(1,(620-py)/80))
            verts.append(((px-640)/80,(360-py)/80,.001*(fi+1)))
            colors.append((*[float(c*mask) for c in color],1))
        faces.append(tuple(range(j,len(verts))))
    # Old ink used BGR; native geometry uses linear RGB emission.
    for k,color in enumerate([(.68,.46,1),(.20,.82,.95),(1,.65,.32)]):
        phase=t*(.25 if k%2 else -.22)+k*math.tau/3
        rr=radius*(1+(.06+.20*be+.34*mi)*np.sin((5+k)*theta+phase*3))
        points=np.column_stack((640+rr*np.cos(theta+phase),275+.78*rr*np.sin(theta+phase)+44*mi*np.sin(3*theta-phase)))
        for j in range(len(points)-1):
            a,z=points[j:j+2]; delta=z-a; normal=np.array([-delta[1],delta[0]])/max(np.linalg.norm(delta),1e-6)*.5
            scan=((j//12*12/1100-t*.24-k*.2)%1)
            energy=strength*(.45+.55*math.exp(-scan*4))
            polygon([a+normal,z+normal,z-normal,a-normal],np.array(color)*energy)
    for j,(a,c1,c,d,e) in enumerate(seeds):
        age=max(0,(sf-3598)/24); angle=a*math.tau+t*(.14+c1*.18)
        rr=radius*(.85+.30*c)+age*(110+190*d)
        px=640+rr*math.cos(angle); py=275+.78*rr*math.sin(angle)+age*age*25
        bright=strength*(.15+.85*mi)*(.35+.65*e); color=(.75,.45,1) if j%2 else (1,.9,.55)
        size=(1+int(c*3))/2
        polygon([(px+size*math.cos(q*math.tau/8),py+size*math.sin(q*math.tau/8)) for q in range(8)],np.array(color)*bright)
    mesh=bpy.data.meshes.new(f'Trace {fi+1}'); mesh.from_pydata(verts,[],faces)
    attr=mesh.color_attributes.new(name='Ink',type='FLOAT_COLOR',domain='POINT'); attr.data.foreach_set('color',np.array(colors,dtype=np.float32).ravel())
    mat=bpy.data.materials.new(mesh.name); mat.use_nodes=True; mat.node_tree.nodes.clear(); nb=Builder(mat.node_tree)
    vc=nb.n.new('ShaderNodeVertexColor'); vc.layer_name='Ink'
    emission=nb.n.new('ShaderNodeEmission'); nb.plug(vc.outputs['Color'],emission.inputs[0])
    for at in [0,fi]+list(range(fi+1,min(count+1,fi+34)))+[fi+34]:
        age=at-fi-1; emission.inputs[1].default_value=.78**age if 0<=age<32 else 0
        emission.inputs[1].keyframe_insert('default_value',frame=at)
    transparent=nb.n.new('ShaderNodeBsdfTransparent'); add=nb.n.new('ShaderNodeAddShader')
    nb.plug(emission.outputs[0],add.inputs[0]); nb.plug(transparent.outputs[0],add.inputs[1]); mo=nb.n.new('ShaderNodeOutputMaterial'); nb.plug(add.outputs[0],mo.inputs[0])
    mesh.materials.append(mat); ob=bpy.data.objects.new(mesh.name,mesh); s.collection.objects.link(ob)
    for at,hidden in [(0,True),(fi,True),(fi+1,False),(fi+33,True)]:ob.hide_render=hidden; ob.keyframe_insert('hide_render',frame=at)

tree=bpy.data.node_groups.new('Native psychedelic refraction and persistence','CompositorNodeTree'); tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor'); s.compositing_node_group=tree; b=Builder(tree)
plate=b.n.new('CompositorNodeImage'); plate.image=img; plate.frame_duration=count; plate.frame_start=1; plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale'); scale.inputs['Type'].default_value='Render Size'; b.plug(plate.outputs[0],scale.inputs['Image']); pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers'); channels=[]
for channel,sign in enumerate([-1,0,1]):
    field=b.combine([rl.outputs[f'DX{channel}'],rl.outputs[f'DY{channel}'],0])
    dis=b.n.new('CompositorNodeDisplace'); dis.inputs['Interpolation'].default_value='Bilinear'; dis.inputs['Extension X'].default_value='Extend'; dis.inputs['Extension Y'].default_value='Extend'
    b.plug(pic,dis.inputs['Image']); b.plug(field,dis.inputs['Displacement']); channels.append(b.split(dis.outputs[0])[channel])
light=rl.outputs['Image']; glow=b.mix(light,(.8,.8,.8,1),mode='MULTIPLY')
for sigma,gain in [(3,1.4),(14,1.1)]:glow=b.mix(glow,b.mix(b.blur(light,sigma,W),(gain,gain,gain,1),mode='MULTIPLY'))
end=b.n.new('NodeGroupOutput'); b.plug(b.mix(b.combine(channels),glow),end.inputs['Image'])
s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'; s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'bends_{W}.blend'))
for f in frames:s.frame_set(f); s.render.filepath=str(out/f'{f:04d}.png'); bpy.ops.render.render(write_still=True)
