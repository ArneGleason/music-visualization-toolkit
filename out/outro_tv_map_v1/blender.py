from pathlib import Path
import bpy,json
OUT=Path(__file__).resolve().parent
cfg=json.loads((OUT/'settings.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.resolution_x=1280; sc.render.resolution_y=720
sc.render.resolution_percentage=100; sc.render.fps=24
sc.frame_start=1; sc.frame_end=cfg['frames']
sc.view_settings.view_transform='Standard'
sc.view_settings.look='None'
ed=sc.sequence_editor_create(); strips=ed.strips
base=strips.new_movie('Accepted A1 Kling',cfg['source'],channel=1,frame_start=1)
overlay=strips.new_image('Biology to star map',str(OUT/'layers/000.png'),channel=2,frame_start=1)
for n in range(1,cfg['frames']): overlay.elements.append(f'{n:03}.png')
overlay.frame_final_duration=cfg['frames']; overlay.blend_type='ALPHA_OVER'
overlay.alpha_mode='STRAIGHT'
sc.render.use_sequencer=True
r=sc.render
if hasattr(r.image_settings,'media_type'): r.image_settings.media_type='VIDEO'
r.image_settings.file_format='FFMPEG'; r.ffmpeg.format='MPEG4'; r.ffmpeg.codec='H264'
r.ffmpeg.constant_rate_factor='HIGH'; r.ffmpeg.audio_codec='NONE'
r.filepath=str(OUT/'clean.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'tv_map.blend'))
bpy.ops.render.render(animation=True)
