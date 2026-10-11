"""Editable headquarters ark. Run with Blender --background --python this_file.

No projected ship artwork: all visible vessel surfaces are actual 3D geometry.
The approved illustration is an artistic proportion guide, not a measured plan.
"""
import argparse
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector, noise


OUT = Path(__file__).resolve().parent
TAU = 2 * math.pi
ROOT = None
COLLECTION = None
CONFIG = {
    'pod_radius': 2.8, 'dome_height': 1.9, 'pod_base_z': .38,
    'pairs': [(-6.0, 4.7), (0.0, 7.2), (6.0, 4.7)],
    'ring_x': 11.2, 'ring_radius': 3.25, 'ring_z': .85,
    'design_units': 'Arbitrary; do not infer a physical size from the illustration.',
    'reference': '../../storyboard/ark-replacement-v01/lab2-06.png',
}


def collection(name, parent=None):
    item = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(item)
    return item


def own(obj, name, mat=None, parent=None):
    obj.name = name
    for owner in list(obj.users_collection):
        owner.objects.unlink(obj)
    COLLECTION.objects.link(obj)
    obj.parent = ROOT if parent is None else parent
    if mat is not None:
        obj.data.materials.append(mat)
    if obj.type == 'MESH':
        for face in obj.data.polygons:
            face.use_smooth = True
    return obj


def empty(name, location=(0, 0, 0), parent=None):
    obj = bpy.data.objects.new(name, None)
    COLLECTION.objects.link(obj)
    obj.parent = parent
    obj.location = location
    return obj


def mat(name, color, metal=0, rough=.4, emission=0, transmission=0):
    item = bpy.data.materials.new(name)
    item.use_nodes = True
    shader = item.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Metallic'].default_value = metal
    shader.inputs['Roughness'].default_value = rough
    shader.inputs['Emission Color'].default_value = (*color, 1)
    shader.inputs['Emission Strength'].default_value = emission
    shader.inputs['Transmission Weight'].default_value = transmission
    shader.inputs['IOR'].default_value = 1.34
    return item


def surface_noise(item, colors, scale=4, bump=.025):
    tree = item.node_tree
    shader = tree.nodes.get('Principled BSDF')
    tex = tree.nodes.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = scale
    tex.inputs['Detail'].default_value = 4
    ramp = tree.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*colors[0], 1)
    ramp.color_ramp.elements[1].color = (*colors[-1], 1)
    if len(colors) > 2:
        ramp.color_ramp.elements.new(.5).color = (*colors[1], 1)
    tree.links.new(tex.outputs['Fac'], ramp.inputs[0])
    tree.links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
    if bump:
        node = tree.nodes.new('ShaderNodeBump')
        node.inputs['Strength'].default_value = .3
        node.inputs['Distance'].default_value = bump
        tree.links.new(tex.outputs['Fac'], node.inputs['Height'])
        tree.links.new(node.outputs['Normal'], shader.inputs['Normal'])


def mesh(name, vertices, faces, material, parent=None):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    COLLECTION.objects.link(obj)
    obj.parent = ROOT if parent is None else parent
    if material:
        data.materials.append(material)
    for face in data.polygons:
        face.use_smooth = True
    return obj


def ellipsoid(name, center, size, material, parent=None, segments=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=24, location=center)
    obj = own(bpy.context.object, name, material, parent)
    obj.scale = size
    return obj


def tube(name, points, radius, material, parent=None, closed=False):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 1
    data.bevel_depth = radius
    data.bevel_resolution = 3
    path = data.splines.new('POLY')
    path.points.add(len(points) - 1)
    for point, co in zip(path.points, points):
        point.co = (*co, 1)
    path.use_cyclic_u = closed
    obj = bpy.data.objects.new(name, data)
    COLLECTION.objects.link(obj)
    obj.parent = ROOT if parent is None else parent
    data.materials.append(material)
    return obj


