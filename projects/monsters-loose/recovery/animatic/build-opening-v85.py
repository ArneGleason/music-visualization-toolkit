import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v84-next-scene-storyboard.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==3775:seq.remove(st)
 elif st.type=='TEXT' and st.name.startswith('lead-043'):seq.remove(st)
 elif st.channel>=100 and st.frame_final_start==3775:
  if st.frame_final_end<=3883:seq.remove(st)
  else:st.frame_final_start=3883
st=seq.new_movie('Scene12 No way / Yes way performances and blur pullback',str(r/'motion-graphics/SCENE12-EXCHANGE-001/exchange-composite-v001.mp4'),channel=1,frame_start=3775,fit_method='FIT');st.frame_final_duration=108;st.channel=1
s.name='Monsters Loose v85 No way Yes way exchange';s.render.filepath=str(o/'MonstersLoose-v85-no-way-yes-way.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v85-no-way-yes-way.blend'))
bpy.ops.render.render(animation=True)
