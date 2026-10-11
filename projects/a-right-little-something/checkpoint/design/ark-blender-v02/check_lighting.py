from pathlib import Path
import bpy

out = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(out/'headquarters-ark-v02.blend'))
scene = bpy.context.scene
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.cycles.samples = 32
for obj in scene.objects:
    if obj.type == 'LIGHT':
        obj.visible_transmission = False
        obj.data.specular_factor = .10
        print(obj.name, obj.visible_glossy, obj.visible_transmission)
scene.render.filepath = str(out/'glass-lighting-test.png')
for pod in [obj for obj in scene.objects if obj.name.startswith('POD_')]:
    data = bpy.data.lights.new('Internal habitat illumination', 'AREA')
    obj = bpy.data.objects.new('Internal habitat illumination / '+pod.name, data)
    scene.collection.objects.link(obj)
    obj.parent = pod
    obj.location = (0, 0, 2.10)
    data.energy = 24
    data.color = (.75, .85, .82)
    data.shape = 'RECTANGLE'
    data.size = 2
    data.size_y = 2
    obj.visible_glossy = False
    obj.visible_transmission = False
scene.render.filepath = str(out/'glass-internal-lighting-test.png')
bpy.ops.render.render(write_still=True)
