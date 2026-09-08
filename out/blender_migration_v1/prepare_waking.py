"""Original plates and numeric eye aperture controls; no composited images."""
from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'waking';(D/'plates').mkdir(parents=True,exist_ok=True)
source=R/'out/garden_eyes_motion_v1/base.mp4'
if not (D/'plates/0081.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-frames:v','81',str(D/'plates/%04d.png')],check=True)
old=R/'out/garden_waking_v3/render.py';code=old.read_text().split(' # Inpaint source eyes only')[0]
code=code.replace('OUT=Path(__file__).resolve().parent',"OUT=ROOT/'out/blender_migration_v1/waking'")
line=" comp=cv2.imread(str(ROOT/'out/garden_eyes_airflow_v2/composite'/f'{frame:04d}.png')).astype(np.float32)"
assert line in code;code=code.replace(line,'')
code=code.replace("'pixels':len(pts)","'pixels':len(pts),'rx':rx,'ry':ry")
code+=" records.append({'song_frame':1569+frame,'eyes':eye_info})\ncap.release()\n"
ns={'__file__':str(old)};exec(compile(code,'eye_tracking','exec'),ns)
rows=ns['records'];assert len(rows)==81
reference=json.loads((R/'out/garden_waking_v3/tracking.json').read_text())
assert all(a['center']==b['center'] and a['opening']==b['opening'] for r,z in zip(rows,reference) for a,b in zip(r['eyes'],z['eyes']))
(D/'controls.json').write_text(json.dumps({'fps':24,'song_frames':[1569,1650],'source_frames':[0,81],'source':str(source.relative_to(R)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':rows},indent=2))
print('Eye centers and openings match accepted tracking exactly')
