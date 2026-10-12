"""Assemble the reviewed first-contact motion pass and two-video finale as V62."""
import copy
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lyric_overlay import write_lyrics


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=OUT,check=True)


plan=read(BASE/'kling-first-contact-motion-v01.json')
media=read(OUT/'media-manifest.json')
assert len(media)==37
manifest={m['id']:m for m in media}
path=BASE/'shots/shotlist.json'
register=read(path)
if not (OUT/'prior-shotlist.json').exists():
    save(OUT/'prior-shotlist.json',register)
shots=sorted((s for s in register['storyboardProposals'] if s.get('batch')=='first-contact-v01'),key=lambda s:s['startFrame'])
assert len(shots)==36 and shots[0]['startFrame']==3144 and shots[-1]['endFrameExclusive']==5266
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
assert len(list((OUT/'finale-frames').glob('frame_*.png')))==235
run(['-framerate','24','-i','finale-frames/frame_%04d.png','-frames:v','235',
     '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','finale-composite.mp4'])
entries=[]
first_pass_credits=sum(read(BASE/plan['output']/s['id']/'submission.json')['body']['creditsConsumed'] for s in plan['shots'])
repair_credits=0
for alternate in {m['planRef'] for m in media}-{'kling-first-contact-motion-v01.json'}:
    alternate_plan=read(BASE/alternate)
    repair_credits+=sum(read(BASE/alternate_plan['output']/s['id']/'submission.json')['body']['creditsConsumed'] for s in alternate_plan['shots'])
credits=first_pass_credits+repair_credits
cumulative=plan['priorConfirmedCumulativeCredits']+credits
for take in plan['shots']:
    m=manifest[take['id']]
    submission=read(BASE/m['submissionRef'])['body']
    s=next(s for s in shots if s['id']==take['shotId'])
    test=dict(id=m['takeId'],plan=m['planRef'],
        motionRef=m['motionRef'],generationId=submission['generationId'],creditsConsumed=submission['creditsConsumed'],
        plate=take['plate'],sourceFrames=m['nativeFrames'],sourceEditStartFrame=m['sourceEditStartFrame'],editFrames=s['frames'],
        availableLeadOutFrames=m['availableLeadOutFrames'],userSelected=False,
        status='Native motion assembled for user review',reviewNotes=m['editorialNotes'],
        continuityFrames=m['qaImages'])
    s['motionTests']=[t for t in s.get('motionTests',[]) if t['id']!=test['id']]+[test]
    s['handles']=dict(leadInFrames=m['sourceEditStartFrame']-1,leadOutFrames=24)
    if take['plate']=='main':
        s['motionSelection']=dict(test,draftForReview=True)
        s['motionRef']=m['motionRef']
        s['motionReview']=dict(notes='Native Kling motion with exact V61 timing; user motion review pending.')
        entries.append(dict(shot=s['id'],file=m['editRef'],frames=s['frames']))
final=shots[-1]
final['compositeSelection']=dict(id='contact-032-blender-motion-v01',
    motionRef=(OUT/'finale-composite.mp4').relative_to(BASE).as_posix(),
    compositor=(OUT/'finale-two-videos.blend').relative_to(BASE).as_posix(),
    sourceTests=[t['id'] for t in final['motionTests'] if t.get('plate') in ('cosmic-background','harper-portrait')],
    sourceEditStartFrame=1,editFrames=235,userSelected=False,draftForReview=True,
    status='Blender superimposition of two separate native videos; review pending')
