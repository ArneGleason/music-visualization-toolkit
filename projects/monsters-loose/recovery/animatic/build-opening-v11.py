import bpy,json,pathlib
root=pathlib.Path(__file__).resolve().parent;job=root.parent
bpy.ops.wm.open_mainfile(filepath=str(root/'MonstersLoose-clean-animatic-v05-full.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
shots=json.loads((job/'shots/shotlist.json').read_text())['shots']
for st in list(seq):
 if st.channel==1 and st.frame_final_start<504:seq.remove(st)
# Keep unanimated remainder of the original sign anchor as a storyboard placeholder.
st=next(st for st in seq if st.channel==1 and st.frame_final_start==504);st.frame_final_start=627
for sh in shots:
 st=seq.new_movie(sh['id'],str(job/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT');st.frame_offset_start=sh['source_in_frame'];st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame'];st.color_multiply=1
 assert st.frame_final_start==sh['start_frame'] and st.frame_final_end==sh['end_frame_exclusive']
 if not s.timeline_markers.get(sh['id']):s.timeline_markers.new(sh['id'],frame=sh['start_frame'])
for sh in shots:seq[sh['id']].channel=1
for st in seq:
 if st.type=='TEXT' and 207<=st.frame_final_start<504:
  if st.channel in (100,101,102):st.transform.offset_y={100:342,101:323,102:304}[st.channel];st.font_size=18
  if st.channel==101:st.text='Harper discovers the loose bolt while something slips away under cover.'
  if st.channel==102:st.text='An unseen viewpoint moves through the foliage farther along the concourse.'
 if st.type=='TEXT' and st.frame_final_start==504 and st.channel in (100,101,102):
  st.alignment_x='LEFT';st.transform.offset_x=-400;st.transform.offset_y={100:344,101:326,102:309}[st.channel];st.font_size=14
  if st.channel==101:st.text='Harper introduces MUCF and its Arctic capture team.'
  if st.channel==102:st.text='The lab mixes things up; a red eye opens behind the mesh.'
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name,a.frame_final_end,b.frame_final_start)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=1304;s.name='Monsters Loose opening through laboratory v11'
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
for frame in (530,566,612,650,1050):
 s.frame_set(frame);s.render.filepath=str(root/f'v11-check-{frame}.png');bpy.ops.render.render(write_still=True)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.filepath=str(root/'MonstersLoose-v11-opening-through-lab.mp4')
s.frame_set(1);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(root/'MonstersLoose-v11-opening-through-lab.blend'));bpy.ops.render.render(animation=True)


