import bpy
from pathlib import Path
r=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(r/'animatic/MonstersLoose-v26-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1305:seq.remove(st)
st=seq.new_image('SWAMP-FROG-PLAN',str(r/'assets/SCN-005-swamp-frog-v001.png'),channel=1,frame_start=1305,fit_method='FIT');st.frame_final_duration=202
for st in seq:
 if st.type=='TEXT' and st.frame_final_start==1305:
  if st.channel==101:st.text='A peaceful swamp outside the facility.'
  if st.channel==102:st.text='An unseen creature takes the frog; only ripples remain.'
s.frame_start=1305;s.frame_end=1506;s.render.filepath=str(r/'animatic/MonstersLoose-swamp-frog-plan.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(r/'animatic/MonstersLoose-swamp-frog-plan.blend'))
bpy.ops.render.render(animation=True)
