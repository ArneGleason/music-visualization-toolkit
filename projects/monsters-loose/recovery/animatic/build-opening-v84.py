import bpy,warnings,json
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v83-cyclops-turbulence.blend'))
s=bpy.context.scene;records=[]
for st in s.sequence_editor.strips:
 if st.channel==1 and 3775<=st.frame_final_start<4126:
  src=Path(bpy.path.abspath(st.directory))/st.elements[0].filename
  records.append(dict(id='SCN-012-EXCHANGE' if st.frame_final_start==3775 else 'SCN-012-ESCAPE-SHOW',start_frame=int(st.frame_final_start),end_frame_exclusive=int(st.frame_final_end),source=src.relative_to(r).as_posix(),source_in_frame=0,media_type='image',status='storyboard_for_review',note=st.name))
(o/'scene12-storyboard-records.json').write_text(json.dumps(records,indent=2))
s.frame_start=1;s.frame_end=4125;s.name='Monsters Loose v84 Scene12 storyboard'
st=s.sequence_editor.strips.new_effect('Scene12 storyboard planning note',type='TEXT',channel=110,frame_start=3775,length=351)
st.text='STORYBOARD / shot planning';st.font_size=21;st.location=(.5,.035);st.color=(1,.85,.45,1);st.use_shadow=True
s.render.filepath=str(o/'MonstersLoose-v84-next-scene-storyboard.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v84-next-scene-storyboard.blend'))
bpy.ops.render.render(animation=True)
