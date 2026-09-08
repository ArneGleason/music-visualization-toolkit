"""Native closed-eye fill, apertures, foliage detail and animated3D airflow."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
import numpy as np
s.render.engine='BLENDER_EEVEE';s.render.film_transparent=True
cam.type='PERSP';cam.lens=50;cam.sensor_width=36;cam.sensor_fit='HORIZONTAL'
camera=json.loads((O.parents[1]/'out/garden_eyes_airflow_v2/camera.json').read_text())
for fi in range(count):
    cz=22/camera['scale'][fi];cx=-(camera['center'][fi][0]-640)/1280*(cz*.72);cy=(camera['center'][fi][1]-360)/1280*(cz*.72)
    co.location=(cx,cy,cz);co.keyframe_insert('location',frame=fi+1)
    plane.location=(cx,cy,0);plane.scale=(cz*.36,cz*.2025,1);plane.keyframe_insert('location',frame=fi+1);plane.keyframe_insert('scale',frame=fi+1)
cover=0;clear=0
for j in range(len(rows[0]['eyes'])):
    eye=[v['eyes'][j] for v in rows]
    cx=b.animated(f'Eye{j} X',[v['center'][0] for v in eye]);cy=b.animated(f'Eye{j} Y',[v['center'][1] for v in eye]);rx=b.animated(f'Eye{j} rx',[v['rx'] for v in eye]);ry=b.animated(f'Eye{j} ry',[v['ry'] for v in eye]);opening=b.animated(f'Eye{j} opening',[v['opening'] for v in eye])
    d=(((x-cx)/(rx+9))**2+((y-cy)/(ry+9))**2)**.5;region=1-((d-.92)/.45).smooth()
    curve=(1-((x-cx)/(rx+12))**2).clamp()**.5;aperture=((opening*(ry+14)*curve-b.op('ABSOLUTE',y-cy))/2.5).smooth()
    hide=region*(1-aperture)*(1-((opening-.85)/.15).smooth())
    cover=b.op('MAXIMUM',cover,hide);clear=b.op('MAXIMUM',clear,region)
def aov(name,value):
    av=s.view_layers[0].aovs.add();av.name=name;av.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
aov('Cover',cover);aov('Clear',clear)
scale=b.animated('Camera noise scale',camera['scale']);cx=b.animated('Camera noise X',[v[0] for v in camera['center']]);cy=b.animated('Camera noise Y',[v[1] for v in camera['center']])
noise=b.n.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=320;noise.inputs['Detail'].default_value=0
b.plug(b.combine([((x-cx)/scale+640)/1280,((y-cy)/scale+360)/1280,0]),noise.inputs['Vector']);b.plug(b.animated('Slow phosphor variation',[7.13+i*.006 for i in range(count)]),noise.inputs['W'])
aov('Noise',noise.outputs['Fac'])
em=b.n.new('ShaderNodeEmission');em.inputs[0].default_value=(0,0,0,1);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
optics=bpy.data.collections.new('Optics');s.collection.children.link(optics)
for c in list(plane.users_collection):c.objects.unlink(plane)
optics.objects.link(plane)
air=bpy.data.collections.new('Air');s.collection.children.link(air)
mat=bpy.data.materials.new('Native Gaussian dust');mat.use_nodes=True;mat.surface_render_method='BLENDED';mat.node_tree.nodes.clear();nb=Builder(mat.node_tree)
uvn=nb.n.new('ShaderNodeTexCoord');sp=nb.n.new('ShaderNodeSeparateXYZ');nb.plug(uvn.outputs['UV'],sp.inputs[0]);ux=Field(nb,sp.outputs[0]);uy=Field(nb,sp.outputs[1]);gauss=(-38*((ux-.5)**2+(uy-.5)**2)).exp()
vc=nb.n.new('ShaderNodeVertexColor');vc.layer_name='Tint';opacity=gauss*Field(nb,vc.outputs['Alpha']);em=nb.n.new('ShaderNodeEmission');em.inputs[1].default_value=1.4;nb.plug(vc.outputs['Color'],em.inputs[0]);transparent=nb.n.new('ShaderNodeBsdfTransparent');mix=nb.n.new('ShaderNodeMixShader');nb.plug(opacity,mix.inputs[0]);nb.plug(transparent.outputs[0],mix.inputs[1]);nb.plug(em.outputs[0],mix.inputs[2]);mo=nb.n.new('ShaderNodeOutputMaterial');nb.plug(mix.outputs[0],mo.inputs[0])
for fi in range(count):
    with np.load(D/'geometry'/f'{fi:04d}.npz') as state:
        vertices=np.concatenate([state[k] for k in ['motes','wisps','halo0','halo1']]);rgba=np.concatenate([state[k+'_rgba'] for k in ['motes','wisps','halo0','halo1']])
    n=len(vertices)//4;mesh=bpy.data.meshes.new(f'Air state{fi+1}');mesh.from_pydata(vertices.tolist(),[],np.arange(n*4).reshape(-1,4).tolist())
    uv=mesh.uv_layers.new();uv.data.foreach_set('uv',np.tile([0,0,1,0,1,1,0,1],n));attr=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');attr.data.foreach_set('color',rgba.ravel());mesh.materials.append(mat)
    ob=bpy.data.objects.new(mesh.name,mesh);air.objects.link(ob)
    for at,hide in [(0,True),(fi,True),(fi+1,False),(fi+2,True)]:ob.hide_render=hide;ob.keyframe_insert('hide_render',frame=at)
s.view_layers[0].name='Optics';s.view_layers[0].layer_collection.children['Air'].exclude=True
layer=s.view_layers.new('Air');layer.layer_collection.children['Optics'].exclude=True
tree=bpy.data.node_groups.new('Native garden waking composite','CompositorNodeTree');tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=tree;b=Builder(tree)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);original=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers');rl.layer='Optics';dust=b.n.new('CompositorNodeRLayers');dust.layer='Air'
raw=[b.display(v) for v in b.split(original)];cover=b.split(rl.outputs['Cover'])[0];clear=b.split(rl.outputs['Clear'])[0]
setalpha=b.n.new('CompositorNodeSetAlpha');setalpha.inputs['Type'].default_value='Replace Alpha';b.plug(b.combine(raw),setalpha.inputs['Image']);b.plug(1-b.op('GREATER_THAN',clear,.02),setalpha.inputs['Alpha'])
fill=b.n.new('CompositorNodeInpaint');fill.inputs['Size'].default_value=round(90*W/1280);b.plug(setalpha.outputs[0],fill.inputs['Image'])
comp=[b.display(a*(1-Field(b,dust.outputs['Alpha']))+z) for a,z in zip(b.split(original),b.split(dust.outputs['Image']))]
comp=[a*(1-cover)+z*cover for a,z in zip(comp,b.split(fill.outputs[0]))]
lum=sum(a*w for a,w in zip(raw,[.299,.587,.114]));leaf=((lum-.015)/.06).smooth()*(1-((lum-.22)/.16).smooth())*(1-clear)
comp=[a+(v**.86-v)*.68*leaf for a,v in zip(comp,raw)]
sobel=b.n.new('CompositorNodeFilter');sobel.inputs['Type'].default_value='Sobel';b.plug(b.combine([lum]*3),sobel.inputs['Image'])
edge=(b.op('ABSOLUTE',b.split(sobel.outputs[0])[0])*7*W/1280).clamp()*leaf
speck=((b.split(rl.outputs['Noise'])[0]-.43)*7).clamp();pulse=b.animated('Waking leaf accent',[1+.35*math.exp(-((i-55)/12)**2) for i in range(count)])
phosphor=edge*speck*(7/255)*pulse;phosphor=phosphor+b.split(b.blur(b.combine([phosphor]*3),1.7,W))[0]*.65
result=b.combine([b.linear((a+phosphor*c).clamp()) for a,c in zip(comp,[.76,1,.66])]);end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'waking_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
