import bpy
from pathlib import Path
r=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(r/'animatic/MonstersLoose-v21-arctic.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in seq:
 if st.channel==1 and st.frame_final_start==1162:st.frame_final_duration=69
st=seq.new_image('HARPER-TALL-GATE-PLAN',str(r/'assets/SCN-004-harper-tall-gate-v001.png'),channel=1,frame_start=1231,fit_method='FIT')
st.frame_final_duration=74
s.frame_start=1162;s.frame_end=1304
s.render.filepath=str(r/'animatic/MonstersLoose-next-two-shots-plan.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(r/'animatic/MonstersLoose-next-two-shots-plan.blend'))
bpy.ops.render.render(animation=True)
