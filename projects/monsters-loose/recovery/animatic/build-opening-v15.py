import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v11-opening-through-lab.blend'))
s=bpy.context.scene
seq=s.sequence_editor.strips
for st in list(seq):
    if st.channel==1 and 627<=st.frame_final_start<1033:seq.remove(st)
shots=json.loads((r/'shots/shotlist.json').read_text())['shots']
for sh in shots:
    if sh['start_frame']<627:continue
    st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT')
    st.frame_offset_start=sh['source_in_frame']
    st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame']
    st.color_multiply=1
    assert st.frame_final_start==sh['start_frame']
    assert st.frame_final_end==sh['end_frame_exclusive']
    s.timeline_markers.new(sh['id'],frame=sh['start_frame'])
for sh in shots:seq[sh['id']].channel=1
for st in seq:
    if st.type=='TEXT' and st.frame_final_start==504:
        if st.channel==101:st.text='MUCF tour, Arctic patrol, and an interrupted warning.'
        if st.channel==102:st.text='Harper listens as three unseen creatures stir inside the cave.'
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=1304
s.name='Monsters Loose Arctic announcement review v15'
s.render.image_settings.media_type='VIDEO'
s.render.image_settings.file_format='FFMPEG'
s.render.filepath=str(o/'MonstersLoose-v15-opening-through-lab.mp4')
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v15-arctic.blend'))
bpy.ops.render.render(animation=True)
