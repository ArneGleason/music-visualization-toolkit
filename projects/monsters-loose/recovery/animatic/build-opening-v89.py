import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v88-remaining-creatures.blend'))
s=bpy.context.scene;records=[]
for st in s.sequence_editor.strips:
 if st.channel==1 and 4242<=st.frame_final_start<5291:
  src=(Path(bpy.path.abspath(st.directory))/st.elements[0].filename).resolve()
  records.append(dict(id={4242:'SCN-014-BEYOND-FENCE',4414:'SCN-014-FINAL-ESCAPE',4951:'SCN-015-FREE',5121:'SCN-015-WORLD'}[int(st.frame_final_start)],start_frame=int(st.frame_final_start),end_frame_exclusive=int(st.frame_final_end),source=src.relative_to(r).as_posix(),source_in_frame=0,media_type='image',status='storyboard_for_review',note=st.name))
(o/'ending-storyboard-records.json').write_text(json.dumps(records,indent=2))
s.frame_start=1;s.frame_end=5290;s.name='Monsters Loose v89 through ending storyboard'
st=s.sequence_editor.strips.new_effect('Ending storyboard planning note',type='TEXT',channel=110,frame_start=4242,length=1049)
st.text='STORYBOARD / shot planning';st.font_size=21;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v89-through-ending.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v89-through-ending.blend'))
bpy.ops.render.render(animation=True)
