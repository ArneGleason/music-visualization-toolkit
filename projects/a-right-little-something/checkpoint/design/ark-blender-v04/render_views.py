"""Render additional look proofs from the saved model, with the GPU explicit."""
import argparse
from pathlib import Path
import sys
import bpy
from mathutils import Vector

out=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--views',default='aft,detail')
parser.add_argument('--width',type=int,default=1600)
parser.add_argument('--samples',type=int,default=96)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(out/'headquarters-ark-v04.blend'))
scene=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX'
prefs.get_devices()
for device in prefs.devices:
    device.use=device.type=='OPTIX'
scene.cycles.device='GPU'
print('Render devices: '+str([(d.name,d.type,d.use) for d in prefs.devices]),flush=True)
scene.cycles.samples=args.samples
scene.cycles.use_denoising=True
scene.render.resolution_x=args.width
scene.render.resolution_y=round(args.width*9/16)
for material in bpy.data.materials:
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type=='AMBIENT_OCCLUSION':
                node.samples=4
scene.frame_set(49)
camera=scene.camera
camera.parent=None
views={'hero':((-25,-32,25),(0,0,.45),30),'aft':((28,-34,27),(0,0,.45),30),
       'detail':((-14,-18,13),(-3,-2,.7),17)}
for view in args.views.split(','):
    pos,target,scale=views[view]
    camera.location=pos
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=scale
    scene.render.filepath=str(out/f'illustrated-{view}.png')
    print('Render view: '+view,flush=True)
    bpy.ops.render.render(write_still=True)
