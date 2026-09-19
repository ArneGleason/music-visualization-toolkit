import bpy,pathlib,json
root=pathlib.Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(root/'MonstersLoose-scene-roughout-v04.blend'))
original=bpy.context.scene
bounds=(original.frame_start,original.frame_end)
bpy.ops.wm.open_mainfile(filepath=str(root/'MonstersLoose-clean-animatic-v05.blend'))
s=bpy.context.scene
s.frame_start,s.frame_end=bounds
visuals=sorted((st for st in s.sequence_editor.strips if st.channel==1),key=lambda st:st.frame_final_start)
assert sum(st.type=='MOVIE' for st in visuals)==2
for st in visuals:
 assert st.color_multiply==1
for left,right in zip(visuals,visuals[1:]):
 assert left.frame_final_end==right.frame_final_start,(left.name,right.name)
assert visuals[0].frame_final_start<=s.frame_start
assert visuals[-1].frame_final_end>s.frame_end
print('FULL_RANGE',bounds,'VISUALS',len(visuals),flush=True)
s.render.image_settings.media_type='IMAGE'
s.render.image_settings.file_format='PNG'
for frame in (1100,2600,4400):
 s.frame_set(frame)
 s.render.filepath=str(root/f'v05-full-check-{frame}.png')
 bpy.ops.render.render(write_still=True)
s.render.image_settings.media_type='VIDEO'
s.render.image_settings.file_format='FFMPEG'
s.render.filepath=str(root/'MonstersLoose-clean-animatic-v05-full.mp4')
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'MonstersLoose-clean-animatic-v05-full.blend'))
bpy.ops.render.render(animation=True)
