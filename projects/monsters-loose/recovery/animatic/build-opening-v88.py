import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v87-gate-procession.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 4126<=st.frame_final_start<4242:seq.remove(st)
 elif st.type=='TEXT' and st.channel in [101,102] and 4126<=st.frame_final_start<4242:
  st.text='The familiar faces follow the armored pig-beast toward freedom.' if st.channel==101 else 'PROPOSED: gentle crane rise; bat flaps continuously; sign connects faces to habitats.'
st=seq.new_image('Scene13 referenced remaining-creature procession',str(r/'assets/SCN-013-PROCESSION-v001.png'),channel=1,frame_start=4126,fit_method='FIT');st.frame_final_duration=116;st.channel=1
s.name='Monsters Loose v88 remaining creatures storyboard';s.render.filepath=str(o/'MonstersLoose-v88-remaining-creatures.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v88-remaining-creatures.blend'))
bpy.ops.render.render(animation=True)
