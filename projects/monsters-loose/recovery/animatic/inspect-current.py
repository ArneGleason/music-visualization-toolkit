import bpy
bpy.ops.wm.open_mainfile(filepath=r'C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913\animatic\MonstersLoose-clean-animatic-v05-full.blend')
for x in bpy.context.scene.sequence_editor.strips:
 if x.frame_final_start<1350 and (x.channel==1 or (x.type=='TEXT' and x.channel in (100,101,102))):print(x.name,x.type,x.channel,x.frame_final_start,x.frame_final_end,getattr(x,'text',''),getattr(x,'filepath',''))