def cylinder(name, center, radius, depth, material, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=radius, depth=depth, location=center)
    obj = own(bpy.context.object, name, material, parent)
    bevel = obj.modifiers.new('Soft machined edge', 'BEVEL')
    bevel.width = min(.08, depth * .22)
    bevel.segments = 3
    obj.modifiers.new('Weighted surface normals', 'WEIGHTED_NORMAL')
    return obj


def torus(name, center, radius, thickness, material, parent=None, vertical=False):
    bpy.ops.mesh.primitive_torus_add(major_segments=96, minor_segments=16,
                                   major_radius=radius, minor_radius=thickness,
                                   location=center)
    obj = own(bpy.context.object, name, material, parent)
    if vertical:
        obj.rotation_euler.y = math.pi / 2
    return obj


def box(name, center, size, material, parent=None, bevel=.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = own(bpy.context.object, name, material, parent)
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new('Rounded panel edges', 'BEVEL')
    mod.width = bevel
    mod.segments = 3
    obj.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return obj


def bezier(a, b, c, d, t):
    return (1-t)**3*Vector(a) + 3*(1-t)**2*t*Vector(b) + 3*(1-t)*t*t*Vector(c) + t**3*Vector(d)


def swept_arm(name, controls, material):
    points = [bezier(*controls, i/40) for i in range(41)]
    vertices, faces = [], []
    # A rounded flattened structural ribbon, rather than an industrial pipe.
    for i, p in enumerate(points):
        tangent = points[min(i+1, 40)] - points[max(i-1, 0)]
        side = Vector((-tangent.y, tangent.x, 0)).normalized()
        width = .53 + .10*math.sin(math.pi*i/40)
        for j in range(12):
            angle = TAU*j/12
            vertices.append(p + side*(width*math.cos(angle)) + Vector((0, 0, .16*math.sin(angle))))
    for i in range(40):
        for j in range(12):
            a = i*12+j
            faces.append((a, i*12+(j+1)%12, (i+1)*12+(j+1)%12, a+12))
    faces.extend([tuple(reversed(range(12))), tuple(range(40*12, 41*12))])
    obj = mesh(name, vertices, faces, material)
    tube(name+' / recessed centre seam', [p+Vector((0, 0, .166)) for p in points], .024, M['graphite'])
    tube(name+' / amber edge', [p+Vector((0, 0, .17)) for p in points[7:35]], .014, M['amber'])
    return obj


SECTIONS = [(-12, .07, .10), (-11, .72, .40), (-9, 1.05, .57),
            (-5, 1.20, .66), (0, 1.28, .69), (5, 1.12, .61),
            (8.5, .88, .52), (10.5, .70, .45)]


def section(x):
    for a, b in zip(SECTIONS, SECTIONS[1:]):
        if a[0] <= x <= b[0]:
            t = (x-a[0])/(b[0]-a[0])
            t = t*t*(3-2*t)
            return a[1]*(1-t)+b[1]*t, a[2]*(1-t)+b[2]*t
    return SECTIONS[-1][1:]


def hull():
    vertices, faces = [], []
    count, sides = 121, 64
    for i in range(count):
        x = -12 + 22.5*i/(count-1)
        width, height = section(x)
        for j in range(sides):
            a = TAU*j/sides
            vertices.append((x, width*math.cos(a), .65+height*math.sin(a)))
    for i in range(count-1):
        for j in range(sides):
            a = i*sides+j
            faces.append((a, i*sides+(j+1)%sides, (i+1)*sides+(j+1)%sides, a+sides))
    faces.extend([tuple(reversed(range(sides))), tuple(range((count-1)*sides, count*sides))])
    obj = mesh('Continuous tapered laboratory spine', vertices, faces, M['ivory'])
    obj.data.materials.append(M['graphite'])
    for face in obj.data.polygons:
        if face.center.z < .3:
            face.material_index = 1
    for x in [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]:
        w, h = section(x)
        points = [(x, (w+.012)*math.cos(TAU*j/64), .65+(h+.012)*math.sin(TAU*j/64)) for j in range(64)]
        tube(f'Spine transverse panel seam {x:+}', points, .012, M['seam'], closed=True)
    for sign in [-1, 1]:
        points = []
        for i in range(101):
            x = -11.5 + 21.5*i/100
            w, h = section(x)
            points.append((x, sign*(w+.023), .69))
        tube(f'Spine amber running edge {sign}', points, .017, M['amber'])
        for k, x in enumerate([-8.5, -4, .5, 5]):
            w, _ = section(x)
            center = (x, sign*(w+.05), .75)
            ellipsoid(f'Culture gallery {sign}:{k} / graphite gasket', center, (1.7, .15, .40), M['graphite'])
            ellipsoid(f'Culture gallery {sign}:{k} / cyan glazing',
                      (x, sign*(w+.145), .75), (1.50, .09, .28), M['gallery'])
            for j in range(5):
                xx = x + (j-2)*.45
                ellipsoid(f'Culture capsule light {sign}:{k}:{j}',
                          (xx, sign*(w+.22), .75), (.065, .025, .18), M['cyan_dim'], segments=16)
    for i, x in enumerate([-6.7, -1.7, 3.2, 7.4]):
        _, h = section(x)
        ellipsoid(f'Dorsal gallery {i} / frame', (x, 0, .65+h), (1.1, .52, .14), M['graphite'])
        ellipsoid(f'Dorsal gallery {i} / glass', (x, 0, .71+h), (.98, .40, .13), M['gallery'])


def land_height(x, y, seed):
    n = noise.fractal(Vector((x*.85+seed*13.1, y*.85-seed*7.7, seed*.8)), 1.0, 2.0, 4)
    ridges = abs(noise.noise(Vector((x*1.1+seed, y*1.1, seed*2.0))))
    edge = max(0, 1-(math.hypot(x, y)/2.72)**6)
    channel = math.exp(-((y-.45*math.sin(x*1.5+seed))/.32)**2)
    mountain = math.exp(-((y-1.3)/.48)**2) * (.35+.65*ridges)
    return .79 + edge*(.16*n + .19*ridges + .66*mountain - .23*channel)


def habitat(parent, seed, kind):
    vertices = [(0, 0, land_height(0, 0, seed))]
    segments, rings = 96, 26
    for row in range(1, rings+1):
        radius = 2.70*row/rings
        for j in range(segments):
            a = TAU*j/segments
            x, y = radius*math.cos(a), radius*math.sin(a)
            vertices.append((x, y, land_height(x, y, seed)))
    faces = [(0, 1+j, 1+(j+1)%segments) for j in range(segments)]
    for row in range(rings-1):
        for j in range(segments):
            a = 1+row*segments+j
            faces.append((a, 1+row*segments+(j+1)%segments,
                          1+(row+1)*segments+(j+1)%segments, a+segments))
    mesh(kind+' / terrain', vertices, faces, HABITATS[kind], parent)
    cylinder(kind+' / basin water', (0, 0, .754), 2.68, .016, M['water'], parent)
    rng = random.Random(seed)
    for i in range(64):
        x, y = rng.uniform(-2.35, 2.35), rng.uniform(-2.35, 2.35)
        if math.hypot(x, y) > 2.4:
            continue
        z = land_height(x, y, seed)
        if z < .77:
            continue
        size = rng.uniform(.03, .065)
        height = rng.uniform(.07, .16)
        # Small colonies communicate terrain scale. Fully volumetric placeholders.
        if kind == 'Dry spirals':
            points = []
            for j in range(17):
                t = j/16
                points.append((x+size*(1-t)*math.cos(t*TAU*1.6),
                               y+size*(1-t)*math.sin(t*TAU*1.6), z+t*height))
            tube(f'{kind} / colony {i}', points, .010, M['flora_ochre'], parent)
        else:
            flora = M['flora_plum'] if kind in ('Branching groves', 'Curled plains') else M['flora_sage']
            ellipsoid(f'{kind} / colony {i}', (x, y, z+height/2),
                      (size, size*.8, height/2), flora, parent, segments=12)
            if kind in ('Fungal wetland', 'Membrane marsh'):
                ellipsoid(f'{kind} / canopy {i}', (x, y, z+height),
                          (size*1.5, size*1.5, .018), flora, parent, segments=12)


def dome(parent):
    vertices, faces = [], []
    segments, rows = 96, 32
    for row in range(rows+1):
        a = .001 + (math.pi/2-.001)*row/rows
        for j in range(segments):
            b = TAU*j/segments
            vertices.append((2.8*math.sin(a)*math.cos(b), 2.8*math.sin(a)*math.sin(b),
                             .66+CONFIG['dome_height']*math.cos(a)))
    for row in range(rows):
        for j in range(segments):
            a = row*segments+j
            faces.append((a+segments, (row+1)*segments+(j+1)%segments,
                          row*segments+(j+1)%segments, a))
    obj = mesh('Biosphere canopy / real transmissive shell', vertices, faces, M['glass'], parent)
    solid = obj.modifiers.new('Glass shell thickness', 'SOLIDIFY')
    solid.thickness = .018
    # Fine structural meridians: a quiet futuristic canopy, not a cage.
    for j in range(8):
        b = TAU*j/8
        points = []
        for k in range(33):
            a = math.pi/2*k/32
            points.append((2.805*math.sin(a)*math.cos(b), 2.805*math.sin(a)*math.sin(b),
                           .667+CONFIG['dome_height']*math.cos(a)))
        tube(f'Canopy meridian {j}', points, .005, M['canopy_rib'], parent)


def pods():
    kinds = {1: ['Branching groves', 'Fungal wetland', 'Dry spirals'],
             -1: ['Water fronds', 'Membrane marsh', 'Curled plains']}
    for sign, side in [(1, 'PORT'), (-1, 'STARBOARD')]:
        for row, (x, y) in enumerate(CONFIG['pairs']):
            kind = kinds[sign][row]
            pod = empty(f'POD_{side}_{row+1} / {kind}', (x, sign*y, 0), ROOT)
            pod['physical_habitat'] = kind
            pod['structural_pair'] = row+1
            pod['fixed_base_level'] = CONFIG['pod_base_z']
            cylinder('Pod lower base', (0, 0, .22), 2.72, .32, M['graphite'], pod)
            cylinder('Pod ivory structural flange', (0, 0, .40), 2.86, .17, M['ivory'], pod)
            torus('Pod graphite outer shoulder', (0, 0, .49), 2.78, .11, M['graphite'], pod)
            torus('Pod amber habitat rim', (0, 0, .595), 2.80, .021, M['amber'], pod)
            torus('Pod top ivory canopy seat', (0, 0, .625), 2.77, .045, M['ivory'], pod)
            for j in range(24):
                a = TAU*j/24
                obj = box(f'Rim inset {j}', (2.78*math.cos(a), 2.78*math.sin(a), .29),
                          (.19, .075, .08), M['cyan'] if j%6 == 0 else M['seam'], pod, .012)
                obj.rotation_euler.z = a+math.pi/2
            dome(pod)
            habitat(pod, row+1+(0 if sign == 1 else 7), kind)
            data = bpy.data.lights.new('Habitat service sun / '+kind, 'AREA')
            sun = bpy.data.objects.new('Habitat service sun / '+kind, data)
            COLLECTION.objects.link(sun)
            sun.parent = pod
            sun.location = (0, 0, 2.10)
            data.energy = 72
            data.color = (.75, .85, .82)
            data.shape = 'RECTANGLE'
            data.size = 2
            data.size_y = 2
            sun.visible_glossy = False
            sun.visible_transmission = False
            for branch in [-1, 1]:
                controls = [(x+branch*1.9, sign*1.05, .44),
                            (x+branch*2.0, sign*2.9, .43),
                            (x+branch*1.8, sign*(y-2.0), .39),
                            (x+branch*.7, sign*(y-1.7), .40)]
                swept_arm(f'Curved support {side} pair {row+1} branch {branch}', controls, M['ivory'])


def drive():
    center = (CONFIG['ring_x'], 0, CONFIG['ring_z'])
    radius = CONFIG['ring_radius']
    torus('Aft drive / graphite core', center, radius, .24, M['graphite'], vertical=True)
    torus('Aft drive / ivory outer jacket', (center[0]+.04, 0, center[2]),
          radius+.05, .14, M['ivory'], vertical=True)
    torus('Aft drive / continuous cyan inner field', (center[0]-.18, 0, center[2]),
          radius-.19, .038, M['cyan'], vertical=True)
    torus('Aft drive / amber outer trim', (center[0]-.12, 0, center[2]),
          radius+.21, .021, M['amber'], vertical=True)
    for i in range(16):
        a = TAU*i/16
        obj = box(f'Aft ring baffle {i}', (center[0]-.03, radius*math.cos(a), center[2]+radius*math.sin(a)),
                  (.40, .16, .10), M['graphite'], bevel=.028)
        obj.rotation_euler.x = a
    # No rocket bells or exhaust. The open ring remains visible from all angles.
    for sign in [-1, 1]:
        controls = [(9.2, sign*.6, .52), (10.4, sign*1.3, .1),
                    (11.0, sign*2.3, -.55), (11.2, sign*2.65, -.9)]
        swept_arm(f'Aft field-ring pylon {sign}', controls, M['graphite'])


def point_camera(camera, location, target=(0, 0, .45)):
    camera.location = location
    camera.rotation_euler = (Vector(target)-camera.location).to_track_quat('-Z', 'Y').to_euler()


def area(name, location, power, color, size):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = own(bpy.context.object, name)
    light.parent = None
    light.data.energy = power
    light.data.color = color
    light.data.shape = 'DISK'
    light.data.size = size
    light.visible_glossy = False
    light.visible_transmission = False
    light.data.specular_factor = .10
    light.rotation_euler = (-light.location).to_track_quat('-Z', 'Y').to_euler()


def starfield():
    global COLLECTION
    COLLECTION = collection('ENVIRONMENT / editable star points')
    rng = random.Random(844)
    for i in range(180):
        direction = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-.3, 1))).normalized()
        location = direction*rng.uniform(75, 110)
        star = ellipsoid(f'Distant star {i}', location, (1, 1, 1), M['star'], segments=8)
        star.scale = (rng.uniform(.01, .035),)*3
        star.parent = None


