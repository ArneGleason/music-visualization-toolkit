import bpy
bpy.ops.wm.open_mainfile(filepath='C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913/animatic/MonstersLoose-v83-cyclops-turbulence.blend')
for x in bpy.context.scene.sequence_editor.strips:
 if x.frame_final_end>3774 and (x.channel==1 or x.type in ['SOUND','TEXT']):print(x.name,x.type,x.channel,x.frame_final_start,x.frame_final_end,getattr(x,'text',''),getattr(x,'filepath',''))

