import bpy,math
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=112
s.view_settings.view_transform='Standard';s.render.use_motion_blur=True;s.render.motion_blur_shutter=.7
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,0,0));plane=bpy.context.object;plane.scale=(9.58,5.4,1)
m=bpy.data.materials.new('Original hunt footage');m.use_nodes=True;n=m.node_tree.nodes;n.clear();tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(o/'source/shot-0001.png'));tex.image.source='SEQUENCE';tex.image_user.frame_duration=112;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True
em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);plane.data.materials.append(m)
bpy.ops.object.camera_add(location=(.2,1.6,26.611111/2.6));cam=bpy.context.object;s.camera=cam;cam.data.type='PERSP';cam.data.lens=50;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
# Close-up through local26, then eight-frame pullback to original full composition.
for f,loc in [(1,(.2,1.6,26.611111/2.6)),(26,(.2,1.6,26.611111/2.6)),(34,(0,0,26.611111)),(112,(0,0,26.611111))]:
 cam.location=loc;cam.keyframe_insert(data_path='location',frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='BEZIER';key.handle_left_type='AUTO_CLAMPED';key.handle_right_type='AUTO_CLAMPED'
(o/'overlay').mkdir(exist_ok=True);s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(o/'overlay/pullback-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Hunt-pullback-v001.blend'));bpy.ops.render.render(animation=True)
