"""Native 3D illustration look-development over the fixed V02 ark geometry."""
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
SOURCE = OUT.parent/'ark-blender-v02'
TAU = 2*math.pi


def helpers():
    spec = importlib.util.spec_from_file_location('ark_geometry', SOURCE/'build_ark.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = bpy.data.objects['ARK_ROOT / animate this transform']
    mod.COLLECTION = bpy.data.collections['ARK / editable ship components']
    return mod


def painted_material(material, palette, metal=.5, rough=.45, scale=(3, 18, 35), bump=.025):
    tree = material.node_tree
    tree.nodes.clear()
    n, link = tree.nodes, tree.links
    output = n.new('ShaderNodeOutputMaterial')
    shader = n.new('ShaderNodeBsdfPrincipled')
    shader.inputs['Metallic'].default_value = metal
    shader.inputs['Roughness'].default_value = rough
    shader.inputs['Coat Weight'].default_value = .10
    coord = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = scale
    link.new(coord.outputs['Generated'], mapping.inputs[0])
    brush = n.new('ShaderNodeTexNoise')
    brush.inputs['Scale'].default_value = 2.7
    brush.inputs['Detail'].default_value = 5
    brush.inputs['Roughness'].default_value = .75
    link.new(mapping.outputs[0], brush.inputs['Vector'])
    colors = n.new('ShaderNodeValToRGB')
    colors.color_ramp.elements[0].position = .20
    colors.color_ramp.elements[0].color = (*palette[0], 1)
    colors.color_ramp.elements[1].position = .80
    colors.color_ramp.elements[1].color = (*palette[-1], 1)
    colors.color_ramp.elements.new(.50).color = (*palette[1], 1)
    link.new(brush.outputs['Fac'], colors.inputs[0])
    ao = n.new('ShaderNodeAmbientOcclusion')
    ao.inputs['Distance'].default_value = .32
    ao.inputs['Color'].default_value = (.78, .84, .91, 1)
    mix = n.new('ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = .65
    link.new(colors.outputs['Color'], mix.inputs[1])
    link.new(ao.outputs['Color'], mix.inputs[2])
    link.new(mix.outputs[0], shader.inputs['Base Color'])
    normal = n.new('ShaderNodeBump')
    normal.inputs['Strength'].default_value = .27
    normal.inputs['Distance'].default_value = bump
    link.new(brush.outputs['Fac'], normal.inputs['Height'])
    link.new(normal.outputs['Normal'], shader.inputs['Normal'])
    link.new(shader.outputs[0], output.inputs['Surface'])
    material.diffuse_color = (*palette[1], 1)


def enrich_terrain(g):
    palettes = {
        'Branching groves': [(.025, .035, .022), (.13, .14, .085), (.38, .32, .21)],
        'Fungal wetland': [(.022, .05, .04), (.07, .15, .105), (.26, .32, .17)],
        'Dry spirals': [(.065, .042, .025), (.22, .16, .08), (.49, .38, .21)],
        'Water fronds': [(.025, .065, .064), (.09, .18, .15), (.32, .38, .23)],
        'Membrane marsh': [(.04, .06, .028), (.18, .18, .065), (.37, .30, .12)],
        'Curled plains': [(.05, .025, .032), (.16, .12, .11), (.34, .25, .18)],
    }
    for kind, palette in palettes.items():
        painted_material(bpy.data.materials['Terrain / '+kind], palette,
                         metal=0, rough=.88, scale=(6, 10, 5), bump=.06)
    water = bpy.data.materials['Habitat water / slate teal']
    painted_material(water, [(.018, .045, .055), (.03, .12, .14), (.08, .21, .21)],
                     metal=.3, rough=.25, scale=(25, 35, 6), bump=.012)
    # Keep all old assets in the saved V02; replace the pebble-like colonies here.
    for obj in list(bpy.data.objects):
        if '/ colony ' in obj.name or '/ canopy ' in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)
    flora_materials = {
        'plum': g.mat('Illustration flora / dark plum', (.15, .055, .08), rough=.78),
        'sage': g.mat('Illustration flora / sage', (.08, .16, .09), rough=.8),
        'ochre': g.mat('Illustration flora / dry ochre', (.35, .24, .105), rough=.8),
    }
    # Build small reusable 3D colony meshes, then instance them into each habitat.
    for index, pod in enumerate(sorted([o for o in bpy.data.objects if o.name.startswith('POD_')], key=lambda o:o.name)):
        kind = pod['physical_habitat']
        material = flora_materials['plum' if kind in ('Branching groves', 'Curled plains') else
                                   'ochre' if kind in ('Dry spirals', 'Membrane marsh') else 'sage']
        prototype = []
        if kind in ('Branching groves', 'Water fronds'):
            for branch in range(4):
                a = TAU*branch/4
                points = [(.045*math.sin(t*1.7)*math.cos(a), .045*math.sin(t*1.7)*math.sin(a), .17*t)
                          for t in [j/12 for j in range(13)]]
                obj = g.tube('Colony prototype / stem', points, .008, material, pod)
                prototype.append(obj)
                if kind == 'Water fronds':
                    prototype.append(g.ellipsoid('Colony prototype / frond',
                        (.035*math.cos(a), .035*math.sin(a), .115), (.018, .018, .068), material, pod, segments=12))
        elif kind in ('Fungal wetland', 'Membrane marsh'):
            prototype.append(g.cylinder('Colony prototype / stem', (0, 0, .065), .012, .13, material, pod))
            prototype.append(g.ellipsoid('Colony prototype / cap', (0, 0, .125),
                                        (.06, .052, .020), material, pod, segments=16))
        else:
            points = []
            for j in range(33):
                t = j/32
                points.append((.055*(1-.7*t)*math.cos(t*TAU*1.7),
                               .055*(1-.7*t)*math.sin(t*TAU*1.7), .18*t))
            prototype.append(g.tube('Colony prototype / curl', points, .010, material, pod))
        # Join the prototype once, keeping linked mesh instances light to animate.
        bpy.ops.object.select_all(action='DESELECT')
        for obj in prototype:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = prototype[0]
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.join()
        master = bpy.context.object
        master.name = 'Colony mesh / '+kind
        master.hide_render = True
        master.hide_viewport = True
        rng = random.Random(199+index)
        seed = int(pod['structural_pair']) + (7 if 'STARBOARD' in pod.name else 0)
        for i in range(210):
            x, y = rng.uniform(-2.55, 2.55), rng.uniform(-2.55, 2.55)
            if math.hypot(x, y) > 2.53:
                continue
            z = g.land_height(x, y, seed)
            if z < .765 and kind != 'Water fronds':
                continue
            obj = bpy.data.objects.new(f'{kind} / fine colony {i}', master.data)
            g.COLLECTION.objects.link(obj)
            obj.parent = pod
            obj.location = (x, y, z)
            obj.rotation_euler.z = rng.uniform(0, TAU)
            s = rng.uniform(.45, 1.0)
            obj.scale = (s, s, s*rng.uniform(.7, 1.25))
        if kind == 'Dry spirals':
            for obj in pod.children:
                if 'basin water' in obj.name:
                    obj.hide_render = True
        # A small amount of atmosphere adds depth without hiding the landscape.
        atmosphere = bpy.data.materials.new('Habitat air / '+kind)
        atmosphere.use_nodes = True
        tree = atmosphere.node_tree
        tree.nodes.clear()
        volume = tree.nodes.new('ShaderNodeVolumePrincipled')
        volume.inputs['Color'].default_value = (.52, .63, .68, 1)
        volume.inputs['Density'].default_value = .025 if kind == 'Fungal wetland' else .012
        volume.inputs['Anisotropy'].default_value = .25
        output = tree.nodes.new('ShaderNodeOutputMaterial')
        tree.links.new(volume.outputs['Volume'], output.inputs['Volume'])
        g.cylinder('Habitat atmosphere / '+kind, (0, 0, 1.22), 2.52, 1.02, atmosphere, pod)
        light = next(o for o in pod.children if o.type == 'LIGHT')
        light.data.energy = 105 if kind == 'Dry spirals' else 92
        light.data.color = (1, .91, .74) if kind == 'Dry spirals' else (.76, .87, .88)


def surface_detail(g):
    ivory = bpy.data.materials['Hull / warm ivory ceramic alloy']
    graphite = bpy.data.materials['Structure / satin graphite']
    painted_material(ivory, [(.12, .11, .09), (.40, .34, .245), (.68, .59, .40)],
                     metal=.64, rough=.36, bump=.018)
    painted_material(graphite, [(.012, .018, .025), (.032, .043, .055), (.085, .09, .095)],
                     metal=.68, rough=.44, scale=(6, 25, 18), bump=.02)
    panel_mat = g.mat('Hull / alternate brushed panel', (.32, .285, .22), .63, .40)
    painted_material(panel_mat, [(.10, .09, .075), (.29, .255, .19), (.51, .44, .31)], bump=.025)
    brass = g.mat('Detail / low-gloss brass fasteners', (.24, .17, .08), .65, .42)
    # Thin fitted armour panels over the original barrel keep its exact silhouette.
    for side in [1, -1]:
        for row, x in enumerate([-9.6, -6.5, -3.4, -.3, 2.8, 5.9, 8.3]):
            vertices, faces = [], []
            for i in range(7):
                xx = x-1.2 + 2.4*i/6
                w, h = g.section(xx)
                for j in range(5):
                    a = .50 + .52*j/4
                    if side == -1:
                        a = math.pi-a
                    vertices.append((xx, (w+.024)*math.cos(a), .65+(h+.024)*math.sin(a)))
            for i in range(6):
                for j in range(4):
                    a = i*5+j
                    face = (a, a+1, a+6, a+5)
                    faces.append(face if side == 1 else tuple(reversed(face)))
            obj = g.mesh(f'Fitted hull armour / {side}:{row}', vertices, faces,
                         panel_mat if row%3 == 1 else ivory)
            solid = obj.modifiers.new('Plate thickness', 'SOLIDIFY')
            solid.thickness = .022
            for xx in [x-1.05, x+1.05]:
                w, h = g.section(xx)
                g.ellipsoid('Small hull fastener', (xx, side*w*.79, .65+h*.63+.035),
                            (.029, .025, .021), brass, segments=12)
    amber = bpy.data.materials['Amber trim / restrained bloom']
    for pod in [o for o in bpy.data.objects if o.name.startswith('POD_')]:
        for i in range(40):
            a = TAU*i/40
            obj = g.box('Pod rim layered plate', (2.745*math.cos(a), 2.745*math.sin(a), .19),
                        (.24, .045, .11), panel_mat if i%4 == 0 else graphite, pod, bevel=.008)
            obj.rotation_euler.z = a+math.pi/2
            g.ellipsoid('Pod rim fine fastener', (2.84*math.cos(a), 2.84*math.sin(a), .41),
                        (.018, .018, .012), brass, pod, segments=8)
    glass = bpy.data.materials['Biosphere / optically clear glass'].node_tree.nodes.get('Principled BSDF')
    glass.inputs['Roughness'].default_value = .065
    glass.inputs['IOR'].default_value = 1.27
    gallery = bpy.data.materials['Culture gallery / blue glass'].node_tree.nodes.get('Principled BSDF')
    gallery.inputs['Base Color'].default_value = (.018, .08, .10, 1)
    gallery.inputs['Emission Strength'].default_value = .12
    gallery.inputs['Metallic'].default_value = .5
    gallery.inputs['Roughness'].default_value = .20
    # Existing capsule lights become narrow bright culture silhouettes behind glass.
    for obj in bpy.data.objects:
        if obj.name.startswith('Culture capsule light'):
            obj.scale.x *= .50
            obj.scale.z *= 1.05
    for mat_name, strength in [('Amber trim / restrained bloom', 6), ('Cyan field and nav lights', 8)]:
        bpy.data.materials[mat_name].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value = strength


def space_backdrop(g):
    material = bpy.data.materials.new('Painted deep-space cloud strata / procedural')
    material.use_nodes = True
    n, link = material.node_tree.nodes, material.node_tree.links
    n.clear()
    tex = n.new('ShaderNodeTexCoord')
    cloud = n.new('ShaderNodeTexNoise')
    cloud.inputs['Scale'].default_value = .044
    cloud.inputs['Detail'].default_value = 6
    cloud.inputs['Roughness'].default_value = .78
    cloud.inputs['Distortion'].default_value = .8
    link.new(tex.outputs['Object'], cloud.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = .39
    ramp.color_ramp.elements[0].color = (.001, .002, .008, 1)
    ramp.color_ramp.elements[1].position = .76
    ramp.color_ramp.elements[1].color = (.025, .14, .23, 1)
    ramp.color_ramp.elements.new(.53).color = (.008, .009, .035, 1)
    ramp.color_ramp.elements.new(.64).color = (.035, .025, .08, 1)
    link.new(cloud.outputs['Fac'], ramp.inputs[0])
    emission = n.new('ShaderNodeEmission')
    emission.inputs['Strength'].default_value = .8
    link.new(ramp.outputs['Color'], emission.inputs[0])
    link.new(emission.outputs[0], n.new('ShaderNodeOutputMaterial').inputs['Surface'])
    g.COLLECTION = bpy.data.collections['ENVIRONMENT / editable star points']
    plane = g.mesh('Deep-space painted cloud backdrop', [(-180,-180,-34), (180,-180,-34),
                   (180,180,-34), (-180,180,-34)], [(0,1,2,3)], material)
    plane.parent = None
    plane.visible_shadow = False
    plane.visible_diffuse = False
    # Dense small 3D stars at different depths provide real camera parallax.
    rng = random.Random(603)
    star_mat = g.mat('Illustrated star cores', (.42, .65, 1), emission=5)
    for i in range(550):
        loc = (rng.uniform(-90, 90), rng.uniform(-90, 90), rng.uniform(-28, -7))
        size = rng.uniform(.008, .028) if i%35 else .065
        star = g.ellipsoid('Fine 3D star '+str(i), loc, (size, size, size), star_mat, segments=8)
        star.parent = None
    g.COLLECTION = bpy.data.collections['ARK / editable ship components']


def lighting(scene):
    settings = {
        'Large warm key': (23000, (1, .78, .48), 7),
        'Cool upper fill': (2800, (.28, .50, 1), 10),
        'Warm aft rim': (12000, (1, .41, .12), 6),
        'Canopy contour strip': (2400, (.63, .79, 1), 14),
    }
    for name, (energy, color, size) in settings.items():
        light = bpy.data.objects[name]
        light.data.energy, light.data.color, light.data.size = energy, color, size
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .10
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium High Contrast'
    except TypeError:
        pass
    scene.view_settings.exposure = .25
    group = scene.compositing_node_group
    n, link = group.nodes, group.links
    n.clear()
    group.name = 'Graphic illustration / restrained bloom and contrast'
    render = n.new('CompositorNodeRLayers')
    glow = n.new('CompositorNodeGlare')
    glow.inputs['Type'].default_value = 'Fog Glow'
    glow.inputs['Quality'].default_value = 'High'
    glow.inputs['Threshold'].default_value = 1.25
    glow.inputs['Size'].default_value = .14
    glow.inputs['Strength'].default_value = .55
    link.new(render.outputs['Image'], glow.inputs['Image'])
    link.new(glow.outputs['Image'], n.new('NodeGroupOutput').inputs['Image'])
    scene.cycles.samples = 96
    scene.cycles.use_denoising = True
    scene.cycles.transparent_max_bounces = 24
    scene.cycles.volume_bounces = 2
    scene.cycles.max_bounces = 12
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default='hero')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'headquarters-ark-v02.blend'))
    scene = bpy.context.scene
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'
    scene.name = 'Headquarters ark / illustrated cinematic material study v03'
    g = helpers()
    before = {o.name: list(o.location) for o in scene.objects if o.name.startswith('POD_')}
    surface_detail(g)
    print('Style stage: surface details ready', flush=True)
    enrich_terrain(g)
    print('Style stage: habitat refinement ready', flush=True)
    space_backdrop(g)
    print('Style stage: backdrop ready', flush=True)
    lighting(scene)
    after = {o.name: list(o.location) for o in scene.objects if o.name.startswith('POD_')}
    assert before == after and len(after) == 6
    scene.frame_set(49)
    # Clear the camera parent solely for exact reference-angle comparison stills.
    camera = scene.camera
    matrix = camera.matrix_world.copy()
    camera.parent = None
    camera.matrix_world = matrix
    views = {'hero': ((-25,-32,25), (0,0,.45), 30),
             'aft': ((28,-34,27), (0,0,.45), 30),
             'detail': ((-14,-18,13), (-3,-2,.7), 17)}
    for view in args.views.split(','):
        pos, target, scale = views[view]
        g.point_camera(camera, pos, target)
        camera.data.ortho_scale = scale
        scene.render.filepath = str(OUT/f'illustrated-{view}.png')
        print('Style render: '+view, flush=True)
        bpy.ops.render.render(write_still=True)
    # Restore the V02 camera orbit for a repeatable motion comparison.
    camera.parent = bpy.data.objects['CAMERA_ORBIT / optional yaw animation']
    camera.location = (-25,-32,25)
    camera.rotation_euler = (Vector((0,0,.45))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale = 30
    scene['style_stage'] = 'V03 warm/cool illustrated lighting, stable brush textures, detailed rim plates and fine ecology; native Blender render.'
    scene['style_limit'] = 'Look-development draft; geometry still simpler than the approved illustration.'
    bpy.data.objects['ARK_ROOT / animate this transform']['design_stage'] = scene['style_stage']
    text = bpy.data.texts.new('Style source / style_ark.py')
    text.write(Path(__file__).read_text(encoding='utf-8'))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v03.blend'))
    (OUT/'style-verification.json').write_text(json.dumps(dict(podCount=6, podTransformsPreserved=before==after,
        styleRoute='Native Blender shaders, geometry, illumination and compositor; no AI image restyling',
        renderSamples=96, width=1600, height=900, paidGenerations=0,
        geometryLimits='V02 proportions retained; plate details and fine habitats added'), indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
