import bpy,json,warnings,sys
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v93-swamp-cousin-beacons.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
changes={4242:'motion-graphics/OUTRO-LIGHTS-002/SCN-014-BEYOND-FENCE-beacons-v002.mp4',4414:'motion-graphics/OUTRO-001/CEO-timed-v001.mp4',4719:'motion-graphics/OUTRO-001/INSPECTOR-timed-v001.mp4',4951:'motion-graphics/OUTRO-LIGHTS-002/SCN-015-FINALE-beacons-v002.mp4'}
for start,source in changes.items():
 old=next(st for st in seq if st.channel==1 and st.frame_final_start==start);duration=int(old.frame_final_duration);seq.remove(old)
 st=seq.new_movie(Path(source).stem,str(r/source),channel=1,frame_start=start,fit_method='FIT');st.frame_final_duration=duration;st.channel=1
def title(name,text,channel,font,size,y):
 st=seq.new_effect(name,type='TEXT',channel=channel,frame_start=5279,length=12)
 st.text=text;st.font=bpy.data.fonts.load(font);st.font_size=size;st.location=(.5,y);st.alignment_x='CENTER';st.anchor_y='CENTER'
 st.color=(1,.90,.69,1);st.use_shadow=True;st.shadow_color=(.012,.017,.015,1)
 return st
title('Final title Monsters Undone','MONSTERS UNDONE',110,'C:/Windows/Fonts/georgiab.ttf',34,.125)
title('Final credit Arne Gleason','© 2026 Arne Gleason',111,'C:/Windows/Fonts/georgia.ttf',22,.068)
s.name='Monsters Undone v94 final credit and refined beacons';s.frame_end=5290
s.render.filepath=str(o/'MonstersUndone-v94.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersUndone-v94.blend'))
if '--still' in sys.argv:
 s.frame_start=5279;s.frame_end=5290;s.render.filepath=str(o/'MonstersUndone-v94-credit-check.mp4');bpy.ops.render.render(animation=True)
else:bpy.ops.render.render(animation=True)
