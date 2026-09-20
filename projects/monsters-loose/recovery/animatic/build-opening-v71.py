import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v70-scene9-performances.blend'))
s=bpy.context.scene;s.frame_start=1;s.frame_end=3378;s.name='Monsters Loose v71 scientist secret storyboard'
st=s.sequence_editor.strips.new_effect('Scene10 storyboard planning note',type='TEXT',channel=110,frame_start=3223,length=156)
st.text='STORYBOARD / shot planning';st.font_size=21;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v71-scientist-secret-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v71-scientist-secret-storyboard.blend'))
bpy.ops.render.render(animation=True)
