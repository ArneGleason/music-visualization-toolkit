import bpy,json
from pathlib import Path
p=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913/animatic')
bpy.ops.wm.open_mainfile(filepath=str(p/'MonstersUndone-v94.blend'))
s=bpy.context.scene
out={'render':{k:getattr(s.render,k) for k in ['resolution_x','resolution_y','resolution_percentage','fps']},'ffmpeg':{k:getattr(s.render.ffmpeg,k) for k in ['format','codec','constant_rate_factor','ffmpeg_preset','audio_codec']},'strips':[]}
for st in s.sequence_editor.strips:
 d=dict(name=st.name,type=st.type,start=st.frame_final_start,end=st.frame_final_end,channel=st.channel)
 if st.type=='MOVIE': d.update(path=bpy.path.abspath(st.filepath),width=st.elements[0].orig_width,height=st.elements[0].orig_height)
 if hasattr(st,'transform'):d['transform']={k:getattr(st.transform,k) for k in ['scale_x','scale_y','offset_x','offset_y']}
 if st.type=='TEXT':d.update(font_size=st.font_size,text=st.text)
 out['strips'].append(d)
(p/'v94-master-audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out['render']),json.dumps(out['ffmpeg']))
