import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v72-scientist-corrected.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==3223:seq.remove(st)
st=seq.new_image('Scientist cautious exit revised acting',str(r/'assets/ANCH-010-A-v003.png'),channel=1,frame_start=3223,fit_method='FIT');st.frame_final_duration=78
s.name='Monsters Loose v73 scientist exit acting';s.render.filepath=str(o/'MonstersLoose-v73-scientist-exit-acting.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v73-scientist-exit-acting.blend'))
bpy.ops.render.render(animation=True)
