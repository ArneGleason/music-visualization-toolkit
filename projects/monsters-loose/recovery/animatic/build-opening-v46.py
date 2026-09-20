import bpy
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v45-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1768:seq.remove(st)
 elif st.type=='TEXT' and st.frame_final_start==1768:
  if st.channel==101:st.text='Almost escaped? A firm stay is all it takes.'
  elif st.channel==102:st.text='Harper and the obedient monster / motion test'
st=seq.new_movie('HARPER STAY001',str(r/'video-tests/KLING-STAY-001/KLING-STAY-001-01.mp4'),channel=1,frame_start=1744,fit_method='FIT');st.frame_offset_start=24;st.frame_final_duration=125;st.channel=1
# Rebuild review captions over this revised beat, eliminating inherited overlapping labels.
for st in list(seq):
 if st.type=='TEXT' and st.channel>=100 and st.frame_final_start<2036 and st.frame_final_end>1768:
  if st.frame_final_start<1768:st.frame_final_end=1768
  elif st.frame_final_end>2036:st.frame_final_start=2036
  else:seq.remove(st)
for start,end,caption in [(1768,1893,'Almost escaped? A firm stay is all it takes.'),(1893,2036,'Kid eye roll / next-shot reference placeholder')]:
 st=seq.new_effect('Review caption',type='TEXT',channel=101,frame_start=start,length=end-start);st.text=caption;st.font_size=28;st.location=(.5,.94);st.alignment_x='CENTER';st.anchor_x='CENTER';st.color=(1,1,.9,1)
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v46 keeper stay gesture'
s.render.filepath=str(o/'MonstersLoose-v46-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v46-through-habitats.blend'));bpy.ops.render.render(animation=True)
