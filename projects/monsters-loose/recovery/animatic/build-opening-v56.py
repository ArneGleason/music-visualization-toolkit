import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v55-countdown-planning.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.name=='NEARMISS-1-001':seq.remove(st)
sh=next(sh for sh in json.loads((r/'shots/shotlist.json').read_text())['shots'] if sh['id']=='NEARMISS-1-001')
st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=2302,fit_method='FIT');st.frame_final_duration=76;st.channel=1
s.frame_start=1;s.frame_end=2905;s.name='Monsters Loose v56 rabbit local motion blur'
s.render.filepath=str(o/'MonstersLoose-v56-through-countdown-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v56-countdown-planning.blend'));bpy.ops.render.render(animation=True)
