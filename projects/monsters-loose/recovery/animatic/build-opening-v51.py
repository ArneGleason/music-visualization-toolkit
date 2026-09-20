import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v50-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for sh in json.loads((r/'shots/shotlist.json').read_text())['shots']:
 if sh['id'] not in ['CREATURE-PORTRAIT-INSECTARIUM-001','CREATURE-PORTRAIT-EXOBIOLOGY-001']:continue
 old=next(st for st in seq if st.channel==1 and st.frame_final_start==sh['start_frame']);seq.remove(old)
 st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=sh['start_frame'],fit_method='FIT');st.frame_final_duration=26;st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v51 portrait beacon accents'
s.render.filepath=str(o/'MonstersLoose-v51-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v51-through-habitats.blend'));bpy.ops.render.render(animation=True)
