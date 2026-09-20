import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v36-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
shots=json.loads((r/'shots/shotlist.json').read_text())['shots'][1:5]
for sh in shots:
 for st in list(seq):
  if st.channel==1 and st.frame_final_start==sh['start_frame']:seq.remove(st)
 st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT');st.frame_offset_start=sh['source_in_frame'];st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v37 early structure beacons'
s.render.filepath=str(o/'MonstersLoose-v37-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v37-through-habitats.blend'));bpy.ops.render.render(animation=True)
