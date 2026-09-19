import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v23-arctic.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 1305<=st.frame_final_start<1507:seq.remove(st)
sh=next(x for x in json.loads((r/'shots/shotlist.json').read_text())['shots'] if x['id']=='EXTERIOR-RESET-001')
st=seq.new_image(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame'],fit_method='FIT')
st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.color_multiply=1
for frame,scale in [(1305,1.035),(1506,1.0)]:
 st.transform.scale_x=scale;st.transform.scale_y=scale
 st.transform.keyframe_insert(data_path='scale_x',frame=frame);st.transform.keyframe_insert(data_path='scale_y',frame=frame)
for st in seq:
 if st.type=='TEXT' and st.frame_final_start==1305:
  if st.channel==100:st.text='05 / BACK AT THE MUCF'
  elif st.channel==101:st.text='A quiet exterior breath before the visitors tour.'
  elif st.channel==102:st.text='The helicopter is parked; the facility appears calm.'
 if st.channel==1 and st.frame_final_start>=1305:st.color_multiply=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
for sh in json.loads((r/'shots/shotlist.json').read_text())['shots']:
 if sh['start_frame']>=1305:s.timeline_markers.new(sh['id'],frame=sh['start_frame'])
s.frame_start=1;s.frame_end=2461
s.name='Monsters Loose v24 planning through habitats'
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG'
s.render.filepath=str(o/'MonstersLoose-v24-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v24-through-habitats.blend'))
bpy.ops.render.render(animation=True)
