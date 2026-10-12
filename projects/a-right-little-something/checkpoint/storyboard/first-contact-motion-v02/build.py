"""Assemble targeted V63 revisions, with fixed musical cues and original audio."""
import copy
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lyric_overlay import write_lyrics
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(a,cwd=None):subprocess.run(['ffmpeg','-y','-v','error',*a],check=True,cwd=cwd)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(p)]))['streams'][0]
codec=['-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv']
prior=read(OUT/'prior-shotlist.json')
register=read(BASE/'shots/shotlist.json')
plan=read(BASE/'kling-first-contact-motion-v02.json')
shots=sorted([s for s in register['storyboardProposals'] if s.get('batch')=='first-contact-v01'],key=lambda s:s['startFrame'])
byid={s['id']:s for s in shots}
for sid,start,end in [('contact-022',4289,4334),('contact-023',4334,4371),('contact-024',4371,4416)]:
    byid[sid].update(startFrame=start,endFrameExclusive=end,frames=end-start)
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
assert sum(s['frames'] for s in shots)==2122 and shots[-1]['startFrame']==5031
(OUT/'clips').mkdir(exist_ok=True);(OUT/'segments').mkdir(exist_ok=True)

effects={}
for name,count in [('opening',68),('travel',42),('tidal',41),('stars',122),('ground',53)]:
    folder=OUT/(name+'-frames');assert len(list(folder.glob('frame_*.png')))==count,(name,count)
    dest=OUT/(name+'-effect.mp4')
    run(['-framerate','24','-i',str(folder/'frame_%04d.png'),'-frames:v',str(count),*codec,str(dest)])
    effects[name]=dest

new={s['shotId']:s for s in plan['shots'] if '-motion-' in s['id']}
old={m['shotId']:m for m in read(OUT.parent/'first-contact-motion-v01/media-manifest.json') if m['plate']=='main'}
local={'contact-001':('opening',0),'contact-002':('opening',18),'contact-017':('tidal',0),'contact-020':('stars',0),'contact-022':('ground',0),'contact-027-travel':('travel',0)}
entries=[]
for s in shots:
    sid=s['id'];item=dict(shot=sid,startFrame=s['startFrame'],frames=s['frames'],endFrameExclusive=s['endFrameExclusive'])
    if sid in local:
        name,lead=local[sid];source=effects[name];item.update(kind='Blender composite' if name in ['opening','travel'] else 'Blender motion graphics',compositor=(OUT/(name+'.blend')).relative_to(BASE).as_posix())
    elif sid in new:
        take=new[sid];source=BASE/plan['output']/take['id']/(take['id']+'-01-clean.mp4');lead=take['sourceEditStartFrame']-1
        receipt=read(BASE/plan['output']/take['id']/'submission.json')['body']
        test=dict(id=take['id'],plan='kling-first-contact-motion-v02.json',motionRef=source.relative_to(BASE).as_posix(),sourceEditStartFrame=lead+1,
            editFrames=s['frames'],generationId=receipt['generationId'],creditsConsumed=receipt['creditsConsumed'],userSelected=False,draftForReview=True,status='Replacement motion for review')
        s['motionTests']=[t for t in s.get('motionTests',[]) if t['id']!=test['id']]+[test]
        s['motionSelection']=copy.deepcopy(test)
        item.update(kind='Replacement native Kling motion',take=take['id'])
    elif sid=='contact-032':
        source=OUT.parent/'first-contact-motion-v01/finale-composite.mp4';lead=0;item['kind']='Retained Blender finale'
    else:
        source=BASE/old[sid]['motionRef'];lead=old[sid]['sourceEditStartFrame']-1;item['kind']='Retained native Kling motion'
    item.update(source=source.relative_to(BASE).as_posix(),sourceIn=lead,clip=(OUT/'clips'/f'{sid}.mp4').relative_to(BASE).as_posix())
    entries.append(item)

def encode_clip(e):
    count=e['frames']+8;dest=BASE/e['clip']
    run(['-reinit_filter','0','-i',str(BASE/e['source']),'-vf',f"trim=start_frame={e['sourceIn']}:end_frame={e['sourceIn']+count},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:0,setsar=1,tpad=stop_mode=clone:stop_duration=0.334",'-frames:v',str(count),*codec,str(dest)])
    assert int(probe(dest)['nb_frames'])==count
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(encode_clip,entries))

