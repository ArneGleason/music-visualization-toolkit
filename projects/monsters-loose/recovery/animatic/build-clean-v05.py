import bpy,json,pathlib,warnings
warnings.filterwarnings('ignore',category=DeprecationWarning)
root=pathlib.Path(__file__).resolve().parent; job=root.parent
bpy.ops.wm.open_mainfile(filepath=str(root/'MonstersLoose-scene-roughout-v04.blend'))
s=bpy.context.scene; seq=s.sequence_editor.strips
# Keep only source visuals, master audio, timed lyric words and scene captions.
for st in list(seq):
 keep=(st.channel==1 or st.type=='SOUND' or (st.type=='TEXT' and ('acoustic_start_seconds' in st or st.channel in (100,101,102))))
 if not keep: seq.remove(st); continue
 if st.channel==1: st.color_multiply=1
 if st.type=='TEXT' and 'acoustic_start_seconds' in st:
  st.font_size*=.5
  st.transform.offset_x*=.5
  st.transform.offset_y=st.transform.offset_y*.5-290
  st.use_shadow=True
 elif st.type=='TEXT' and st.channel in (100,101,102):
  st.transform.offset_y={100:331,101:303,102:278}[st.channel]
  st.font_size={100:21,101:22,102:22}[st.channel]
  st.use_shadow=True
  if st.name.startswith('01 /') and st.channel==101:st.text='Visitors approach the remote swamp zoo by helicopter.'
  if st.name.startswith('01 /') and st.channel==102:st.text='A gentle landing brings them to the laboratory compound.'
# Move the animated lyric bounce along with the static word positions.
lyric_paths={st.path_from_id()+'.transform.offset_y' for st in seq if st.type=='TEXT' and 'acoustic_start_seconds' in st}
for layer in s.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for curve in bag.fcurves:
    if curve.data_path in lyric_paths:
     for point in curve.keyframe_points:
      point.co.y=point.co.y*.5-290
      point.handle_left.y=point.handle_left.y*.5-290
      point.handle_right.y=point.handle_right.y*.5-290
     curve.update()
# Use the opening shotlist's timing-grid-derived frame boundaries.
for st in list(seq):
 if st.channel==1 and st.frame_final_start<207:seq.remove(st)
shots=json.loads((job/'shots'/'shotlist.json').read_text(encoding='utf-8'))['shots']
for sh in shots:
 st=seq.new_movie(sh['id'],str(job/sh['source']),channel=1,frame_start=sh['start_frame']-sh['source_in_frame'],fit_method='FIT')
 st.frame_offset_start=sh['source_in_frame'];st.frame_final_duration=sh['end_frame_exclusive']-sh['start_frame']
 assert st.frame_final_start==sh['start_frame'] and st.frame_final_end==sh['end_frame_exclusive']
 s.timeline_markers.new(sh['id'],frame=sh['start_frame'])
s.name='Monsters Loose - clean video animatic v05'
s.frame_start=1;s.frame_end=360
s.render.resolution_percentage=100
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
for frame in (20,150,240,330):
 s.frame_set(frame);s.render.filepath=str(root/f'v05-preview-{frame}.png');bpy.ops.render.render(write_still=True)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG'
s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH';s.render.ffmpeg.audio_codec='AAC';s.render.ffmpeg.audio_bitrate=256
s.render.filepath=str(root/'MonstersLoose-clean-animatic-v05-first15s.mp4');s.frame_set(1)
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(root/'MonstersLoose-clean-animatic-v05.blend'))
if '--render' in __import__('sys').argv:bpy.ops.render.render(animation=True)
