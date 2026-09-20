import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v62-next-creation-planning.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 2906<=st.frame_final_start<3223:seq.remove(st)
shots=[('Lab discussion','ANCH-009-A-v001.png',2906,2974),('Town fire reprise','SCN-009-town-gorilla-v001.png',2974,3031),('New monster pitch','ANCH-009-B-v001.png',3031,3096),('Fifty foot schematic','SCN-009-scale-diagram-v001.png',3096,3223)]
for name,file,a,b in shots:
 st=seq.new_image(name,str(r/'assets'/file),channel=1,frame_start=a,fit_method='FIT');st.frame_final_duration=b-a
 base_x=st.transform.scale_x;base_y=st.transform.scale_y
 if name=='New monster pitch':
  for f,z,x,y in [(3031,1,0,0),(3079,1,0,0),(3095,1.42,90,90)]:
   t=st.transform;t.scale_x=z*base_x;t.scale_y=z*base_y;t.offset_x=x;t.offset_y=y
   for prop in ['scale_x','scale_y','offset_x','offset_y']:t.keyframe_insert(data_path=prop,frame=f)
 if name=='Fifty foot schematic':
  for f,z in [(3096,1),(3158,1.035),(3222,1.035)]:
   st.transform.scale_x=z*base_x;st.transform.scale_y=z*base_y
   st.transform.keyframe_insert(data_path='scale_x',frame=f);st.transform.keyframe_insert(data_path='scale_y',frame=f)
# One visible eye in the side-facing creature silhouette, behind cage bars.
for label,size,color,alpha in [('halo',25,(.8,.005,.003,1),.25),('eye',12,(1,.015,.006,1),1),('hot core',5,(1,.35,.08,1),.8)]:
 st=seq.new_effect('Rear cage '+label,type='TEXT',channel=86+['halo','eye','hot core'].index(label),frame_start=2932,length=42)
 st.text='•';st.font_size=size;st.location=(.925,.757);st.color=color;st.use_shadow=False
 for f,v in [(2932,0),(2940,alpha),(2964,alpha*.8),(2973,alpha)]:
  st.blend_alpha=v;st.keyframe_insert(data_path='blend_alpha',frame=f)
for st in seq:
 if st.name=='Scene9 storyboard planning note':st.text='SHOT PLAN / performances pending'
 if st.type=='TEXT' and st.channel==102 and st.frame_final_start==2906:st.text='Town-fire reprise, then the proposed monster at fifty feet'
s.frame_start=1;s.frame_end=3222;s.name='Monsters Loose v63 scene9 directed shot plan'
s.render.filepath=str(o/'MonstersLoose-v63-scene9-shot-plan.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v63-scene9-shot-plan.blend'))
bpy.ops.render.render(animation=True)
