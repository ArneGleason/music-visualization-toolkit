import bpy,subprocess,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
p=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913/animatic');o=p/'youtube-thumbnails'
bpy.ops.wm.open_mainfile(filepath=str(p/'MonstersUndone-v94-master-1080p.blend'))
s=bpy.context.scene
for st in s.sequence_editor.strips:
 if st.type=='TEXT':st.mute=True
for f,name in [(2170,'MonstersUndone-thumbnail-lizard'),(4234,'MonstersUndone-thumbnail-procession'),(4970,'MonstersUndone-thumbnail-swamp')]:
 s.frame_start=f;s.frame_end=f;s.render.filepath=str(o/(name+'.mp4'));bpy.ops.render.render(animation=True)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/(name+'.mp4')),'-frames:v','1',str(o/(name+'.png'))],check=True)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/(name+'.mp4')),'-frames:v','1','-q:v','2',str(o/(name+'.jpg'))],check=True)
