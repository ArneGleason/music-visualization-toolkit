import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v69-natural-snow-overlap.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if (st.channel==1 and 2906<=st.frame_final_start<3088) or st.name=='Scene9 storyboard planning note':seq.remove(st)
for name,a,n in [('discussion',2906,68),('fire',2974,57),('presentation',3031,57)]:
 st=seq.new_movie('Scene9 '+name+' motion',str(r/f'motion-graphics/SCENE9-PERFORMANCES-001/{name}-timed-v001.mp4'),channel=1,frame_start=a,fit_method='FIT');st.frame_final_duration=n;st.channel=1
 if name=='presentation':
  bx=st.transform.scale_x;by=st.transform.scale_y
  for f,z,x,y in [(3031,1,0,0),(3078,1,0,0),(3087,1.1,16,20)]:
   t=st.transform;t.scale_x=z*bx;t.scale_y=z*by;t.offset_x=x;t.offset_y=y
   for prop in ['scale_x','scale_y','offset_x','offset_y']:t.keyframe_insert(data_path=prop,frame=f)
for st in seq:
 if st.channel==1 and st.frame_final_start==3088:st.filepath=str(r/'motion-graphics/SCHEMATIC-ZOOM-002/schematic-blur-zoom-v001.mp4')
 if st.name.startswith('Rear cage '):
  for f,x,y in [(26,158,136),(34,166,121),(42,164,112),(50,169,103),(58,168,99),(67,170,93)]:
   st.location=((1080+x)/1280,1-(30+y)/720);st.keyframe_insert(data_path='location',frame=2906+f)
visuals=sorted([st for st in seq if st.channel==1],key=lambda x:x.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
s.name='Monsters Loose v70 scene9 performances';s.frame_start=1;s.frame_end=3222
s.render.filepath=str(o/'MonstersLoose-v70-scene9-performances.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v70-scene9-performances.blend'))
bpy.ops.render.render(animation=True)
