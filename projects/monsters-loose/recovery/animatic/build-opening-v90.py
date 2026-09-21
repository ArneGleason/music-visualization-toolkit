import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v89-through-ending.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==4126:seq.remove(st)
 elif st.channel>=100 and 4126<=st.frame_final_start<4242:seq.remove(st)
st=seq.new_movie('Scene13 familiar faces procession performance',str(r/'motion-graphics/SCENE13-PROCESSION-001/procession-timed-v001.mp4'),channel=1,frame_start=4126,fit_method='FIT');st.frame_final_duration=116;st.channel=1
s.name='Monsters Loose v90 familiar faces procession';s.render.filepath=str(o/'MonstersLoose-v90-familiar-faces-procession.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v90-familiar-faces-procession.blend'))
bpy.ops.render.render(animation=True)
