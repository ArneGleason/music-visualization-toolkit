"""Check every selected native-review clip against the locked frame grid."""
from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
edl=json.loads((O/'full_native_review_draft.json').read_text());register=json.loads((O/'migration_register.json').read_text())['shots'];cache={};checks=[]
for shot,reg in zip(edl['shots'],register):
 a,z=reg['song_frames'];clip=shot['clip'];p=Path(clip['file'].replace('\\','/'));p=p if p.is_absolute() else R/p;issues=[]
 if shot['id']!=reg['id'] or round(shot['start_sec']*24)!=a or round(shot['end_sec']*24)!=z:issues.append('Timing mismatch')
 if float(clip.get('speed',1))!=1:issues.append('Unexpected speed')
 if p.exists():
  if str(p) not in cache:cache[str(p)]=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration,nb_frames,r_frame_rate,width,height','-of','json',str(p)]))['streams'][0]
  stream=cache[str(p)];available=float(stream['duration'])*24;start=round(float(clip.get('in_sec',0))*24)
  if available+.51<start+z-a:issues.append(f'Coverage {available:.3f} < {start+z-a}')
 else:issues.append('Missing rendered source')
 checks.append({'id':reg['id'],'review_number':reg['review_number'],'song_frames':[a,z],'file':str(p),'source_in_frame':round(float(clip.get('in_sec',0))*24),'issues':issues})
(O/'full_selection_check.json').write_text(json.dumps(checks,indent=2));print(json.dumps([v for v in checks if v['issues']],indent=2))
