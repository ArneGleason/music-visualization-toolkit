import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v54-through-nearmisses.blend'))
s=bpy.context.scene;s.frame_start=1;s.frame_end=2905;s.name='Monsters Loose v55 countdown planning preview'
st=s.sequence_editor.strips.new_effect('Arctic replacement planning note',type='TEXT',channel=110,frame_start=2510,length=396)
st.text='STORYBOARD PLACEHOLDER: red rival will become the Arctic monster';st.font_size=22;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v55-through-countdown-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v55-countdown-planning.blend'));bpy.ops.render.render(animation=True)
