import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v38-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1708:seq.remove(st)
 elif st.channel==1 and st.frame_final_start==1779:seq.remove(st)
 elif st.type=='TEXT' and st.channel in (100,101,102):
  if st.frame_final_start==1708:st.frame_final_end=1768
  elif st.frame_final_start==1779:
   end=st.frame_final_end;st.frame_start-=11;st.frame_final_end=end
st=seq.new_movie('HARPER-LASSO-001 early twirl',str(r/'video-tests/KLING-TEST-004/KLING-TEST-004-clean.mp4'),channel=1,frame_start=1708,fit_method='FIT');st.frame_final_duration=60;st.channel=1
st=seq.new_image('Net incident placeholder',str(r/'assets/ANCH-006-B-v001.png'),channel=1,frame_start=1768,fit_method='FIT');st.frame_final_duration=268;st.channel=1
for m in s.timeline_markers:
 if m.frame==1708:m.name='LASSO: retained take004 source0'
s.timeline_markers.new('NET PLAN lead-in before One',frame=1768)
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v39 early lasso twirl'
s.render.filepath=str(o/'MonstersLoose-v39-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v39-through-habitats.blend'));bpy.ops.render.render(animation=True)
