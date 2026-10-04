"""Render a native ship with distant illustration plate and separate actor card."""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


def main():
    project = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
    out = project / 'generated/storyboard/hybrid-ship-v01'
    bpy.ops.wm.open_mainfile(filepath=str(project / 'generated/storyboard/opening-v02/opening-storyboard-v01.blend'))
    scene = next(s for s in bpy.data.scenes if s.name.startswith('opening-004'))
    bpy.context.window.scene = scene
    for other in list(bpy.data.scenes):
        if other != scene:
            bpy.data.scenes.remove(other)
    scene.name = 'Hybrid / rigid ship, distant plate, illustrated actor'
    scene.frame_set(13)
    bpy.context.view_layer.update()
    root = next(o for o in scene.objects if o.name.startswith('SHIP ROOT'))
    camera = scene.camera
    camera.data.clip_end = 100000
    scene['experiment'] = 'Native rigid ship; far static celestial plate; flat illustrated actor, limited camera angles'

    def ancestor(obj, prefix):
        while obj:
            if obj.name.startswith(prefix):
                return True
            obj = obj.parent
        return False

    for obj in scene.objects:
        if any(ancestor(obj, name) for name in ('FIGURE ROOT', 'PLANET ROOT', 'Moon A', 'Moon B')):
            obj.hide_render = True
    # Retain the same complete ring/platform/engine geometry and clear shell.
    for name, color, metal, rough in (
        ('Slate metal / structural masses', (.12, .14, .16, 1), .55, .34),
        ('Light decks / readable blockout', (.23, .22, .20, 1), .45, .38)):
        material = bpy.data.materials.get(name)
        shader = material.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Base Color'].default_value = color
        shader.inputs['Metallic'].default_value = metal
        shader.inputs['Roughness'].default_value = rough

    def material(name, color, emission=0, metal=0, rough=.4):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        shader = mat.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Base Color'].default_value = (*color, 1)
        shader.inputs['Metallic'].default_value = metal
        shader.inputs['Roughness'].default_value = rough
        shader.inputs['Emission Color'].default_value = (*color, 1)
        shader.inputs['Emission Strength'].default_value = emission
        return mat

    trim = material('Hybrid / dark panel seams', (.028, .032, .036), metal=.3)
    nav = material('Hybrid / icy cyan rectangular lamps', (.10, .65, 1), 4)
    amber = bpy.data.materials['Amber seam light']
    shader = amber.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Emission Color'].default_value = (1, .22, .025, 1)
    shader.inputs['Emission Strength'].default_value = 1.5
    cyan_shader = bpy.data.materials['Cyan orientation and engine light'].node_tree.nodes.get('Principled BSDF')
    cyan_shader.inputs['Emission Color'].default_value = (.02, .30, 1, 1)
    cyan_shader.inputs['Emission Strength'].default_value = 1.5

    def curve(name, points, radius, mat):
        data = bpy.data.curves.new(name, 'CURVE')
        data.dimensions = '3D'
        data.bevel_depth = radius
        data.bevel_resolution = 1
        spline = data.splines.new('POLY')
        spline.points.add(len(points) - 1)
        for point, co in zip(spline.points, points):
            point.co = (*co, 1)
        obj = bpy.data.objects.new(name, data)
        scene.collection.objects.link(obj)
        obj.parent = root
        data.materials.append(mat)
        return obj

    for i in range(32):
        angle = i * math.tau / 32
        c, s = math.cos(angle), math.sin(angle)
        curve('Equator / radial plate seam', [(3.026*c, 3.026*s, .147),
            (3.475*c, 3.475*s, .147), (3.475*c, 3.475*s, -.147)], .006, trim)
    for i in range(12):
        angle = i * math.tau / 12
        bpy.ops.mesh.primitive_cube_add(size=1, location=(3.484*math.cos(angle), 3.484*math.sin(angle), 0))
        lamp = bpy.context.object
        lamp.name = 'Equator / rectangular cyan nav lamp'
        lamp.parent = root
        lamp.scale = (.028, .20, .055)
        lamp.rotation_euler.z = angle
        lamp.data.materials.append(nav)
        bevel = lamp.modifiers.new('Soft lamp corners', 'BEVEL')
        bevel.width = .035
        bevel.segments = 3
    for sign in (-1, 1):
        z = sign * 2.08
        for i in range(16):
            angle = i * math.tau / 16
            curve('Platform / radial inset seam', [(r*math.cos(angle), r*math.sin(angle), z+sign*.084)
                for r in (.34, 1.66)], .004, trim)
        bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.67, depth=.055, location=(0, 0, z-sign*.10))
        rim = bpy.context.object
        rim.name = 'Platform / layered underside metal rim'
        rim.parent = root
        rim.data.materials.append(bpy.data.materials['Slate metal / structural masses'])

    def image_material(name, path, transparent=False):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = bpy.data.images.load(str(path))
        texture.image.pack()
        emission = nodes.new('ShaderNodeEmission')
        mat.node_tree.links.new(texture.outputs['Color'], emission.inputs['Color'])
        output = nodes.new('ShaderNodeOutputMaterial')
        if transparent:
            clear = nodes.new('ShaderNodeBsdfTransparent')
            mix = nodes.new('ShaderNodeMixShader')
            mat.node_tree.links.new(texture.outputs['Alpha'], mix.inputs[0])
            mat.node_tree.links.new(clear.outputs[0], mix.inputs[1])
            mat.node_tree.links.new(emission.outputs[0], mix.inputs[2])
            mat.node_tree.links.new(mix.outputs[0], output.inputs['Surface'])
            mat.surface_render_method = 'DITHERED'
        else:
            mat.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
        return mat, texture.image

    def card(name, location, width, height, rotation, mat):
        bpy.ops.mesh.primitive_plane_add(size=2, location=location)
        obj = bpy.context.object
        obj.name = name
        obj.rotation_euler = rotation
        obj.scale = (width/2, height/2, 1)
        obj.data.materials.append(mat)
        obj['purpose'] = name
        return obj

    backdrop, image = image_material('Hybrid / distant illustrated environment',
        project / 'generated/storyboard/opening-v02/opening-001-starting-frame-v01.png')
    distance = 50000
    quaternion = camera.rotation_euler.to_quaternion()
    position = camera.location + quaternion @ Vector((0, 0, -distance))
    width = 2 * distance * math.tan(camera.data.angle_x/2) * 1.05
    plate = card('DISTANT PLATE / planet, moons and stars; no near moon meshes',
        position, width, width*9/16, camera.rotation_euler, backdrop)
    plate['distance_ship_radii'] = distance / 3
    actor_mat, actor_image = image_material('Hybrid / Harper RGBA actor', out / 'harper-cutout-v01.png', True)
    # Single facing card for this restrained exterior widening experiment.
    actor = card('HARPER / illustrated actor card; limited view angle', (0, 0, .10),
        2.6 * actor_image.size[0] / actor_image.size[1], 2.6,
        camera.rotation_euler, actor_mat)
    actor.parent = root
    for frame, z in ((1, .08), (122, .16)):
        actor.location.z = z
        actor.keyframe_insert('location', frame=frame)
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'AREA':
            obj.data.energy *= 2
    fill_data = bpy.data.lights.new('Hybrid / warm broad key', 'AREA')
    fill_data.energy = 1700
    fill_data.shape = 'DISK'
    fill_data.size = 7
    fill_data.color = (1, .80, .59)
    fill = bpy.data.objects.new(fill_data.name, fill_data)
    scene.collection.objects.link(fill)
    fill.location = (7, -7, 10)
    fill.rotation_euler = (-fill.location).to_track_quat('-Z', 'Y').to_euler()
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
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
    except Exception:
        pass
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.frame_start = 1
    scene.frame_end = 122
    scene.frame_set(13)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'hybrid-ship-v01.blend'))
    scene.render.filepath = str(out / 'hybrid-edit-in.png')
    bpy.ops.render.render(write_still=True)
    (out / 'manifest.json').write_text(json.dumps({'sourceShot': 'opening-004', 'fps': 24,
        'framesWithHandles': 122, 'editFrames': 98, 'leadInFrames': 12, 'leadOutFrames': 12,
        'resolution': [1920, 1080], 'actor': 'Flat RGBA card; no articulated animation',
        'ship': 'Native rigid mesh/curves, refinements to panel seams, lamps and platform rims',
        'celestials': 'One world-space image plate at 50000 units; no nearby moon geometry'}, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
