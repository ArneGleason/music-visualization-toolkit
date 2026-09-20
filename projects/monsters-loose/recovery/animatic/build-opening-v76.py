import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v75-gate-release.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if (st.channel==1 and st.frame_final_start==3223) or st.name=='Scene10 storyboard planning note':seq.remove(st)
st=seq.new_movie('Scientist stealth exit performance',str(r/'motion-graphics/SCENE10-EXIT-001/exit-timed-v001.mp4'),channel=1,frame_start=3223,fit_method='FIT');st.frame_final_duration=78;st.channel=1
s.name='Monsters Loose v76 stealth exit and gate release';s.render.filepath=str(o/'MonstersLoose-v76-stealth-exit.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v76-stealth-exit.blend'))
bpy.ops.render.render(animation=True)
