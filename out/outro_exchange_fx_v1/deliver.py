from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import load_decisions,resolve_clip
files=['out/outro_tv_map_v2/clean.mp4','out/outro_B1_afterglow_v4/clean.mp4','out/outro_A2_tv_v1/clean.mp4','out/outro_B2_afterglow_v1/clean.mp4']
cuts=[(0,12,67,4177,4232),(1,67,97,4232,4262),(0,97,166,4262,4331),(3,11,42,4331,4362),(2,42,80,4362,4400),(3,80,111,4400,4431),(2,111,141,4431,4461),(3,141,184,4461,4504)]
args=['ffmpeg','-v','error','-n']
for f in files:args+=['-i',str(ROOT/f)]
args+=['-i',str(ROOT/'audio/song.wav')]
fg=[];snap=[]
for j,(k,a,b,s,e) in enumerate(cuts):
    # Explicit review IDs, not a replacement of production shot IDs.
    shot={'id':f'outro_v2_review_{j}','setup':'outro_v2_review','clip':{'file':files[k],'in_sec':a/24,'speed':1}}
    resolve_clip(ROOT,shot,24,load_decisions(ROOT),start=s,end=e)
    assert b-a==e-s
    fg.append(f'[{k}:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{j}]')
    snap.append({'song':[s,e],'source':[a,b],'file':files[k]})
fg.append(''.join(f'[v{j}]' for j in range(len(cuts)))+'concat=n=8:v=1:a=0[v]')
fg.append(f'[4:a]atrim=start={4177/24}:end={4504/24},asetpts=PTS-STARTPTS[a]')
subprocess.run(args+['-filter_complex',';'.join(fg),'-map','[v]','-map','[a]','-frames:v','327','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
for f,n in [(files[2],191),(files[3],191),('out/outro_exchange_fx_v1/preview.mp4',327)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/f),'-f','null','-'],check=True)
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(ROOT/f)]))
    assert p['streams'][0]['nb_read_frames']==str(n) and p['streams'][0]['r_frame_rate']=='24/1'
(OUT/'cut_snapshot.json').write_text(json.dumps(snap,indent=2))
print('327-frame straight-cut exchange decoded and verified, song4177..4504.')
