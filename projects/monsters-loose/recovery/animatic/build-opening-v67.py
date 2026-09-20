import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v66-five-timing-duel-roar.blend'))
s=bpy.context.scene;st=s.sequence_editor.strips.get('Count punch 5 corrected')
assert st.frame_start==2531 and st.frame_final_duration==6
curves=[c for a in bpy.data.actions for l in a.layers for t in l.strips for b in t.channelbags for c in b.fcurves]
target=[c for c in curves if '["Count punch 5 corrected"]' in c.data_path]
assert len(target)==3
saved=[(k,k.co.copy(),k.handle_left.copy(),k.handle_right.copy()) for c in target for k in c.keyframe_points]
other=[(c,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right)) for k in c.keyframe_points]) for c in curves if c not in target]
st.frame_start=2523
for k,co,left,right in saved:
 k.co=(co.x-8,co.y);k.handle_left=(left.x-8,left.y);k.handle_right=(right.x-8,right.y)
for c,points in other:
 assert points==[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right)) for k in c.keyframe_points],c.data_path
assert st.frame_final_end==2529
s.name='Monsters Loose v67 five eight frames earlier';s.frame_start=1;s.frame_end=3222
s.render.filepath=str(o/'MonstersLoose-v67-five-eight-frames-earlier.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v67-five-eight-frames-earlier.blend'))
bpy.ops.render.render(animation=True)
