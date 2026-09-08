from pathlib import Path
import bpy, math, random, sys
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
HEIGHT=int(args[0]) if args else 720
CHECK=int(args[1]) if len(args)>1 else 0
OUT=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES';sc.cycles.samples=24
sc.render.resolution_x=round(HEIGHT*16/9);sc.render.resolution_y=HEIGHT;sc.render.resolution_percentage=100
sc.render.fps=24;sc.frame_start=1;sc.frame_end=22
sc.render.use_motion_blur=True;sc.render.motion_blur_shutter=.5
sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
sc.world=bpy.data.worlds.new('Black emission background');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0,0,0,1)
cam_data=bpy.data.cameras.new('Frame-space camera');cam=bpy.data.objects.new('Frame-space camera',cam_data)
sc.collection.objects.link(cam);cam.location=(0,0,10);cam_data.type='PERSP';cam_data.lens=22.5;cam_data.sensor_width=36;sc.camera=cam
mat=bpy.data.materials.new('Spatially coherent colored emission');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();attr=n.new('ShaderNodeVertexColor');attr.layer_name='CloudColor'
em=n.new('ShaderNodeEmission');em.inputs['Strength'].default_value=.75
out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(attr.outputs['Color'],em.inputs['Color']);mat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
rng=random.Random(9821);verts=[];faces=[];colors=[];ends=[]
for j in range(2400):
    while True:
        if rng.random()<.78:
            sx=rng.gauss(.498,.16);sy=rng.gauss(.78,.145)
        else:
            sx=rng.uniform(-.08,1.08);sy=rng.uniform(.32,1.04)
        if not (.33<sx<.68 and sy<.57):break
    z=rng.uniform(-2.3,2.0)
    radius=rng.uniform(.006,.017)
    # Smooth large color domains; neighbors inherit the same local cloud hue.
    field=.5+.5*math.sin(sx*7+sy*4+math.sin(sy*6)*.7)
    rose=(.52,.035,.15);violet=(.15,.045,.58)
    color=tuple(rose[k]*(1-field)+violet[k]*field for k in range(3))+(1,)
    # Only the beginning of a long inward drift is shown, never a completed intake.
    ex=sx+(.498-sx)*.18+(.012*math.sin(sy*10))
    ey=sy+(.806-sy)*.18+.017*math.sin(sx*6)
    base=len(verts)
    for k in range(8):
        ang=k*math.tau/8;dx=radius*math.cos(ang);dy=radius*math.sin(ang)
        verts.append(((sx-.5)*16*(10-z)/10+dx,(.5-sy)*9*(10-z)/10+dy,z))
        ez=z*.9
        ends.append(((ex-.5)*16*(10-ez)/10+dx,(.5-ey)*9*(10-ez)/10+dy,ez))
    faces.append(tuple(range(base,base+8)));colors.append(color)
mesh=bpy.data.meshes.new('2400 depth-distributed motes');mesh.from_pydata(verts,[],faces);mesh.materials.append(mat)
obj=bpy.data.objects.new('Slow colored atmosphere',mesh);sc.collection.objects.link(obj)
col=mesh.color_attributes.new(name='CloudColor',type='FLOAT_COLOR',domain='CORNER')
for poly,color in zip(mesh.polygons,colors):
    for loop in poly.loop_indices:col.data[loop].color=color
obj.shape_key_add(name='Basis');drift=obj.shape_key_add(name='Beginning of return')
for vert,end in zip(drift.data,ends):vert.co=end
drift.value=0;drift.keyframe_insert('value',frame=1)
drift.value=1;drift.keyframe_insert('value',frame=22)
tree=bpy.data.node_groups.new('Additive atmosphere compositor','CompositorNodeTree')
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
sc.compositing_node_group=tree
nodes=tree.nodes;links=tree.links
render=nodes.new('CompositorNodeRLayers')
glare=nodes.new('CompositorNodeGlare');glare.inputs['Type'].default_value='Fog Glow';glare.inputs['Quality'].default_value='High'
glare.inputs['Threshold'].default_value=.08;glare.inputs['Strength'].default_value=1.8;glare.inputs['Size'].default_value=.22
links.new(render.outputs['Image'],glare.inputs['Image'])
plate=nodes.new('CompositorNodeImage');plate.image=bpy.data.images.load(str(OUT.parent/'outro_mote_cloud_blender_v1/plate/0001.png'))
scale=nodes.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';links.new(plate.outputs['Image'],scale.inputs['Image'])
add=nodes.new('ShaderNodeMix');add.data_type='RGBA';add.blend_type='ADD';add.inputs[0].default_value=1;add.clamp_result=False
links.new(scale.outputs['Image'],add.inputs[6]);links.new(glare.outputs['Image'],add.inputs[7])
result=nodes.new('NodeGroupOutput');links.new(add.outputs[2],result.inputs['Image'])
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
sc.render.filepath=str(OUT/'frames/')
(OUT/'frames').mkdir(exist_ok=True)
if not CHECK:bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'shot8.blend'))
for frame in ([CHECK] if CHECK else range(1,23)):
    sc.frame_set(frame)
    plate.image=bpy.data.images.load(str(OUT.parent/'outro_mote_cloud_blender_v1/plate'/f'{frame:04}.png'),check_existing=True)
    sc.render.filepath=str(OUT/'frames'/f'{frame:04}.png') if not CHECK else str(OUT/f'check_{HEIGHT}_{frame:04}.png')
    bpy.ops.render.render(write_still=True)
