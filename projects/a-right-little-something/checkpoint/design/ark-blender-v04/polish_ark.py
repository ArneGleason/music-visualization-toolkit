"""Physical recessed galleries and restrained illustrated metal, over V03."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent/'ark-blender-v03'


def load_style():
    spec = importlib.util.spec_from_file_location('ark_style', SOURCE/'style_ark.py')
    style = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(style)
    return style, style.helpers()


def subtract(body, cutter):
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    mod = body.modifiers.new('Recessed gallery aperture', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def galleries(g):
    body = bpy.data.objects['Continuous tapered laboratory spine']
    graphite = bpy.data.materials['Structure / satin graphite']
    cyan = bpy.data.materials['Culture capsule cyan']
    lens = g.mat('Gallery / clear cyan glazing', (.69, .91, 1), rough=.045, transmission=1)
    lens.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value = 1.27
    cyan.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value = 2.8
    for obj in list(bpy.data.objects):
        if obj.name.startswith(('Culture gallery ', 'Culture capsule light ', 'Dorsal gallery ')):
            bpy.data.objects.remove(obj, do_unlink=True)
    for sign in [-1, 1]:
        for k, x in enumerate([-8.5, -4, .5, 5]):
            w, h = g.section(x)
            cutter = g.ellipsoid('TEMP / side gallery opening', (x, sign*(w+.02), .75),
                                  (1.52, .59, .33), None)
            subtract(body, cutter)
            g.ellipsoid('Side gallery / dark recessed lining', (x, sign*(w-.39), .75),
                        (1.47, .07, .28), graphite)
            points = [(x+1.55*math.cos(g.TAU*i/96), sign*(w+.05), .75+.345*math.sin(g.TAU*i/96))
                      for i in range(96)]
            g.tube('Side gallery / deep graphite rim', points, .033, graphite, closed=True)
            g.ellipsoid('Side gallery / transparent lens', (x, sign*(w+.065), .75),
                        (1.47, .035, .30), lens)
            for i in range(6):
                xx = x + (i-2.5)*.41
                g.ellipsoid('Side gallery / culture vessel', (xx, sign*(w-.12), .75),
                            (.054, .08, .22), cyan, segments=20)
                g.box('Side gallery / vessel support', (xx, sign*(w-.16), .48), (.16,.13,.025), graphite, bevel=.005)
                points = [(xx-.065, sign*(w-.07), .52), (xx-.065, sign*(w-.07), .97)]
                g.tube('Side gallery / internal gantry', points, .012, graphite)
    for x in [-6.7, -1.7, 3.2, 7.4]:
        _, h = g.section(x)
        z = .65+h
        subtract(body, g.ellipsoid('TEMP / dorsal gallery opening', (x,0,z+.02), (1.04,.44,.32), None))
        g.ellipsoid('Dorsal gallery / dark recessed lining', (x,0,z-.22), (1.02,.40,.04), graphite)
        points = [(x+1.06*math.cos(g.TAU*i/96), .46*math.sin(g.TAU*i/96), z+.035) for i in range(96)]
        g.tube('Dorsal gallery / thin graphite rim', points, .026, graphite, closed=True)
        g.ellipsoid('Dorsal gallery / transparent lens', (x,0,z+.07), (.99,.40,.025), lens)
        for i in range(3):
            g.ellipsoid('Dorsal gallery / culture vessel', (x+(i-1)*.52,0,z-.09), (.068,.20,.065), cyan, segments=20)


def field(g):
    # A faint field membrane, with real curved filaments anchored to the ring.
    material = bpy.data.materials.new('Aft drive / faint illustrated field membrane')
    material.use_nodes = True
    n, link = material.node_tree.nodes, material.node_tree.links
    n.clear()
    transparent = n.new('ShaderNodeBsdfTransparent')
    emission = n.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (.018,.10,.32,1)
    emission.inputs[1].default_value = .6
    mix = n.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = .09
    link.new(transparent.outputs[0],mix.inputs[1])
    link.new(emission.outputs[0],mix.inputs[2])
    link.new(mix.outputs[0],n.new('ShaderNodeOutputMaterial').inputs['Surface'])
    vertices = [(11.28,0,.85)] + [(11.28,3.0*math.cos(g.TAU*i/128),.85+3.0*math.sin(g.TAU*i/128)) for i in range(128)]
    faces = [(0,i+1,(i+1)%128+1) for i in range(128)]
    obj = g.mesh('Aft field / subtle open membrane',vertices,faces,material)
    obj.visible_shadow = False
    filament = g.mat('Aft field / violet-cyan filaments', (.05,.20,.60), emission=1.4)
    for phase in [-.5,.1,.7]:
        points = []
        for i in range(65):
            t = i/64
            a = -.7 + t*1.2
            radius = 2.73 + .06*math.sin(t*8+phase)
            points.append((11.0+.07*math.sin(t*10),radius*math.cos(a+phase),.85+radius*math.sin(a+phase)))
        g.tube('Aft field / curved energy filament', points, .014, filament)


def refine_sky(g):
    rng = random.Random(708)
    star_material = bpy.data.materials['Illustrated star cores']
    # Instance one small mesh instead of invoking mesh operators hundreds of times.
    template = g.ellipsoid('Star mesh template', (0,0,-15), (.02,.02,.02), star_material, segments=8)
    bpy.ops.object.select_all(action='DESELECT')
    template.select_set(True)
    bpy.context.view_layer.objects.active = template
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    template.hide_render = True
    template.hide_viewport = True
    for i in range(650):
        obj = bpy.data.objects.new('Illustrated fine star '+str(i), template.data)
        bpy.data.collections['ENVIRONMENT / editable star points'].objects.link(obj)
        obj.location = (rng.uniform(-45,45),rng.uniform(-45,45),rng.uniform(-27,-8))
        obj.scale = (rng.uniform(.24,1.1),)*3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default='hero')
    parser.add_argument('--width', type=int, default=1600)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'headquarters-ark-v03.blend'))
    scene = bpy.context.scene
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'
    style, g = load_style()
    before = {o.name:list(o.location) for o in scene.objects if o.name.startswith('POD_')}
    style.painted_material(bpy.data.materials['Hull / warm ivory ceramic alloy'],
        [(.24,.23,.20),(.40,.37,.30),(.51,.47,.37)], metal=.70, rough=.34,scale=(9,15,25),bump=.008)
    style.painted_material(bpy.data.materials['Hull / alternate brushed panel'],
        [(.15,.17,.18),(.26,.27,.245),(.39,.36,.29)], metal=.64,rough=.38,scale=(9,15,25),bump=.012)
    galleries(g)
    print('Physical recessed gallery geometry ready',flush=True)
    field(g)
    refine_sky(g)
    after = {o.name:list(o.location) for o in scene.objects if o.name.startswith('POD_')}
    assert before == after and len(after) == 6
    scene.cycles.samples = 96
    scene.render.resolution_x = args.width
    scene.render.resolution_y = round(args.width*9/16)
    scene.frame_set(49)
    camera = scene.camera
    matrix = camera.matrix_world.copy()
    camera.parent = None
    camera.matrix_world = matrix
    views = {'hero':((-25,-32,25),(0,0,.45),30),'aft':((28,-34,27),(0,0,.45),30),
             'detail':((-14,-18,13),(-3,-2,.7),17)}
    # Save before rendering as well, so the modelling work survives any render fault.
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v04.blend'))
    for view in args.views.split(','):
        pos,target,scale=views[view]
        g.point_camera(camera,pos,target)
        camera.data.ortho_scale=scale
        scene.render.filepath=str(OUT/f'illustrated-{view}.png')
        print('Illustrated polish render: '+view,flush=True)
        bpy.ops.render.render(write_still=True)
    camera.parent=bpy.data.objects['CAMERA_ORBIT / optional yaw animation']
    camera.location=(-25,-32,25)
    camera.rotation_euler=(Vector((0,0,.45))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=30
    scene['style_stage']='V04 illustrated light/material proof, physical gallery recesses, fine habitats, restrained field membrane and bloom'
    scene['style_limit']='Native 3D illustration study; hull and landscape geometry remain simpler than the target painting.'
    text=bpy.data.texts.new('Polish source / polish_ark.py')
    text.write(Path(__file__).read_text(encoding='utf-8'))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v04.blend'))
    (OUT/'style-verification.json').write_text(json.dumps(dict(podCount=6,podTransformsPreserved=before==after,
        styleRoute='Native Blender illustration shaders, illumination and actual recessed galleries',
        renderSamples=96,width=args.width,height=round(args.width*9/16),paidGenerations=0),indent=2),encoding='utf-8')


if __name__=='__main__':
    main()
