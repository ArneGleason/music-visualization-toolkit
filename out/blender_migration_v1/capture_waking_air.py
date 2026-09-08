"""Capture accepted eight-substep3D airflow as numeric mesh state, not pixels."""
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'waking';(D/'geometry').mkdir(parents=True,exist_ok=True)
old=R/'out/garden_eyes_airflow_v2/render_particles.py';code=old.read_text()
needle="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'camera':camera,'clearance':clearance})"
assert needle in code
replacement='''
s=s.replace('OUT=ROOT/"out/garden_eyes_airflow_v2"','OUT=ROOT/"out/blender_migration_v1/waking"')
s=s.replace('(OUT/"controls.json").write_text','(OUT/"air_controls.json").write_text')
s=s.replace('        bpy.ops.render.render(write_still=True)', """        payload={'camera':np.asarray(sc.camera.location)}
        for label,m,c in [('motes',mesh,colors),('wisps',haze,haze_colors)]+[(f'halo{k}',hm,hc) for k,(hm,hc,spread,energy) in enumerate(halos)]:
            co=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',co)
            rgba=np.empty(len(c.data)*4,dtype=np.float32);c.data.foreach_get('color',rgba)
            payload[label]=co.reshape(-1,3);payload[label+'_rgba']=rgba.reshape(-1,4)
        np.savez_compressed(OUT/'geometry'/f'{frame:04d}.npz',**payload)""")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'camera':camera,'clearance':clearance})
'''
code=code.replace(needle,replacement)
exec(compile(code,str(old),'exec'),{'__file__':str(old),'__name__':'capture'})
