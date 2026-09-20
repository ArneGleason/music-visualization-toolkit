import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=16
s.view_settings.view_transform='Standard';s.render.use_motion_blur=True;s.render.motion_blur_shutter=.9
for idx,file in enumerate([str(o/'presentation-last.png'),str(r/'assets/SCN-009-scale-diagram-v001.png')]):
 bpy.ops.mesh.primitive_plane_add(size=2,location=(0,0,0));ob=bpy.context.object;ob.name=file;ob.scale=(6.4,3.6,1)
 m=bpy.data.materials.new(file);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(r/'assets'/file))
 em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);ob.data.materials.append(m)
 for f,v in [(1,idx==1),(8,idx==1),(9,idx==0),(16,idx==0)]:ob.hide_render=v;ob.keyframe_insert(data_path='hide_render',frame=f)
bpy.ops.object.camera_add(location=(0,0,17.77778));cam=bpy.context.object;s.camera=cam;cam.data.type='PERSP';cam.data.lens=50;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
for f,loc in [(1,(-.2,-.25,16.1616)),(4,(-.8,-.8,12)),(8,(-1.5,-1.3,7.5)),(9,(0,0,15.5)),(12,(0,0,17.1)),(16,(0,0,17.77778))]:
 cam.location=loc;cam.keyframe_insert(data_path='location',frame=f)
nt=bpy.data.node_groups.new('Schematic radial blur transition','CompositorNodeTree');s.compositing_node_group=nt
nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
src=nt.nodes.new('CompositorNodeRLayers');blur=nt.nodes.new('CompositorNodeDBlur');out=nt.nodes.new('NodeGroupOutput')
nt.links.new(src.outputs['Image'],blur.inputs['Image']);nt.links.new(blur.outputs['Image'],out.inputs['Image'])
blur.inputs['Samples'].default_value=24
print('BLUR INPUTS',[(i.name,i.default_value) for i in blur.inputs if i.name!='Image'])
for f,z in [(1,0),(5,.12),(8,.3),(9,.3),(12,.08),(16,0)]:
 blur.inputs['Scale'].default_value=1+z;blur.inputs['Scale'].keyframe_insert(data_path='default_value',frame=f)
(o/'frames').mkdir(exist_ok=True);s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(o/'frames/zoom-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Schematic-blur-zoom-v001.blend'));bpy.ops.render.render(animation=True)
