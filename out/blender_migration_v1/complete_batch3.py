"""Join local render jobs, then validate and export the contextual previews."""
from pathlib import Path
import time,json,subprocess,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
queues={'batch3_queue.json':10,'batch3_extra_queue.json':4,'batch3_geometry_queue.json':4,'batch3_insert_queue.json':4}
deadline=time.monotonic()+1800
while True:
    done=True
    for name,n in queues.items():
        p=O/name
        try:rows=json.loads(p.read_text())
        except (FileNotFoundError,json.JSONDecodeError):done=False;continue
        if any(v['status']=='failed' for v in rows):raise RuntimeError('Render failure in '+name)
        done=done and len(rows)==n
    if done:break
    if time.monotonic()>deadline:raise RuntimeError('Render join timed out; outputs retained for diagnosis')
    time.sleep(5)
print('All local native render jobs complete.',flush=True)
for script in ['finish_batch3.py','check_batch3.py']:
    subprocess.run([sys.executable,str(O/script)],cwd=R,check=True)
with (O/'batch3_blend_audit.log').open('w') as log:
    subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',str(O/'audit_native_blends.py')],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
audit=json.loads((O/'batch3_blend_audit.json').read_text());assert len(audit)==24 and not any(r['errors'] for r in audit),audit
print('Saved-scene audit passed for 24 scenes.',flush=True)
subprocess.run([sys.executable,str(O/'render_batch3_previews.py')],cwd=R,check=True)
print('Review exports ready.',flush=True)
