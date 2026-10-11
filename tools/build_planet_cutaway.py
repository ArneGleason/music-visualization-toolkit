"""Render an editable Blender image-plane drift for a planet cutaway review.

This is composition/motion blocking, not simulated axial rotation or true orbit.
Run Blender with --python this_file -- project.json planet-cutaway-v01.json.
"""
import json
import pathlib
import sys

import bpy


def main():
    args = sys.argv[sys.argv.index('--')+1:]
    project_path, plan_path = map(pathlib.Path, args[:2])
    base = project_path.resolve().parent
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    register = json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
    shot = next(s for s in register['storyboardProposals'] if s['id'] == plan['shot'])
    out = base/plan['output']
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = register['fps']
    scene.frame_start = 1
    scene.frame_end = shot['handles']['generatedFrames']
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    image = bpy.data.images.load(str(base/plan['image']))
    image.pack()
    aspect = image.size[0]/image.size[1]
    bpy.ops.mesh.primitive_plane_add(size=2)
    plane = bpy.context.object
    plane.name = 'Planet illustration / review projection only'
    plane.scale = (aspect, 1, 1)
    material = bpy.data.materials.new('Unlit original illustration')
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    texture = nodes.new('ShaderNodeTexImage')
    texture.image = image
    emission = nodes.new('ShaderNodeEmission')
    output = nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(texture.outputs['Color'], emission.inputs['Color'])
    material.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
    plane.data.materials.append(material)
    bpy.ops.object.camera_add(location=(0, 0, 10))
    camera = bpy.context.object
    camera.name = 'Gentle horizon drift / draft camera'
    camera.data.type = 'ORTHO'
    # Small overscan allows continuous drift without exposing an image edge.
    camera.data.ortho_scale = min(2*aspect, 2*1920/1080)*0.92
    scene.camera = camera
    for frame, x, y in [(1, -0.025, 0.012), (scene.frame_end, 0.025, -0.012)]:
        camera.location = (x, y, 10)
        camera.keyframe_insert(data_path='location', frame=frame)
    scene['shot_id'] = shot['id']
    scene['song_start_frame'] = shot['startFrame']
    scene['edit_in_local_frame'] = shot['handles']['editInLocalFrame']
    scene['note'] = 'Image-plane motion review; final orbital parallax to be generated after review.'
    scene.frame_set(1)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(out/'frames/frame-')
    (out/'frames').mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/plan['blendFilename']))
    bpy.ops.render.render(animation=True)
    print('Rendered planet draft:', scene.frame_end, 'frames')


if __name__ == '__main__':
    main()
