"""Assemble reviewed native action with the accepted nine optical still cuts."""
import copy
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
sys.path.insert(0,str(BASE.parents[1]/'tools'))
from lyric_overlay import write_lyrics
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],check=True,cwd=OUT)
def probe(p): return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(p)]))['streams'][0]
plan=read(BASE/'kling-departure-discovery-v01.json')
reviews=read(OUT/'native-review.json')
assert len(plan['collectedShotIds'])==7
assert all(reviews[t['shotId']]['usable'] for t in plan['shots'])
r=read(BASE/'shots/shotlist.json');assert r['activeReviewEdit']=='v54'
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'}
segments=[]
for t in plan['shots']:
    lead=t['sourceEditStartFrame']-1
    count=t['editFrames']
    p=BASE/t.get('editMotionRef',t['motionRef']);info=probe(p)
    assert int(info['nb_frames'])>=lead+count
    name=t['id']+'-selected.mp4'
    # Accommodate the provider's 1916-pixel width without changing framing.
    vf=f'fps=24,trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB),scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
    run(['-i',str(p),'-vf',vf,'-frames:v',str(count),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',name])
    segments.append(dict(start=t['startFrame'],end=t['startFrame']+count,file=name))
    selection=dict(id=t['id'],motionRef=t.get('editMotionRef',t['motionRef']),sourceEditStartFrame=t['sourceEditStartFrame'],sourceLeadInFrames=lead,availableLeadOutFrames=int(info['nb_frames'])-lead-count,generationId=t['generationId'],plan='kling-departure-discovery-v01.json',userSelected=False,status='Reviewed native draft; playback review pending',reviewNotes=reviews[t['shotId']]['notes'],retime=t.get('retime'))
    s=shots[t['shotId']]
    s.setdefault('motionTests',[]).append(selection)
    s.update(motionSelection=selection,motionRef=t['motionRef'],videoPrompt=t['prompt'],motionReview=reviews[t['shotId']])
    s['nativePlacements']=t['placements']
    t['reviewNotes']=reviews[t['shotId']]['notes']
still_source=BASE/'generated/storyboard/departure-discovery-v04/stills-picture.mp4'
run(['-i',str(still_source),'-vf','trim=start_frame=278:end_frame=351,setpts=N/(24*TB),setsar=1','-frames:v','73','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','zoom-stills.mp4'])
segments.append(dict(start=2873,end=2946,file='zoom-stills.mp4'))
segments.sort(key=lambda s:s['start'])
assert segments[0]['start']==2595 and segments[-1]['end']==3144
assert all(a['end']==b['start'] for a,b in zip(segments,segments[1:]))
assert sum(s['end']-s['start'] for s in segments)==549
(OUT/'concat.txt').write_text(''.join("file '"+s['file']+"'\n" for s in segments),encoding='utf-8')
run(['-f','concat','-safe','0','-i','concat.txt','-an','-c','copy','hybrid-picture.mp4'])
assert int(probe(OUT/'hybrid-picture.mp4')['nb_frames'])==549
data=read(BASE/'generated/animatic/animatic-data.json')
captions=copy.deepcopy(data);captions['phrases']=[p for p in captions['phrases'] if 2595<=p['startFrame']<3144]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=2594;item['endFrameExclusive']-=2594
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
(OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
run(['-i','hybrid-picture.mp4','-i',str(BASE/plan['sourceAnimatic']),'-filter_complex',f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={2594/24}:end={3143/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','549','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==549
save(BASE/'shots/shotlist.json',r);save(BASE/'kling-departure-discovery-v01.json',plan)
save(OUT/'timing-check.json',dict(frames=549,fps=24,startFrame=2595,endFrameExclusive=3144,segments=segments,nineZoomCues=[2873,2887,2891,2894,2899,2903,2908,2912,2915],planetRevealFrame=2946,departureDissolve=False))
options=read(BASE/'generated/storyboard/departure-discovery-v04/review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=plan['sourceAnimatic'],useMotion=True,motionShotIds=[t['shotId'] for t in plan['shots']],presentation='Clean native departure/discovery with immediate camera pullback and nine held optical views',mediaLabel='Departure and discovery / clean motion',continuationNotes='V55: seven clean native takes, immediate departure camera pullback, nine optical still steps at exact cues; planet reveal2946; original master audio retained.')
save(OUT/'review-options.json',options)
cards=[]
for t in plan['shots']:
    src=Path('../../kling-tests/departure-discovery-v01')/t['id']/Path(t['motionRef']).name
    cards.append(f'<article><h2>{html.escape(t["title"])}</h2><video controls preload="metadata" src="{src.as_posix()}"></video><p>{html.escape(t["reviewNotes"])}</p></article>')
(OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Departure and discovery — clean motion</title><style>body{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px}video{width:100%}a{color:#9bd9e9}article{margin:24px 0}</style><h1>Departure and discovery — clean motion</h1><video controls src="timed-still-board.mp4"></video><p><a href="/?v=v55">Full V55</a> · <a href="hybrid-picture.mp4">Clean assembled passage</a></p>'+''.join(cards),encoding='utf-8')
print('Prepared exact 549-frame native assembly')
