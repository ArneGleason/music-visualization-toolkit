import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v40-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start in (1708,1768):seq.remove(st)
 elif st.type=='TEXT' and st.frame_final_start==1708:
  if st.channel==101:st.text='A simple keeper tool: rope, ready for the job.'
  elif st.channel==102:st.text='Bundled coil and short dangling length / demonstration test'
st=seq.new_movie('HARPER rope demonstration',str(r/'video-tests/KLING-ROPE-DEMO-001/KLING-ROPE-DEMO-001-01.mp4'),channel=1,frame_start=1696,fit_method='FIT');st.frame_offset_start=12;st.frame_final_duration=60;st.channel=1
st=seq.new_image('Net incident placeholder - rope demo reference',str(r/'assets/SCN-006-rope-demo-v001.png'),channel=1,frame_start=1768,fit_method='FIT');st.frame_final_duration=268;st.channel=1
for m in s.timeline_markers:
 if m.frame==1708:m.name='ROPE DEMO001 source12'
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v41 simple rope demonstration'
s.render.filepath=str(o/'MonstersLoose-v41-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v41-through-habitats.blend'));bpy.ops.render.render(animation=True)
