"""Prove saved native scenes can render selected frames out of order."""
from pathlib import Path
import bpy,json,sys,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
checks=[('world',42),('orb',110),('meaning',150),('night',50),('room_late',65),('close_cloud',60),('return_cloud',70)]
records=[]
for family,frame in checks:
 D=O/family;bpy.ops.wm.open_mainfile(filepath=str(D/f'{family}_1280.blend'));s=bpy.context.scene
 s.frame_set(s.frame_end);s.frame_set(frame)
 for layer in s.view_layers:layer.use=True
 s.render.filepath=str(D/f'repeat_{frame:04d}.png');bpy.ops.render.render(write_still=True)
 a=cv2.imread(str(D/'native_1280'/f'{frame:04d}.png'));b=cv2.imread(s.render.filepath);error=np.abs(a.astype(float)-b)
 records.append({'family':family,'frame':frame,'max_difference':float(error.max()),'mean_difference':float(error.mean()),'passed':bool(error.mean()<.1)})
 (O/'autonomous_random_access.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
