import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v65-schematic-chewing.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.name=='Count punch 5':seq.remove(st)
st=seq.new_effect('Count punch 5 corrected',type='TEXT',channel=108,frame_start=2531,length=6)
st.text='5';st.font=bpy.data.fonts.load(str(r/'motion-graphics/HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf'));st.location=(.5,.49);st.color=(1,.91,.66,1)
st.use_shadow=True;st.use_outline=True;st.outline_width=.045;st.outline_color=(.015,.02,.025,1)
for f,size,alpha,angle in [(2531,180,.8,-.13),(2533,565,1,.04),(2534,475,1,-.025),(2535,475,1,-.025),(2536,620,.4,.02)]:
 st.font_size=size;st.blend_alpha=alpha;st.transform.rotation=angle
 st.keyframe_insert(data_path='font_size',frame=f);st.keyframe_insert(data_path='blend_alpha',frame=f);st.transform.keyframe_insert(data_path='rotation',frame=f)
# Replace source in place so existing kick-impact keyframes remain identical.
st=next(st for st in seq if st.channel==1 and st.frame_final_start==2638)
st.filepath=str(r/'motion-graphics/DUEL-ROAR-001/duel-roar-v001.mp4')
s.frame_start=1;s.frame_end=3222;s.name='Monsters Loose v66 five timing and duel roar'
s.render.filepath=str(o/'MonstersLoose-v66-five-timing-duel-roar.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v66-five-timing-duel-roar.blend'))
bpy.ops.render.render(animation=True)
