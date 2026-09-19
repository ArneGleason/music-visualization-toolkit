import bpy,pathlib
r=pathlib.Path(r'C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913')
bpy.ops.wm.open_mainfile(filepath=str(r/'animatic'/'MonstersLoose-v09-harper-pov-through-sign.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
old=seq['STEALTH-POV'];start=int(old.frame_final_start);end=int(old.frame_final_end);offset=int(old.frame_offset_start);seq.remove(old)
st=seq.new_movie('STEALTH-POV - experimental depth',str(r/'motion-graphics'/'STEALTH-POV-001'/'Stealth-POV-parallax-v003.mp4'),channel=1,frame_start=start-offset,fit_method='FIT');st.frame_offset_start=offset;st.frame_final_duration=end-start;st.channel=1
assert st.frame_final_start==380 and st.frame_final_end==504
s.render.filepath=str(r/'animatic'/'MonstersLoose-v10-parallax-experiment.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(r/'animatic'/'MonstersLoose-v10-parallax-experiment.blend'))
bpy.ops.render.render(animation=True)
