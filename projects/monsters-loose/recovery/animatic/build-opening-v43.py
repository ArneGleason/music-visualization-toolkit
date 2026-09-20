import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v42-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1768:seq.remove(st)
 elif st.type=='TEXT' and st.frame_final_start==1768:
  st.frame_final_end=1893
  if st.channel==101:st.text='Near escape: Harper triggers the safety net.'
  elif st.channel==102:st.text='New starting-frame storyboard / animation pending'
st=seq.new_image('NET INTERCEPTION starting-frame storyboard',str(r/'assets/SCN-006-net-interception-v001.png'),channel=1,frame_start=1768,fit_method='FIT');st.frame_final_duration=125;st.channel=1
st=seq.new_image('Eye roll beat placeholder',str(r/'assets/SCN-006-rope-demo-v001.png'),channel=1,frame_start=1893,fit_method='FIT');st.frame_final_duration=143;st.channel=1
s.timeline_markers.new('NET storyboard end / eye roll planning',frame=1893)
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v43 net interception storyboard'
s.render.filepath=str(o/'MonstersLoose-v43-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v43-through-habitats.blend'));bpy.ops.render.render(animation=True)
