from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent;R=O.parents[1];BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe';records=[]
for family,n in [('tunnel',57),('titles',72)]:
    for width in [1280,1920]:
        wanted=list(range(1,n+1)) if width==1280 else [1,n//2,n]
        missing=[f for f in wanted if not (O/family/f'native_{width}/{f:04d}.png').exists()]
        if missing:
            args=([family] if family!='titles' else [])+[str(width),','.join(map(str,missing))]
            with (O/f'{family}_{width}_queue.log').open('w') as log:
                p=subprocess.run([BL,'-b','--python-exit-code','1','-P',str(O/f'{family}_native.py'),'--']+args,cwd=R,stdout=log,stderr=subprocess.STDOUT)
            status='rendered' if p.returncode==0 else 'failed'
        else:status='existing'
        records.append({'family':family,'width':width,'status':status});(O/'batch3_geometry_queue.json').write_text(json.dumps(records,indent=2));print(family,width,status,flush=True)
