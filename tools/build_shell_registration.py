"""Render bright shell guides and an optional geodesic display network in Blender.

blender -b --python tools/build_shell_registration.py -- <storyboard.blend>
"""
import json
import math
import pathlib
import sys

import bpy
import bmesh
from mathutils import Vector


def main():
    source=pathlib.Path(sys.argv[sys.argv.index('--')+1]).resolve()
    out=source.parent
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=next(s for s in bpy.data.scenes if s.get('shot_id')=='opening-005')
    bpy.context.window.scene=scene
    scene.frame_set(1)
    ship=next(o for o in scene.objects if o.name.startswith('SHIP ROOT'))
    shell=next(o for o in scene.objects if o.name.startswith('Clear spherical cabin'))
    radius=shell.scale.x
    collection=bpy.data.collections.new('OPTIONAL / shell geodesic display')
    scene.collection.children.link(collection)

    # Dual of a triangular icosphere: mostly hexagons, twelve pentagonal
    # closures. Project every point back onto the sphere to avoid flat panels.
    mesh=bmesh.new()
    bmesh.ops.create_icosphere(mesh,subdivisions=3,radius=1)
    centres={f:sum((v.co for v in f.verts),Vector()).normalized() for f in mesh.faces}
    edges=[]
    for edge in mesh.edges:
        a,b=(centres[f] for f in edge.link_faces)
        edges.append((a,b))
    counts={n:sum(len(v.link_faces)==n for v in mesh.verts) for n in (5,6)}
    curve=bpy.data.curves.new('Spherical dual-icosphere cell edges','CURVE')
    curve.dimensions='3D';curve.bevel_depth=.006;curve.bevel_resolution=2
    for a,b in edges:
        spline=curve.splines.new('POLY');spline.points.add(4)
        for i,point in enumerate(spline.points):
            point.co=(*(a.lerp(b,i/4).normalized()*(radius-.004)),1)
    network=bpy.data.objects.new('Shell display / mostly hexagonal geodesic network',curve)
    collection.objects.link(network);network.parent=ship
    network['purpose']='Optional technological display and geometry registration; not structural seams'
    network['hexagonal_cells']=counts[6];network['pentagonal_closures']=counts[5]
    network['shell_assumption']='Ultra-thin, highly transparent, durable active material'
    material=bpy.data.materials.new('Shell network / low-opacity cyan emission')
    material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();links=material.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial')
    transparent=nodes.new('ShaderNodeBsdfTransparent')
    emission=nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value=(.12,.8,1,1)
    emission.inputs['Strength'].default_value=2
    mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.28
    links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2])
    links.new(mix.outputs[0],output.inputs['Surface'])
    curve.materials.append(material)

    # Neutral reference fill is separate from the story's coherent solar light.
    lightdata=bpy.data.lights.new('Registration fill / reference only','AREA')
    lightdata.energy=650;lightdata.shape='DISK';lightdata.size=5
    light=bpy.data.objects.new(lightdata.name,lightdata)
    collection.objects.link(light);light.location=scene.camera.location
    light.rotation_euler=scene.camera.rotation_euler
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
    scene.view_settings.exposure=.7
    scene.render.engine='CYCLES';scene.cycles.samples=32
    scene.render.resolution_x=1280;scene.render.resolution_y=720
    scene.render.image_settings.media_type='IMAGE';scene.render.image_settings.file_format='PNG'
    network.hide_render=True
    scene.render.filepath=str(out/'opening-005-neutral-registration.png')
    bpy.ops.render.render(write_still=True)
    network.hide_render=False
    scene.render.filepath=str(out/'opening-005-geodesic-registration.png')
    bpy.ops.render.render(write_still=True)
    scene['registration_guide']='Neutral fill and cyan network are reference aids; optional diegetic display'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'shell-registration-v01.blend'))
    (out/'shell-registration-manifest.json').write_text(json.dumps({
        'hexagonalCells':counts[6],'pentagonalClosures':counts[5],
        'sphereRadius':radius,'networkRadius':radius-.004,
        'referenceFillOnly':True,'baseStoryboardUnchanged':str(source)},indent=2)+'\n')
    mesh.free()


main()
