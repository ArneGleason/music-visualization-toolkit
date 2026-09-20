import bpy,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v63-scene9-shot-plan.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
for st in list(seq):
 if st.channel==1 and 3031<=st.frame_final_start<3223:seq.remove(st)
st=seq.new_image('New monster pitch',str(r/'assets/ANCH-009-B-v001.png'),channel=1,frame_start=3031,fit_method='FIT');st.frame_final_duration=57
bx=st.transform.scale_x;by=st.transform.scale_y
for f,z,x,y in [(3031,1,0,0),(3078,1,0,0),(3087,1.1,16,20)]:
 t=st.transform;t.scale_x=z*bx;t.scale_y=z*by;t.offset_x=x;t.offset_y=y
 for prop in ['scale_x','scale_y','offset_x','offset_y']:t.keyframe_insert(data_path=prop,frame=f)
for name,path,a,length in [('Schematic blur zoom','SCHEMATIC-ZOOM-001/schematic-blur-zoom-v001.mp4',3088,16),('Living schematic swallow','SCHEMATIC-ACTION-001/schematic-timed-v001.mp4',3104,119)]:
 st=seq.new_movie(name,str(r/'motion-graphics'/path),channel=1,frame_start=a,fit_method='FIT');st.frame_final_duration=length;st.channel=1
# Static original-paper strips keep ruler and heading perfectly legible.
for name,left,right,bottom,top in [('ruler',1480,0,0,0),('header',0,0,810,0)]:
 st=seq.new_image('Fixed schematic '+name,str(r/'assets/SCN-009-scale-diagram-v001.png'),channel=83 if name=='ruler' else 84,frame_start=3104,fit_method='FIT')
 st.frame_final_duration=119;st.blend_type='ALPHA_OVER'
 st.crop.min_x=left;st.crop.max_x=right;st.crop.min_y=bottom;st.crop.max_y=top
for st in seq:
 if st.name=='Scene9 storyboard planning note':
  st.frame_final_duration=198;st.text='LAB / FIRE performances pending'
visuals=sorted([st for st in seq if st.channel==1],key=lambda x:x.frame_final_start)
for a,b in zip(visuals,visuals[1:]):assert a.frame_final_end==b.frame_final_start,(a.name,b.name)
s.frame_start=1;s.frame_end=3222;s.name='Monsters Loose v64 living schematic'
s.render.filepath=str(o/'MonstersLoose-v64-living-schematic.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v64-living-schematic.blend'))
bpy.ops.render.render(animation=True)
