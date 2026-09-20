import bpy,json,math,sys
from pathlib import Path
o=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=76;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
bpy.ops.object.camera_add(location=(0,0,5));s.camera=bpy.context.object
nt=bpy.data.node_groups.new('Rabbit tracked blur with protected bat face','CompositorNodeTree');s.compositing_node_group=nt;nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');nodes=nt.nodes;links=nt.links
out=nodes.new('NodeGroupOutput')
def sequence(name,folder,prefix,color):
 n=nodes.new('CompositorNodeImage');n.name=name;n.image=bpy.data.images.load(str(o/folder/(prefix+'0001.png')));n.image.source='SEQUENCE';n.image.colorspace_settings.name=color;n.frame_duration=76;n.frame_start=1;n.use_auto_refresh=True;return n
src=sequence('Untouched original','source','frame-','sRGB');mask=sequence('Feathered rabbit minus head protection','masks','mask-','Non-Color')
blur=nodes.new('CompositorNodeDBlur');blur.name='Short directional smear following rabbit turn';blur.inputs['Samples'].default_value=16;links.new(src.outputs['Image'],blur.inputs['Image'])
soft=nodes.new('CompositorNodeBlur');soft.name='Small softness within rabbit only';soft.inputs['Size'].default_value=(2.5,2.5);links.new(blur.outputs['Image'],soft.inputs['Image'])
mix=nodes.new('ShaderNodeMix');mix.data_type='RGBA';links.new(mask.outputs['Image'],mix.inputs[0]);links.new(src.outputs['Image'],mix.inputs[6]);links.new(soft.outputs['Image'],mix.inputs[7]);links.new(mix.outputs[2],out.inputs['Image'])
for rec in json.loads((o/'tracking.json').read_text()):
 f=rec['local_frame']+1;blur.inputs['Amount'].default_value=rec['blur_pixels']/1280;blur.inputs['Amount'].keyframe_insert('default_value',frame=f);blur.inputs['Direction'].default_value=rec['angle'];blur.inputs['Direction'].keyframe_insert('default_value',frame=f)
(o/'render').mkdir(exist_ok=True);s.render.filepath=str(o/'render/frame-');bpy.ops.wm.save_as_mainfile(filepath=str(o/'Rabbit-local-motion-blur-v001.blend'))
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if args:s.frame_set(int(args[0]));s.render.filepath=str(o/'test.png');bpy.ops.render.render(write_still=True)
else:bpy.ops.render.render(animation=True)
