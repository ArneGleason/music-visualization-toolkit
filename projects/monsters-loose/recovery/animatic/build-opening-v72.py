import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v71-scientist-secret-storyboard.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 3223<=st.frame_final_start<3379:seq.remove(st)
for name,a,file in [('Scientist covert laboratory exit',3223,'ANCH-010-A-v002.png'),('Right mechanical hand releases gates',3301,'ANCH-010-B-v002.png')]:
 st=seq.new_image(name,str(r/'assets'/file),channel=1,frame_start=a,fit_method='FIT');st.frame_final_duration=78
s.frame_start=1;s.frame_end=3378;s.name='Monsters Loose v72 corrected scientist anatomy'
s.render.filepath=str(o/'MonstersLoose-v72-scientist-corrected.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v72-scientist-corrected.blend'))
bpy.ops.render.render(animation=True)
