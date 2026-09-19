import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v31-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 1507<=st.frame_final_start<1708:seq.remove(st)
for sh in json.loads((r/'shots/shotlist.json').read_text())['shots']:
 if sh['id'] not in ['HARPER-TOUR-001','HARPER-AQUARIUM-001']:continue
 if sh['media_type']=='video':
  st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT');st.frame_offset_start=sh['source_in_frame']
 else:st=seq.new_image(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame'],fit_method='FIT')
 st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.channel=1;st.color_multiply=1
 s.timeline_markers.new(sh['id'],frame=sh['start_frame'])
for st in seq:
 if st.type=='TEXT' and st.frame_final_start==1507:
  if st.channel==101:st.text='Harper leads the visitors past the occupied enclosures.'
  if st.channel==102:st.text='Then: an enormous sea creature, safely behind aquarium glass.'
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v32 fixed-camera tour'
s.render.filepath=str(o/'MonstersLoose-v32-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v32-through-habitats.blend'));bpy.ops.render.render(animation=True)
