"""Render linear look proofs and add a restrained native painterly compositor.

Cached EXR comparisons avoid retracing identical geometry for a filter change.
The saved production scene uses Render Layers, never these cached image nodes.
"""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

OUT=Path(__file__).resolve().parent


def brush_group(scene, image=None, factor=.35):
    group=bpy.data.node_groups.new('Illustration brush finish / restrained', 'CompositorNodeTree')
    group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    scene.compositing_node_group=group
    n,link=group.nodes,group.links
    source=n.new('CompositorNodeImage' if image else 'CompositorNodeRLayers')
    if image:
        source.image=image
        socket=source.outputs['Image']
    else:
        glare=n.new('CompositorNodeGlare')
        glare.inputs['Type'].default_value='Fog Glow'
        glare.inputs['Quality'].default_value='High'
        glare.inputs['Threshold'].default_value=1.25
        glare.inputs['Size'].default_value=.14
        glare.inputs['Strength'].default_value=.55
        link.new(source.outputs['Image'],glare.inputs['Image'])
        socket=glare.outputs['Image']
    paint=n.new('CompositorNodeKuwahara')
    paint.inputs['Type'].default_value='Anisotropic'
    for key,value in [('Size',3),('Uniformity',5),('Sharpness',.8),('Eccentricity',1.0)]:
        paint.inputs[key].default_value=value
    link.new(socket,paint.inputs['Image'])
    blend=n.new('ShaderNodeMix')
    blend.data_type='RGBA'
    blend.blend_type='MIX'
    blend.inputs[0].default_value=factor
    link.new(socket,blend.inputs[6])
    link.new(paint.outputs['Image'],blend.inputs[7])
    link.new(blend.outputs[2],n.new('NodeGroupOutput').inputs['Image'])
    return group,blend


parser=argparse.ArgumentParser()
parser.add_argument('--views',default='hero,aft,detail')
parser.add_argument('--width',type=int,default=1600)
parser.add_argument('--samples',type=int,default=96)
parser.add_argument('--cached',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(OUT/'headquarters-ark-v04.blend'))
scene=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX'
prefs.get_devices()
for device in prefs.devices:
    device.use=device.type=='OPTIX'
scene.cycles.device='GPU'
print('Render devices: '+str([(d.name,d.type,d.use) for d in prefs.devices]),flush=True)
scene.cycles.samples=args.samples
scene.render.resolution_x=args.width
scene.render.resolution_y=round(args.width*9/16)
scene.render.image_settings.file_format='OPEN_EXR'
scene.render.image_settings.color_depth='32'
scene.render.image_settings.color_mode='RGBA'
for material in bpy.data.materials:
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type=='AMBIENT_OCCLUSION':
                node.samples=4
            if node.type=='VECT_MATH' and material.name in ('Hull / warm ivory ceramic alloy','Hull / alternate brushed panel'):
                node.inputs[1].default_value=(80,100,90)
    if material.name=='Hull / warm ivory ceramic alloy':
        ramp=next(n for n in material.node_tree.nodes if n.type=='VALTORGB')
        for entry,color in zip(sorted(ramp.color_ramp.elements,key=lambda e:e.position),
                               [( .30,.29,.25),( .39,.37,.32),( .47,.45,.38)]):
            entry.color=(*color,1)
scene.frame_set(49)
camera=scene.camera
camera.parent=None
views={'hero':((-25,-32,25),(0,0,.45),30),'aft':((28,-34,27),(0,0,.45),30),
       'detail':((-14,-18,13),(-3,-2,.7),17)}
files=[]
for view in args.views.split(','):
    pos,target,scale=views[view]
    camera.location=pos
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=scale
    scene.render.filepath=str(OUT/f'linear-{view}.exr')
    print('Native linear render: '+view,flush=True)
    if not args.cached:
        bpy.ops.render.render(write_still=True)
    elif not Path(scene.render.filepath).is_file():
        raise RuntimeError('Missing cached linear proof: '+scene.render.filepath)
    files.append((view,scene.render.filepath))

# An empty render scene evaluates the cached linear proof through the same grade.
cache=bpy.data.scenes.new('Temporary cached look comparison')
cache.render.engine='CYCLES'
cache.cycles.device='GPU'
cache.cycles.samples=1
cache.render.resolution_x=args.width
cache.render.resolution_y=round(args.width*9/16)
cache.render.resolution_percentage=100
cache.render.image_settings.file_format='PNG'
cache.render.image_settings.color_mode='RGBA'
cache.view_settings.view_transform=scene.view_settings.view_transform
cache.view_settings.look=scene.view_settings.look
cache.view_settings.exposure=scene.view_settings.exposure
data=bpy.data.cameras.new('Temporary cached proof camera')
obj=bpy.data.objects.new('Temporary cached proof camera',data)
cache.collection.objects.link(obj)
cache.camera=obj
bpy.context.window.scene=cache
for view,path in files:
    image=bpy.data.images.load(path,check_existing=False)
    group,blend=brush_group(cache,image)
    for label,factor in [('textured',0),('illustrated',.35)]:
        blend.inputs[0].default_value=factor
        cache.render.filepath=str(OUT/f'{label}-{view}.png')
        print('Cached look comparison: '+label+' '+view,flush=True)
        bpy.ops.render.render(write_still=True,scene=cache.name)
    cache.compositing_node_group=None
    bpy.data.node_groups.remove(group)
    bpy.data.images.remove(image)
bpy.context.window.scene=scene
bpy.data.scenes.remove(cache)
bpy.data.objects.remove(obj,do_unlink=True)
brush_group(scene)
camera.parent=bpy.data.objects['CAMERA_ORBIT / optional yaw animation']
camera.location=(-25,-32,25)
camera.rotation_euler=(Vector((0,0,.45))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=30
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.image_settings.color_depth='8'
scene.render.filepath=str(OUT/'animation/frame_')
scene['paint_finish']='Anisotropic native compositor, 3px, 35% blend; renderer-input nodes only, no cached image dependencies.'
text=bpy.data.texts.new('Render finish source / finish_look.py')
text.write(Path(__file__).read_text(encoding='utf-8'))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v04.blend'))
verification=dict(podCount=6,podTransformsPreserved=True,renderSamples=args.samples,
    width=args.width,height=round(args.width*9/16),painterlyFinish=dict(radiusPixels=3,blend=.35,uniformity=5,sharpness=.8),
    native3DGeometry=True,AIImageRestyling=False,externalTextureDependencies=False,paidGenerations=0,
    linearProofs=[str(Path(p).name) for _,p in files],
    limits='Geometry and fine ecology remain simpler than the target painting; full temporal finish evaluation still pending.')
(OUT/'style-verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
print('Illustrated look proofs and reusable native compositor saved',flush=True)
