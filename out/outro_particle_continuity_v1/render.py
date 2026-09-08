from pathlib import Path
import bpy,math,random,sys
from mathutils import Vector
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
mode=sys.argv[-1];close=mode=='close';N=128 if close else 2400
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16
sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100;sc.render.fps=24
sc.render.use_motion_blur=True;sc.render.motion_blur_shutter=.5
sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
sc.world=bpy.data.worlds.new('Black');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
cam=bpy.data.cameras.new('Perspective');co=bpy.data.objects.new('Camera',cam);sc.collection.objects.link(co);co.location=(0,0,10);cam.type='PERSP';cam.lens=22.5;cam.sensor_width=36;sc.camera=co
def smooth(a,b,t):
    v=max(0,min(1,(t-a)/(b-a)));return v*v*(3-2*v)
def project(x,y,z):return ((x-.5)*16*(10-z)/10,(.5-y)*9*(10-z)/10,z)
rng=random.Random(9821);seeds=[];cols=[]
for j in range(N):
    if close:
        sx=rng.uniform(.12,.88);sy=rng.uniform(.2,.95);z=rng.uniform(-1.5,1.5);radius=rng.uniform(.011,.025)
    else:
        while True:
            if rng.random()<.78:sx=rng.gauss(.498,.16);sy=rng.gauss(.78,.145)
            else:sx=rng.uniform(-.08,1.08);sy=rng.uniform(.32,1.04)
            if not (.33<sx<.68 and sy<.57):break
        z=rng.uniform(-2.3,2);radius=rng.uniform(.006,.017)
    d=math.sqrt(((sx-.498)*16)**2+((sy-.806)*9)**2+z*z)
    life=(.98+.115*min(d,6)) if j<N-24 else 2.7+(j%7)*.07
    seeds.append((sx,sy,z,radius,life))
    mix=(1 if j%2 else 0) if close else smooth(.44,.56,sx+.025*math.sin(sy*7))
    left=(.68,.20,.025);right=(.02,.44,.66)
    cols.append(tuple(left[k]*(1-mix)+right[k]*mix for k in range(3))+(1,))
def state(j,frame):
    sx,sy,z,r,life=seeds[j]
    if close:
        # Prewarmed, one continuous population over all84frames.
        t=(4538+frame-1)/24;age=(j/N+t*(.17+(j%5)*.013))%1
        sx=.5+(1 if j%2 else -1)*(.10+.32*age)+.04*math.sin(age*6.28+j)
        sy=.90-.65*age+.025*math.sin(age*9+j)
        fade=smooth(0,.12,age)*(1-smooth(.86,1,age))
        return project(sx,sy,z),r*math.sqrt(fade)
    t=(frame-1)/24;p=min(1,(t/life)**2)
    target_y=.806+.068*smooth(1.0,2.0,t)
    # Acceleration is distance-dependent; depth bows toward camera en route.
    sx=sx+(.498-sx)*p+.035*math.sin(math.pi*p)*math.sin(j*.2)
    sy=sy+(target_y-sy)*p+.035*math.sin(math.pi*p)
    zz=z*(1-p)+1.2*math.sin(math.pi*p)
    fade=1-smooth(.91,1,p)
    return project(sx,sy,zz),r*math.sqrt(fade)
verts=[];faces=[]
for j in range(N):
    pos,r=state(j,1);base=len(verts)
    for k in range(8):
        a=k*math.tau/8;verts.append((pos[0]+r*math.cos(a),pos[1]+r*math.sin(a),pos[2]))
    faces.append(tuple(range(base,base+8)))
mesh=bpy.data.meshes.new('Persistent particle field');mesh.from_pydata(verts,[],faces)
ob=bpy.data.objects.new('Particle cloud',mesh);sc.collection.objects.link(ob)
mat=bpy.data.materials.new('Warm left / cool right emission');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear()
attr=n.new('ShaderNodeVertexColor');attr.layer_name='CloudColor';em=n.new('ShaderNodeEmission');em.inputs[1].default_value=1.3 if close else .8;out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(attr.outputs[0],em.inputs[0]);mat.node_tree.links.new(em.outputs[0],out.inputs[0]);mesh.materials.append(mat)
color=mesh.color_attributes.new(name='CloudColor',type='FLOAT_COLOR',domain='CORNER')
for poly,c in zip(mesh.polygons,cols):
    for idx in poly.loop_indices:color.data[idx].color=c
ob.shape_key_add(name='Basis')
for f in range(1,85 if close else 89):
    key=ob.shape_key_add(name=f'Time{f}')
    for j in range(N):
        pos,r=state(j,f)
        for k in range(8):
            a=k*math.tau/8;key.data[j*8+k].co=(pos[0]+r*math.cos(a),pos[1]+r*math.sin(a),pos[2])
    key.value=0;key.keyframe_insert('value',frame=f-1);key.value=1;key.keyframe_insert('value',frame=f);key.value=0;key.keyframe_insert('value',frame=f+1)
