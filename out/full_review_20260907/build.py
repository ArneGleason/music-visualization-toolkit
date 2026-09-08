"""Current full review, reusing only verified unchanged previous assembly spans."""
import copy,json,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import inspect_video,load_decisions,resolve_clip
from assembly_timebase import conform_clip
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
END=3830
old=ROOT/'out/opening_through_meant_v1'
edl=json.loads((ROOT/'out/bends_mind_fx_v2/shotlist.json').read_text())
cues=json.loads((ROOT/'out/bends_mind_fx_v2/overlay_cues.json').read_text())
prior=json.loads((old/'shotlist.json').read_text())['shots']
oldc=json.loads((old/'overlay_cues.json').read_text())['shots']
differences=[(a,b) for a,b in zip(prior,edl['shots']) if a!=b]
assert len(differences)==1
a,b=differences[0];assert a['id']==b['id']=='exchange_listener_audition'
assert round(b['start_sec']*24)==2016 and round(b['end_sec']*24)==2122
aa=copy.deepcopy(a);aa['clip']=b['clip'];aa['description']=b['description'];assert aa==b
assert oldc==cues['shots'][:len(oldc)]
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
canal=copy.deepcopy(next(s for s in prod['shots'] if s['id']=='s049'))
canal.update(start_sec=3778/24,end_sec=END/24,dur_sec=(END-3778)/24,frames=END-3778)
edl['shots'].append(canal)
cues['shots'].append({'id':canal['id'],'setup':canal['setup'],'section':canal['section'],'start':3778,'end':END,'lyric':canal['lyric']})
edl['duration_sec']=cues['duration_sec']=END/24;cues['frames']=END
boundary=0
for s in edl['shots']:
    assert round(s['start_sec']*24)==boundary,(s['id'],boundary)
    boundary=round(s['end_sec']*24)
assert boundary==END
decisions=load_decisions(ROOT)
decisions.update(json.loads((ROOT/'out/receiver_voice_review/receiver_decision.json').read_text()))
checks=[]
for s in edl['shots']:
    c=conform_clip(ROOT,resolve_clip(ROOT,s,24,decisions),24,prepare=True)
    if c.get('file'):
        rate,n=inspect_video(str(ROOT/c['file']))
        assert round(c.get('in_sec',0)*24)+s['frames']<=n,(s['id'],n)
        checks.append({'id':s['id'],'source':c,'frames':n})
for name,d in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(d,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"full_review_20260907"')
(OUT/'blender_review.py').write_text(adapter)
for name,start,end in [('specimen',2016,2122),('continuation',2658,END)]:
    with (OUT/(name+'.log')).open('w') as log:
        run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start',start,'--end',end-1,'--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/(name+'.mp4')],stdout=log,stderr=subprocess.STDOUT)
    assert inspect_video(str(OUT/(name+'.mp4')))==(24.,end-start)
graph=(f'[0:v]trim=start_frame=0:end_frame=2016,setpts=N/(24*TB)[a];'
       '[1:v]setpts=N/(24*TB)[b];'
       '[0:v]trim=start_frame=2122:end_frame=2658,setpts=N/(24*TB)[c];'
       '[2:v]setpts=N/(24*TB)[d];'
       '[a][b][c][d]concat=n=4:v=1:a=0,setsar=1[v];'
       f'[3:a]atrim=start=0:end={END/24},asetpts=PTS-STARTPTS[audio]')
run(['ffmpeg','-v','error','-y','-i',old/'preview.mp4','-i',OUT/'specimen.mp4','-i',OUT/'continuation.mp4','-i',ROOT/'audio/song.wav','-filter_complex',graph,'-map','[v]','-map','[audio]','-frames:v',END,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(str(OUT/'preview.mp4'))==(24.,END)
(OUT/'verification.json').write_text(json.dumps({'fps':24,'frames':END,'duration_seconds':END/24,'reused_verified_unchanged_ranges':[[0,2016],[2122,2658]],'newly_rendered_ranges':[[2016,2122],[2658,END]],'early_edl_and_cues_compared':True,'source_checks':checks,'master_once':True,'status':'full review rendered, not production merge'},indent=2))
print('Verified full preview complete.',flush=True)
