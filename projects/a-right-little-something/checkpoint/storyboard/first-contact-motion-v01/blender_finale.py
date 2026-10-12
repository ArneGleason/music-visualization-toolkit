"""Composite the two independently generated finale videos in editable Blender."""
import json
from pathlib import Path
import bpy

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
register=json.loads((BASE/'shots/shotlist.json').read_text(encoding='utf-8'))
plan=next(s for s in register['storyboardProposals'] if s['id']=='contact-032')['compositePlan']
count=plan['frames']
assert count==235 and plan['startFrame']==5031
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=1;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.fps=24;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.frame_start=1;scene.frame_end=count
camera=bpy.data.cameras.new('Compositor render camera')
obj=bpy.data.objects.new('Compositor render camera',camera)
scene.collection.objects.link(obj);scene.camera=obj
group=bpy.data.node_groups.new('Independent cosmic and Harper video plates','CompositorNodeTree')
group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
scene.compositing_node_group=group
nodes,links=group.nodes,group.links
sources=[]
for index,source in enumerate(plan['videoInputs']):
    folder=OUT/('finale-'+source['id'])
    assert len(list(folder.glob('frame_*.png')))==count, folder
    node=nodes.new('CompositorNodeImage');node.name=source['id']+' / independently generated Kling video'
    node.image=bpy.data.images.load(str(folder/'frame_0001.png'))
    node.image.source='SEQUENCE'
    node.frame_duration=count;node.frame_start=1
    node.frame_offset=0;node.use_auto_refresh=True;node.use_cyclic=False
    node.location=(-400,200-index*300)
    sources.append(node)
blend=nodes.new('ShaderNodeMix');blend.data_type='RGBA';blend.blend_type='SCREEN';blend.clamp_factor=True
blend.name='Harper visible from cut / editable superimposition';blend.location=(0,100)
links.new(sources[0].outputs['Image'],blend.inputs[6]);links.new(sources[1].outputs['Image'],blend.inputs[7])
for frame,opacity in [(1,.80),(count,.86)]:
    blend.inputs[0].default_value=opacity;blend.inputs[0].keyframe_insert(data_path='default_value',frame=frame)
output=nodes.new('NodeGroupOutput');output.location=(300,100)
links.new(blend.outputs[2],output.inputs['Image'])
scene['song_start_frame']=5031;scene['song_end_frame_exclusive']=5266
scene['production_note']='Two separate silent Kling12second videos, each trimmed source frames25-259. Blender controls the overlay; no generated composite. Source sequences retain independent native movement.'
(OUT/'finale-frames').mkdir(exist_ok=True)
scene.render.filepath=str(OUT/'finale-frames/frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'finale-two-videos.blend'))
bpy.ops.render.render(animation=True)
