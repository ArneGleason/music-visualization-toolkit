import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v82-insect-impact.blend'))
s=bpy.context.scene
for st in s.sequence_editor.strips:
 if st.channel==1:
  name={3724:'smoke-b'}.get(int(st.frame_final_start))
  if name:st.filepath=str(r/f'motion-graphics/SCENE11-SMOKE-003/{name}-turbulence-v001.mp4')
s.name='Monsters Loose v83 swirling Cyclops materialization';s.render.filepath=str(o/'MonstersLoose-v83-cyclops-turbulence.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v83-cyclops-turbulence.blend'))
bpy.ops.render.render(animation=True)


