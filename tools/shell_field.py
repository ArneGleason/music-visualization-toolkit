"""Shared ultra-thin shell and editable geodesic display for Blender scenes."""
import bpy
import bmesh
from mathutils import Vector


def add_shell_field(scene, parent, radius, opacity=.12):
    mesh=bmesh.new()
    bmesh.ops.create_icosphere(mesh,subdivisions=3,radius=1)
    centres={f:sum((v.co for v in f.verts),Vector()).normalized() for f in mesh.faces}
    curve=bpy.data.curves.new('Geodesic field / shared topology','CURVE')
    curve.dimensions='3D';curve.bevel_depth=.004;curve.bevel_resolution=1
    for edge in mesh.edges:
        a,b=(centres[f] for f in edge.link_faces)
        spline=curve.splines.new('POLY');spline.points.add(4)
        for i,point in enumerate(spline.points):
            point.co=(*(a.lerp(b,i/4).normalized()*(radius-.004)),1)
    network=bpy.data.objects.new('Thin field / faint geodesic network',curve)
    scene.collection.objects.link(network);network.parent=parent
    network['hexagonal_cells']=sum(len(v.link_faces)==6 for v in mesh.verts)
    network['pentagonal_closures']=sum(len(v.link_faces)==5 for v in mesh.verts)
    network['purpose']='Ultra-thin active shell display; not structural window seams'
    material=bpy.data.materials.new('Thin field / cyan display')
    material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();links=material.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial')
    transparent=nodes.new('ShaderNodeBsdfTransparent')
    emission=nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value=(.12,.8,1,1)
    emission.inputs['Strength'].default_value=1.5
    mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=opacity
    links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2])
    links.new(mix.outputs[0],output.inputs['Surface'])
    curve.materials.append(material);mesh.free()
    return network
