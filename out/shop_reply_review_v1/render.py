"""Existing souvenir shop, whole-phrase reply after approved world blossom."""
import copy
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
START, CUT, END = 2330, 2399, 2484

def run(args, **kwargs):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True, **kwargs)

edl=json.loads((ROOT/'out/colony_world_blossom_v2/shotlist.json').read_text())
cues=json.loads((ROOT/'out/colony_world_blossom_v2/overlay_cues.json').read_text())
production=json.loads((ROOT/'shots/shotlist.json').read_text())
shot=copy.deepcopy(next(s for s in production['shots'] if s['id']=='s029'))
lyric="No. Don't make it better. Don't want fake shit."
shot.update(id='shop_reply_timing_test',start_sec=CUT/24,end_sec=END/24,
            dur_sec=(END-CUT)/24,frames=END-CUT,lyric=lyric,
            clip={'file':'clips/raw/counterfeit_parade_v6.mp4','in_sec':0,'speed':1})
edl['shots'].append(shot)
cues['shots'].append({'id':shot['id'],'setup':shot['setup'],'section':shot['section'],
                      'start':CUT,'end':END,'lyric':lyric})
edl['duration_sec']=cues['duration_sec']=END/24
cues['frames']=END
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]:
    (OUT/name).write_text(json.dumps(data,indent=2))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b',
         '--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy',
         '--start',START,'--end',END-1,'--shotlist',OUT/'shotlist.json',
         '--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],
        stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav',
     '-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={START/24}:end={END/24},asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v',END-START,'-c:v','libx264','-crf','17',
     '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Shop reply preview ready:154 frames, unchanged footage, revised phrase boundary.')
