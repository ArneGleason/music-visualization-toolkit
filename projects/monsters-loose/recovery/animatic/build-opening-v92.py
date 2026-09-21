import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v91-swamp-meeting.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 4414<=st.frame_final_start<5291:seq.remove(st)
 elif st.type=='TEXT' and st.channel>=100 and st.frame_final_start>=4414:seq.remove(st)
for take in json.loads((r/'motion-graphics/OUTRO-001/selections.json').read_text())['selections']:
 st=seq.new_movie(take['id'],str(r/take['source']),channel=1,frame_start=take['start_frame'],fit_method='FIT')
 st.frame_final_duration=take['duration_frames'];st.channel=1
assert sorted((int(st.frame_final_start),int(st.frame_final_end)) for st in seq if st.channel==1 and st.frame_final_start>=4414)==[(4414,4465),(4465,4495),(4495,4538),(4538,4568),(4568,4624),(4624,4719),(4719,4793),(4793,4951),(4951,5291)]
s.frame_end=5290;s.name='Monsters Loose v92 complete outro performances';s.render.filepath=str(o/'MonstersLoose-v92-outro-performances.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v92-outro-performances.blend'))
bpy.ops.render.render(animation=True)
