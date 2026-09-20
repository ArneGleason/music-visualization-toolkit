import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v52-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.name.startswith('HUNT-'):seq.remove(st)
 elif st.channel==1 and st.frame_final_start==2462:st.frame_final_start=2510
 elif st.type=='TEXT' and st.channel>=100:
  if st.frame_final_end==2462:st.frame_final_end=2510
  elif st.frame_final_start==2462:st.frame_final_start=2510
 elif st.type=='TEXT' and st.name.startswith(('lead-027','lead-028')) and st.frame_final_start==2503:st.frame_final_start=2510
for sh in json.loads((r/'shots/shotlist.json').read_text())['shots']:
 if not sh['id'].startswith(('HUNT-','NEARMISS-')):continue
 st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT');st.frame_offset_start=sh['source_in_frame'];st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name,a.frame_final_end,b.frame_final_start)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2509;s.name='Monsters Loose v53 near misses'
s.render.filepath=str(o/'MonstersLoose-v53-opening-through-nearmisses.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v53-through-nearmisses.blend'));bpy.ops.render.render(animation=True)
