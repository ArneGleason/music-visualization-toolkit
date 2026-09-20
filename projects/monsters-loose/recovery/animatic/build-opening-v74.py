import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v73-scientist-exit-acting.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==3301:seq.remove(st)
st=seq.new_image('Closed gates pull-back release reference',str(r/'assets/ANCH-010-B-v003.png'),channel=1,frame_start=3301,fit_method='FIT');st.frame_final_duration=78
s.name='Monsters Loose v74 closed gates pull lever';s.render.filepath=str(o/'MonstersLoose-v74-closed-gates-pull-lever.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v74-closed-gates-pull-lever.blend'))
bpy.ops.render.render(animation=True)
