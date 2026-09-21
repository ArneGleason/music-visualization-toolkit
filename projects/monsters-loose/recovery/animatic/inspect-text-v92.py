import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(r/'MonstersLoose-v92-outro-performances.blend'))
rows=[]
for s in bpy.context.scene.sequence_editor.strips:
 if s.type=='TEXT':rows.append(dict(name=s.name,channel=s.channel,text=s.text,location=list(s.location),start=int(s.frame_final_start),end=int(s.frame_final_end)))
(r/'v92-text-strips.json').write_text(json.dumps(rows,indent=2))
groups={}
for s in rows:groups.setdefault(str(s['channel']),[]).append(s)
for ch,ss in groups.items():print(ch,len(ss),ss[:2])
