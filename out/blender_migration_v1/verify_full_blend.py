"""Verify actual Blender edit strips, preserving review numbers in the saved file."""
from pathlib import Path
import bpy,json,sys
O=Path(__file__).resolve().parent;R=O.parents[1];p=O/'full_native_assembly.blend'
sys.path.insert(0,str(R/'tools'))
from assembly_timebase import conform_clip
bpy.ops.wm.open_mainfile(filepath=str(p));s=next(q for q in bpy.data.scenes if q.name=='RiversOfMars');strips=s.sequence_editor.strips
rows=json.loads((O/'full_selection_check.json').read_text());issues=[];checks=[]
if s.view_settings.view_transform!='Standard' or s.view_settings.look!='None':issues.append('Unexpected assembly display transform')
shot_meta={q['id']:q for q in json.loads((O/'full_native_review_draft.json').read_text())['shots']}
for row in rows:
 expected_name=row['id']+'_'+shot_meta[row['id']]['setup']
 matches=[st for st in strips if st.type=='MOVIE' and st.name==expected_name]
 if len(matches)!=1:issues.append('Movie selection count '+row['id']);continue
 st=matches[0];a,z=row['song_frames'];path=Path(bpy.path.abspath(st.filepath)).resolve()
 expected=conform_clip(R,{'file':row['file'],'in_sec':row['source_in_frame']/24,'speed':1},24)['file']
 if path!=Path(expected).resolve():issues.append('Unexpected picture '+row['id']+': '+str(path))
 if (st.frame_final_start,st.frame_final_end)!=(a+1,z+1):issues.append('Wrong cut bounds '+row['id'])
 if st.frame_offset_start!=row['source_in_frame']:issues.append('Wrong source inpoint '+row['id'])
 checks.append({'id':row['id'],'start':st.frame_final_start,'end':st.frame_final_end,'source_in':st.frame_offset_start,'file':str(path)})
 name='review_number_'+row['id']
 if not strips.get(name):
  num=strips.new_effect(name=name,type='TEXT',channel=110,frame_start=a+1,length=z-a);num.text=str(row['review_number']);num.font_size=round(720*.032);num.location=(.957,.954);num.color=(1,1,1,1);num.use_shadow=True;num.shadow_color=(0,0,0,1);num.use_outline=True;num.outline_color=(0,0,0,1);num.outline_width=.075
if any(st.name=='beat_flash' and not st.mute for st in strips):issues.append('Retired flash active')
(O/'full_blend_check.json').write_text(json.dumps({'issues':issues,'checks':checks,'frame_range':[s.frame_start,s.frame_end]},indent=2))
assert not issues,issues
bpy.ops.wm.save_as_mainfile(filepath=str(p));print('Verified70movie cuts; preserved review labels in saved assembly.')
