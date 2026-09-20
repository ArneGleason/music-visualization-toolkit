import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v48-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==2036:seq.remove(st)
for sh in json.loads((r/'shots/shotlist.json').read_text())['shots']:
 if sh['id'] not in ['HABITATS-CHOOSE-001','ANCH-007-A-REMAINDER-PLAN']:continue
 if sh['media_type']=='video':
  st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT');st.frame_offset_start=sh['source_in_frame']
 else:st=seq.new_image(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame'],fit_method='FIT')
 st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v49 choose your creature'
s.render.filepath=str(o/'MonstersLoose-v49-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v49-through-habitats.blend'));bpy.ops.render.render(animation=True)
