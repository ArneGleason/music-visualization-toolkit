import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v79-transformations.blend'))
s=bpy.context.scene;st=next(x for x in s.sequence_editor.strips if x.channel==1 and x.frame_final_start==3724)
st.filepath=str(r/'motion-graphics/SCENE11-SMOKE-002/smoke-b-timed-v001.mp4');assert st.frame_final_duration==51
s.name='Monsters Loose v80 referenced vapor Cyclops';s.render.filepath=str(o/'MonstersLoose-v80-vapor-cyclops.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v80-vapor-cyclops.blend'))
bpy.ops.render.render(animation=True)
