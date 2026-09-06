import copy
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
OLD=ROOT/'out/specimen_mismatch_v1'
p=OLD/'handoff.json'
previous=json.loads(p.read_text())
result=previous['claude_result']['base']
actual=hashlib.sha256((ROOT/result['file']).read_bytes()).hexdigest().upper()
assert actual==result['sha256']
previous['status']='owner_requested_replacement_retained_as_spare'
previous['owner_review']={
 'date':'2026-09-06',
 'decision':'Replace with separated rotations and a gentle overhead camera push.',
 'feedback':'Owner reports pieces seem to fit perfectly then snap apart, and a fragment grows back around5s. Even a pre-glitch excerpt does not convey the intended action.',
 'receipt_disagreement':'Claude marked candidate usable and reported no morph; owner playback judgment takes precedence for creative selection. No independent visual diagnosis of the reported glitch claimed here.',
 'source_hash_verified':actual,
 'replacement_handoff':'out/specimen_mismatch_v2/handoff.json',
 'preserve_originals':True}
p.write_text(json.dumps(previous,indent=2)+'\n',encoding='utf-8')
h=copy.deepcopy(previous)
for key in ('claude_result','owner_review'):
 h.pop(key,None)
h['test_id']='specimen_mismatch_v2'
h['status']='ready_for_claude_not_submitted'
h['task']='One replacement take: separated fingertip rotations, gentle overhead dolly push. No joining or snapping.'
h['supersedes']='out/specimen_mismatch_v1/handoff.json'
h['authorization']['max_flow_submissions']=1
h['authorization']['automatic_retries']=False
lock=(OLD/'style_lock_v2.txt').read_bytes()
(OUT/'style_lock_v2.txt').write_bytes(lock)
prompt=(OUT/'direction.txt').read_text(encoding='utf-8').rstrip()+'\n\n'+lock.decode('utf-8')
(OUT/'flow_prompt.txt').write_text(prompt,encoding='utf-8')
for key,name in [('prompt','flow_prompt.txt'),('lock','style_lock_v2.txt')]:
 h['inputs'][key]={'file':f'out/specimen_mismatch_v2/{name}','sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest().upper()}
h['output']['base']='out/specimen_mismatch_v2/base.mp4'
h['output']['receipt']='out/specimen_mismatch_v2/RECEIPT.md'
h['proposed_review_cut']['note']='Candidate source48..97 remains provisional. Select separated turning, not a joining event. Song interval670..719 remains unchanged.'
h['coverage']['note']='Preserve full eight seconds. Identify at least49 clean consecutive frames of separated rotation with stable geometry, including review of the late5s region.'
h['continuity']['intent']='Alternate detail coverage of continued inspection, not matching or breaking objects. Broad separation and different orientations convey uncertainty.'
h['polling']={'first_check_after_seconds':60,'subsequent_check_interval_seconds':25,
 'note':'Use normal visible status checks when available; honor service rate limits and explicit retry guidance. Check/download promptly once ready. Do not submit another job while waiting. Report failures or prolonged unchanged status rather than silently waiting many minutes.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
assert (OUT/'style_lock_v2.txt').read_bytes()==lock
print('v1 result hash verified and owner review recorded; v2 ready, one100-credit Flow submission, no Kling.')
