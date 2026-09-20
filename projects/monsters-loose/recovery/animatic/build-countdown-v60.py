import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v59-countdown-animatic.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
selections=json.loads((r/'motion-graphics/COUNTDOWN-EDIT-001/selections.json').read_text())
for st in list(seq):
 if st.channel==1 and 2510<=st.frame_final_start<2906 and st.name!='SCN-008-count4':seq.remove(st)
for name,sel in selections.items():
 st=seq.new_movie('SCN-008-'+name,str(r/sel['output']),channel=1,frame_start=sel['start_frame'],fit_method='FIT')
 st.frame_final_duration=sel['frames'];st.channel=1
# Move counts above faces and apply brief supported impact jolts.
for st in seq:
 if st.type=='TEXT' and st.name.startswith('Remaining '):st.location=(.07,.91)
 if st.type=='TEXT' and 2510<=st.frame_final_start<2906 and not st.name.startswith('Remaining '):
  if 'spectators' in st.text or 'Visitors root' in st.text or 'OPEN:' in st.text:st.text='Wilderness battle ladder: green reptile versus Arctic finalist'
  elif 'over mountains' in st.text:st.text='One kick launches the Arctic beast toward its home mountains'
  elif 'prepares to return' in st.text:st.text='A long snow skid; the indestructible beast rests intact'
for name,hit in [('count5',2513),('count4',2537),('count3',2552),('count2',2603),('duel',2775),('landing',2833)]:
 st=next(x for x in seq if x.name=='SCN-008-'+name)
 t=st.transform
 for f,x,y,z in [(hit-1,0,0,1.025),(hit,7,-4,1.025),(hit+1,-5,3,1.025),(hit+2,3,-1,1.025),(hit+4,0,0,1.025)]:
  t.offset_x=x;t.offset_y=y;t.scale_x=z;t.scale_y=z
  for prop in ['offset_x','offset_y','scale_x','scale_y']:t.keyframe_insert(data_path=prop,frame=f)
visuals=sorted((st for st in seq if st.channel==1),key=lambda st:st.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
s.frame_start=1;s.frame_end=2905;s.name='Monsters Loose v60 countdown and Arctic homecoming'
s.render.filepath=str(o/'MonstersLoose-v60-through-arctic-homecoming.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v60-countdown-and-kick.blend'))
bpy.ops.render.render(animation=True)
