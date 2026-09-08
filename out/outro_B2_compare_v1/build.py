"""Matched B2 comparison and proposed best-of; review only."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip
folders=['outro_B2_take1_kling_v1','outro_B2_v2']
paths=[];checks=[]
for folder in folders:
    d=ROOT/'out'/folder;h=json.loads((d/'handoff.json').read_text())
    for key in ['synced','synced_original']:
        r=h['claude_result'][key]
        assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256']
    paths.append(conform_clip(ROOT,{'file':str(d/'synced.mp4'),'speed':1},24,prepare=True)['file'])
    def audio(p):
        return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4')
    a=audio(d/'synced.mp4');b=audio(d/'guide.wav');n=min(len(a),len(b))
    c=float(np.corrcoef(a[:n],b[:n])[0,1]); assert c>.95
    checks.append({'take':folder,'hashes_verified':True,'audio_zero_lag_correlation':c})
ranges=[(11,42),(80,111),(141,184)]
common=['ffmpeg','-v','error','-n','-i',paths[0],'-i',paths[1],'-i',str(ROOT/'audio/song.wav')]
def render(name,compare):
    fg=[]
    for j,(lo,hi) in enumerate(ranges):
        if compare:
            for k in range(2):
                # Larger face view for the diagnostic, identical crop in both takes.
                fg.append(f'[{k}:v]trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,crop=640:500:320:0,scale=640:500,pad=640:540:0:40,drawtext=fontfile=\'C\\:/Windows/Fonts/arial.ttf\':text=\'Take {k+1}\':x=18:y=8:fontsize=24:fontcolor=white[p{j}{k}]')
            fg.append(f'[p{j}0][p{j}1]hstack=inputs=2[v{j}]')
        else:
            k=0 if j<2 else 1
            fg.append(f'[{k}:v]trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS[v{j}]')
        fg.append(f'[2:a]atrim=start={(4320+lo)/24}:end={(4320+hi)/24},asetpts=PTS-STARTPTS[a{j}]')
    fg.append('[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]')
    target=OUT/name
    subprocess.run(common+['-filter_complex',';'.join(fg),'-map','[v]','-map','[a]','-frames:v','105','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(target)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(target)]))
    assert p['streams'][0]['nb_read_frames']=='105' and p['streams'][0]['r_frame_rate']=='24/1'
render('comparison.mp4',True)
render('proposed_best_of.mp4',False)
(OUT/'verification.json').write_text(json.dumps({'checks':checks,'ranges':ranges,'frames':105,'fps':24,'proposed_takes':[1,1,2],'production_changed':False},indent=2))
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'comparison.mp4'),'-vf',r'select=eq(n\,40)','-frames:v','1',str(OUT/'check.png')],check=True)
print('Both105-frame reviews verified. No offsets or cut changes.')