def setup():
    global ROOT, COLLECTION, M, HABITATS
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = 'Headquarters ark / geometry and materials refinement v02'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 10
    scene.cycles.transmission_bounces = 8
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Deep indigo studio space')
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (.025, .038, .068, 1)
    bg.inputs[1].default_value = .32
    M = {
        'ivory': mat('Hull / warm ivory ceramic alloy', (.49, .46, .39), .67, .30),
        'graphite': mat('Structure / satin graphite', (.035, .045, .06), .78, .31),
        'seam': mat('Recessed panel joins', (.018, .022, .030), .45, .40),
        'amber': mat('Amber trim / restrained bloom', (1, .29, .055), .25, .24, 4),
        'cyan': mat('Cyan field and nav lights', (.015, .62, 1), .1, .19, 5),
        'cyan_dim': mat('Culture capsule cyan', (.04, .54, .67), .18, .26, .7),
        'gallery': mat('Culture gallery / blue glass', (.026, .18, .24), .25, .18, .35, .25),
        'glass': mat('Biosphere / optically clear glass', (.985, .995, 1), .0, .075, 0, 1),
        'canopy_rib': mat('Fine canopy meridians', (.32, .40, .43), .65, .28),
        'water': mat('Habitat water / slate teal', (.03, .16, .19), .35, .20),
        'flora_sage': mat('Tiny alien colonies / muted sage', (.19, .25, .12), 0, .75),
        'flora_plum': mat('Tiny alien colonies / muted plum', (.24, .105, .16), 0, .7),
        'flora_ochre': mat('Tiny dry spiral colonies', (.45, .34, .20), 0, .70),
        'star': mat('Distant star points', (.55, .70, 1), 0, .5, 3),
        'clay': mat('Geometry review clay', (.45, .49, .54), .05, .67),
    }
    surface_noise(M['ivory'], [(.43, .40, .34), (.62, .58, .49)], scale=150, bump=.006)
    palettes = {
        'Branching groves': [(.04, .05, .035), (.13, .13, .085), (.25, .23, .17)],
        'Fungal wetland': [(.025, .055, .04), (.07, .12, .07), (.19, .23, .12)],
        'Dry spirals': [(.09, .055, .035), (.22, .16, .09), (.40, .32, .18)],
        'Water fronds': [(.025, .05, .055), (.065, .12, .095), (.23, .27, .17)],
        'Membrane marsh': [(.05, .055, .025), (.14, .15, .06), (.28, .25, .10)],
        'Curled plains': [(.05, .025, .035), (.14, .09, .085), (.28, .21, .16)],
    }
    HABITATS = {}
    for kind, colors in palettes.items():
        HABITATS[kind] = mat('Terrain / '+kind, colors[1], rough=.84)
        surface_noise(HABITATS[kind], colors, 7, .045)
    COLLECTION = collection('ARK / editable ship components')
    ROOT = empty('ARK_ROOT / animate this transform')
    ROOT.empty_display_type = 'PLAIN_AXES'
    ROOT.empty_display_size = 3
    ROOT['design_stage'] = 'V02 editable geometry with refined terrain, glass and material proof; not final illustration match'
    ROOT['forward_axis'] = '-X; port +Y; common habitat bases Z=.38'
    ROOT['reference_image'] = str((OUT/CONFIG['reference']).resolve())
    hull()
    pods()
    drive()
    COLLECTION = collection('REVIEW / cameras and illumination')
    area('Large warm key', (-10, -9, 18), 15000, (1, .83, .62), 15)
    area('Cool upper fill', (4, 12, 16), 11000, (.38, .66, 1), 12)
    area('Warm aft rim', (15, -3, 5), 5500, (1, .48, .18), 9)
    # One narrow softbox gives a restrained continuous glass highlight.
    area('Canopy contour strip', (0, -3, 18), 1200, (.65, .8, 1), 14)
    strip = bpy.context.object
    strip.visible_glossy = True
    strip.data.shape = 'RECTANGLE'
    strip.data.size_y = .28
    bpy.ops.object.camera_add()
    camera = own(bpy.context.object, 'CAMERA / approved forward-quarter proof')
    camera.parent = None
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 30
    camera.data.clip_end = 250
    scene.camera = camera
    point_camera(camera, (-25, -32, 25))
    starfield()
    group = bpy.data.node_groups.new('Restrained illustrated trim bloom', 'CompositorNodeTree')
    group.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    scene.compositing_node_group = group
    render = group.nodes.new('CompositorNodeRLayers')
    glow = group.nodes.new('CompositorNodeGlare')
    glow.inputs['Type'].default_value = 'Fog Glow'
    glow.inputs['Quality'].default_value = 'High'
    glow.inputs['Threshold'].default_value = 2
    glow.inputs['Size'].default_value = .12
    glow.inputs['Strength'].default_value = .25
    group.links.new(render.outputs['Image'], glow.inputs['Image'])
    group.links.new(glow.outputs['Image'], group.nodes.new('NodeGroupOutput').inputs['Image'])
    scene['geometry_contract'] = 'Six fixed pods, three mirrored pairs; middle pair outboard; one aft vertical ring. No AI view reinterpretation.'
    scene['reference_limit'] = 'An authored reconstruction from one illustrated camera; unseen surfaces are design decisions.'
    scene.frame_start = 1
    scene.frame_end = 120
    return scene, camera


