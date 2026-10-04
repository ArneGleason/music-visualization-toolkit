"""Native locked-camera field test: stable junctions and traveling brightness."""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


def glow(name, opacity):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    clear = nodes.new('ShaderNodeBsdfTransparent')
    light = nodes.new('ShaderNodeEmission')
    light.inputs['Color'].default_value = (.10, .65, 1, 1)
    light.inputs['Strength'].default_value = 1.5
    mix = nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = opacity
    links = mat.node_tree.links
    links.new(clear.outputs[0], mix.inputs[1])
    links.new(light.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], out.inputs['Surface'])
    return mat, mix.inputs[0]


def main():
    project = Path(sys.argv[sys.argv.index('--')+1]).resolve()
    dest = project/'generated/storyboard/energy-field-v01'
    dest.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(project/'generated/storyboard/hybrid-ship-v01/hybrid-ship-v01.blend'))
    scene = bpy.context.scene
    shot = next(s for s in json.loads((project/'shots/shotlist.json').read_text())['shots'] if s['id']=='opening-004')
    lead = shot['handles']['leadInFrames']
    count = lead+shot['frames']+shot['handles']['leadOutFrames']
    scene.frame_set(lead+1)
    bpy.context.view_layer.update()
    scene.camera.animation_data_clear()
    network = next(o for o in scene.objects if o.name.startswith('Thin field / faint geodesic network'))
    rig = bpy.data.objects.new('FIELD DISPLAY / independent slow rotation', None)
    scene.collection.objects.link(rig)
    rig.parent = network.parent
    network.hide_render = True
    network.hide_set(True)
    junctions = {}
    direction = Vector((.8, -.3, .55)).normalized()
    for index, spline in enumerate(network.data.splines):
        coords = [p.co.xyz.copy() for p in spline.points]
        for co in (coords[0], coords[-1]):
            junctions[tuple(round(v, 5) for v in co)] = co
        curve = bpy.data.curves.new(f'Energy edge {index:03}', 'CURVE')
        curve.dimensions = '3D'
        curve.bevel_depth = .004
        curve.bevel_resolution = 1
        line = curve.splines.new('POLY')
        line.points.add(len(coords)-1)
        for point, co in zip(line.points, coords):
            point.co = (*co, 1)
        obj = bpy.data.objects.new(curve.name, curve)
        scene.collection.objects.link(obj)
        obj.parent = rig
        mat, intensity = glow(f'Energy / edge {index:03}', .02)
        curve.materials.append(mat)
        phase = sum(coords, Vector())/len(coords)
        # A broad traveling activation front, with a weaker second swell.
        # Fixed topology and steady junctions; only the line opacity changes.
        for frame in range(1, count+1, 4):
            t = (frame-1)/24
            wave = (.5+.5*math.sin(phase.dot(direction)*1.7-t*1.35))**4
            swell = (.5+.5*math.sin(phase.z*2.1+t*.7))**6
            intensity.default_value = .012+.19*wave+.035*swell
            intensity.keyframe_insert('default_value', frame=frame)
    dot_mat, _ = glow('Energy / steady junction dots', .23)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=.012)
    first = bpy.context.object
    first.name = 'Energy junction 000'
    first.data.materials.append(dot_mat)
    for index, co in enumerate(junctions.values()):
        dot = first if index == 0 else bpy.data.objects.new(f'Energy junction {index:03}', first.data)
        if index:
            scene.collection.objects.link(dot)
        dot.parent = rig
        dot.location = co
    for frame, angle in ((1, 0), (count, 6)):
        rig.rotation_euler.z = math.radians(angle)
        rig.keyframe_insert('rotation_euler', frame=frame)
    scene.frame_start = 1
    scene.frame_end = count
    scene.cycles.samples = 8
    scene['field_behavior'] = 'Steady junction dots; continuous geodesic edges; traveling energy brightness; six-degree display-only rotation; camera fixed'
    scene.frame_set(lead+1)
    scene.render.filepath = str(dest/'energy-edit-in.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(dest/'energy-field-v01.blend'))
    bpy.ops.render.render(write_still=True)
    (dest/'manifest.json').write_text(json.dumps({'sourceShot': shot['id'],
        'fps': 24, 'frames': count, 'editFrames': shot['frames'], 'leadInFrames': lead,
        'leadOutFrames': shot['handles']['leadOutFrames'], 'rotationDegrees': 6,
        'junctionCount': len(junctions), 'camera': 'Locked', 'paidGeneration': False}, indent=2))
    scene.render.filepath = str(dest/'frames/frame_')
    bpy.ops.render.render(animation=True)


if __name__ == '__main__':
    main()
