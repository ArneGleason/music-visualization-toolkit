"""Record collected motion, source frames and provisional continuity review."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('plan')
parser.add_argument('take')
parser.add_argument('--notes', default='Collected for motion review; user approval pending.')
args = parser.parse_args()
base = Path(__file__).resolve().parents[2]
plan_path = base/args.plan
plan = json.loads(plan_path.read_text(encoding='utf-8'))
entry = next(e for e in plan['shots'] if e['id']==args.take)
folder = base/plan['output']/entry['id']
raw = folder/(entry['id']+'-01-clean.mp4')
if not raw.exists():
    raw = folder/(entry['id']+'-01.mp4')
assert raw.exists(), raw
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(raw)]))['streams'][0]
assert info['r_frame_rate']=='24/1' and info['height']==1080 and info['width']<=1920, info
lead, length = entry['leadInFrames'], entry['editFrames']
assert int(info['nb_frames']) >= lead+length+entry['leadOutFrames']
reference_frames = []
for label, frame in [('edit-in',lead),('mid',lead+length//2),('edit-out',lead+length-1),('tail',int(info['nb_frames'])-1)]:
    image = folder/(label+'.png')
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-vf',f'select=eq(n\\,{frame})','-frames:v','1',str(image)],check=True)
    reference_frames.append(dict(label=label, sourceFrame=frame+1,image=image.relative_to(base).as_posix(),use='Provisional continuity reference; inspect before reusing'))
path = base/'shots/shotlist.json'
register = json.loads(path.read_text(encoding='utf-8'))
shot = next(s for s in register['storyboardProposals'] if s['id']==entry['shotId'])
submission = json.loads((folder/'submission.json').read_text(encoding='utf-8'))['body']
test = dict(id=entry['id'],plan=plan_path.relative_to(base).as_posix(),motionRef=raw.relative_to(base).as_posix(),status='Collected for review',reviewNotes=args.notes,generationId=submission['generationId'],creditsConsumed=submission.get('creditsConsumed'),sourceFrames=int(info['nb_frames']),sourceEditStartFrame=lead+1,editFrames=length,availableLeadOutFrames=int(info['nb_frames'])-lead-length,continuityFrames=reference_frames,userSelected=False)
shot['motionTests'] = [t for t in shot.get('motionTests',[]) if t['id']!=test['id']]+[test]
path.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Registered',test['id'],test['sourceFrames'],'source frames;',length,'edit frames;',test['creditsConsumed'],'credits')
