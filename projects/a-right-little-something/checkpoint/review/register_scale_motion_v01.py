from pathlib import Path
import json

base=Path('projects/a-right-little-something').resolve()
q=base/'shots/shotlist.json'
r=json.loads(q.read_text(encoding='utf-8'))
assert r['activeReviewEdit']=='v24'
plan=json.loads((base/'kling-scale-motion-v01.json').read_text(encoding='utf-8'))
entry=plan['shots'][0]
directory=base/plan['output']/entry['id']
body=json.loads((directory/'submission.json').read_text(encoding='utf-8'))['body']
source=(directory/(entry['id']+'-01-clean.mp4')).relative_to(base).as_posix()
test=dict(id=entry['id'],plan='kling-scale-motion-v01.json',motionRef=source,status='Agent-reviewed working take in v24; user playback review pending',reviewNotes=entry['reviewNotes'],generationId=body['generationId'],creditsConsumed=48,sourceFrames=145,sourceEditStartFrame=25,editFrames=58,availableLeadOutFrames=63,userSelected=False,draftForReview=True,continuityFrames=[dict(label=label,sourceFrame=frame,image=(directory/f'source-{frame:04}.png').relative_to(base).as_posix(),use='Inspect before using as a later shot reference') for label,frame in [('edit-in',25),('mid',55),('edit-out',82),('tail',145)]])
shot=next((s for s in r['storyboardProposals'] if s['id']=='scale-reveal-new'),None)
if shot is None:
    shot=dict(id='scale-reveal-new',batch='scale-motion-v01',type='storyboard',title=entry['title'],description='Small ship and Harper against an immense living world; actual cloud/light movement beneath a purposeful editorial camera reveal.',startFrame=854,endFrameExclusive=912,frames=58,startSeconds=853/24,endSeconds=911/24,handles=dict(leadInFrames=24,leadOutFrames=24,generatedFrames=145,editInLocalFrame=25,editOutLocalFrameExclusive=83),lyrics=['Show you just how big you are.'],startingFrameSelection=dict(image=entry['firstImage'],status='Reviewed still used for the explicitly requested Kling animation',userSelected=True))
    r['storyboardProposals'].append(shot)
shot.update(motionRef=source,motionSelection=test,motionReview=dict(notes=entry['reviewNotes']),prompt=entry['prompt'])
shot.setdefault('motionTests',[])
if not any(t['id']==test['id'] for t in shot['motionTests']): shot['motionTests'].append(test)
r['reviewEdits']['v24']['scaleMotion']=test['id']
q.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
q=base/'generated/review/chorus-revision-v04-ledger.json'
d=json.loads(q.read_text(encoding='utf-8'))
d['verification']['status']='Technical checks and full-film proof inspection passed'
d['verification']['pictureQA']='Native frames 1,25,55,82,110,145 and full-film scale/fade frames 849,854,859,875,889,903,907,912,917 inspected. Actual clouds/illumination evolve; ship geometry and editorial reveal remain coherent.'
q.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
q=base/'revision-chorus-v04.json'
d=json.loads(q.read_text(encoding='utf-8'))
d['status']='V24 agent-checked working review; scale still replaced with Kling animation'
q.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Scale motion registered canonically; v24 verified; cumulative 1784 credits; no pending tasks')
