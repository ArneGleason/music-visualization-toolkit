"""Promote reviewed remainder starters into the authoritative edit."""
from pathlib import Path
from copy import deepcopy
import json,shutil
P=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
shotpath=P/'shots/shotlist.json';projectpath=P/'project.json'
for src,name in [(shotpath,'shotlist-before.json'),(projectpath,'project-before.json')]:
 if not (N/name).exists():shutil.copy2(src,N/name)
score=json.loads((N/'shotlist-before.json').read_text());project=json.loads((N/'project-before.json').read_text())
m=json.loads((P/'shots/rest-of-song-starters-v039/manifest.json').read_text())
assert score['shots'][-1]['endFrameExclusive']==1956
original=deepcopy(score['shots']); lock=(P/'shots/rest-of-song-starters-v039/prompt-lock.txt').read_text()
for item in m['shots']:
 s=deepcopy(item);s['displayId']=s['id'];s['shotNumber']=s['id'].split('-SH')[1].lstrip('0');s['description']=s['action'];s['promptLock']=lock;s['starterRevision']=s['starterImage'].split('/')[-2].split('-')[-1]
 if s['id']=='S11-SH05':s['starterImage']='generated/storyboard/rest-of-song-starters-v040/S11-SH05.png';s['starterRevision']='v040'
 s['status']='approved_starter_animatic';s['startSeconds']=s['startFrame']/24;s['endSeconds']=s['endFrameExclusive']/24
 s['videoHandles'].update(editInSourceFrame=24,editOutSourceFrameExclusive=24+s['frames'],sourceStartMasterFrame=s['startFrame']-24,sourceEndMasterFrameExclusive=s['endFrameExclusive']+24,status='not_generated',note='Still shown at edit startFrame. Starter represents future source lead-in;24frame source handle does not shift still placement.')
 tr=s.get('transitionInProposal',{})
 if tr.get('type') in ('crossfade','wipe') and tr.get('frames',0):
  s['transitionIn']={'type':'soft_wipe' if tr['type']=='wipe' else 'crossfade','frames':tr['frames'],'alignment':'start','direction':'left_to_right','featherFraction':.1}
 else:s['transitionIn']={'type':'cut','frames':0}
 for key in ['imageUrl','revisionLabel','reviewNote']:s.pop(key,None)
 assert (P/s['starterImage']).is_file()
 score['shots'].append(s)
for scene in m['scenes']:
 s=deepcopy(scene);s['shotIds']=[x['id'] for x in m['shots'] if x['sceneId']==s['id']];score['scenes'].append(s)
score.pop('reviewTail',None);score['totalFrames']=5190;score['endFrameExclusive']=5190;score['status']='Full-song animatic with accepted motion and approved remainder starters'
project['render'].pop('reviewStoryProposal',None)
assert score['shots'][:len(original)]==original
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(score['shots'],score['shots'][1:]))
assert score['shots'][-1]['endFrameExclusive']==5190
shotpath.write_text(json.dumps(score,indent=2)+'\n');projectpath.write_text(json.dumps(project,indent=2)+'\n')
video=P/'generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4';backup=P/'generated/storyboard/full-song-starters-v041/before-starter-integration.mp4'
if not backup.exists():shutil.copy2(video,backup)
(N/'integration-notes.md').write_text('# Full-song starters v041\n\nApproved v040 Taffy scale selected. All40 remainder shots promoted into shots/shotlist.json at exact edit boundaries1956–5190. Existing Scenes1–6 untouched, including video trims/camera moves/transitions. Total5190frames/216.25s at24fps. New still transitions use start alignment so incoming artwork never appears before its shot boundary. Source video handles stay24frames on each side, separate from still placement. Planning black/story overlays replaced by starter art with small lyrics and scene/shot labels. Three proposed wipes included. Prior render and JSON saved.\n')
print(len(score['shots']),'shots; original',len(original),'unchanged; total5190frames')
