import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v76-stealth-exit.blend'))
s=bpy.context.scene
for st in s.sequence_editor.strips:
 if st.channel==1 and 3379<=st.frame_final_start<3775:print('NEXT',st.name,st.frame_final_start,st.frame_final_end,st.directory,st.elements[0].filename)
s.frame_start=1;s.frame_end=3774;s.name='Monsters Loose v77 containment failures storyboard'
st=s.sequence_editor.strips.new_effect('Scene11 storyboard planning note',type='TEXT',channel=110,frame_start=3379,length=396)
st.text='STORYBOARD / shot planning';st.font_size=21;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v77-containment-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v77-containment-storyboard.blend'))
bpy.ops.render.render(animation=True)
