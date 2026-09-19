import bpy,math,pathlib
root=pathlib.Path(__file__).resolve().parent;job=root.parent.parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=193
s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,10));s.camera=bpy.context.object
s.use_nodes=True
g=bpy.data.node_groups.new('Concealed POV - gait and optical treatment','CompositorNodeTree');s.compositing_node_group=g
socket=g.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
clip=g.nodes.new('CompositorNodeMovieClip');clip.clip=bpy.data.movieclips.load(str(job/'video-tests'/'KLING-POV-002'/'KLING-POV-002-01.mp4'))
scale=g.nodes.new('CompositorNodeScale');scale.inputs['X'].default_value=1280/1916;scale.inputs['Y'].default_value=720/1080
g.links.new(clip.outputs['Image'],scale.inputs['Image'])
move=g.nodes.new('CompositorNodeTransform');move.label='Small weighted bob, lateral drift and roll'
g.links.new(scale.outputs['Image'],move.inputs['Image'])
move.inputs['Scale'].default_value=1.07
for f in range(1,194):
 t=(f-1)/24;phase=2*math.pi*1.35*t
 # Uneven but restrained walking rhythm with slow lateral breathing.
 values={'X':5.5*math.sin(phase*.5)+1.5*math.sin(2*math.pi*.23*t),
         'Y':7.5*math.sin(phase)+2*math.sin(phase*2+.6),
         'Angle':math.radians(.32)*math.sin(phase*.5+.5),
         'Scale':1.07+.003*math.sin(phase-.4)}
 for k,v in values.items():move.inputs[k].default_value=v;move.inputs[k].keyframe_insert(data_path='default_value',frame=f)
lens=g.nodes.new('CompositorNodeLensdist');lens.label='Mild peripheral curvature, very slight color separation'
lens.inputs['Distortion'].default_value=.035;lens.inputs['Dispersion'].default_value=.002;lens.inputs['Fit'].default_value=True
# Curvature is a stylized optical cue, not a claim about any species vision.
g.links.new(move.outputs['Image'],lens.inputs['Image'])
out=g.nodes.new('NodeGroupOutput');g.links.new(lens.outputs['Image'],out.inputs['Image'])
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.frame_set(70);s.render.filepath=str(root/'pov-effect-check.png');bpy.ops.render.render(write_still=True)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG'
s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH'
s.render.filepath=str(root/'Stealth-POV-motion-lens-v001.mp4');s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Stealth-POV-motion-lens-v001.blend'))
bpy.ops.render.render(animation=True)
