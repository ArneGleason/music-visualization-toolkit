"""Render the approved corrected title text into the isolated migration folder."""
from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[1]
args=sys.argv[sys.argv.index('--')+1:];W=int(args[0]);D=O/'titles';D.mkdir(exist_ok=True)
src=R/'out/closing_titles_blender_v1/render.py'
code=src.read_text()
code=code.replace("OUT = Path(__file__).resolve().parent",f"OUT = Path({str(D)!r})")
code=code.replace("OUT / 'frames'",f"OUT / 'native_{W}'")
code=code.replace('s.render.resolution_x = 1280',f's.render.resolution_x = {W}').replace('s.render.resolution_y = 720',f's.render.resolution_y = {W*9//16}')
code=code.replace("OUT / 'closing_titles.blend'",f"OUT / 'titles_{W}.blend'")
if len(args)>1:
    frames=list(map(int,args[1].split(',')))
    code=code.replace('bpy.ops.render.render(animation=True)',f"for f in {frames!r}:\n    s.frame_set(f)\n    s.render.filepath=str(OUT/'native_{W}'/f'{{f:04d}}.png')\n    bpy.ops.render.render(write_still=True)")
exec(compile(code,str(src),'exec'),{'__name__':'__main__','__file__':str(src)})
