import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v46-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1893:seq.remove(st)
 elif st.type=='TEXT' and st.channel>=100 and st.frame_final_start==1893:st.text='Really? The kid gives Harper an eye roll.'
st=seq.new_movie('KID EYEROLL001',str(r/'video-tests/KLING-EYEROLL-001/KLING-EYEROLL-001-01.mp4'),channel=1,frame_start=1881,fit_method='FIT');st.frame_offset_start=12;st.frame_final_duration=143;st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v47 kid eye roll'
s.render.filepath=str(o/'MonstersLoose-v47-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v47-through-habitats.blend'));bpy.ops.render.render(animation=True)
