"""Resume-safe native outro renders; no production promotion."""
from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent;R=O.parents[1]
B='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
jobs=[('tv_late','tv_late_native.py',105,[15,65,92,105]),
      ('close_cloud','close_cloud_native.py',84,[1,36,60,84]),
      ('return_cloud','return_cloud_native.py',88,[1,20,50,70,88]),
      ('afterglow_b1','afterglow_native.py',191,[68,78,97]),
      ('afterglow_b2','afterglow_native.py',191,[12,90,155]),
      ('tv','tv_native.py',191,[13,54,111,156])]
for family,script,count,samples in jobs:
 d=O/family
 # TV vector builders take only width; lighting builders also take family.
 args=([family] if script in ('afterglow_native.py','close_cloud_native.py','return_cloud_native.py') else [])
 with (d/'queue_1080.log').open('w') as log:
  subprocess.run([B,'-b','-t','6','--python-exit-code','1','-P',str(O/script),'--',*args,'1920',','.join(map(str,samples))],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
 if family not in ('tv','afterglow_b1'):
  with (d/'queue_720.log').open('w') as log:
   subprocess.run([B,'-b',str(d/f'{family}_1280.blend'),'-t','6','--python-exit-code','1','-P',str(O/'render_saved_frames.py'),'--',str(d/'native_1280'),'1',str(count+1)],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
 (d/'queue_complete.json').write_text(json.dumps({'frames':count,'resolution_samples':samples,'not_production_promoted':True},indent=2))