if close:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.08,location=(0,0,0));guide=bpy.context.object
    m=bpy.data.materials.new('Green guide');m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(.25,1,.3,1);e.inputs[1].default_value=4;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);guide.data.materials.append(m)
    for f in range(1,85):
        u=(4538+f-1-4574)/48
        if u<0:guide.scale=(0,0,0)
        else:guide.scale=(1,1,1)
        guide.location=project((800+280*math.sin(u*math.tau*.8))/1280,(220+100*math.sin(u*math.tau*1.6))/720,0)
        guide.keyframe_insert('location',frame=f);guide.keyframe_insert('scale',frame=f)
tree=bpy.data.node_groups.new('Native light composite','CompositorNodeTree');tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');sc.compositing_node_group=tree;n=tree.nodes;l=tree.links
rl=n.new('CompositorNodeRLayers');g=n.new('CompositorNodeGlare');g.inputs['Type'].default_value='Fog Glow';g.inputs['Quality'].default_value='High';g.inputs['Threshold'].default_value=.06;g.inputs['Strength'].default_value=2.4;g.inputs['Size'].default_value=.25;l.new(rl.outputs['Image'],g.inputs['Image'])
plate=n.new('CompositorNodeImage');header=n.new('CompositorNodeImage')
def mix(a,b,factor=1,blend='ADD'):
    node=n.new('ShaderNodeMix');node.data_type='RGBA';node.blend_type=blend;node.clamp_result=False
    if isinstance(factor,(int,float)):node.inputs[0].default_value=factor
    else:l.new(factor,node.inputs[0])
    l.new(a,node.inputs[6]);l.new(b,node.inputs[7]);return node.outputs[2]
if close:
    lights=n.new('CompositorNodeImage');sep=n.new('CompositorNodeSeparateColor');l.new(lights.outputs['Image'],sep.inputs[0])
    sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';l.new(sep.outputs[0],sub.inputs[0]);l.new(sep.outputs[2],sub.inputs[1])
    positive=n.new('ShaderNodeMath');positive.operation='MAXIMUM';l.new(sub.outputs[0],positive.inputs[0]);positive.inputs[1].default_value=0
    gain=n.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=5;l.new(positive.outputs[0],gain.inputs[0])
    tint=n.new('ShaderNodeMix');tint.data_type='RGBA';tint.blend_type='MULTIPLY';tint.clamp_result=False;tint.inputs[0].default_value=1;l.new(gain.outputs[0],tint.inputs[6]);tint.inputs[7].default_value=(1,.5,.085,1)
    ag=n.new('CompositorNodeGlare');ag.inputs['Type'].default_value='Fog Glow';ag.inputs['Threshold'].default_value=.05;ag.inputs['Strength'].default_value=1.5;ag.inputs['Size'].default_value=.2;l.new(tint.outputs[2],ag.inputs['Image'])
    artifact=mix(plate.outputs['Image'],ag.outputs['Image'])
    crop=n.new('CompositorNodeCrop');crop.inputs['X'].default_value=445;crop.inputs['Y'].default_value=20;crop.inputs['Width'].default_value=400;crop.inputs['Height'].default_value=225;l.new(artifact,crop.inputs['Image'])
    scale=n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';l.new(crop.outputs['Image'],scale.inputs['Image']);base=scale.outputs['Image']
else:base=plate.outputs['Image']
combined=mix(base,g.outputs['Image'])
mask=n.new('CompositorNodeBoxMask');mask.inputs['Position'].default_value=(.5,.9361);mask.inputs['Size'].default_value=(1,.1278)
final=mix(combined,header.outputs['Image'],mask.outputs[0],'MIX');output=n.new('NodeGroupOutput');l.new(final,output.inputs['Image'])
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
folder=OUT/mode;folder.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{mode}.blend'))
frames=range(1,85) if close else list(range(1,23))+list(range(50,89))
for frame in frames:
    sc.frame_set(frame);song=(4538 if close else 4622)+frame-1
    if close:
        source=23+frame-1
        plate.image=bpy.data.images.load(str(ROOT/'out/outro_B2_afterglow_v1/optical'/f'{source:03}.png'),check_existing=True)
        lights.image=bpy.data.images.load(str(ROOT/'out/outro_B2_afterglow_v1/lights'/f'{source:03}.png'),check_existing=True)
    else:
        plate.image=bpy.data.images.load(str(OUT/'cleanplates'/f'{song-4538+1:04}.png'),check_existing=True)
    header.image=bpy.data.images.load(str(OUT/'plates'/f'{song-4538+1:04}.png'),check_existing=True)
    sc.render.filepath=str(folder/f'{song:04}.png');bpy.ops.render.render(write_still=True)
