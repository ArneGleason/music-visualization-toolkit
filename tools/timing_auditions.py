"""Isolated, same-assembler timing hypotheses. Never change the production EDL."""
import copy
import hashlib
import json
import pathlib
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
from assembly_timebase import conform_clip
from assembly_sources import inspect_video

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT/'out/timing_auditions_v1'
FPS = 24


def run(command):
    subprocess.run([str(x) for x in command],cwd=ROOT,check=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    edl_path=ROOT/'shots/shotlist.json'
    original=digest(edl_path)
    edl=json.loads(edl_path.read_text())
    offset=next(t['offsetSec'] for t in json.loads(
        (ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())['tracks']
        if t['id']=='lead-vocal')
    indexed={s['id']:s for s in edl['shots']}
    cases=[
        ('01_opening',143,305,[
            ('A','Current source mapping',{}),
            ('B','Stem-clock correction; missing head held for test',{'s003':6.4758+offset})]),
        ('02_cut43',3290,3382,[
            ('A','Current mapping: old 2.84-second in-point',{}),
            ('B','Old trim removed only',{'s042':137.578}),
            ('C','Old trim removed plus stem-clock correction',{'s042':137.578+offset})]),
        ('03_outro',4165,4262,[
            ('A','Current source mapping',{}),
            ('B','Stem-clock correction; existing head coverage',
             {'o02':4165/FPS+offset,'o03':4165/FPS+offset})])]
    manifest={'production_edl_sha256':original,'master_sha256':digest(ROOT/'audio/song.wav'),
        'fps':FPS,'stem_offset_seconds':offset,'cases':[],
        'limits':'Source timing only. Fixed editorial boundaries, lyrics and master. Held heads are diagnostic, not regenerated phonemes or genuine pre-roll.'}
    for name,first,end,variants in cases:
        parts=[]
        entry={'name':name,'song_frames':[first,end],'variants':[]}
        for letter,label,origins in variants:
            stem=f'{name}_{letter}'
            snapshot=copy.deepcopy(edl)
            changes=[]
            for shot in snapshot['shots']:
                sid=shot['id']
                if sid not in origins:
                    continue
                origin=round(origins[sid]*FPS)
                start=round(shot['start_sec']*FPS)
                desired=start-origin
                source=conform_clip(ROOT,shot['clip'],FPS)
                record={'shot_id':sid,'original_source':shot['clip']['file'],
                    'source_sha256':digest(ROOT/shot['clip']['file']),
                    'old_in_sec':shot['clip']['in_sec'],'measured_song_origin_sec':origins[sid],
                    'quantized_song_origin_frame':origin,'desired_source_in_frame':desired,
                    'held_head_frames':max(0,-desired)}
                if desired<0:
                    # Explicit diagnostic placeholder for unavailable coverage.
                    padded=OUT/f'{stem}_{sid}_headhold.mp4'
                    _,count=inspect_video(source['file'])
                    run(['ffmpeg','-y','-v','error','-i',source['file'],'-vf',
                        f'setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration={-desired/FPS}',
                        '-frames:v',count-desired,'-c:v','libx264','-crf','16','-an',padded])
                    source['file']=str(padded)
                    source['in_sec']=0
                else:
                    source['in_sec']=desired/FPS
                shot['clip']=source
                record['candidate_clip']=source
                changes.append(record)
            shotfile=OUT/f'{stem}_shotlist.json'
            shotfile.write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
            raw=OUT/f'{stem}_blender.mp4'
            with (OUT/f'{stem}.log').open('w') as log:
                subprocess.run([sys.executable,'tools/blender_comp.py','--proxy',
                    '--start',str(first),'--end',str(end-1),'--shotlist',str(shotfile),
                    '--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)],
                    cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
            banner=Image.new('RGBA',(1280,64),(0,0,0,218))
            draw=ImageDraw.Draw(banner)
            font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
            draw.text((18,7),f'{name[3:].replace("_"," ").upper()} | {letter}: {label}',font=font,fill='white')
            small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
            heads=', '.join(f"{c['shot_id']}: {c['held_head_frames']} missing frames held" for c in changes if c['held_head_frames'])
            draw.text((18,39),heads or 'Same song, cut points and lyric timing. Only source mapping varies.',font=small,fill=(220,220,220))
            png=OUT/f'{stem}_label.png';banner.save(png)
            part=OUT/f'{stem}.mp4';parts.append(part)
            graph=(f'[0:v]setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0:format=auto[outv];'
                   f'[2:a]atrim=start={first/FPS}:end={end/FPS},asetpts=PTS-STARTPTS[a]')
            run(['ffmpeg','-y','-v','error','-i',raw,'-i',png,'-i',ROOT/'audio/song.wav',
                '-filter_complex',graph,'-map','[outv]','-map','[a]',
                '-frames:v',end-first,'-c:v','libx264','-preset','fast','-crf','17',
                '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
                '-avoid_negative_ts','disabled','-movflags','+faststart',part])
            entry['variants'].append({'letter':letter,'label':label,'changes':changes,
                                      'file':str(part.relative_to(ROOT))})
        final=OUT/f'{name}_comparison.mp4'
        command=['ffmpeg','-y','-v','error']
        for part in parts:command+=['-i',part]
        graph=''
        for i in range(len(parts)):
            graph+=f'[{i}:v]setpts=PTS-STARTPTS[v{i}];[{i}:a]atrim=end_sample={(end-first)*2000},asetpts=PTS-STARTPTS[a{i}];'
        graph+=''.join(f'[v{i}][a{i}]' for i in range(len(parts)))+f'concat=n={len(parts)}:v=1:a=1[v][a]'
        command+=['-filter_complex',graph,'-map','[v]','-map','[a]',
            '-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',
            '-c:a','aac','-b:a','256k','-avoid_negative_ts','disabled','-movflags','+faststart',final]
        run(command)
        entry['comparison']=str(final.relative_to(ROOT));manifest['cases'].append(entry)
        print('DONE',name,flush=True)
    assert original==digest(edl_path),'Production edit changed during audition'
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')


if __name__=='__main__':main()
