import bpy,json,warnings,sys
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v58-countdown-planning.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if (st.channel==1 and 2510<=st.frame_final_start<2906) or st.name=='Arctic replacement planning note':seq.remove(st)
shots=[('count5',2510,2537),('count4',2537,2548),('count3',2548,2578),('count2',2578,2638),('duel',2638,2791),('flight',2791,2828),('landing',2828,2906)]
for name,a,b in shots:
 st=seq.new_image('SCN-008-'+name,str(r/'assets'/('SCN-008-'+name+'-v001.png')),channel=1,frame_start=a)
 st.frame_final_duration=b-a
for number,a,b in [('5',2510,2537),('4',2537,2548),('3',2548,2578),('2',2603,2638)]:
 st=seq.new_effect('Remaining '+number,type='TEXT',channel=108,frame_start=a,length=b-a)
 st.text=number;st.location=(.11,.78);st.font_size=110;st.color=(1,.9,.64,1);st.use_shadow=True
 st.font=bpy.data.fonts.load(str(r/'motion-graphics/HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf'))
 if hasattr(st,'use_outline'):st.use_outline=True;st.outline_width=.06;st.outline_color=(.015,.02,.025,1)
 for f,size in [(a,72),(a+2,142),(a+5,110)]:
  st.font_size=size;st.keyframe_insert(data_path='font_size',frame=f)
s.frame_start=2510;s.frame_end=2905
s.render.filepath=str(o/'MonstersLoose-v59-countdown-animatic.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v59-countdown-animatic.blend'))
bpy.ops.render.render(animation=True)
