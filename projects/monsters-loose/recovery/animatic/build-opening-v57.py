import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v56-countdown-planning.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==2036:seq.remove(st)
sh=next(sh for sh in json.loads((r/'shots/shotlist.json').read_text())['shots'] if sh['id']=='HABITATS-CHOOSE-001')
st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=2036,fit_method='FIT');st.frame_final_duration=56;st.channel=1
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
s.frame_start=1;s.frame_end=2905;s.name='Monsters Loose v57 enclosed reptile roar'
s.render.filepath=str(o/'MonstersLoose-v57-through-countdown-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v57-countdown-planning.blend'));bpy.ops.render.render(animation=True)
