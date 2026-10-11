"""Blender 3D orbital glyphs, anchored to measured points in a generated take.

Run with Blender --background --python this_file -- plan.json [--stills].
Depth/tilt are artistic assumptions. Per-frame projection matches the source
lights, while planetary markers orbit real 3D curves with perspective.
"""
import argparse
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector


def emission(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    light = nodes.new('ShaderNodeEmission')
    light.inputs['Color'].default_value = (*color, 1)
    light.inputs['Strength'].default_value = strength
    out = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(light.outputs[0], out.inputs['Surface'])
    return mat


def curve(name, points, parent, material, width):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 1
    data.bevel_depth = width
    data.bevel_resolution = 2
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    data.materials.append(material)
    return obj


def ball(name, radius, parent, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=radius)
    obj = bpy.context.object
    obj.name = name
    obj.parent = parent
    obj.data.materials.append(material)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def orbit(radius, phase, z=0, eccentricity=0):
    return (radius*(math.cos(phase)-eccentricity),
            radius*math.sqrt(1-eccentricity**2)*math.sin(phase), z)


def eccentric_angle(mean, eccentricity):
    angle = mean
    for _ in range(5):
        angle -= (angle-eccentricity*math.sin(angle)-mean)/(1-eccentricity*math.cos(angle))
    return angle


def empty(name, parent=None, tilt=(0, 0, 0)):
    obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    obj.rotation_euler = [math.radians(a) for a in tilt]
    return obj


def asteroid_belt(name, belt, parent, radius, unit, material, seed):
    """Fixed seeded particles in a thickened orbital band; no random flicker."""
    rig = empty(name, parent, belt.get('inclinationDegrees', (0, 0, 0)))
    rng = random.Random(seed)
    vertices, faces = [], []
    for _ in range(belt['count']):
        phase = rng.random()*math.tau
        clumps = belt.get('clumps', 0)
        if clumps and rng.random() < belt.get('clumpWeight', .65):
            phase = rng.randrange(clumps)*math.tau/clumps+rng.gauss(0, .20)
        r = radius*(belt['radiusRatio']+rng.uniform(-1, 1)*belt['widthRatio']/2)
        thickness = belt.get('thicknessRatio', .016)
        centre = Vector(orbit(r, phase, rng.uniform(-1, 1)*radius*thickness))
        size = unit*rng.uniform(*belt.get('particleSizePx', (.50, 1.05)))
        first = len(vertices)
        vertices.extend(centre+Vector(v)*size for v in
                        ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)))
        faces.extend(tuple(first+i for i in f) for f in
                     ((0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)))
    mesh = bpy.data.meshes.new(name+' / seeded particles')
    mesh.from_pydata(vertices, [], faces)
    obj = bpy.data.objects.new(name+' / particles', mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = rig
    mesh.materials.append(material)
    rig['particle_count'] = belt['count']
    return rig


GLYPHS = {
    'fork': [[(-.24,-.45),(-.24,.46),(.13,.17),(.35,.44)],
             [(-.24,.06),(.23,-.15),(.08,-.44)]],
    'loop': [[(-.28,-.44),(-.28,.24),(-.09,.46),(.23,.35),(.28,.05),
              (.10,-.13),(-.28,.02)],[(.05,-.13),(.27,-.44)]],
    'zig': [[(-.31,.40),(.28,.40),(-.17,.05),(.25,-.06),(-.28,-.44)],
            [(-.31,-.13),(-.31,.12)]],
    'kite': [[(0,.46),(.31,.11),(0,-.19),(-.30,.11),(0,.46)],
             [(0,-.19),(0,-.46)],[(.14,-.30),(.30,-.30)]],
    'wave': [[(-.31,-.42),(-.31,.31),(-.08,.46),(.10,.12),(.30,.36)],
             [(-.31,-.05),(.13,-.05),(.26,-.40)]],
}


def system_label(system, unit, material):
    """Two invented curve glyphs in a camera-facing plane, not a text font."""
    label = system.get('label')
    if not label:
        return None
    rig = empty(system['id']+' / camera-facing label')
    rig['label_identity'] = label['codeId']
    rig['glyph_pair'] = label['glyph']+' + ordinal rune '+str(label['ordinal'])
    height = label['heightPx']*unit
    for index, points in enumerate(GLYPHS[label['glyph']]):
        curve(rig.name+f' / identity stroke {index}',
              [(x*height,y*height,0) for x,y in points],rig,material,1.05*unit)
    # A small open diamond with distinct bars acts as an alien numerical rune.
    curve(rig.name+' / index rune',
          [(x*height,y*height,0) for x,y in
           ((.64,.28),(.82,.05),(.64,-.19),(.46,.05),(.64,.28))],
          rig,material,.85*unit)
    for index in range(label['ordinal']):
        y=-.30-index*.105
        curve(rig.name+f' / index bar {index}',
              [(.50*height,y*height,0),(.78*height,(y+.04)*height,0)],
              rig,material,.8*unit)
    dx,dy=label['offsetPx']
    length=math.hypot(dx,dy)
    # Coordinates start at the label; the other end stops short of the star.
    near=(-dx*unit*(1-14/length),dy*unit*(1-14/length),0)
    curve(rig.name+' / leader',
          [(-13*unit,-8*unit,0),(-22*unit,-8*unit,0),near],
          rig,material,.52*unit)
    return rig


def linear_keys(obj):
    if not obj.animation_data or not obj.animation_data.action:
        return
    for layer in obj.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for key in fc.keyframe_points:
                        key.interpolation = 'LINEAR'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--stills', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    project = args.plan.resolve().parent
    plan = json.loads(args.plan.read_text())
    dest = project/plan['output']
    tracking = json.loads((dest/'tracking.json').read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 8
    scene.render.resolution_x = plan['width']
    scene.render.resolution_y = plan['height']
    scene.render.resolution_percentage = 100
    scene.render.fps = tracking['fps']
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = str(dest/'main/frame_')
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.world = bpy.data.worlds.new('Black additive substrate')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0
    camera = bpy.data.cameras.new('Matched locked perspective / assumed 45 mm')
    camera.lens = plan['camera']['lensMm']
    camera.sensor_width = plan['camera']['sensorWidthMm']
    camera.sensor_fit = 'HORIZONTAL'
    camera.clip_start = .01
    obj = bpy.data.objects.new('CAMERA / image-space registration', camera)
    scene.collection.objects.link(obj)
    scene.camera = obj  # Default camera looks down negative Z, Y up.
    focal = plan['width']*camera.lens/camera.sensor_width
    cyan = emission('Orbit / quiet cyan', (.06, .42, .62), .75)
    accent = emission('Orbit / bright sweep', (.13, .72, 1), 1.4)
    pearl = emission('Planet / cyan white', (.35, .82, 1), 1.7)
    amber = emission('Home / warm amber', (1, .32, .055), 1.2)
    for index, system in enumerate(plan['systems']):
        root = bpy.data.objects.new(f'SYSTEM / {system["id"]}', None)
        scene.collection.objects.link(root)
        root['registration'] = 'Per-frame source-light coordinates; artist-assigned depth'
        root['depth'] = system['depth']
        root['screen_radius_px'] = system['radiusPx']
        root['birth_frame'] = system['birthFrame']
        root.rotation_euler = [math.radians(a) for a in system['tiltDegrees']]
        unit = system['depth']/focal
        radius = system['radiusPx']*unit
        curves = []
        markers = []
        moons = []
        belts = []
        color = system.get('displayColor')
        orbit_mat, accent_mat, planet_mat, star_mat, dust_mat = cyan, accent, pearl, pearl, cyan
        if color:
            orbit_mat = emission(system['id']+' / coded orbit', tuple(v*.38 for v in color), .9)
            accent_mat = emission(system['id']+' / coded sweep', color, 1.3)
            planet_mat = emission(system['id']+' / planet beacon', tuple(.22+v*.78 for v in color), 1.5)
            star_mat = emission(system['id']+' / star color', color, 2.3)
            dust_mat = emission(system['id']+' / belt glow', tuple(.10+v*.4 for v in color), .85)
        elif system['color'] == 'amber':
            star_mat = amber
        label_mat = emission(system['id']+' / readable glyph light',
            tuple(.24+.76*v for v in (color or (.13,.72,1))),1.1)
        label_rig = system_label(system,unit,label_mat)
        core = ball(f'{system["id"]} / star point', system.get('starSizePx',2.1)*unit, root, star_mat)
        bodies = system.get('planets', [
            {'radiusRatio':ratio,'sizePx':1.9+.3*n,'phaseDegrees':math.degrees(index*.91+n*2.1),
             'speedRadiansPerFrame':.025+.004*n} for n,ratio in enumerate((.40,.68,1.0))])
        root['planet_count'] = len(bodies)
        root['palette'] = system['color']
        for ring_index, body in enumerate(bodies):
            ratio = body['radiusRatio']
            r = radius*ratio
            eccentricity = body.get('eccentricity',0)
            plane = empty(f'{system["id"]} / orbital plane {ring_index+1}', root,
                          body.get('inclinationDegrees',(0,0,0)))
            curves.append(curve(f'{system["id"]} / orbit {ring_index+1}',
                [orbit(r, i*math.tau/128, eccentricity=eccentricity) for i in range(129)], plane,
                orbit_mat if color else amber if system['id']=='home' and ring_index==0 else cyan, .65*unit))
            marker = ball(f'{system["id"]} / planet {ring_index+1}',
                          body['sizePx']*unit, plane, planet_mat)
            # Eccentric trajectories retain planet beacons; circular ones also
            # have a moving arc that stays exactly on their orbital curve.
            sweep = None
            if eccentricity == 0:
                sweep = curve(f'{system["id"]} / orbit energy {ring_index+1}',
                    [orbit(r,i*.65/32) for i in range(33)],plane,accent_mat,.88*unit)
            markers.append((marker,sweep,r,body))
            if body.get('ringed'):
                ring_plane = empty(marker.name+' / tilted rings',marker,(38,-16,25))
                for ratio in (1.9,2.3):
                    curves.append(curve(marker.name+f' / ring {ratio}',
                        [orbit(body['sizePx']*unit*ratio,i*math.tau/64) for i in range(65)],
                        ring_plane,orbit_mat,.42*unit))
            for moon_index in range(body.get('moonCount',0)):
                moon = ball(marker.name+f' / moon {moon_index+1}',.95*unit,marker,planet_mat)
                moons.append((moon,body['sizePx']*unit*(3.5+moon_index*1.7),moon_index))
        for belt_index,belt in enumerate(system.get('asteroidBelts',[])):
            field_mat=dust_mat
            if belt.get('outerCloud'):
                field_mat=emission(system['id']+f' / outer cloud {belt_index}',
                    tuple(.10+.6*v for v in color),belt.get('strength',1.0))
            belt_rig=asteroid_belt(f'{system["id"]} / asteroid belt {belt_index+1}',
                belt,root,radius,unit,field_mat,seed=713+index*101+belt_index)
            belts.append((belt_rig,belt))
        # Sparse radial bearing ticks support the oblique plane without text.
        ticks=system.get('bearingTicks',12)
        for tick in range(ticks):
            angle = tick*math.tau/ticks
            curves.append(curve(f'{system["id"]} / bearing {tick:02}',
                [orbit(radius*1.04, angle), orbit(radius*1.09, angle)], root,
                orbit_mat, .5*unit))
        for row in tracking['systems'][system['id']]:
            frame = row['frame']
            x, y = row['pixel']
            root.location = ((x-plan['width']/2)*unit,
                             (plan['height']/2-y)*unit, -system['depth'])
            t = max(0, min(1, (frame-system['birthFrame'])/system['unfoldFrames']))
            unfold = t*t*(3-2*t)
            root.scale = (max(.001, unfold),)*3
            root.keyframe_insert('location', frame=frame)
            root.keyframe_insert('scale', frame=frame)
            root.rotation_euler.z = math.radians(system['tiltDegrees'][2]+max(0,frame-system['birthFrame'])*.06)
            root.keyframe_insert('rotation_euler', frame=frame)
            if label_rig:
                label=system['label']
                dx,dy=label['offsetPx']
                label_rig.location=root.location+Vector((dx*unit*unfold,-dy*unit*unfold,.02))
                # Labels grow with the display, then retain their readable size.
                label_rig.scale=(max(.001,unfold),)*3
                label_rig.keyframe_insert('location',frame=frame)
                label_rig.keyframe_insert('scale',frame=frame)
            for marker,sweep,r,body in markers:
                mean=math.radians(body['phaseDegrees'])+(frame-system['birthFrame'])*body['speedRadiansPerFrame']
                phase=eccentric_angle(mean,body.get('eccentricity',0))
                marker.location=orbit(r,phase,eccentricity=body.get('eccentricity',0))
                marker.keyframe_insert('location', frame=frame)
                if sweep:
                    sweep.rotation_euler.z=phase-.5
                    sweep.keyframe_insert('rotation_euler',frame=frame)
            for moon,r,n in moons:
                moon.location=orbit(r,(frame-system['birthFrame'])*.11+n*2.5,r*.22*math.sin(frame*.08+n))
                moon.keyframe_insert('location',frame=frame)
            for belt_rig,belt in belts:
                belt_rig.rotation_euler.z=math.radians(belt['inclinationDegrees'][2])+(frame-system['birthFrame'])*belt['rotationRadiansPerFrame']
                belt_rig.keyframe_insert('rotation_euler',frame=frame)
                if belt.get('outerCloud'):
                    age=frame-system['birthFrame']
                    growth=max(0,min(1,(age-5)/22))
                    extent=.55+.45*growth*growth*(3-2*growth)
                    belt_rig.scale=(extent,)*3
                    belt_rig.keyframe_insert('scale',frame=frame)
        for child in [root, core, *curves, *[a for m in markers for a in m[:2] if a],
                      *[m[0] for m in moons],*[b[0] for b in belts],label_rig]:
            if child:
                linear_keys(child)
    scene.frame_start = plan['renderStartFrame']
    scene.frame_end = plan['sourceFrames']
    scene['method'] = plan['depthMethod']
    scene['source_take'] = plan['source']
    scene['song_edit_frames'] = tracking['editFrames']
    scene['song_start_frame'] = tracking['songStartFrame']
    scene['source_lead_in_frames'] = tracking['leadInFrames']
    # Blender 5.x compositor: separate unmasked light, two grades and mask A/B.
    group = bpy.data.node_groups.new('Hologram / linear-light composite', 'CompositorNodeTree')
    group.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    scene.compositing_node_group = group
    nodes, links = group.nodes, group.links
    render = nodes.new('CompositorNodeRLayers')
    glare = nodes.new('CompositorNodeGlare')
    glare.inputs['Type'].default_value = 'Fog Glow'
    glare.inputs['Quality'].default_value = 'High'
    glare.inputs['Threshold'].default_value = .7
    glare.inputs['Size'].default_value = .15
    links.new(render.outputs['Image'], glare.inputs['Image'])
    source = nodes.new('CompositorNodeImage')
    source.image = bpy.data.images.load(str(dest/'source/frame_0001.png'))
    source.image.source = 'SEQUENCE'
    source.frame_duration = plan['sourceFrames']
    source.frame_start = 1
    source.use_auto_refresh = True
    source_socket=source.outputs['Image']
    if plan.get('tintSourceStarCores'):
        tint=nodes.new('CompositorNodeImage')
        tint.image=bpy.data.images.load(str(dest/f'star-tint/frame_{plan["renderStartFrame"]:04d}.png'))
        tint.image.source='SEQUENCE'
        tint.image.colorspace_settings.name='Non-Color'
        tint.frame_start=1
        tint.frame_duration=plan['sourceFrames']
        tint.use_auto_refresh=True
        grade=nodes.new('ShaderNodeMix')
        grade.data_type='RGBA'
        grade.blend_type='MULTIPLY'
        grade.inputs[0].default_value=1
        links.new(source_socket,grade.inputs[6])
        links.new(tint.outputs['Image'],grade.inputs[7])
        source_socket=grade.outputs[2]
    mask = nodes.new('CompositorNodeImage')
    mask.image = bpy.data.images.load(str(dest/f'holdout/frame_{plan["renderStartFrame"]:04d}.png'))
    mask.image.source = 'SEQUENCE'
    mask.image.colorspace_settings.name = 'Non-Color'
    mask.frame_duration = plan['sourceFrames']
    mask.frame_start = 1
    mask.use_auto_refresh = True
    invert = nodes.new('CompositorNodeInvert')
    links.new(mask.outputs['Image'], invert.inputs['Color'])
    held = nodes.new('ShaderNodeMix')
    held.data_type = 'RGBA'
    held.blend_type = 'MULTIPLY'
    held.inputs[0].default_value = 1
    links.new(glare.outputs['Image'], held.inputs[6])
    links.new(invert.outputs['Color'], held.inputs[7])
    output = nodes.new('NodeGroupOutput')
    # In 5.2 file-output items are explicit; their subpaths retain source indices.
    def write_plate(name, socket):
        node = nodes.new('CompositorNodeOutputFile')
        node.directory = str(dest/name)
        node.file_name = 'frame_####'
        node.format.media_type = 'IMAGE'
        node.format.file_format = 'PNG'
        node.format.color_mode = 'RGB'
        node.save_as_render = True
        item = node.file_output_items.new('RGBA', 'Image')
        links.new(socket, node.inputs[item.name])
    write_plate('light', glare.outputs['Image'])
    write_plate('mask-check', mask.outputs['Image'])
    for name, light_socket, gain in (
        ('restrained', held.outputs[2], plan['composite']['restrainedGain']),
        ('rich', held.outputs[2], plan['composite']['richGain']),
        ('unmasked', glare.outputs['Image'], plan['composite']['richGain'])):
        dim = nodes.new('ShaderNodeMix')
        dim.data_type = 'RGBA'
        dim.blend_type = 'MULTIPLY'
        dim.inputs[0].default_value = 1
        dim.inputs[7].default_value = (gain, gain, gain, 1)
        links.new(light_socket, dim.inputs[6])
        add = nodes.new('ShaderNodeMix')
        add.data_type = 'RGBA'
        add.blend_type = 'ADD'
        add.inputs[0].default_value = 1
        links.new(source_socket, add.inputs[6])
        links.new(dim.outputs[2], add.inputs[7])
        write_plate(name, add.outputs[2])
        if name == 'rich':
            links.new(add.outputs[2], output.inputs['Image'])
    scene.frame_set(125)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest/(dest.name+'.blend')))
    if args.stills:
        for frame in (101, 113, 125, 144):
            scene.frame_set(frame)
            bpy.ops.render.render()
    else:
        bpy.ops.render.render(animation=True)


if __name__ == '__main__':
    main()
