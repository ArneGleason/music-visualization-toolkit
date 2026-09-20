import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v81-transformation-polish.blend'))
s=bpy.context.scene
for st in s.sequence_editor.strips:
 if st.channel==1:
  name={3515:'grow-a',3551:'grow-b'}.get(int(st.frame_final_start))
  if name:st.filepath=str(r/f'motion-graphics/SCENE11-INSECT-002/{name}-polished-v001.mp4')
s.name='Monsters Loose v82 stronger insect growth and breakout';s.render.filepath=str(o/'MonstersLoose-v82-insect-impact.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v82-insect-impact.blend'))
bpy.ops.render.render(animation=True)

