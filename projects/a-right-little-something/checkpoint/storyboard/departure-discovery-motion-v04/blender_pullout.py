"""Editable Blender compositor: slight departure pullout and cyan station twinkle."""
import sys
from pathlib import Path
import bpy
import numpy as np

OUT=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=1
scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED'
scene.render.threads=8
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.render.fps=24
scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
scene.render.filepath=str(OUT/'departure-frames/frame_')
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.view_settings.exposure=0
scene.view_settings.gamma=1
scene.frame_start=1
scene.frame_end=59
camera=bpy.data.cameras.new('Compositor render camera')
obj=bpy.data.objects.new('Compositor render camera',camera)
scene.collection.objects.link(obj)
scene.camera=obj

group=bpy.data.node_groups.new('Departure / pullout and station twinkle','CompositorNodeTree')
group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
scene.compositing_node_group=group
nodes,links=group.nodes,group.links
source=nodes.new('CompositorNodeImage')
source.name='Accepted V56 reversed departure / untouched source'
source.image=bpy.data.images.load(str(OUT/'departure-source/001.png'))
source.image.source='SEQUENCE'
source.frame_start=1
source.frame_duration=140
source.use_auto_refresh=True
source.location=(-600,100)

# Procedural light, stored inside the blend. Coordinates measured on the source.
# Blender image pixel rows run bottom-to-top; station is at (960, 514) from top.
y,x=np.mgrid[0:1080,0:1920].astype(np.float32)
dx=x-960
dy=y-(1079-514)
r2=dx*dx+dy*dy
core=np.exp(-r2/5.0)*1.7
halo=np.exp(-r2/180.0)*.055
horizontal=np.exp(-np.abs(dx)/18-np.abs(dy)/.8)*.42
vertical=np.exp(-np.abs(dx)/.8-np.abs(dy)/11)*.30
light=core+halo+horizontal+vertical
rgba=np.ones((1080,1920,4),dtype=np.float32)
rgba[:,:,:3]=light[:,:,None]*np.array([.10,.78,1.0],dtype=np.float32)
twinkle=bpy.data.images.new('Procedural cyan station departure twinkle',width=1920,height=1080,float_buffer=True)
twinkle.colorspace_settings.name='Non-Color'
twinkle.pixels.foreach_set(rgba.ravel())
twinkle.pack()
light_node=nodes.new('CompositorNodeImage')
light_node.image=twinkle
light_node.location=(-600,-180)
add=nodes.new('ShaderNodeMix')
add.data_type='RGBA'
add.blend_type='ADD'
add.clamp_factor=True
add.location=(-300,100)
links.new(source.outputs['Image'],add.inputs[6])
links.new(light_node.outputs['Image'],add.inputs[7])
for frame,power in [(1,0),(3,.20),(6,1),(9,.45),(13,.12),(17,0),(59,0)]:
    add.inputs[0].default_value=power
    add.inputs[0].keyframe_insert(data_path='default_value',frame=frame)

transform=nodes.new('CompositorNodeTransform')
transform.name='18 percent closer to full frame / song 111.0 to 113.417'
transform.location=(-50,100)
transform.inputs['Interpolation'].default_value='Bicubic'
links.new(add.outputs[2],transform.inputs['Image'])
for frame in range(1,60):
    t=(frame-1)/58
    transform.inputs['Scale'].default_value=1+.18*(1-t)**1.6
    transform.inputs['Scale'].keyframe_insert(data_path='default_value',frame=frame)
output=nodes.new('NodeGroupOutput')
output.location=(240,100)
links.new(transform.outputs['Image'],output.inputs['Image'])
scene['song_start_frame']=2665
scene['full_frame_at_song_frame']=2723
scene['source']='V56 reversed departure, original 140 frames; source time unchanged'
scene['station_twinkle']='Cyan pulse at source pixel 960,514; local 1–17; peak6'
scene.frame_set(1)
(OUT/'departure-frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'departure-pullout-twinkle.blend'))
if '--preview' in sys.argv:
    for frame in [1,6,17,30,59]:
        scene.frame_set(frame)
        scene.render.filepath=str(OUT/f'preview-{frame:03d}.png')
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
