"""Review number only; the clean title delivery remains unlabelled."""
from pathlib import Path
import bpy
O=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=72
s.view_settings.view_transform='Standard';s.view_settings.look='None'
se=s.sequence_editor_create();se.strips.new_movie(name='Corrected closing title',filepath=str(O/'titles/native_clean.mp4'),channel=1,frame_start=1)
n=se.strips.new_effect(name='Review number',type='TEXT',channel=2,frame_start=1,length=72);n.text='70';n.font_size=23;n.location=(.957,.954);n.color=(1,1,1,1);n.use_shadow=True
r=s.render;r.engine='BLENDER_EEVEE';r.use_sequencer=True
if hasattr(r.image_settings,'media_type'):r.image_settings.media_type='VIDEO'
r.image_settings.file_format='FFMPEG';r.ffmpeg.format='MPEG4';r.ffmpeg.codec='H264';r.ffmpeg.constant_rate_factor='HIGH';r.ffmpeg.audio_codec='NONE';r.filepath=str(O/'batch3_titles_context.mp4')
bpy.ops.render.render(animation=True)
