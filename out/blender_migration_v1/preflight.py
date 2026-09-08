"""Fail closed before a full native assembly. Never substitute baked references."""
from pathlib import Path
import json,sys,hashlib
O=Path(__file__).resolve().parent
register=json.loads((O/'migration_register.json').read_text())
if register['gaps_or_overlaps']:raise SystemExit('Unreconciled timing')
verified_path=O/'verified_native_shots.json'
verified=json.loads(verified_path.read_text()) if verified_path.exists() else {}
def validate_record(shot,record):
    if not record:return ['missing verified record']
    errors=[]
    if record.get('status')!='verified_native':errors.append('not verified_native')
    if record.get('song_frames')!=shot['song_frames']:errors.append('song clock differs')
    if record.get('fps')!=24:errors.append('fps differs')
    if record.get('baked_fx_dependencies',True):errors.append('baked FX dependency unresolved')
    if not record.get('resolution_review_passed'):errors.append('resolution review missing')
    artifacts=record.get('artifacts',[])
    if not artifacts:errors.append('no reproducible artifacts')
    for item in artifacts:
        path=Path(item.get('file',''))
        if not path.is_absolute():path=O.parents[1]/path
        if not path.is_file():errors.append('missing artifact '+str(path))
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=item.get('sha256'):errors.append('changed artifact '+str(path))
    return errors
issues={s['id']:validate_record(s,verified.get(s['id'])) for s in register['shots']}
pending=[ident for ident,errors in issues.items() if errors]
if pending:
    print(f'FULL NATIVE ASSEMBLY NOT READY: {len(pending)} cuts await verified native dependency records.')
    print('Candidate renders are not verified/published replacements. See STATUS.md.')
    for ident in pending:print(ident+': '+', '.join(issues[ident]))
    sys.exit(2)
print('All selected cuts have verified native dependencies.')
