from pathlib import Path
import bpy,json
OUT=Path(__file__).resolve().parent
cfg=json.loads((OUT/'settings.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100
sc.render.fps=24;sc.frame_start=1;sc.frame_end=cfg['frames'];sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
strips=sc.sequence_editor_create().strips
for ch,folder,blend in [(1,'optical','REPLACE'),(2,'lights','ADD'),(3,'room','ADD')]:
    parent=OUT if folder=='room' else OUT.parent/'outro_B1_afterglow_v1'
    st=strips.new_image(folder,str(parent/folder/'000.png'),channel=ch,frame_start=1)
    for i in range(1,cfg['frames']):st.elements.append(f'{i:03}.png')
    st.frame_final_duration=cfg['frames'];st.blend_type=blend
r=sc.render;r.use_sequencer=True
if hasattr(r.image_settings,'media_type'):r.image_settings.media_type='VIDEO'
r.image_settings.file_format='FFMPEG';r.ffmpeg.format='MPEG4';r.ffmpeg.codec='H264';r.ffmpeg.constant_rate_factor='HIGH';r.ffmpeg.audio_codec='NONE';r.filepath=str(OUT/'clean.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'afterglow.blend'))
bpy.ops.render.render(animation=True)
