"""Reuse accepted Blender three-band airflow on the new moving plate."""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import garden_dust_pilot as pilot
pilot.FIRST,pilot.END=1569,1650
camera=json.loads((OUT/'camera.json').read_text())
clearance=np.load(OUT/'eye_clearance.npy')
p=ROOT/'tools/garden_airflow.py';s=p.read_text()
def replace(a,b):
 global s
 assert a in s,a
 s=s.replace(a,b)
replace('OUT=ROOT/"out/garden_airflow"','OUT=ROOT/"out/garden_eyes_airflow_v2"')
replace('PULSE_LIGHT="--pulse-light" in sys.argv','PULSE_LIGHT=True')
replace('BLOOM_DEPTH="--bloom-depth" in sys.argv','BLOOM_DEPTH=True')
replace('OUT=ROOT/"out/garden_airflow_pulse"','OUT=ROOT/"out/garden_eyes_airflow_v2"')
replace('OUT=ROOT/"out/garden_airflow_bloom_depth"','OUT=ROOT/"out/garden_eyes_airflow_v2"')
replace('resolution_x=1920; sc.render.resolution_y=1080','resolution_x=1280; sc.render.resolution_y=720')
replace('sc.render.fps=24; sc.render.image_settings.file_format="PNG"',
 'sc.render.fps=24; sc.render.image_settings.file_format="PNG"')
replace('ROOT/"codex/out/forest_fauna_eyes_a.jpg"','ROOT/"out/garden_eyes_motion_v1/base.mp4"')
replace('emission=next(n for n in mat.node_tree.nodes if n.type=="EMISSION")', 'tex.image_user.use_auto_refresh=True; tex.image_user.frame_duration=192; tex.image_user.frame_start=1\n    emission=next(n for n in mat.node_tree.nodes if n.type=="EMISSION")')
replace('OUT/"frames"','OUT/"composite"')
replace('for frame in range(-24,68):','for frame in range(-24,81):')
replace('flow += np.array([.7,.25,.45])','''# Forward flow with loose helical eddies around the camera axis.
            radius=np.linalg.norm(pos[:,:2],axis=1)
            swirl=(.24+.12*level)*np.exp(-(radius/6)**2)
            flow[:,0] += -pos[:,1]*swirl + .16
            flow[:,1] += pos[:,0]*swirl + .08
            flow[:,2] += .8 + .45*level''')
replace('width=(22-pos[:,2])*.72\n        sx=768+pos[:,0]/width*1536\n        sy=432-pos[:,1]/width*1536', '''scale=camera['scale'][frame]
        cz=22/scale
        cx=-(camera['center'][frame][0]-640)/1280*(cz*.72)
        cy=(camera['center'][frame][1]-360)/1280*(cz*.72)
        sc.camera.location=(cx,cy,cz)
        # Keep native plate pixels fixed in frame. Only the 3D motes receive
        # reconstructed camera travel; do not double-zoom the generated movie.
        plate.location=(cx,cy,0); plate.scale=(cz*.36,cz*.2025,1)
        sc.frame_set(frame+1)
        width=(cz-pos[:,2])*.72
        sx=768+(pos[:,0]-cx)/width*1536
        sy=432-(pos[:,1]-cy)/width*1536''')
replace('for x,y,r in pilot.EYES:\n            visibility*=np.clip((np.hypot(sx-x,sy-y)-r*.75)/25,0,1)', '''ix=np.clip((sx/1.2).astype(int),0,1279)
        iy=np.clip((sy/1.2).astype(int),0,719)
        visibility*=clearance[frame,iy,ix]''')
# Preserve approximate foliage depth blockers, following the broad push.
replace('inside=np.sqrt(((sx-x)/rx)**2+((sy-y)/ry)**2)', '''x=768+(x-768)*scale; y=432+(y-432)*scale
            inside=np.sqrt(((sx-x)/(rx*scale))**2+((sy-y)/(ry*scale))**2)''')
replace('"frame":pilot.FIRST+frame,"drum":pulse', '"camera_z":cz,"frame":pilot.FIRST+frame,"drum":pulse')
# Assembly and soundtrack are handled separately, exactly once.
s=s[:s.index('    command(["ffmpeg"')] + '''    (OUT/"controls.json").write_text(json.dumps({"song_frames":[1569,1650],"seed":19031,"motes":COUNT,"wisps":WISPS,"depth":"approximate three bands; moving eye masks and foliage proxies","diagnostics":diagnostics},indent=2))
if __name__=="__main__":
    main()
'''
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'camera':camera,'clearance':clearance})
