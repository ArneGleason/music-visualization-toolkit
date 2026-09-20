import bpy,json,warnings,sys,math
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v60-countdown-and-kick.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
proof='--proof' in sys.argv
for st in list(seq):
 if st.name.startswith('Remaining '):seq.remove(st)
font=bpy.data.fonts.load(str(r/'motion-graphics/HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf'))
for number,a in [('5',2510),('4',2537),('3',2548),('2',2603)]:
 st=seq.new_effect('Count punch '+number,type='TEXT',channel=108,frame_start=a,length=10)
 st.text=number;st.font=font;st.location=(.5,.49);st.color=(1,.91,.66,1)
 st.use_shadow=True;st.use_outline=True;st.outline_width=.045;st.outline_color=(.015,.02,.025,1)
 for offset,size,alpha,angle in [(0,180,.8,-.13),(1,565,1,.04),(3,475,1,-.025),(6,475,1,-.025),(8,620,.6,.02),(9,740,0,.04)]:
  st.font_size=size;st.blend_alpha=alpha;st.transform.rotation=angle
  st.keyframe_insert(data_path='font_size',frame=a+offset)
  st.keyframe_insert(data_path='blend_alpha',frame=a+offset)
  st.transform.keyframe_insert(data_path='rotation',frame=a+offset)
if not proof:
 for st in list(seq):
  if st.channel==1 and st.frame_final_start==2537:seq.remove(st)
 st=seq.new_movie('SCN-008-count4-motion',str(r/'motion-graphics/COUNTDOWN-EDIT-002/count4-timed-v001.mp4'),channel=1,frame_start=2537,fit_method='FIT')
 st.frame_final_duration=11;st.channel=1
 for f,x,y,z in [(2537,0,0,1.025),(2540,0,0,1.025),(2541,10,-8,1.04),(2542,-7,5,1.035),(2543,4,-2,1.03),(2545,0,0,1.025)]:
  t=st.transform;t.offset_x=x;t.offset_y=y;t.scale_x=z;t.scale_y=z
  for prop in ['offset_x','offset_y','scale_x','scale_y']:t.keyframe_insert(data_path=prop,frame=f)
 # Short radial impact strokes, behind the numeral and above the live action.
 for i in range(7):
  angle=2*math.pi*i/7
  st=seq.new_effect('Arm impact ray '+str(i),type='COLOR',channel=85+i,frame_start=2541,length=3)
  st.color=(1,.83,.4);t=st.transform
  t.rotation=angle;t.scale_x=.022;t.scale_y=.005
  for f,dist,alpha in [(2541,35,.9),(2542,57,.75),(2543,76,0)]:
   t.offset_x=-285+math.cos(angle)*dist;t.offset_y=-180+math.sin(angle)*dist;st.blend_alpha=alpha
   t.keyframe_insert(data_path='offset_x',frame=f);t.keyframe_insert(data_path='offset_y',frame=f);st.keyframe_insert(data_path='blend_alpha',frame=f)
s.frame_start=2510 if proof else 1;s.frame_end=2637 if proof else 2905
s.render.filepath=str(o/('v61-number-proof.mp4' if proof else 'MonstersLoose-v61-countdown-punches.mp4'))
if not proof:
 s.name='Monsters Loose v61 animated four and countdown punches'
 bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v61-countdown-punches.blend'))
bpy.ops.render.render(animation=True)
