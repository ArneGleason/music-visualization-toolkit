"""Editable 3D orbital flight, with a plate-matched and a native look test.

Run Blender -b --python this_file -- plan.json --variant hybrid|native.
Use --frames 25,80,150 for look development before rendering the sequence.
"""
import argparse
import bisect
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector, noise


def material(name, color, strength=0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = .65
    shader.inputs['Emission Color'].default_value = (*color, 1)
    shader.inputs['Emission Strength'].default_value = strength
    return mat


def unlit(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    e = nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*color, 1)
    e.inputs[1].default_value = strength
    mat.node_tree.links.new(e.outputs[0], nodes.new('ShaderNodeOutputMaterial').inputs[0])
    return mat


def sphere(name, radius, mat, location=(0, 0, 0), segments=96, rings=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def curve(name, points, width, mat):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 1
    data.bevel_depth = width
    data.bevel_resolution = 2
    s = data.splines.new('POLY')
    s.points.add(len(points)-1)
    for p, co in zip(s.points, points):
        p.co = (*co, 1)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def lerp(a, b, t):
    return Vector(a).lerp(Vector(b), t)


def resample(points, count=601):
    distance = [0]
    for a, b in zip(points, points[1:]):
        distance.append(distance[-1]+(b-a).length)
    result = []
    for i in range(count):
        d = distance[-1]*i/(count-1)
        index = min(len(points)-2, max(0, bisect.bisect_right(distance, d)-1))
        result.append(lerp(points[index], points[index+1], (d-distance[index])/max(1e-9, distance[index+1]-distance[index])))
    return result


def orbit(world, phase, radius_ratio=1.55, inclination=65):
    radius, centre = world['radius']*radius_ratio, Vector(world['centre'])
    a = math.radians(phase)
    eccentricity = world.get('orbitEccentricity',0)
    if eccentricity:
        anomaly = a-math.radians(world.get('periapsisPhase',330))
        radius *= (1-eccentricity**2)/(1+eccentricity*math.cos(anomaly))
    tilt = math.radians(inclination)
    v = Vector((radius*math.cos(a), radius*math.sin(a)*math.cos(tilt), -radius*math.sin(a)*math.sin(tilt)))
    # A slanted ellipse rather than a flat horizontal annotation.
    turn = math.radians(-18)
    return centre+Vector((v.x*math.cos(turn)-v.y*math.sin(turn), v.x*math.sin(turn)+v.y*math.cos(turn), v.z))


def flight(worlds, continuous=False):
    if continuous:
        return continuous_flight(worlds)
    a, b = worlds[1:]
    launch = Vector((-4.5, -1.2, -19))
    a_in, a_out = orbit(a, 220), orbit(a, 630)
    b_in, b_out = orbit(b, 150, 1.6, 58), orbit(b, 560, 1.6, 58)
    def tangent(world, phase, ratio=1.55, tilt=65):
        return (orbit(world, phase+.1, ratio, tilt)-orbit(world, phase-.1, ratio, tilt)).normalized()
    def bezier(p, q, r, s, t):
        return (1-t)**3*p+3*(1-t)**2*t*q+3*(1-t)*t*t*r+t**3*s
    points = []
    for i in range(101):
        t = i/100
        points.append(bezier(launch, launch+Vector((.1, 3, 1)), a_in-tangent(a,220)*.9, a_in, t))
    points += [orbit(a, 220+410*i/240) for i in range(1, 241)]
    points += [bezier(a_out, a_out+tangent(a,630)*1.2, b_in-tangent(b,150,1.6,58)*1.3, b_in, i/80) for i in range(1, 81)]
    points += [orbit(b, 150+410*i/240, 1.6, 58) for i in range(1, 241)]
    points += [bezier(b_out, b_out+tangent(b,560,1.6,58)*1.5, Vector((12, 2, -12)), Vector((14, 4, -11)), i/80) for i in range(1, 81)]
    return resample(points)


def continuous_flight(worlds, metadata=False):
    """Authored loops with position, tangent and curvature matched at joins.

    These are illustrative visits, not a numerical gravity-assist simulation.
    Quintic connectors begin bending well before reaching the circular arcs.
    """
    a, b = worlds[1:]
    def state(world, phase, speed, ratio=1.55, tilt=65):
        p = orbit(world, phase, ratio, tilt)
        h = math.radians(.05)
        before, after = orbit(world,phase-.05,ratio,tilt), orbit(world,phase+.05,ratio,tilt)
        derivative = (after-before)/(2*h)
        second = (after-2*p+before)/h**2
        normal = second-derivative*(second.dot(derivative)/derivative.length_squared)
        return p, derivative.normalized()*speed, normal*speed**2/derivative.length_squared
    def connector(start, end, count=160):
        p, v, acceleration = start
        q, w, end_acceleration = end
        controls = [p, p+v/5, p+2*v/5+acceleration/20,
                    q-2*w/5+end_acceleration/20, q-w/5, q]
        return [sum((controls[j]*math.comb(5,j)*(1-i/count)**(5-j)*(i/count)**j
                     for j in range(6)), Vector()) for i in range(count+1)]
    entry_a = state(a, 270, 5)
    exit_a = state(a, 630, 5)
    entry_b = state(b, 270, 5, 1.6, 58)
    exit_b = state(b, 630, 5, 1.6, 58)
    launch = (Vector((-7, -.5, -19)), Vector((7, 2, 1)), Vector())
    finish = (Vector((15, -2.8, -13)), Vector((6, .1, 1)), Vector())
    points = connector(launch, entry_a)
    points += [orbit(a, 270+360*i/360) for i in range(1,361)]
    points += connector(exit_a, entry_b)[1:]
    points += [orbit(b, 270+360*i/360, 1.6, 58) for i in range(1,361)]
    points += connector(exit_b, finish)[1:]
    sampled = resample(points)
    if not metadata:
        return sampled
    distances = [0]
    for left,right in zip(points,points[1:]):
        distances.append(distances[-1]+(right-left).length)
    spans = [distances[i]/distances[-1] for i in (160,520,680,1040)]
    return sampled, spans


def flight_timing(points, worlds, spans):
    """Vis-viva loop speeds, with authored smooth approach/transfer speeds.

    mu=a gives dimensionless speed. The final time scale fits the song span;
    these fictional world sizes and connector paths are not an N-body solve.
    """
    def orbital_speed(world, p, ratio):
        a = world['radius']*ratio
        r = (p-Vector(world['centre'])).length
        return math.sqrt(max(.01,2*a/r-1))
    a,b = worlds[1:]
    va = orbital_speed(a,orbit(a,270),1.55)
    vb = orbital_speed(b,orbit(b,270,1.6,58),1.6)
    def blend(x,y,t):
        t = max(0,min(1,t)); t=t*t*(3-2*t)
        return x+(y-x)*t
    speeds=[]
    for i,p in enumerate(points):
        u=i/(len(points)-1)
        if u<spans[0]: v=blend(.62,va,u/spans[0])
        elif u<=spans[1]: v=orbital_speed(a,p,1.55)
        elif u<spans[2]:
            t=(u-spans[1])/(spans[2]-spans[1])
            v=blend(va,.65,t*2) if t<.5 else blend(.65,vb,(t-.5)*2)
        elif u<=spans[3]: v=orbital_speed(b,p,1.6)
        else: v=blend(vb,.85,(u-spans[3])/(1-spans[3]))
        speeds.append(v)
    times=[0]
    for i,(left,right) in enumerate(zip(points,points[1:])):
        times.append(times[-1]+2*(right-left).length/(speeds[i]+speeds[i+1]))
    times=[t/times[-1] for t in times]
    return times,speeds


def fading_trail(name, points, width, color, power, lifetime, travel_frames, travel_start, passage_times=None, decay=None):
    """UV.x stores path distance; animated head distance gives each point an age."""
    vertices, faces = [], []
    sides = 6
    for i, p in enumerate(points):
        tangent = (points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        across = tangent.cross(Vector((0,0,1))).normalized()
        normal = tangent.cross(across).normalized()
        for j in range(sides):
            angle = 2*math.pi*j/sides
            vertices.append(p+width*(across*math.cos(angle)+normal*math.sin(angle)))
    for i in range(len(points)-1):
        for j in range(sides):
            faces.append((i*sides+j,i*sides+(j+1)%sides,
                          (i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    uv = mesh.uv_layers.new(name='Distance along trajectory')
    for face in mesh.polygons:
        face.use_smooth = True
        for loop in face.loop_indices:
            index=mesh.loops[loop].vertex_index//sides
            timestamp=passage_times[index] if passage_times else index/(len(points)-1)
            uv.data[loop].uv = (timestamp,0)
    obj = bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(obj)
    mat = bpy.data.materials.new(name+' / age decay')
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    head = nodes.new('ShaderNodeValue'); head.name = 'Animated ship distance'
    for frame in (1, travel_start+travel_frames+1, bpy.context.scene.frame_end):
        head.outputs[0].default_value = (frame-1-travel_start)/travel_frames
        head.outputs[0].keyframe_insert('default_value',frame=frame)
    coordinate = nodes.new('ShaderNodeTexCoord')
    separate = nodes.new('ShaderNodeSeparateXYZ'); links.new(coordinate.outputs['UV'],separate.inputs[0])
    def operation(kind, a, b):
        node = nodes.new('ShaderNodeMath'); node.operation = kind
        for index, value in enumerate((a,b)):
            if isinstance(value,(float,int)): node.inputs[index].default_value = value
            else: links.new(value,node.inputs[index])
        return node.outputs[0]
    age = operation('SUBTRACT',head.outputs[0],separate.outputs[0])
    visited = operation('GREATER_THAN',age,0)
    remaining = operation('SUBTRACT',1,operation('MULTIPLY',age,travel_frames/lifetime))
    if decay:
        age_frames=operation('MAXIMUM',operation('MULTIPLY',age,travel_frames),0)
        bright=operation('MULTIPLY',operation('POWER',math.e,operation('MULTIPLY',age_frames,-1/decay['brightFrames'])),1-decay['tailWeight'])
        tail=operation('MULTIPLY',operation('POWER',math.e,operation('MULTIPLY',age_frames,-1/decay['tailFrames'])),decay['tailWeight'])
        fade=operation('MULTIPLY',visited,operation('MULTIPLY',operation('ADD',bright,tail),operation('MAXIMUM',remaining,0)))
    else:
        fade = operation('MULTIPLY',visited,operation('POWER',operation('MAXIMUM',remaining,0),2))
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (*color,1)
    if decay:
        emission.inputs[1].default_value=power
    else:
        links.new(operation('MULTIPLY',fade,power),emission.inputs[1])
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    links.new(fade,mix.inputs[0]); links.new(transparent.outputs[0],mix.inputs[1]); links.new(emission.outputs[0],mix.inputs[2])
    links.new(mix.outputs[0],nodes.new('ShaderNodeOutputMaterial').inputs[0])
    mesh.materials.append(mat)
    linear_keys(mat.node_tree)
    return obj


def linear_keys(obj):
    if not obj.animation_data or not obj.animation_data.action:
        return
    for layer in obj.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for key in fc.keyframe_points:
                        key.interpolation = 'LINEAR'


def world_material(name, palette):
    mat = material(name, palette[0])
    n, links = mat.node_tree.nodes, mat.node_tree.links
    shader = n.get('Principled BSDF')
    tex = n.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = 7
    tex.inputs['Detail'].default_value = 6
    tex.inputs['Roughness'].default_value = .7
    colors = n.new('ShaderNodeValToRGB')
    colors.color_ramp.elements.remove(colors.color_ramp.elements[1])
    for i, color in enumerate(palette):
        e = colors.color_ramp.elements[0] if i == 0 else colors.color_ramp.elements.new(i/(len(palette)-1))
        e.position = i/(len(palette)-1)
        e.color = (*color, 1)
    links.new(tex.outputs['Fac'], colors.inputs[0])
    links.new(colors.outputs[0], shader.inputs['Base Color'])
    grain = n.new('ShaderNodeTexNoise')
    grain.inputs['Scale'].default_value = 145
    grain.inputs['Detail'].default_value = 3
    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .3
    bump.inputs['Distance'].default_value = .045
    links.new(grain.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs[0], shader.inputs['Normal'])
    shader.inputs['Emission Strength'].default_value = .06
    links.new(colors.outputs[0], shader.inputs['Emission Color'])
    return mat


def native_world(world, index):
    root = bpy.data.objects.new(world['name']+' / world root', None)
    bpy.context.scene.collection.objects.link(root)
    root.location = world['centre']
    radius = world['radius']
    palettes = [
        [(0.005,.04,.07),(.012,.29,.32),(.12,.65,.60),(.8,.53,.30),(.09,.12,.20),(.7,.6,.46)],
        [(.10,.045,.07),(.34,.19,.11),(.72,.40,.14),(.9,.64,.30),(.15,.22,.27),(.73,.62,.44)],
        [(.008,.02,.09),(.02,.12,.32),(.025,.5,.62),(.29,.12,.47),(.5,.48,.68),(.76,.62,.70)]
    ]
    planet = sphere(world['name']+' / displaced painted terrain', radius, world_material(world['name']+' / painted geology', palettes[index]), segments=160, rings=80)
    planet.parent = root
    for v in planet.data.vertices:
        normal = v.co.normalized()
        height = noise.fractal(normal*3.7+Vector((index*8, 2, 3)), 1.0, 2.0, 5)
        v.co *= 1+max(0, height-.33)*.105
    ocean = sphere(world['name']+' / shallow colored water', radius*1.006, material(world['name']+' / turquoise depth', palettes[index][1]))
    ocean.parent = root
    ocean_mat = ocean.data.materials[0].node_tree.nodes.get('Principled BSDF')
    ocean_mat.inputs['Roughness'].default_value = .25
    # Transparent noisy cloud shell: fully editable geometry and shader.
    cloud_mat = material(world['name']+' / warm layered clouds', (.94,.79,.63))
    n, links = cloud_mat.node_tree.nodes, cloud_mat.node_tree.links
    tex = n.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = 12
    tex.inputs['Detail'].default_value = 5
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = .53
    ramp.color_ramp.elements[1].position = .67
    links.new(tex.outputs['Fac'], ramp.inputs[0])
    clear = n.new('ShaderNodeBsdfTransparent')
    mix = n.new('ShaderNodeMixShader')
    links.new(ramp.outputs[0], mix.inputs[0])
    links.new(clear.outputs[0], mix.inputs[1])
    links.new(n.get('Principled BSDF').outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], n.get('Material Output').inputs[0])
    clouds = sphere(world['name']+' / cloud layer', radius*1.045, cloud_mat)
    clouds.parent = root
    atmo = bpy.data.materials.new(world['name']+' / blue limb scattering')
    atmo.use_nodes = True
    n, links = atmo.node_tree.nodes, atmo.node_tree.links
    n.clear()
    edge = n.new('ShaderNodeFresnel'); edge.inputs['IOR'].default_value = 1.07
    clear = n.new('ShaderNodeBsdfTransparent')
    light = n.new('ShaderNodeEmission'); light.inputs[0].default_value = (.08,.45,1,1); light.inputs[1].default_value = .4
    mix = n.new('ShaderNodeMixShader')
    links.new(edge.outputs[0], mix.inputs[0]); links.new(clear.outputs[0], mix.inputs[1]); links.new(light.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], n.new('ShaderNodeOutputMaterial').inputs[0])
    limb = sphere(world['name']+' / atmosphere', radius*1.015, atmo)
    limb.parent = root
    return root


def background():
    mat = unlit('Procedural indigo / violet nebula', (.015,.012,.05), 1)
    n, links = mat.node_tree.nodes, mat.node_tree.links
    tex = n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 3.8; tex.inputs['Detail'].default_value = 6
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.0003,.001,.008,1); ramp.color_ramp.elements[0].position = .3
    ramp.color_ramp.elements[1].color = (.12,.025,.25,1); ramp.color_ramp.elements[1].position = .72
    links.new(tex.outputs['Fac'], ramp.inputs[0]); links.new(ramp.outputs[0], n.get('Emission').inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,-55))
    obj = bpy.context.object; obj.name = 'Procedural nebula / no image plate'; obj.scale=(18,12,1); obj.data.materials.append(mat)
    rng = random.Random(731)
    verts, faces = [], []
    for _ in range(1600):
        x,y=rng.uniform(-17,17),rng.uniform(-10,10)
        r=rng.uniform(.005,.018)
        a=len(verts); verts.extend([(x-r,y,-48),(x,y+r,-48),(x+r,y,-48),(x,y-r,-48)]); faces.append((a,a+1,a+2,a+3))
    mesh=bpy.data.meshes.new('Seeded distant stars'); mesh.from_pydata(verts,[],faces)
    obj=bpy.data.objects.new(mesh.name,mesh); bpy.context.scene.collection.objects.link(obj); mesh.materials.append(unlit('Quiet ice stars',(.6,.75,1),2))
    centre=Vector((11.7,6.25,-12))
    sphere('Illustrated star / white gold core',.19,unlit('Star radiance',(1,.8,.4),25),centre,32,16)
    for i in range(14):
        a=2*math.pi*i/14+.14; length=3.2+(i%4)*1.3
        direction=Vector((math.cos(a),math.sin(a),0))
        for j in range(3):
            start=.20+j*length/3; finish=.20+(j+1)*length/3
            curve('Illustrated star / authored tapered ray', [centre+direction*start,centre+direction*finish], .022/(j+1), unlit('Ray / warm decay',(1,.45,.11),3/(j+1)))


def load_ship(base, plan):
    with bpy.data.libraries.load(str(base/plan['shipLibrary']), link=False) as (src, dst):
        dst.collections=[c for c in src.collections if '01 SHIP' in c]
    collection=dst.collections[0]; bpy.context.scene.collection.children.link(collection)
    root=next(o for o in collection.all_objects if o.name.startswith('SHIP ROOT'))
    for obj in collection.all_objects:
        if obj is None:
            continue
        obj.animation_data_clear(); obj.hide_render=False
    root.parent=None; root.scale=(.058,)*3
    root.rotation_euler=(math.radians(68),math.radians(-12),math.radians(-28))
    return root


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path)
    parser.add_argument('--variant',choices=['hybrid','native'],required=True)
    parser.add_argument('--frames',help='Comma-separated look-test frames, otherwise full sequence')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    plan=json.loads(args.plan.read_text(encoding='utf-8')); base=args.plan.resolve().parent
    dest=base/plan['output']/args.variant; dest.mkdir(parents=True,exist_ok=True); (dest/'frames').mkdir(exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene; scene.name='Orbital flight / '+args.variant
    scene.render.engine='CYCLES'; scene.cycles.samples=plan.get('samples',16); scene.cycles.use_denoising=True
    if plan.get('motionBlur'):
        scene.render.use_motion_blur=True
        scene.render.motion_blur_shutter=plan['motionBlur']['shutterFrames']
        scene.render.motion_blur_position='CENTER'
    prefs=bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type='OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use=d.type=='OPTIX'
    scene.cycles.device='GPU'; scene.cycles.transparent_max_bounces=32
    width=plan['nativeWidth'] if args.variant=='native' else plan['width']
    scene.render.resolution_x=width; scene.render.resolution_y=round(width*9/16); scene.render.resolution_percentage=100
    scene.render.fps=24; scene.frame_start=1; scene.frame_end=plan['sourceFrames']
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
    scene.render.filepath=str(dest/'frames/frame_')
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
    scene.world=bpy.data.worlds.new('Space'); scene.world.use_nodes=True; scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=0
    bpy.ops.object.camera_add(); scene.camera=bpy.context.object; scene.camera.name='Matched orthographic composition / assumed depth'; scene.camera.data.type='ORTHO'; scene.camera.data.ortho_scale=24; scene.camera.data.clip_end=150
    black=unlit('Black planetary depth occluder',(0,0,0),0)
    worlds=plan['worlds']
    for i,world in enumerate(worlds):
        root=native_world(world,i) if args.variant=='native' else sphere(world['name']+' / 3D occlusion sphere',world['radius'],black,world['centre'])
        if args.variant=='native':
            root.rotation_euler.y=.07; root.keyframe_insert('rotation_euler',frame=1)
            root.rotation_euler.y=.13; root.keyframe_insert('rotation_euler',frame=scene.frame_end)
        else:
            for frame,centre,radius in world['keys']:
                root.location=centre; root.scale=(radius/world['radius'],)*3; root.keyframe_insert('location',frame=frame); root.keyframe_insert('scale',frame=frame)
        linear_keys(root)
    if args.variant=='native': background()
    for name,loc,color,power,size in [('Warm upper-right key',(12,10,-5),(1,.63,.3),2400,8),('Cool diffuse fill',(-9,3,-7),(.13,.4,1),800,12)]:
        bpy.ops.object.light_add(type='AREA',location=loc); obj=bpy.context.object; obj.name=name; obj.data.energy=power; obj.data.color=color; obj.data.shape='DISK'; obj.data.size=size; obj.rotation_euler=(Vector((0,0,-22))-obj.location).to_track_quat('-Z','Y').to_euler()
    ship=load_ship(base,plan)
    continuous=plan.get('flightLanguage')=='continuous-loops'
    variable=plan.get('velocityModel')=='vis-viva-loops'
    if variable:
        points,spans=continuous_flight(worlds,metadata=True)
        passage_times,speeds=flight_timing(points,worlds,spans)
    else:
        points=flight(worlds,continuous)
        passage_times=[i/(len(points)-1) for i in range(len(points))]
        speeds=[1]*len(points)
    travel_frames=plan.get('travelFrames',scene.frame_end-1)
    travel_start=plan.get('travelStartFrame',1)-1
    (dest/'trajectory.json').write_text(json.dumps({
        'points':[list(p) for p in points], 'travelFrames':travel_frames, 'travelStartFrame':travel_start+1,
        'sourceFrames':scene.frame_end, 'worlds':worlds,
        'passageTimes':passage_times, 'relativeSpeeds':speeds,
        'description':'Distance-dependent vis-viva loop speeds; authored transfers and song time scale, not a full gravity simulation.' if variable else 'Authored continuous loops; projected composition and assumed depths, not a physics solve.'
    },indent=2)+'\n',encoding='utf-8')
    layers=[]
    for name,width,color,power,wake,offset in [
        ('Amber history / visited orbital loops',.014,(1,.36,.07),3,False,0),
        ('Cyan living wake',.026,(.04,.55,1),8,True,0),
        ('White blue filament',.009,(.6,.9,1),10,True,0),
        ('Violet companion filament',.013,(.42,.15,1),6,True,.11),
        ('Warm companion filament',.014,(1,.56,.17),7,True,-.10)]:
        path=[p+Vector((0,offset*math.sin(i*.22),offset*math.cos(i*.22))) for i,p in enumerate(points)]
        if continuous:
            decay=plan.get('trailDecay')
            if decay:
                power*=plan.get('trailPowerScale',.22)
                life=decay['supportFrames']
            else:
                life=plan.get('trailLifetimeFrames',30) if not wake else 22
            obj=fading_trail(name,path,width,color,power,life,travel_frames,travel_start,passage_times,decay)
        else:
            obj=curve(name,path,width,unlit(name,color,power))
        layers.append((obj,wake))
    rng=random.Random(191)
    particles=[]
    for i in range(plan.get('sparkCount',120)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=rng.uniform(.013,.032))
        obj=bpy.context.object; obj.name='Wake / seeded warm cyan spark'; obj.data.materials.append(unlit(obj.name,(.1,.7,1) if i%3 else (1,.45,.12),plan.get('sparkPower',7))); particles.append((obj,rng.random(),rng.uniform(.04,.19),rng.random()*6.28))
    def point(u):
        x=max(0,min(1,u))*(len(points)-1); i=min(len(points)-2,int(x)); return lerp(points[i],points[i+1],x-i)
    def progress(clock):
        if not variable: return clock
        clock=max(0,min(1,clock))
        i=min(len(points)-2,max(0,bisect.bisect_right(passage_times,clock)-1))
        t=(clock-passage_times[i])/(passage_times[i+1]-passage_times[i])
        return (i+t)/(len(points)-1)
    beacon=None
    if plan.get('headBeacon'):
        settings=plan['headBeacon']
        beacon=sphere('Ship / brightest white-cyan tracking core',settings['radius'],unlit('Ship / luminous tracking core',(.65,.9,1),settings['power']),segments=24,rings=12)
    key_steps=plan.get('motionBlur',{}).get('keySamplesPerFrame',1)
    previous_yaw=None
    for step in range((scene.frame_end-1)*key_steps+1):
        frame=1+step/key_steps
        clock=(frame-1-travel_start)/travel_frames
        u=progress(clock)
        ship.location=point(u); ship.keyframe_insert('location',frame=frame)
        direction=point(min(1,max(.002,u+.002)))-point(max(0,min(.998,u-.002)))
        yaw=math.atan2(direction.y,direction.x)+math.pi/2
        if previous_yaw is not None:
            yaw=previous_yaw+(yaw-previous_yaw+math.pi)%(2*math.pi)-math.pi
        previous_yaw=yaw
        ship.rotation_euler.z=yaw
        ship.keyframe_insert('rotation_euler',frame=frame)
        if beacon:
            beacon.location=point(u); beacon.keyframe_insert('location',frame=frame)
        for obj,wake in layers:
            if continuous:
                continue
            obj.data.bevel_factor_end=u; obj.data.bevel_factor_start=max(0,u-.16) if wake else 0
            obj.data.keyframe_insert('bevel_factor_end',frame=frame); obj.data.keyframe_insert('bevel_factor_start',frame=frame)
        if (variable and step%key_steps==0) or (not variable and (frame-1)%4==0) or frame==scene.frame_end:
            for obj,age,spread,phase in particles:
                lag=age*plan.get('sparkLifetimeFrames',travel_frames*.18)
                particle_clock=clock-lag/travel_frames
                t=progress(particle_clock) if variable else particle_clock
                obj.location=point(t)+Vector((spread*math.sin(phase+frame*.11),spread*math.cos(phase+frame*.09),spread*.3))
                visible=0<particle_clock<1
                size=math.exp(-lag/4) if variable else max(.12,1-age)
                obj.scale=(size*int(visible),)*3; obj.keyframe_insert('location',frame=frame); obj.keyframe_insert('scale',frame=frame)
    linear_keys(ship)
    if beacon: linear_keys(beacon)
    if plan.get('motionBlur'):
        for obj in scene.objects:
            if obj.type=='MESH':
                obj.cycles.motion_steps=plan['motionBlur'].get('motionSteps',5)
                obj.cycles.use_motion_blur=True
    for obj,_ in layers: linear_keys(obj.data)
    for obj,_,_,_ in particles: linear_keys(obj)
    group=bpy.data.node_groups.new('Orbital glow / illustrated bloom','CompositorNodeTree'); group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor'); scene.compositing_node_group=group
    n,links=group.nodes,group.links; render=n.new('CompositorNodeRLayers'); socket=render.outputs['Image']
    for size,strength in [(.10,1.1),(.28,.65)]:
        glow=n.new('CompositorNodeGlare'); glow.inputs['Type'].default_value='Fog Glow'; glow.inputs['Quality'].default_value='High'; glow.inputs['Threshold'].default_value=.9; glow.inputs['Size'].default_value=size; glow.inputs['Strength'].default_value=strength; links.new(socket,glow.inputs['Image']); socket=glow.outputs['Image']
    links.new(socket,n.new('NodeGroupOutput').inputs['Image'])
    scene['method']='Actual 3D trajectory geometry, planetary depth occlusion and reused native ship geometry. Hybrid contains black depth stand-ins, not reconstructed visible terrain.'
    scene['song_start_frame']=1412; scene['edit_in_local_frame']=25; scene['edit_frames']=138
    scene['source_plate']=plan['source']; scene['native_limit']='Procedural look study; not an exact reconstruction of the illustrated source.'
    scene['flight_language']=plan.get('flightLanguage','legacy loops')
    scene['trail_decay_frames']=plan.get('trailLifetimeFrames',0)
    scene['velocity_model']=plan.get('velocityModel','constant arc speed')
    scene['motion_blur_shutter_frames']=plan.get('motionBlur',{}).get('shutterFrames',0)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest/('orbit-'+args.variant+'.blend')))
    if args.frames:
        for frame in map(int,args.frames.split(',')):
            scene.frame_set(frame); scene.render.filepath=str(dest/f'look-{frame:04}.png'); bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)


if __name__=='__main__': main()
