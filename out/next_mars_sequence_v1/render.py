"""Extend approved globe, correctly place old sync, land in existing colony."""
import json,subprocess,copy,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)

# Reuse v2's exact generator construction, then apply the approved v3 backdrop.
builder=(ROOT/'out/world_pullback_refined_v2/render.py').read_text().split("exec(compile(s,str(p),'exec')")[0]
ns={'__file__':str(OUT/'render.py')}
exec(compile(builder,'build_globe','exec'),ns)
core=ns['s'].split('def run(a,**kw):')[0]
core=core.replace('for i,sf in enumerate(range(2122,2199)):',
                  'stars=make_space(cv2,x,y)\nfor i,sf in enumerate(range(2122,2233)):')
# Nothing before frame2199 changes. Continue subtle surface rotation and pullback.
core=core.replace('    nx=(x-640)/radius;',
                  '    radius*=1-.035*smooth((sf-2199)/34)\n    nx=(x-640)/radius;')
core=core.replace('u=((longitude/np.pi+.5)*475)',
                  'u=((longitude/np.pi+.5+max(0,sf-2199)*.0006)*475)')
space=runpy.run_path(str(ROOT/'out/world_nebula_v3/space.py'))['make_space']
exec(compile(core,'render_globe','exec'),{'__file__':str(OUT/'render.py'),'make_space':space})
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','111','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'planet_clean.mp4'])

# Measured guide source origin: raw stem91.9655 + placement.178348.
# Conform after precise trim so no extra frame-rounded source offset is applied.
origin=92.143848
source_in=2233/24-origin
run(['ffmpeg','-v','error','-y','-i',ROOT/'clips/raw/astronaut_close_sync_s026_kling.mp4',
     '-vf',f'trim=start={source_in:.12f},setpts=PTS-STARTPTS,fps=24',
     '-frames:v','38','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'close_clean.mp4'])

edl=json.loads((ROOT/'out/specimen_signal_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/specimen_signal_v1/overlay_cues.json').read_text())
world=edl['shots'][-1]
world.update(end_sec=2233/24,dur_sec=111/24,frames=111,
             lyric='I see the world plus more. More is probably nothing. Yes, I see the world.',
             description='Approved nebula reveal extended with subtle continuing surface rotation and pullback.',
             still='Mars globe, procedural nebula and message traces.',
             clip={'file':'out/next_mars_sequence_v1/planet_clean.mp4','in_sec':0,'speed':1})
cues['shots'][-1].update(end=2233,lyric=world['lyric'])
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
for old_id,new_id,start,end,filename,source_in_sec,lyric in [
    ('s026','close_reply_timing_test',2233,2271,'out/next_mars_sequence_v1/close_clean.mp4',0,'Close but no see car.'),
    ('s027','mars_colony_reply_test',2271,2399,'clips/raw/mars_domes_wide_v6.mp4',.5,"Subject: Mars! You come back around. I'll pull it into a shape and spin your world around.")]:
    shot=copy.deepcopy(next(s for s in prod['shots'] if s['id']==old_id))
    shot.update(id=new_id,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start,
                lyric=lyric,prompt='',clip={'file':filename,'in_sec':source_in_sec,'speed':1})
    edl['shots'].append(shot)
    cues['shots'].append({'id':new_id,'setup':shot['setup'],'section':shot['section'],'start':start,'end':end,'lyric':lyric})
edl['duration_sec']=cues['duration_sec']=2399/24;cues['frames']=2399
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2122','--end','2398','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={2122/24}:end={2399/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','277','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','preview_song_frames':[2122,2399],'frames':277,
    'planet_song_frames':[2122,2233],'planet_extension':'34 new procedural frames, no loop/freeze; slow surface drift and3.5percent radius reduction.',
    'close_song_frames':[2233,2271],'close_original_source_seconds':[source_in,source_in+38/24],
    'close_measured_song_origin_seconds':origin,'guide_alignment_correlation':.90890569,
    'returned_audio_guide_correlation':.99991944,'close_conform':'trim at measured in-point, timestamp-based fps24; no slowdown or audio stretch; native30fps sample quantization remains.',
    'colony_song_frames':[2271,2399],'colony_source_frames':[12,140],'colony_source_origin':2259,
    'audio':'Master once; all generated audio discarded','production_merged':False},indent=2))
print('Next Mars sequence ready:277frames.')
