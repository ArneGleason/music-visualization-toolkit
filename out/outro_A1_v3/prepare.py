"""Build the authorized single performance retry without touching v2."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / 'out/outro_A1_v2'
assert not (OUT / 'handoff.json').exists(), 'Do not reset an existing handoff.'
shutil.copyfile(OLD / 'first_frame.png', OUT / 'first_frame.png')
lock = ROOT / 'out/astronaut_reply_v1/style_lock_v2.txt'
prompt = OUT / 'flow_prompt.txt'
prompt.write_bytes((OUT / 'direction.txt').read_bytes().rstrip() + b'\n\n' + lock.read_bytes())
assert prompt.read_bytes().endswith(lock.read_bytes())
data = json.loads((OLD / 'handoff.json').read_text())
data.pop('claude_result', None)
data.pop('codex_result', None)
data['test_id'] = 'outro_A1_v3'
data['status'] = 'ready_for_claude_not_submitted'
data['task'] = 'ONE authorized Flow base retry: mission accomplished, not grateful smiling. TV response allowed. NO Kling.'
data['supersedes_for_review'] = 'out/outro_A1_v2/base.mp4 (retain as spare; not overwritten)'
data['owner_direction'] = 'Change the grateful smile to mission well done; TV flash/reflected face light is acceptable. No automatic further retries.'
for key, path in [('first_frame', OUT / 'first_frame.png'), ('prompt', prompt)]:
    data['inputs'][key] = {'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
data['output']['base'] = 'out/outro_A1_v3/base.mp4'
data['output']['receipt'] = 'out/outro_A1_v3/RECEIPT.md'
data['review']['checks'] = ['identity/outfit/props stable', 'mission accomplished, not grateful or celebratory grin',
    'natural open articulation without deadpan regression', 'face near-frontal through question',
    'TV unobstructed; brief static/reflected light ALLOWED, not a failure', 'no cuts/reset; continuity at source155']
(OUT / 'handoff.json').write_text(json.dumps(data, indent=2) + '\n')
print('Retry ready. Same first frame and source clock; exact style lock preserved; one Flow, zero Kling.')
