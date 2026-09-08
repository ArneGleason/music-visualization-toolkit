"""Read-only reconciliation of approved snapshots. Does not promote production edits."""
from pathlib import Path
import json, sys, hashlib
O = Path(__file__).resolve().parent
R = O.parents[1]
sys.path.insert(0, str(R/'tools'))
from assembly_sources import load_decisions, resolve_clip

def read(p):
    return json.loads((R/p).read_text(encoding='utf-8'))

base = read('shots/shotlist.json')
latest = read('out/swirl_tail_review_v1/shotlist.json')
decisions = load_decisions(R)
decisions.update(read('out/receiver_voice_review/receiver_decision.json'))
rows = []
for shot in latest['shots']:
    a,b = round(shot['start_sec']*24), round(shot['end_sec']*24)
    if a >= 4177: continue
    assert b <= 4177, (shot['id'], a, b)
    errors = []
    try:
        clip = resolve_clip(R, shot, 24, decisions, start=a, end=b)
    except ValueError as exc:
        clip = shot.get('clip', {})
        errors.append(str(exc))
    path = clip.get('file', '').replace('\\','/')
    folder = (R/path).parent
    rows.append(dict(id=shot['id'], song_frames=[a,b], selected_reference=path,
                     source_start_frame=round(clip.get('in_sec',0)*24),
                     speed=clip.get('speed',1), file_exists=(R/path).is_file(),
                     status='dependency_audit_pending',
                     recipe_candidates=[str(p.relative_to(R)).replace('\\','/') for p in folder.glob('*.py')],
                     resolver_errors=errors))
for j,cut in enumerate(read('out/outro_exchange_fx_v1/cut_snapshot.json')[:4]):
    rows.append(dict(id=f'outro_lead_{j+1}',song_frames=cut['song'],selected_reference=cut['file'],
                     source_start_frame=cut['source'][0],status='native_fx_migration_pending'))
cuts = [(4362,4400),(4400,4431),(4431,4449),(4449,4516),(4516,4538),(4538,4574),
        (4574,4622),(4622,4644),(4644,4671),(4671,4710),(4710,4782),(4782,4854)]
for j,(a,b) in enumerate(cuts):
    rows.append(dict(id=f'outro_review_{j+1}',song_frames=[a,b],
                     selected_reference='out/closing_titles_blender_v1/preview_numbered.mp4',
                     source_start_frame=a-4362,
                     status='title_native_recipe_text_updated_not_rendered' if j==11 else 'native_fx_migration_pending',
                     note='Snapshot reference only; do not use numbered/baked movie as final plate.'))
rows.sort(key=lambda x:x['song_frames'][0])
gaps=[]
for a,b in zip(rows,rows[1:]):
    if a['song_frames'][1] != b['song_frames'][0]: gaps.append([a['id'],b['id'],a['song_frames'][1],b['song_frames'][0]])
for j,row in enumerate(rows,1): row['review_number']=j
hidden={'s001':['out/observatory_phosphor_start/render.py'],
        's012':['out/rosette_duet_trial/preview.mp4 (resolve approved wrapper before migration)']}
for row in rows:
    if row['id'] in hidden:
        row['assembly_layer_audit']=hidden[row['id']]
        row['note']='Effects can be injected by review wrappers even when selected source is untreated.'
payload=dict(fps=24,frame_count=4854,range_end_exclusive=True,
             status='AUDIT_NOT_FINAL_ASSEMBLY',gaps_or_overlaps=gaps,
             canonical_source='shots/shotlist.json', approved_snapshot='out/swirl_tail_review_v1/shotlist.json',
             canonical_sha256=hashlib.sha256((R/'shots/shotlist.json').read_bytes()).hexdigest(),
             warning='Review snapshots reconciled for migration only. Never silently overwrite canonical shotlist.',shots=rows)
(O/'migration_register.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps({'shots':len(rows),'gaps':gaps,'resolver_errors':[r for r in rows if r.get('resolver_errors')],
                  'end':rows[-1]['song_frames'][1]},indent=2))
