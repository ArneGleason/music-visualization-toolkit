import bpy,warnings,json
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v78-transformation-starts.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if (st.channel==1 and 3379<=st.frame_final_start<3775) or st.name=='Scene11 storyboard planning note':seq.remove(st)
sel=json.loads((r/'motion-graphics/SCENE11-TRANSFORMS-001/selections.json').read_text())
for name,d in sel.items():
 st=seq.new_movie('Scene11 '+name+' performance',str(r/d['output']),channel=1,frame_start=d['start_frame'],fit_method='FIT');st.frame_final_duration=d['frames'];st.channel=1
visuals=sorted([st for st in seq if st.channel==1],key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
s.name='Monsters Loose v79 six transformation performances';s.render.filepath=str(o/'MonstersLoose-v79-transformations.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v79-transformations.blend'))
bpy.ops.render.render(animation=True)
