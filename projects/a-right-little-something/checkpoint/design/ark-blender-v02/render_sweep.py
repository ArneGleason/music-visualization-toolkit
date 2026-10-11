"""Render the saved camera rig. Vessel geometry stays fixed throughout."""
from pathlib import Path
import bpy

out = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(out/'headquarters-ark-v02.blend'))
scene = bpy.context.scene
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 120
scene.camera = bpy.data.objects['CAMERA / approved forward-quarter proof']
frames = out/'sweep-frames'
frames.mkdir(exist_ok=True)
scene.render.filepath = str(frames/'frame_')
for frame in (1, 60, 120):
    scene.frame_set(frame)
    pods = [o for o in scene.objects if o.name.startswith('POD_')]
    assert len(pods) == 6
    for row in range(1, 4):
        pair = [o for o in pods if o['structural_pair'] == row]
        assert abs(pair[0].matrix_world.translation.y + pair[1].matrix_world.translation.y) < 1e-6
        assert abs(pair[0].matrix_world.translation.z - pair[1].matrix_world.translation.z) < 1e-6
bpy.ops.render.render(animation=True)
