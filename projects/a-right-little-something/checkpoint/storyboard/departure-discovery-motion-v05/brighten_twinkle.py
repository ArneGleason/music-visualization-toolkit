"""Increase only the existing Blender twinkle; retain its timing and pullout."""
from pathlib import Path
import shutil
import bpy
import numpy as np

OUT=Path(__file__).resolve().parent
OLD=OUT.with_name('departure-discovery-motion-v04')
(OUT/'departure-frames').mkdir(exist_ok=True)
for source in (OLD/'departure-frames').glob('frame_*.png'):
    shutil.copy2(source,OUT/'departure-frames'/source.name)
bpy.ops.wm.open_mainfile(filepath=str(OLD/'departure-pullout-twinkle.blend'))
scene=bpy.context.scene
image=bpy.data.images['Procedural cyan station departure twinkle']
y,x=np.mgrid[0:1080,0:1920].astype(np.float32)
dx=(x-960)/2
dy=(y-(1079-514))/2
r2=dx*dx+dy*dy
light=2.5*(np.exp(-r2/5.0)*1.7 + np.exp(-r2/180.0)*.055
    + np.exp(-np.abs(dx)/18-np.abs(dy)/.8)*.42
    + np.exp(-np.abs(dx)/.8-np.abs(dy)/11)*.30)
rgba=np.ones((1080,1920,4),dtype=np.float32)
rgba[:,:,:3]=light[:,:,None]*np.array([.10,.78,1.0],dtype=np.float32)
image.pixels.foreach_set(rgba.ravel())
image.pack()
scene['station_twinkle']='V59: 2x spatial size and 2.5x linear light; same cyan and local1–17 pulse, peak6'
scene.render.filepath=str(OUT/'departure-frames/frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'departure-pullout-twinkle.blend'))
for frame in range(1,18):
    scene.frame_set(frame)
    scene.render.filepath=str(OUT/'departure-frames'/f'frame_{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
print('Brighter twinkle rendered; frames18–140 retained from V58.')
