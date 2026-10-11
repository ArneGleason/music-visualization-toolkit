"""Save useful startup framing and embedded documentation; geometry unchanged."""
from pathlib import Path
import bpy
from mathutils import Vector

out = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(out/'headquarters-ark-v02.blend'))
scene = bpy.context.scene
scene.frame_set(49)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_location = Vector((0, 0, .6))
            area.spaces.active.region_3d.view_distance = 34
            area.spaces.active.region_3d.view_rotation = scene.camera.rotation_euler.to_quaternion()
            area.spaces.active.shading.type = 'SOLID'
            area.spaces.active.shading.color_type = 'MATERIAL'
for material in bpy.data.materials:
    shader = material.node_tree.nodes.get('Principled BSDF') if material.node_tree else None
    if shader:
        material.diffuse_color = shader.inputs['Base Color'].default_value
for obj in scene.objects:
    obj.select_set(False)
root = bpy.data.objects['ARK_ROOT / animate this transform']
root.select_set(True)
bpy.context.view_layer.objects.active = root
notes = bpy.data.texts.new('READ ME / headquarters ark model')
notes.write((out.parents[2]/'ARK-BLENDER-MODEL.md').read_text(encoding='utf-8'))
builder = bpy.data.texts.new('Build source / build_ark.py')
builder.write((out/'build_ark.py').read_text(encoding='utf-8'))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'headquarters-ark-v02.blend'))
print('Startup framing and model notes embedded; geometry and animation unchanged.')
