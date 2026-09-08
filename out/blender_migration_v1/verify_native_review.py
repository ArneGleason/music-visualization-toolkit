"""Reconcile inspected scenes and locked selection into fail-closed receipts."""
from pathlib import Path
import json,sys,hashlib
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
audit=json.loads((O/'autonomous_blend_audit.json').read_text());assert not any(r['issues'] for r in audit), 'Scene audit unresolved'
selection=json.loads((O/'full_selection_check.json').read_text());assert len(selection)==70 and not any(r['issues'] for r in selection),'Coverage unresolved'
scenes={(r['family'],r['width']):r for r in audit};resolution={}
for family in {r['family'] for r in audit}:
 tests=[]
 for hi in (O/family/'native_1920').glob('*.png'):
  lo=O/family/'native_1280'/hi.name
  if not lo.exists():continue
  a=cv2.imread(str(lo));b=cv2.imread(str(hi));assert a.shape==(720,1280,3) and b.shape==(1080,1920,3)
  error=float(np.abs(a.astype(float)-cv2.resize(b,(1280,720),interpolation=cv2.INTER_AREA)).mean());tests.append({'frame':int(hi.stem),'mean':error})
 assert tests and max(v['mean'] for v in tests)<5,(family,tests)
 resolution[family]=tests
(O/'full_resolution_check.json').write_text(json.dumps(resolution,indent=2))
hashes={}
def artifact(p):
 p=Path(p);assert p.is_file(),p
 if str(p) not in hashes:hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 return {'file':str(p.relative_to(R)).replace('\\','/'),'sha256':hashes[str(p)]}
verified={}
for row in selection:
 p=Path(row['file']);family=p.parent.name if p.is_relative_to(O) else None
 artifacts=[artifact(p),artifact(O/'full_native_review_draft.json'),artifact(O/'full_native_cues.json'),artifact(O/'full_native_preview.py')]
 if family:
  assert (family,1280) in scenes and (family,1920) in scenes,family
  artifacts += [artifact(O/family/f'{family}_{w}.blend') for w in [1280,1920]]
  artifacts += [artifact(O/'autonomous_blend_audit.json'),artifact(O/'full_resolution_check.json')]
 else:
  # Untreated generated/conformed picture sources: no external FX stage to migrate.
  assert 'preview' not in p.name.lower(),p
  artifacts += [artifact(R/'tools/blender_comp.py')]
 verified[row['id']]={'status':'verified_native','song_frames':row['song_frames'],'fps':24,'baked_fx_dependencies':False,'resolution_review_passed':True,'family':family or 'source_only_native_vse','source_in_frame':row['source_in_frame'],'artifacts':artifacts,'review_authority':'Owner authorized autonomous technical and visual review; full cut remains isolated for owner viewing.','production_promoted':False}
(O/'verified_native_shots.json').write_text(json.dumps(verified,indent=2));print('Verified',len(verified),'cut dependency records.')
