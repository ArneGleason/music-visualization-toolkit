"""Editable Blender V64 camera moves, sphere transmission, and portrait fade."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np

OUT = Path(__file__).resolve().parent
OLD = OUT.parent/'first-contact-motion-v02'
FIRST = OUT.parent/'first-contact-motion-v01'
parser = argparse.ArgumentParser()
parser.add_argument('--shot', required=True)
parser.add_argument('--preview', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
entries = json.loads((OUT/'assembly-plan.json').read_text())['entries']
entry = next(e for e in entries if e.get('effect') == args.shot)
count = entry['frames'] + (0 if args.shot == 'finale' else 8)

if args.shot == 'travel':
    bpy.ops.wm.open_mainfile(filepath=str(OLD/'travel.blend'))
elif args.shot == 'finale':
    bpy.ops.wm.open_mainfile(filepath=str(FIRST/'finale-two-videos.blend'))
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 1
    scene.cycles.use_denoising = False
    camera = bpy.data.objects.new('Compositor camera',bpy.data.cameras.new('Compositor camera'))
    scene.collection.objects.link(camera)
    scene.camera = camera
    group = bpy.data.node_groups.new('V64 '+args.shot,'CompositorNodeTree')
    group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    scene.compositing_node_group = group

scene = bpy.context.scene
group = scene.compositing_node_group
nodes, links = group.nodes, group.links
scene.render.threads_mode = 'FIXED'
scene.render.threads = 8
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.frame_start = 1
scene.frame_end = count

def image_sequence(path, label):
    n = nodes.new('CompositorNodeImage')
    n.name = label
    n.image = bpy.data.images.load(str(path))
    if path.suffix == '.exr':
        n.image.colorspace_settings.name = 'Non-Color'
    n.image.source = 'SEQUENCE'
    n.frame_duration = count
    n.frame_start = 1
    n.use_auto_refresh = True
    return n.outputs['Image']

def key(node, name, value, frame):
    node.inputs[name].default_value = value
    node.inputs[name].keyframe_insert(data_path='default_value',frame=frame)

if args.shot == 'travel':
    # The foreground remains untouched. Refraction and transmission affect
    # only the independent warp environment behind its transparent sphere.
    over = next(n for n in nodes if n.bl_idname == 'CompositorNodeAlphaOver')
    bg = over.inputs['Background'].links[0].from_socket
    # Realize the transformed background at the render canvas before UV
    # sampling; Map UV otherwise samples its larger, translated source domain.
    background_folder = OUT/'travel-background-frames'
    background_folder.mkdir(exist_ok=True)
    output = next(n for n in nodes if n.bl_idname == 'NodeGroupOutput')
    links.new(bg, output.inputs['Image'])
    scene.render.filepath = str(background_folder/'frame_')
    bpy.ops.render.render(animation=True)
    links.new(over.outputs['Image'], output.inputs['Image'])
    bg = image_sequence(background_folder/'frame_0001.png','Realized full-frame warp background')
    maps = OUT/'sphere-maps'
    maps.mkdir(exist_ok=True)
    y,x = np.mgrid[0:1080,0:1920].astype(np.float32)
    uv = bpy.data.images.new('Animated local sphere refraction',1920,1080,float_buffer=True)
    tint = bpy.data.images.new('Animated cyan transmission',1920,1080,float_buffer=True)
    for im in [uv,tint]:
        im.colorspace_settings.name = 'Non-Color'
        im.file_format = 'OPEN_EXR'
    for f in range(1,count+1):
        t = (f-1)/(entry['frames']-1)
        s = 1-.025*t
        cx = 960+(840-960)*s+10*t
        cy = 540+(522-540)*s+3*math.sin(t*math.pi)
        radius = 350*s
        r2 = ((x-cx)/radius)**2+((y-cy)/radius)**2
        mask = np.clip((1-r2)/.055,0,1)
        mask = mask*mask*(3-2*mask)
        curve = np.maximum(0,1-r2)**1.15
        pixels = np.ones((1080,1920,4),dtype=np.float32)
        pixels[:,:,0] = (x+.5-(x-cx)*.028*curve)/1920
        pixels[:,:,1] = (y+.5-(y-cy)*.028*curve)/1080
        # Map UV uses the third vector component as sampling opacity.
        pixels[:,:,2] = 1
        uv.pixels.foreach_set(pixels.ravel())
        uv.filepath_raw = str(maps/f'uv_{f:04}.exr')
        uv.save()
        # Slightly stronger attenuation near the curved edge; no opaque disk.
        depth = mask*(.82+.18*np.clip(r2,0,1))
        pixels[:,:,:3] = 1-depth[:,:,None]*np.array([.36,.20,.13],dtype=np.float32)
        tint.pixels.foreach_set(pixels.ravel())
        tint.filepath_raw = str(maps/f'tint_{f:04}.exr')
        tint.save()
    refract = nodes.new('CompositorNodeMapUV')
    refract.name = 'Mild sphere-local refraction, maximum about 4 pixels'
    links.new(bg,refract.inputs['Image'])
    links.new(image_sequence(maps/'uv_0001.exr','Sphere refraction UV sequence'),refract.inputs['UV'])
    transmit = nodes.new('ShaderNodeMix')
    transmit.data_type = 'RGBA'
    transmit.blend_type = 'MULTIPLY'
    transmit.name = 'Dark cyan transparent field transmission'
    transmit.inputs[0].default_value = 1
    links.new(refract.outputs['Image'],transmit.inputs[6])
    links.new(image_sequence(maps/'tint_0001.exr','Sphere-only transmission sequence'),transmit.inputs[7])
    links.new(transmit.outputs[2],over.inputs['Background'])
    over.name = 'Independent ship and Harper over refracted cyan field'
    scene['composite_note'] = 'V64: localized dark cyan transmission and mild radial refraction behind foreground only; no reflected streak synthesis.'
elif args.shot == 'finale':
    blend = next(n for n in nodes if n.bl_idname == 'ShaderNodeMix')
    blend.name = 'Harper fades 3:34 to 3:36, cosmic plate continues'
    for f in range(1,count+1):
        global_frame = 5030+f
        opacity = .80+.06*(f-1)/(count-1)
        opacity *= max(0,min(1,(5185-global_frame)/48))
        key(blend,0,opacity,f)
    scene['production_note'] = 'V64: unchanged independent cosmic/portrait sources; Harper opacity fades global frames 5137 through 5185. Separate title overlay enters from 5185.'
else:
    source = image_sequence(OUT/'sources'/args.shot/'frame_0001.png','Retained native motion source')
    move = nodes.new('CompositorNodeTransform')
    move.name = 'Continuous editorial camera move'
    move.inputs['Interpolation'].default_value = 'Bicubic'
    links.new(source,move.inputs['Image'])
    settings = {
        'contact-027': (1.015,1.13,-4,-55,5,-12),
        'contact-029': (1.025,1.17,-5,22,0,-10),
        'contact-030': (1.045,1.17,30,-65,-6,12),
        'contact-031': (1.025,1.095,-6,18,0,9),
    }
    a,b,x0,x1,y0,y1 = settings[args.shot]
    for f in range(1,count+1):
        t = (f-1)/(entry['frames']-1)
        key(move,'Scale',a+(b-a)*t,f)
        key(move,'X',x0+(x1-x0)*t,f)
        key(move,'Y',y0+(y1-y0)*t,f)
    output = nodes.new('NodeGroupOutput')
    links.new(move.outputs['Image'],output.inputs['Image'])
    scene['source_note'] = 'Retained Kling footage with deterministic Blender move. Frame counts and edit cues remain canonical.'

folder = OUT/(args.shot+'-frames')
folder.mkdir(exist_ok=True)
scene.render.filepath = str(folder/'frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(args.shot+'.blend')))
if args.preview:
    frames = [1,entry['frames']//2,entry['frames']]
    if args.shot == 'finale':
        frames = [106,130,155,210]
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath = str(OUT/f'{args.shot}-preview-{f:03}.png')
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
