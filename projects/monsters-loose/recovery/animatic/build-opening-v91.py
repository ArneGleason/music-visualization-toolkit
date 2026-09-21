import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v90-familiar-faces-procession.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==4242:seq.remove(st)
 elif st.type=='TEXT' and st.channel>=100 and st.frame_final_start==4242:
  if st.frame_final_end<=4414:seq.remove(st)
  else:st.frame_final_start=4414
st=seq.new_movie('Scene14 cautious swamp-cousin meeting',str(r/'motion-graphics/SCENE14-MEETING-001/meeting-timed-v001.mp4'),channel=1,frame_start=4242,fit_method='FIT');st.frame_final_duration=172;st.channel=1
s.name='Monsters Loose v91 cautious swamp meeting';s.render.filepath=str(o/'MonstersLoose-v91-swamp-meeting.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v91-swamp-meeting.blend'))
bpy.ops.render.render(animation=True)
