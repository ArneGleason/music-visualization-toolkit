import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v68-cliff-snow-impact.blend'))
s=bpy.context.scene;st=next(x for x in s.sequence_editor.strips if x.channel==1 and x.frame_final_start==2791)
st.filepath=str(r/'motion-graphics/FLIGHT-SNOW-002/flight-snow-v002.mp4')
assert st.frame_final_duration==37
s.name='Monsters Loose v69 natural snow overlap';s.frame_start=1;s.frame_end=3222
s.render.filepath=str(o/'MonstersLoose-v69-natural-snow-overlap.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v69-natural-snow-overlap.blend'))
bpy.ops.render.render(animation=True)
