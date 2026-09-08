"""Bounded existing-footage audition, complete lyric phrases, no paid work."""
import copy
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
previous=ROOT/'out/garden_guide_conductor_v4'
edl=json.loads((previous/'shotlist.json').read_text())
cues=json.loads((previous/'overlay_cues.json').read_text())
production=json.loads((ROOT/'shots/shotlist.json').read_text())
mapping=[]
for old_id,new_id,start,end,origin,lyric in [
    ('s023','exchange_specimens_audition',1854,2016,1842,
     "Okay, there. You've got it. That should be enough. Just look and tell me."),
    ('s024','exchange_listener_audition',2016,2122,2004,
     "Do you see a pattern? I'm sure it's there. Hard to find, right?"),
]:
    shot=copy.deepcopy(next(s for s in production['shots'] if s['id']==old_id))
    shot.update(id=new_id,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,
                frames=end-start,lyric=lyric,prompt='',
                description='Existing footage timing audition. Offscreen astronomer voice; not a new generation prompt.',
                transition={'type':'cut','dur_sec':0})
    shot['clip'].update(in_sec=(start-origin)/24,speed=1)
    source=ROOT/shot['clip']['file']
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=r_frame_rate,nb_frames','-of','json',str(source)]))['streams'][0]
    assert info['r_frame_rate']=='24/1'
    assert end-origin<=int(info['nb_frames'])
    edl['shots'].append(shot)
    cues['shots'].append({'id':new_id,'setup':shot['setup'],'section':shot['section'],
                          'start':start,'end':end,'lyric':lyric})
    mapping.append({'id':new_id,'song_frames':[start,end],'source':shot['clip']['file'],
                    'source_frames':[start-origin,end-origin],'source_song_origin':origin,
                    'physical_exit_frames':int(info['nb_frames'])-(end-origin)})
edl['duration_sec']=cues['duration_sec']=2122/24
cues['frames']=2122
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending',
    'preview_song_frames':[1786,2122],'preview_frames':336,'fps':24,
    'new_shots':mapping,'garden':'Approved conductor/bloom treatment, original unsynced face while Claude works.',
    'review_cautions':['Specimen source has pronounced framing changes.','Inspection open mouth may read as surprise or speech rather than listening.'],
    'audio':'master only; original clip audio discarded','production_modified':False},indent=2))
def run(args,**kwargs):
    subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kwargs)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b',
         '--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy',
         '--start','1786','--end','2121','--shotlist',OUT/'shotlist.json',
         '--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],
         stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav',
     '-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={1786/24:.12f}:end={2122/24:.12f},asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','336','-c:v','libx264','-crf','17',
     '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Complete:336frames,14seconds; garden, specimens, listener.')
