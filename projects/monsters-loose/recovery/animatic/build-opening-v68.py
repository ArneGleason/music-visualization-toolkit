import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v67-five-eight-frames-earlier.blend'))
s=bpy.context.scene;st=next(x for x in s.sequence_editor.strips if x.channel==1 and x.frame_final_start==2791)
st.filepath=str(r/'motion-graphics/FLIGHT-SNOW-001/flight-snow-v001.mp4')
assert st.frame_final_duration==37
s.name='Monsters Loose v68 cliff snow impact';s.frame_start=1;s.frame_end=3222
s.render.filepath=str(o/'MonstersLoose-v68-cliff-snow-impact.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v68-cliff-snow-impact.blend'))
bpy.ops.render.render(animation=True)
