"""Build and render an editable Blender ship/planet continuity experiment.

blender -b --python tools/build_ship_blockout.py -- projects/<song>/blockout.json
"""
import json
import math
import pathlib
import sys

import bpy
from mathutils import Vector


def main():
    config_path = pathlib.Path(sys.argv[sys.argv.index('--')+1]).resolve()
    config = json.loads(config_path.read_text(encoding='utf-8'))
    out = config_path.parent / config['output']
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = 'Sphere spacecraft / geometry experiment'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = config['render']['samples']
    scene.cycles.use_denoising = True
    scene.cycles.transparent_max_bounces = 12
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'OPTIX'
        prefs.get_devices()
        for device in prefs.devices:
            device.use = device.type != 'CPU'
        if any(d.use for d in prefs.devices):
            scene.cycles.device = 'GPU'
    except Exception as error:
        print('Using CPU render:', error)
    scene.render.resolution_x = config['render']['width']
    scene.render.resolution_y = config['render']['height']
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.fps = 24
    scene.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.new('Dark blue space')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (.025, .045, .075, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = .3
    scene.world = world

    def collection(name):
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        return c

    ship = collection('01 SHIP / reusable geometry')
    figure = collection('02 FIGURE / scale and pose proxy')
    planet = collection('03 PLANET / scale may be art directed')
    marks = collection('04 ORIENTATION / hide for clean compositions')
    cameras = collection('05 CAMERAS / shared geometry')
    refs = collection('06 REFERENCES / viewport only')
    lights = collection('07 LIGHTING')
    moons = collection('08 MOONS / independent artistic placement')

    def move(obj, coll):
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        coll.objects.link(obj)
        return obj

    def empty(name, coll, at=(0,0,0)):
        obj = bpy.data.objects.new(name, None)
        coll.objects.link(obj)
        obj.location = at
        return obj

    ship_root = empty('SHIP ROOT / bow -Y, engine +Y, up +Z', ship)
    planet_root = empty('PLANET ROOT / independent artistic scale', planet, config['planet']['location'])
    figure_root = empty('FIGURE ROOT / floating pose', figure)
    figure_root.parent = ship_root

    def material(name, color, metallic=0, rough=.4, emission=0):
        m = bpy.data.materials.new(name)
        m.diffuse_color = (*color,1)
        m.use_nodes = True
        p = m.node_tree.nodes.get('Principled BSDF')
        p.inputs['Base Color'].default_value = (*color,1)
        p.inputs['Metallic'].default_value = metallic
        p.inputs['Roughness'].default_value = rough
        p.inputs['Emission Color'].default_value = (*color,1)
        p.inputs['Emission Strength'].default_value = emission
        return m

    metal = material('Slate metal / structural masses', (.20,.25,.30), .65, .28)
    deck = material('Light decks / readable blockout', (.48,.53,.56), .35, .4)
    amber = material('Amber seam light', (1,.43,.08), .2, .3, 3)
    cyan = material('Cyan orientation and engine light', (.06,.65,1), .15, .3, 3)
    proxy = material('Warm figure proxy', (.65,.32,.17), 0, .58)
    face = material('Face direction patch', (.9,.68,.43), 0, .6)
    glass = bpy.data.materials.new('Clear shell / transparent centre, reflective rim')
    glass.use_nodes = True
    n = glass.node_tree.nodes
    n.clear()
    output = n.new('ShaderNodeOutputMaterial')
    transparent = n.new('ShaderNodeBsdfTransparent')
    reflective = n.new('ShaderNodeBsdfPrincipled')
    reflective.inputs['Base Color'].default_value = (.3,.64,.8,1)
    reflective.inputs['Metallic'].default_value = .8
    reflective.inputs['Roughness'].default_value = .12
    fresnel = n.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 1.18
    mix = n.new('ShaderNodeMixShader')
    links = glass.node_tree.links
    links.new(fresnel.outputs[0],mix.inputs[0])
    links.new(transparent.outputs[0],mix.inputs[1])
    links.new(reflective.outputs[0],mix.inputs[2])
    links.new(mix.outputs[0],output.inputs[0])
    glass.diffuse_color = (.3,.6,.8,.08)

    def finish(obj, name, mat, coll, parent=None):
        obj.name = name
        move(obj,coll)
        if mat:
            obj.data.materials.append(mat)
        if parent:
            obj.parent = parent
        if obj.type == 'MESH':
            for p in obj.data.polygons:
                p.use_smooth = True
        return obj

    def sphere(name, location, scale, mat, coll, parent=None):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=location)
        o = finish(bpy.context.object,name,mat,coll,parent)
        o.scale = scale
        return o

    def torus(name, radius, tube, z, mat, coll=ship, parent=ship_root, at=None, vertical=False):
        bpy.ops.mesh.primitive_torus_add(major_radius=radius,minor_radius=tube,major_segments=96,minor_segments=12,location=at or (0,0,z))
        o = finish(bpy.context.object,name,mat,coll,parent)
        if vertical:
            o.rotation_euler.x = math.pi/2
        return o

    def annulus(name, radius, width, height, z, mat, at=None, vertical=False):
        verts, faces = [], []
        for zz,rr in [(-height/2,radius-width/2),(-height/2,radius+width/2),(height/2,radius-width/2),(height/2,radius+width/2)]:
            for i in range(96):
                a=i*math.tau/96
                verts.append((rr*math.cos(a),rr*math.sin(a),zz))
        for i in range(96):
            j=(i+1)%96
            for a,b in [(0,1),(1,3),(3,2),(2,0)]:
                faces.append((a*96+i,a*96+j,b*96+j,b*96+i))
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata(verts,[],faces)
        obj=bpy.data.objects.new(name,mesh)
        ship.objects.link(obj)
        obj.location=at or (0,0,z)
        if vertical:
            obj.rotation_euler.x=math.pi/2
        obj.parent=ship_root
        obj.data.materials.append(mat)
        bevel=obj.modifiers.new('Soft blockout edges','BEVEL')
        bevel.width=.035
        bevel.segments=2
        return obj

    def cylinder(name, location, radius, depth, mat, coll=ship, parent=ship_root):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=location)
        return finish(bpy.context.object,name,mat,coll,parent)

    def line(name, points, radius, mat, coll, parent=None):
        curve=bpy.data.curves.new(name,'CURVE')
        curve.dimensions='3D'
        curve.bevel_depth=radius
        curve.bevel_resolution=2
        s=curve.splines.new('POLY')
        s.points.add(len(points)-1)
        for p,v in zip(s.points,points):
            p.co=(*v,1)
        obj=bpy.data.objects.new(name,curve)
        coll.objects.link(obj)
        obj.data.materials.append(mat)
        obj.parent=parent
        return obj

    d=config['ship']
    sphere('Clear spherical cabin', (0,0,0), (d['radius'],)*3,glass,ship,ship_root)
    annulus('Broad equatorial band',d['ringRadius'],d['ringWidth'],d['ringHeight'],0,metal)
    for z in [-d['ringHeight']/2,d['ringHeight']/2]:
        torus('Equator amber seam',d['ringRadius']+.22,.018,z,amber)
    for sign, label in [(-1,'Lower'),(1,'Upper')]:
        z=sign*d['platformZ']
        cylinder(label+' circular platform',(0,0,z),d['platformRadius'],.16,deck)
        torus(label+' platform rim',d['platformRadius'],.035,z,amber)
        torus(label+' inset orientation circle',d['platformRadius']*.72,.009,z-sign*.09,metal)
        cylinder(label+' hub',(0,0,z-sign*.09),.13,.012,amber)
    engine=(0,d['engineY'],.15)
    annulus('Vertical aft engine ring',d['engineRadius'],.28,.32,0,metal,at=engine,vertical=True)
    for y in [d['engineY']-.18,d['engineY']+.18]:
        torus('Engine circular light',d['engineRadius']-.15,.035,0,cyan,at=(0,y,.15),vertical=True)
    for x in [-.55,.55]:
        line('Engine bridge strut',[(x,2.95,-.1),(x,3.2,-.5),(x,3.65,-.8)],.09,metal,ship,ship_root)
    for i in range(16):
        a=i*math.tau/16
        line('Equator navigation tick',[(3.08*math.cos(a),3.08*math.sin(a),.15),(3.4*math.cos(a),3.4*math.sin(a),.15)],.016,cyan if i%4==0 else amber,marks,ship_root)
    # Distinct bow wedge makes camera/character direction readable.
    line('BOW / negative Y chevron',[(-.16,-3.43,.18),(0,-3.16,.18),(.16,-3.43,.18)],.03,cyan,marks,ship_root)

    sphere('Torso',(-.02,0,.48),(.25,.16,.40),proxy,figure,figure_root)
    sphere('Pelvis',(.16,0,.02),(.23,.16,.19),proxy,figure,figure_root)
    sphere('Head',(-.13,0,1.04),(.19,.17,.24),proxy,figure,figure_root)
    sphere('Face / looking towards bow',(-.13,-.147,1.04),(.12,.045,.14),face,figure,figure_root)
    for name, pts in [
        ('Left arm',[(-.22,0,.75),(-.45,-.07,.40),(-.64,-.12,.10)]),
        ('Right arm',[(.21,0,.75),(.44,-.05,.51),(.67,-.12,.38)]),
        ('Left leg',[(.02,0,.01),(.22,-.09,-.52),(-.01,-.16,-.98)]),
        ('Right leg',[(.28,0,.01),(.51,.08,-.46),(.35,.08,-.88)])]:
        line(name,pts,.085,proxy,figure,figure_root)
        for j,v in enumerate(pts):
            sphere(name+f' joint {j}',v,(.092,)*3,proxy,figure,figure_root)

    planet_mat=material('Globe placeholder / blue-grey checker',(.08,.20,.27),.1,.8)
    nodes=planet_mat.node_tree.nodes
    tex=nodes.new('ShaderNodeTexChecker')
    tex.inputs['Color1'].default_value=(.025,.07,.12,1)
    tex.inputs['Color2'].default_value=(.10,.21,.25,1)
    tex.inputs['Scale'].default_value=7
    planet_mat.node_tree.links.new(tex.outputs['Color'],nodes['Principled BSDF'].inputs['Base Color'])
    radius=config['planet']['radius']
    globe=sphere('Placeholder globe', (0,0,0),(radius,)*3,planet_mat,planet,planet_root)
    grid_mat=material('Globe latitude longitude',(.16,.38,.45),0,.6,.15)
    for latitude in [-60,-30,0,30,60]:
        a=math.radians(latitude)
        rr=(radius+.03)*math.cos(a)
        zz=(radius+.03)*math.sin(a)
        pts=[(rr*math.cos(i*math.tau/144),rr*math.sin(i*math.tau/144),zz) for i in range(145)]
        line(f'Latitude {latitude}',pts,.025,amber if latitude==0 else grid_mat,planet,planet_root)
    for longitude in range(0,180,30):
        a=math.radians(longitude)
        pts=[((radius+.03)*math.cos(t)*math.cos(a),(radius+.03)*math.cos(t)*math.sin(a),(radius+.03)*math.sin(t)) for t in [i*math.tau/144 for i in range(145)]]
        line(f'Meridian {longitude}',pts,.025,grid_mat,planet,planet_root)
    sphere('Globe north pole marker',(0,0,radius+.05),(.28,)*3,cyan,planet,planet_root)

    for moon in config.get('moons', []):
        root = empty(moon['name'] + ' ROOT', moons, moon['location'])
        root['purpose'] = 'Art-directed size and placement; shared sunlight'
        for key in ('id', 'surface', 'identity'):
            root[key] = moon.get(key, '')
        mat = material(moon['name'] + ' matte rock', moon['color'], 0, .85)
        noise = mat.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 8
        noise.inputs['Detail'].default_value = 3
        bump = mat.node_tree.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .35
        bump.inputs['Distance'].default_value = .12
        mat.node_tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        mat.node_tree.links.new(bump.outputs['Normal'], mat.node_tree.nodes['Principled BSDF'].inputs['Normal'])
        if moon.get('surface') in ('volcanic', 'ice'):
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            shader = nodes['Principled BSDF']
            coords = nodes.new('ShaderNodeTexCoord')
            # Object-local coordinates keep the surface fixed when the moon moves.
            distort = nodes.new('ShaderNodeVectorMath')
            distort.operation = 'SCALE'
            distort.inputs['Scale'].default_value = .22
            links.new(noise.outputs['Color'], distort.inputs[0])
            add = nodes.new('ShaderNodeVectorMath')
            add.operation = 'ADD'
            links.new(coords.outputs['Generated'], add.inputs[0])
            links.new(distort.outputs['Vector'], add.inputs[1])
            cracks = nodes.new('ShaderNodeTexVoronoi')
            cracks.feature = 'DISTANCE_TO_EDGE'
            cracks.inputs['Scale'].default_value = 5
            links.new(add.outputs['Vector'], cracks.inputs['Vector'])
            ramp = nodes.new('ShaderNodeValToRGB')
            ramp.color_ramp.elements[0].position = .015
            ramp.color_ramp.elements[1].position = .045
            volcanic = moon['surface'] == 'volcanic'
            ramp.color_ramp.elements[0].color = (1,.12,.003,1) if volcanic else (.025,.16,.3,1)
            ramp.color_ramp.elements[1].color = (*moon['color'],1)
            links.new(cracks.outputs['Distance'], ramp.inputs[0])
            links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
            shader.inputs['Roughness'].default_value = .85 if volcanic else .38
            if volcanic:
                mask = nodes.new('ShaderNodeMath')
                mask.operation = 'LESS_THAN'
                mask.inputs[1].default_value = .025
                links.new(cracks.outputs['Distance'], mask.inputs[0])
                glow = nodes.new('ShaderNodeMath')
                glow.operation = 'MULTIPLY'
                glow.inputs[1].default_value = 3
                links.new(mask.outputs[0], glow.inputs[0])
                links.new(glow.outputs[0], shader.inputs['Emission Strength'])
                shader.inputs['Emission Color'].default_value = (1,.12,.003,1)
        body = sphere(moon['name'], (0,0,0), (moon['radius'],)*3, mat, moons, root)
        body['celestial_id'] = moon.get('id', '')
        body['visual_identity'] = moon.get('identity', '')

    studio_lights = [
        ('Warm key',(-5,-7,9),1800,7,(1,.73,.45)),
        ('Cool fill',(8,-2,5),1200,6,(.35,.65,1)),
        ('Rear edge',(0,6,7),2200,5,(1,.5,.18))]
    for name,location,power,size,color in ([] if 'sun' in config else studio_lights):
        data=bpy.data.lights.new(name,'AREA')
        data.energy=power;data.shape='DISK';data.size=size;data.color=color
        obj=bpy.data.objects.new(name,data);lights.objects.link(obj);obj.location=location
        obj.rotation_euler=(Vector((0,0,0))-obj.location).to_track_quat('-Z','Y').to_euler()
    # One distant source gives the ship, planet and moons coherent lit sides.
    solar = config.get('sun', {})
    sun_data=bpy.data.lights.new('Shared distant sun','SUN')
    sun_data.energy=solar.get('energy',1.6)
    sun_data.angle=solar.get('angle',.15)
    sun_data.color=solar.get('color',(1,1,1))
    sun=bpy.data.objects.new('Shared distant sun',sun_data);lights.objects.link(sun)
    if 'towards' in solar:
        sun.rotation_euler=(-Vector(solar['towards'])).to_track_quat('-Z','Y').to_euler()
        sun['direction_towards_source']=solar['towards']
    else:
        sun.rotation_euler=(.4,-.5,-.7)

    camera_objs={}
    for name,view in config['cameras'].items():
        data=bpy.data.cameras.new(name)
        obj=bpy.data.objects.new(name,data);cameras.objects.link(obj)
        obj.location=view['location'];obj.rotation_euler=(Vector(view['target'])-obj.location).to_track_quat('-Z','Y').to_euler()
        if 'ortho' in view:
            data.type='ORTHO';data.ortho_scale=view['ortho']
        else:
            data.lens=view['lens']
        data.clip_end=1000
        obj['planet_scale_override']=view.get('planetScale',1)
        obj['purpose']='Composition study; shared ship, independent planet scale'
        camera_objs[name]=obj
    for i,path in enumerate(config['references']):
        img=bpy.data.images.load(str(config_path.parent/path))
        img.pack()
        obj=empty('Reference '+pathlib.Path(path).stem,refs,(-7+i*7,8,4))
        obj.empty_display_type='IMAGE';obj.data=img;obj.empty_display_size=6
        obj.hide_render=True
    refs.hide_viewport=True

    # A separate inspection camera leaves every storyboard camera editable.
    inspect_data=camera_objs['Exterior'].data.copy()
    inspect_camera=bpy.data.objects.new('Inspection arc / 3 seconds, not song timing',inspect_data)
    cameras.objects.link(inspect_camera)
    target=Vector(config['cameras']['Exterior']['target'])
    start=Vector(config['cameras']['Exterior']['location'])
    radius=math.hypot(start.x-target.x,start.y-target.y)
    angle=math.atan2(start.y-target.y,start.x-target.x)
    for frame,delta in [(1,0),(36,math.radians(12)),(72,math.radians(24))]:
        inspect_camera.location=(target.x+radius*math.cos(angle+delta),target.y+radius*math.sin(angle+delta),start.z)
        inspect_camera.rotation_euler=(target-inspect_camera.location).to_track_quat('-Z','Y').to_euler()
        inspect_camera.keyframe_insert('location',frame=frame)
        inspect_camera.keyframe_insert('rotation_euler',frame=frame)
    scene.frame_start=1;scene.frame_end=72;scene.frame_set(1)
    scene.timeline_markers.new('DESIGN INSPECTION / separate from music edit',frame=1)

    scene['notes']='Shared editable ship geometry. Bow=-Y; aft engine=+Y; up=+Z. Figure is a scale proxy. Globe/camera proportions are artistic assumptions. Orientation collection may be hidden.'
    scene['source_config']=str(config_path)
    scene.camera=camera_objs['Exterior']
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_perspective='CAMERA'
                area.spaces.active.shading.type='MATERIAL'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'sphere-ship-blockout.blend'))
    manifest=[]
    for name, camera in camera_objs.items():
        scene.camera=camera
        planet_root.scale=(camera['planet_scale_override'],)*3
        planet.hide_render='layout' in name
        moons.hide_render='layout' in name
        scene.render.filepath=str(out/(name.lower().replace(' ','-')+'.png'))
        bpy.ops.render.render(write_still=True)
        manifest.append({'camera':name,'image':scene.render.filepath})
    planet.hide_render=False;moons.hide_render=False;planet_root.scale=(1,1,1);scene.camera=camera_objs['Exterior']
    scene.render.filepath=str(out/'exterior.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'sphere-ship-blockout.blend'))
    (out/'views.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    if '--motion' in sys.argv:
        scene.camera=inspect_camera
        scene.render.resolution_x=854;scene.render.resolution_y=480
        scene.cycles.samples=8
        scene.render.image_settings.media_type='VIDEO'
        scene.render.image_settings.file_format='FFMPEG'
        scene.render.ffmpeg.format='MPEG4'
        scene.render.ffmpeg.codec='H264'
        scene.render.ffmpeg.constant_rate_factor='MEDIUM'
        scene.render.filepath=str(out/'inspection-arc.mp4')
        bpy.ops.render.render(animation=True)
    print('BLOCKOUT COMPLETE',out,flush=True)


main()
