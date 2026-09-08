"""Resumable local render queue. No paid services, no production promotion."""
from pathlib import Path
import subprocess,json,time
O=Path(__file__).resolve().parent;R=O.parents[1]
BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
jobs=[('swimmers_native.py','swim043',1280,116),('swimmers_native.py','swim044',1280,67),('swimmers_native.py','swim047',1280,68),('guide_native.py','guide',1280,60)]
jobs += [(script,family,1920,n) for script,family,w,n in jobs]
jobs += [('birds_native.py','birds',1920,76),('opening_native.py','opening',1920,86)]
records=[]
for script,family,width,n in jobs:
    frames=list(range(1,n+1)) if width==1280 else [1,n//2,n]
    missing=[f for f in frames if not (O/family/f'native_{width}/{f:04d}.png').exists()]
    if missing:
        with (O/f'{family}_{width}_queue.log').open('w') as log:
            p=subprocess.run([BL,'-b','--python-exit-code','1','-P',str(O/script),'--',family,str(width),','.join(map(str,missing))],cwd=R,stdout=log,stderr=subprocess.STDOUT)
        status='rendered' if p.returncode==0 else 'failed'
    else:status='existing'
    records.append({'family':family,'width':width,'status':status,'frames':frames})
    (O/'batch3_queue.json').write_text(json.dumps(records,indent=2))
    print(family,width,status,flush=True)
