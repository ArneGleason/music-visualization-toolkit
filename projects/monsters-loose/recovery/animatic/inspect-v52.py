import bpy
from pathlib import Path
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');bpy.ops.wm.open_mainfile(filepath=str(r/'animatic/MonstersLoose-v52-through-habitats.blend'))
for x in bpy.context.scene.sequence_editor.strips:
 if x.type=='SOUND' or x.frame_final_end>2440:print('STRIP',x.name,x.type,x.channel,x.frame_start,x.frame_final_start,x.frame_final_end,getattr(x,'text','')[:150])