fades={f'contact-{i:03}':4 for i in [16,17,18]}
fades.update({s['id']:6 for s in shots if 4583<=s['startFrame']<5031})
fades['contact-032']=4
segments=[]
for i,e in enumerate(entries):
    count=e['frames'];n=fades.get(e['shot'],0)
    if n:
        prev=entries[i-1];fade=OUT/'segments'/(e['shot']+'-dissolve.mp4')
        filters=(f"[0:v]trim=start_frame={prev['frames']}:end_frame={prev['frames']+n},setpts=N/(24*TB)[a];"
            f"[1:v]trim=start_frame=0:end_frame={n},setpts=N/(24*TB)[b];"
            f"[a][b]blend=all_expr='A*(1-(T*24+1)/{n+1})+B*((T*24+1)/{n+1})'[v]")
        run(['-i',str(BASE/prev['clip']),'-i',str(BASE/e['clip']),'-filter_complex',filters,'-map','[v]','-frames:v',str(n),*codec,str(fade)])
        assert int(probe(fade)['nb_frames'])==n
        segments.append(fade);e['transition']=dict(type='dissolve',frames=n,startFrame=e['startFrame'],outgoingHandles=True)
    body=OUT/'segments'/(e['shot']+'-body.mp4')
    run(['-i',str(BASE/e['clip']),'-vf',f'trim=start_frame={n}:end_frame={count},setpts=N/(24*TB)','-frames:v',str(count-n),*codec,str(body)])
    assert int(probe(body)['nb_frames'])==count-n
    segments.append(body)
    print('Assembled',e['shot'],count,'frames',f'dissolve {n}' if n else '',flush=True)
(OUT/'concat.txt').write_text(''.join("file '"+p.as_posix()+"'\n" for p in segments),encoding='utf-8')
run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-an','-c','copy',str(OUT/'motion-picture.mp4')])
assert int(probe(OUT/'motion-picture.mp4')['nb_frames'])==2122
data=read(BASE/'generated/animatic/animatic-data.json');captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if 3144<=p['startFrame']<5266]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=3143;item['endFrameExclusive']-=3143
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
(OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v62.mp4'
run(['-reinit_filter','0','-i','motion-picture.mp4','-i',str(source),'-filter_complex',
    '[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start=130.958333333333:end=219.375,asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v','2122','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'],cwd=OUT)
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==2122

for e in entries:
    s=byid[e['shot']]
    if e['shot'] in local:
        s['motionSelection']=dict(id=e['shot']+'-blender-v63',motionRef=e['clip'],sourceEditStartFrame=1,editFrames=s['frames'],compositor=e['compositor'],userSelected=False,draftForReview=True,status='Local effects/composite revision for review')
    elif e['shot']=='contact-024':s['motionSelection']['editFrames']=45
    s['motionRef']=s['motionSelection']['motionRef']
    if 'transition' in e:s['editorialTransition']=e['transition']
    s['status']='V63 revision review pending' if e['shot'] in local or e['shot'] in new or 'transition' in e or e['shot'] in ['contact-023','contact-024'] else s['status']
for sid,filename,title,description in [
    ('contact-010','creatures-clearing.png','Toward the Clearing','Two creatures walk into an open canopy clearing and look toward the sky; no contact wisp.'),
    ('contact-014','home-awning.png','Making Home Comfortable','A creature pulls the vine cord to lower a woven awning over its familiar home belongings.')]:
    s=byid[sid];s.update(title=title,description=description)
    s['startingFrameSelection']=dict(id=sid+'-v63',image=(OUT/filename).relative_to(BASE).as_posix(),userSelected=False,status='Replacement still and motion draft',generationMode='built-in ImageGen')
byid['contact-001'].update(title='Warp Departure / Initiation',description='First 18 frames of one continuous rear-oblique Blender departure composite.')
byid['contact-002'].update(title='Warp Departure / Forward Travel',description='Continuation of the same rear-oblique departure composite; independent Harper/ship and warp layers.')
byid['contact-026']['description']='Harper remains in profile or facing away toward the planet, avoiding a rear-to-front face reveal.'
for sid in ['contact-022','contact-023','contact-024']:
    byid[sid]['timingRevision']='V63: projection advances to DAW bar 69 beat 1, frame 4334; projection retains 37 frames; eye gets 45 frames; night orbit stays at 4416.'
spec=dict(id='first-contact-v01',output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),useMotion=True,
    shotIds=[s['id'] for s in shots],motionShotIds=[s['id'] for s in shots],draftForReview=True,
    mediaLabel='V62 review revisions / separate warp layers and local polish',
    presentation='Targeted native replacements, Blender warp composites, gentle pans, tracked star twinkles, short ecology/outro dissolves and longer eye glint.',
    continuationNotes='V63 targets the V62 review. Six new native sources cost 248 credits. Simple ship/Harper and warp composites; reflected streak synthesis deferred. Earlier V62 retained. Total first-contact spend 1880 credits, project cumulative 5264. User review pending.')
