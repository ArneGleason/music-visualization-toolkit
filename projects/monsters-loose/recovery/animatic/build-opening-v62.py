import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v61-countdown-punches.blend'))
s=bpy.context.scene;s.frame_start=1;s.frame_end=3222
s.name='Monsters Loose v62 next creation planning preview'
st=s.sequence_editor.strips.new_effect('Scene9 storyboard planning note',type='TEXT',channel=110,frame_start=2906,length=317)
st.text='STORYBOARD / shot planning';st.font_size=21;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v62-through-next-creation-storyboard.mp4')
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v62-next-creation-planning.blend'))
bpy.ops.render.render(animation=True)
