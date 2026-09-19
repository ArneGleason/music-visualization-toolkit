import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(r/'MonstersLoose-v23-arctic.blend'))
s=bpy.context.scene
out=[]
for st in s.sequence_editor.strips:
 if st.channel==1 or (st.type=='TEXT' and 1250<=st.frame_final_start<2000):
  out.append({'name':st.name,'type':st.type,'start':st.frame_final_start,'end':st.frame_final_end,'channel':st.channel,'text':getattr(st,'text',''),'directory':getattr(st,'directory',''),'elements':[e.filename for e in st.elements] if st.type=='IMAGE' else []})
(r/'v23-timeline-inspect.json').write_text(json.dumps(out,indent=2))