save(OUT/'review-options.json',spec)
before=read(BASE/'shots/shotlist.json');save(BASE/'shots/shotlist.json',register)
try:
    subprocess.run([sys.executable,str(ROOT/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v63'],check=True)
except BaseException:
    save(BASE/'shots/shotlist.json',before);raise
register=read(BASE/'shots/shotlist.json')
register['reviewEdits']['v63'].update(type='Targeted motion and compositing revisions',newPaidCredits=248,preservedVersion='v62',reviewStatus='Pending user review',reflectionSynthesis='Deferred until simple composite accepted')
register['firstContactSequence'].update(status='V63 revised motion assembled; review pending',animaticVersion='v63',actualCredits=1880,confirmedCumulativeKlingCredits=5264,
    reviewUrl='http://127.0.0.1:8768/?v=v63',motionReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-motion-v02/',nativeMotionRevisionPlan='kling-first-contact-motion-v02.json')
for e in entries:
    s=next(s for s in register['storyboardProposals'] if s['id']==e['shot'])
    s['animaticPlacement']['kind']=e['kind']
    if 'transition' in e:s['animaticPlacement']['transition']=e['transition']
    for stored in register['reviewEdits']['v63']['entries']:
        if stored['shot']==e['shot']:stored.update(s['animaticPlacement'])
save(BASE/'shots/shotlist.json',register)
save(OUT/'assembly-plan.json',dict(version='v63',source='v62',fps=24,startFrame=3144,endFrameExclusive=5266,frames=2122,entries=entries))
save(OUT/'verification.json',dict(fullFrames=5265,fps=24,width=1920,height=1080,sectionFrames=2122,newPaidCredits=248,sectionTotalCredits=1880,
    finaleStartFrame=5031,eyeFrames=45,eyePriorFrames=27,nightOrbitStartFrame=4416,v62Preserved=source.exists(),audio='V62 original AAC packets verified identical by insertion tool',reviewStatus='Pending user review'))
plan.update(status='V63 revisions assembled; review pending',actualCredits=248,animaticVersion='v63');save(BASE/'kling-first-contact-motion-v02.json',plan)
page='''<!doctype html><meta charset="utf-8"><title>V63 motion revisions</title><style>body{background:#10242a;color:#eee4d2;font:16px/1.5 system-ui;max-width:1100px;margin:30px auto;padding:0 24px}a{color:#9cdfea}video{width:100%;background:#000}h2{margin-top:40px}</style><h1>V63 · Motion revisions</h1><p><a href="/?v=v63">Full animatic</a> · <a href="/?v=v62">V62 comparison</a></p><h2>Revised passage with song</h2><video controls src="timed-still-board.mp4"></video><h2>Simple ship / Harper + warp composite</h2><p>Reflected streak synthesis is deferred. Existing single-generation travel remains in V62 for comparison.</p><video controls loop src="travel-effect.mp4"></video><h2>Continuous rear departure</h2><video controls loop src="opening-effect.mp4"></video>'''
(OUT/'index.html').write_text(page,encoding='utf-8')
print('V63 ready: 5265 frames, original audio, 248 new credits.',flush=True)