final['motionSelection']=copy.deepcopy(final['compositeSelection'])
final['motionRef']=final['compositeSelection']['motionRef']
final['motionReview']=dict(notes='Two independently generated twelve-second video plates, each trimmed to235frames and superimposed in Blender. Direct cut from galaxy at3:29.583; Harper visible immediately. User review pending.')
entries.append(dict(shot=final['id'],file=final['motionRef'],frames=235))
entries.sort(key=lambda e:next(s['startFrame'] for s in shots if s['id']==e['shot']))
assert sum(e['frames'] for e in entries)==2122 and first_pass_credits==1528 and credits<=2000
save(path,register)
(OUT/'concat.txt').write_text(''.join("file '"+(BASE/e['file']).as_posix()+"'\n" for e in entries),encoding='utf-8')
run(['-f','concat','-safe','0','-i','concat.txt','-an','-c','copy','motion-picture.mp4'])
data=read(BASE/'generated/animatic/animatic-data.json')
captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if 3144<=p['startFrame']<5266]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=3143;item['endFrameExclusive']-=3143
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
(OUT/'fonts').mkdir(exist_ok=True)
shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v61.mp4'
run(['-reinit_filter','0','-i','motion-picture.mp4','-i',str(source),'-filter_complex',
     '[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start=130.958333333333:end=219.375,asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','2122','-c:v','libx264','-preset','fast','-crf','18',
     '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
spec=dict(id='first-contact-v01',output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic=source.relative_to(BASE).as_posix(),useMotion=True,
    motionShotIds=[s['id'] for s in shots],draftForReview=True,
    mediaLabel='First contact / clean Kling motion and Blender finale',
    presentation='V61 timing retained;36 motion shots from37 native silent Kling videos. Separate finale plates composited in Blender.',
    continuationNotes=f'V62 first-contact clean motion pass ready for review.37 selected silent1080p sources; first pass1528credits plus{repair_credits} for corrections, total{credits}; cumulative{cumulative}. Finale cuts directly from galaxy at3:29.583, with235frame Blender overlay of separate cosmic and Harper video plates. V61 preserved.')
save(OUT/'review-options.json',spec)
subprocess.run([sys.executable,str(ROOT/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),
                str(OUT/'review-options.json'),'--version','v62'],check=True)
register=read(path)
for shot in register['storyboardProposals']:
    if shot.get('batch')!='first-contact-v01':
        continue
    shot['animaticPlacement']['kind']='Blender composite of two native Kling videos' if shot['id']=='contact-032' else 'native Kling motion'
    shot['status']='Native motion draft in V62; user review pending'
    if shot['id']=='contact-004':
        shot['description']='Tight hand selecting a valley in the large volumetric terrain map inside the hexagonal dome; no real planet behind it.'
    for entry in register['reviewEdits']['v62']['entries']:
        if entry['shot']==shot['id']:
            entry.update(shot['animaticPlacement'])
register['reviewEdits']['v62'].update(actualCredits=credits,preservedVersion='v61',reviewStatus='Motion review pending',
    separateFinaleVideoPlates=True,compositor=(OUT/'finale-two-videos.blend').relative_to(BASE).as_posix())
register['firstContactSequence'].update(status='V62 native motion assembled; user review pending',animaticVersion='v62',
    nativeMotionPlan='kling-first-contact-motion-v01.json',actualCredits=credits,confirmedCumulativeKlingCredits=cumulative,
    reviewUrl='http://127.0.0.1:8768/?v=v62',motionReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-motion-v01/',
    timedPreview=(OUT/'timed-still-board.mp4').relative_to(BASE).as_posix(),timedPreviewStartFrame=3144,
    finaleBlender=(OUT/'finale-two-videos.blend').relative_to(BASE).as_posix())
save(path,register)
plan.update(status='V62 clean motion pass assembled; user review pending',actualCredits=first_pass_credits,
            repairCredits=repair_credits,combinedPassCredits=credits,animaticVersion='v62')
save(BASE/'kling-first-contact-motion-v01.json',plan)
save(OUT/'assembly-plan.json',dict(version='v62',source='v61',fps=24,startFrame=3144,endFrameExclusive=5266,frames=2122,
    entries=entries,finaleStartFrame=5031,finaleFrames=235,compositor='finale-two-videos.blend'))
save(OUT/'verification.json',dict(fullFrames=5265,fps=24,width=1920,height=1080,shots=36,sourceVideos=37,
    sectionFrames=2122,finaleStartFrame=5031,finaleFrames=235,actualCredits=credits,firstPassCredits=first_pass_credits,repairCredits=repair_credits,
    audio='Original V61 AAC packet hash verified identical by insertion tool',v61Preserved=source.exists(),motionApproval='Pending user review'))
cards=[]
for item in media:
    cards.append(f'<section><h2>{html.escape(item["id"])}</h2><video controls preload="metadata" src="edits/{Path(item["editRef"]).name}"></video><p>{item["editFrames"]} frames from source frame{item["sourceEditStartFrame"]}. Clean silent take; review in the full animatic for song timing.</p></section>')
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First contact · clean motion review</title><style>body{background:#111820;color:#e3e9ed;font:16px system-ui;max-width:1100px;margin:auto;padding:24px}a{color:#8edbea}section{border-top:1px solid #46515b;padding:20px 0}h2{font-size:18px}video{width:100%;max-height:600px;background:black}p{line-height:1.5}</style><h1>First contact · clean motion review</h1><p><a href="/?v=v62">Full V62 animatic with original song</a> ·37 source videos,1528 credits. V61 timing retained.</p><section><h2>Finale · two separate video plates combined in Blender</h2><video controls preload="metadata" src="finale-composite.mp4"></video><p>Direct galaxy-to-Harper cut at3:29.583;235frames. The cosmic and portrait sources remain independent.</p></section>'''
page=page.replace('37 source videos,1528 credits.',f'37 selected source videos;{credits} credits including targeted corrections.')
(OUT/'index.html').write_text(page+'\n'.join(cards),encoding='utf-8')
print(f'V62 ready;{credits}credits;37 selected native sources;36 exact timed shots; original audio verified.',flush=True)
