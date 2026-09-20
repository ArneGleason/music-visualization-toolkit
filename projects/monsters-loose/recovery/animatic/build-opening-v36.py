import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v35-through-habitats.blend'))
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
# Keep review labels clear of the expanding dialogue, only during aquarium cut.
for old in list(seq):
 if old.type=='TEXT' and old.channel in (100,101,102) and old.frame_final_start==1507:
  old.frame_final_end=1625
  new=seq.new_effect(name='Aquarium review label '+str(old.channel),type='TEXT',channel=old.channel,frame_start=1625,length=83)
  for prop in ['font','font_size','color','blend_type','location','anchor_x','anchor_y','alignment_x']:
   setattr(new,prop,getattr(old,prop))
  new.text={100:'06 / THE AQUARIUM',101:'A hungry resident tests the glass.',102:'Harper has a ready answer.'}[old.channel]
  new.transform.offset_x=300;new.transform.offset_y=old.transform.offset_y

visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v36 aquarium wisecrack'
s.render.filepath=str(o/'MonstersLoose-v36-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v36-through-habitats.blend'));bpy.ops.render.render(animation=True)
