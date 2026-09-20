import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v64-living-schematic.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==3104:seq.remove(st)
st=seq.new_movie('Living schematic sustained chewing',str(r/'motion-graphics/SCHEMATIC-ACTION-002/schematic-timed-v001.mp4'),channel=1,frame_start=3104,fit_method='FIT')
st.frame_final_duration=119;st.channel=1
s.frame_start=1;s.frame_end=3222;s.name='Monsters Loose v65 static paper and chewing'
s.render.filepath=str(o/'MonstersLoose-v65-schematic-chewing.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v65-schematic-chewing.blend'))
bpy.ops.render.render(animation=True)