VIEWS = {
    '01-forward-quarter': ((-25, -32, 25), 30),
    '02-aft-quarter': ((28, -34, 27), 30),
    '03-top-plan': ((0, 0, 50), 37),
    '04-side-profile': ((-8, -42, 12), 29),
}


def validate(scene):
    pods = [obj for obj in scene.objects if obj.name.startswith('POD_')]
    assert len(pods) == 6
    for row, (x, y) in enumerate(CONFIG['pairs']):
        pair = [obj for obj in pods if obj['structural_pair'] == row+1]
        assert len(pair) == 2
        assert sorted(round(obj.location.y, 5) for obj in pair) == [-y, y]
        assert all(obj.location.x == x and obj.location.z == 0 for obj in pair)
    return {'podCount': len(pods), 'pairCenters': CONFIG['pairs'], 'podRadius': CONFIG['pod_radius'],
            'sameBaseLevel': True, 'mirroredStructuralLayout': True,
            'habitatOrder': [{'name': obj.name, 'center': list(obj.location), 'kind': obj['physical_habitat']} for obj in pods],
            'objectCount': len(scene.objects), 'actual3DGeometry': True,
            'referenceMatch': 'Proportion study, not a pixel-exact or measured reconstruction.'}


def main():
    global COLLECTION
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=','.join(VIEWS))
    parser.add_argument('--stage', choices=['clay', 'lookdev', 'both'], default='both')
    parser.add_argument('--width', type=int, default=1280)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    OUT.mkdir(parents=True, exist_ok=True)
    scene, camera = setup()
    scene.render.resolution_x = args.width
    scene.render.resolution_y = round(args.width*9/16)
    (OUT/'model-parameters.json').write_text(json.dumps(CONFIG, indent=2), encoding='utf-8')
    (OUT/'geometry-verification.json').write_text(json.dumps(validate(scene), indent=2), encoding='utf-8')
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v02.blend'))
    for stage in (['clay', 'lookdev'] if args.stage == 'both' else [args.stage]):
        scene.view_layers[0].material_override = M['clay'] if stage == 'clay' else None
        scene.cycles.samples = 24 if stage == 'clay' else 48
        bpy.data.collections['ENVIRONMENT / editable star points'].hide_render = stage == 'clay'
        for name in args.views.split(','):
            location, scale = VIEWS[name]
            point_camera(camera, location)
            camera.data.ortho_scale = scale
            scene.render.filepath = str(OUT/f'{stage}-{name}.png')
            bpy.ops.render.render(write_still=True)
    scene.view_layers[0].material_override = None
    bpy.data.collections['ENVIRONMENT / editable star points'].hide_render = False
    point_camera(camera, VIEWS['01-forward-quarter'][0])
    camera.data.ortho_scale = 30
    scene.cycles.samples = 48
    scene.render.filepath = str(OUT/'animation'/'frame_')
    # Keep named alternative cameras and an animation-ready orbit controller.
    COLLECTION = bpy.data.collections['REVIEW / cameras and illumination']
    orbit = empty('CAMERA_ORBIT / optional yaw animation', parent=None)
    for name, (location, scale) in VIEWS.items():
        data = bpy.data.cameras.new('Lens / '+name)
        obj = bpy.data.objects.new('VIEW / '+name, data)
        COLLECTION.objects.link(obj)
        data.type = 'ORTHO'
        data.ortho_scale = scale
        data.clip_end = 250
        point_camera(obj, location)
    camera.parent = orbit
    orbit.rotation_euler.z = math.radians(-24)
    orbit.keyframe_insert(data_path='rotation_euler', frame=1)
    orbit.rotation_euler.z = math.radians(36)
    orbit.keyframe_insert(data_path='rotation_euler', frame=120)
    scene.frame_set(49)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'headquarters-ark-v02.blend'))
    print('ARK MODEL COMPLETE / six mirrored pods / editable geometry, materials, cameras')


if __name__ == '__main__':
    main()
