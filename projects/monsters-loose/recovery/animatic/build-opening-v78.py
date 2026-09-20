import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v77-containment-storyboard.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 3379<=st.frame_final_start<3775:seq.remove(st)
for name,a,b in [('SHRINK-A',3379,3425),('SHRINK-B',3425,3515),('GROW-A',3515,3551),('GROW-B',3551,3642),('SMOKE-A',3642,3724),('SMOKE-B',3724,3775)]:
 st=seq.new_image('Scene11 '+name+' starting frame',str(r/f'assets/SCN-011-{name}-v001.png'),channel=1,frame_start=a,fit_method='FIT');st.frame_final_duration=b-a
for st in seq:
 if st.name=='Scene11 storyboard planning note':st.text='STARTING FRAMES / animation planning'
 if st.type=='TEXT' and st.channel==101 and st.frame_final_start==3642:st.text='The space-octopus Cyclops becomes vapor and escapes through the keyhole.'
s.name='Monsters Loose v78 six transformation starting frames';s.render.filepath=str(o/'MonstersLoose-v78-transformation-starts.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v78-transformation-starts.blend'))
bpy.ops.render.render(animation=True)
