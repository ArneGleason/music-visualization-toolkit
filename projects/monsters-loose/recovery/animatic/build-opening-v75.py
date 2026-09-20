import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v74-closed-gates-pull-lever.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==3301:seq.remove(st)
 elif st.name=='Scene10 storyboard planning note':st.frame_final_duration=78
st=seq.new_movie('Approved gate release grip change',str(r/'motion-graphics/SCENE10-GATE-001/gate-timed-v001.mp4'),channel=1,frame_start=3301,fit_method='FIT');st.frame_final_duration=78;st.channel=1
s.name='Monsters Loose v75 approved gate release';s.render.filepath=str(o/'MonstersLoose-v75-gate-release.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v75-gate-release.blend'))
bpy.ops.render.render(animation=True)

