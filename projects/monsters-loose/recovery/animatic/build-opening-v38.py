import bpy,json
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v37-through-habitats.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and st.frame_final_start==1708:st.frame_offset_start+=71
sh=next(x for x in json.loads((r/'shots/shotlist.json').read_text())['shots'] if x['id']=='HARPER-LASSO-001')
st=seq.new_movie(sh['id'],str(r/sh['source']),channel=1,frame_start=1648,fit_method='FIT');st.frame_offset_start=60;st.frame_final_duration=71;st.channel=1
s.timeline_markers.new('LASSO: retained take004 source60',frame=1708);s.timeline_markers.new('PLAN: rope-net intercept on One',frame=1779)
# Make the upcoming incident placeholder explicit without inventing footage.
for st in list(seq):
 if st.type=='TEXT' and st.channel in (100,101,102) and st.frame_final_start==1708:
  end=st.frame_final_end;st.frame_final_end=1779
  new=seq.new_effect(name='Upcoming net shot plan '+str(st.channel),type='TEXT',channel=st.channel,frame_start=1779,length=end-1779)
  for prop in ['font','font_size','color','blend_type','location','anchor_x','anchor_y','alignment_x']:setattr(new,prop,getattr(st,prop))
  new.transform.offset_x=st.transform.offset_x;new.transform.offset_y=st.transform.offset_y
  new.text={100:'06 / UPCOMING SHOT PLAN',101:'Near escape: Harper triggers a falling rope net.',102:'Existing still is a placeholder; incident not generated.'}[st.channel]
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,a.frame_final_end,b.name,b.frame_final_start)
assert sum(st.type=='SOUND' for st in seq)==1
s.frame_start=1;s.frame_end=2461;s.name='Monsters Loose v38 retained lasso selection'
s.render.filepath=str(o/'MonstersLoose-v38-opening-through-habitats.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v38-through-habitats.blend'));bpy.ops.render.render(animation=True)
