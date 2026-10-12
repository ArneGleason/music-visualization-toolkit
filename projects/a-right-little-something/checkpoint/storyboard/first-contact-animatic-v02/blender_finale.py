"""Editable two-source finale preview. Replace still inputs with clean takes later."""
from pathlib import Path
import json
import sys
import bpy

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
register=json.loads((BASE/'shots/shotlist.json').read_text(encoding='utf-8'))
plan=next(s for s in register['storyboardProposals'] if s['id']=='contact-032')['compositePlan']
count=plan['frames']
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=1;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.fps=24;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.frame_start=1;scene.frame_end=count
camera=bpy.data.cameras.new('Empty camera for compositor render')
obj=bpy.data.objects.new('Empty camera for compositor render',camera)
scene.collection.objects.link(obj);scene.camera=obj
group=bpy.data.node_groups.new('Separate cosmic and Harper source plates','CompositorNodeTree')
group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
scene.compositing_node_group=group
nodes,links=group.nodes,group.links
sources=[]
for index,source in enumerate(plan['videoInputs']):
    image=nodes.new('CompositorNodeImage');image.name=source['id']+' / separate replaceable source'
    image.image=bpy.data.images.load(str(BASE/source['still']));image.image.pack()
    image.location=(-700,200-index*300)
    scale=nodes.new('CompositorNodeScale')
    scale.inputs['X'].default_value=1920/image.image.size[0]
    scale.inputs['Y'].default_value=1080/image.image.size[1]
    scale.inputs['Interpolation'].default_value='Bicubic'
    scale.location=(-480,200-index*300);links.new(image.outputs['Image'],scale.inputs['Image'])
    sources.append(scale)
travel=nodes.new('CompositorNodeTransform');travel.name='Gentle forward cosmic drift'
travel.location=(-240,200);travel.inputs['Interpolation'].default_value='Bicubic'
links.new(sources[0].outputs['Image'],travel.inputs['Image'])
for frame in range(1,count+1):
    travel.inputs['Scale'].default_value=1+.035*(frame-1)/max(1,count-1)
    travel.inputs['Scale'].keyframe_insert(data_path='default_value',frame=frame)
blend=nodes.new('ShaderNodeMix');blend.data_type='RGBA';blend.blend_type='SCREEN';blend.clamp_factor=True
blend.name='Harper visible from the first frame / editorial preview';blend.location=(20,100)
links.new(travel.outputs['Image'],blend.inputs[6]);links.new(sources[1].outputs['Image'],blend.inputs[7])
for frame,opacity in [(1,.80),(count,.86)]:
    blend.inputs[0].default_value=opacity;blend.inputs[0].keyframe_insert(data_path='default_value',frame=frame)
output=nodes.new('NodeGroupOutput');output.location=(300,100);links.new(blend.outputs[2],output.inputs['Image'])
scene['song_start_frame']=plan['startFrame'];scene['song_end_frame_exclusive']=plan['endFrameExclusive']
scene['production_note']='Two independent still sources here. Generate two separate clean videos later, replace image nodes, and retain Blender control over the superimposition.'
scene['preview_only']='This is editorial still compositing; no generated character motion.'
(OUT/'finale-frames').mkdir(exist_ok=True)
scene.render.filepath=str(OUT/'finale-frames/frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'finale-two-plates.blend'))
if '--preview' in sys.argv:
    scene.frame_set(40);scene.render.filepath=str(OUT/'finale-preview.png')
    bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
