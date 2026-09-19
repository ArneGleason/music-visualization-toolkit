import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v26-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1305:seq.remove(st)
sh=next(x for x in json.loads((r/'shots/shotlist.json').read_text())['shots'] if x['id']=='SWAMP-FROG-001')
st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=1293,fit_method='FIT');st.frame_offset_start=12;st.frame_final_duration=202;st.channel=1
for st in seq:
 if st.type=='TEXT' and st.frame_final_start==1305:
  if st.channel==101:st.text='A peaceful swamp outside the facility.'
  if st.channel==102:st.text='An unseen creature takes the frog; only ripples remain.'
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v27 swamp bridge'
s.render.filepath=str(o/'MonstersLoose-v27-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v27-through-habitats.blend'));bpy.ops.render.render(animation=True)
