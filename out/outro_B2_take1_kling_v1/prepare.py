"""Kling-only comparison of archived first B2 performance."""
from pathlib import Path
import json,hashlib,wave
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists()
def ref(p):
    return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
base=ref(OUT/'base.mp4');guide=ref(OUT/'guide.wav')
assert base['sha256']=='ed5f2e2fe7872b682bf1d0b50f8997887e654746a9de53935f5e14fc842f63be'
assert guide['sha256']=='ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004'
assert base==dict(ref(ROOT/'out/outro_B2_v2/take1/base.mp4'),file=base['file'])
with wave.open(str(OUT/'guide.wav')) as w:
    assert (w.getnframes(),w.getframerate(),w.getnchannels())==(384000,48000,1)
prior=json.loads((ROOT/'out/outro_B2_v2/handoff.json').read_text())
h={'schema_version':1,'test_id':'outro_B2_take1_kling_v1','project_root':ROOT.as_posix(),
 'status':'ready_for_claude_not_submitted',
 'task':'ONE Kling Lip Sync on archived FIRST Flow take of B2 for phrase-by-phrase comparison. NO Flow.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False,'owner_override':'Owner explicitly requests one Kling test on take1 despite its known downward gaze/missing final articulation. Do not reapply the prior base gate and withhold this authorized test.'},
 'inputs':{'base':base,'guide':guide},'original_source':ref(ROOT/'out/outro_B2_v2/take1/base.mp4'),
 'generation':{'kling':prior['generation']['kling'],'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Expected10Kling credits based on previous identical-length pass. Verify UI; no purchases, upgrades or substitutes.'},
 'clock':prior['clock'],'guide_provenance':prior['guide_provenance'],'visible_cuts':prior['visible_cuts'],
 'polling':prior['polling'],
 'comparison':{'existing_take2_synced':'out/outro_B2_v2/synced.mp4','primary_target':'You did, source80..111. Compare other two passages too; no requirement that take1 improve every line.','selection':'Codex and owner will choose per cut later. Do not change take2, historical manifests, production shotlist or future B3 anchor.'},
 'output':{'synced':'out/outro_B2_take1_kling_v1/synced.mp4','receipt':'out/outro_B2_take1_kling_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'assembly_guard':'Same origin4320 and continuous8second guide as take2, no new offset. Preserve all gaps and native timestamps. Do not restart or slide individual phrases. This is comparison material, not an automatic replacement.',
 'completion':'Download original and byte-identical synced.mp4 in THIS folder. Write RECEIPT.md with hashes, job ID, actual credits, settings, native fps/frame count/dimensions/video and audio durations/start times and observations on each visible cut. Add claude_result and set claude_done_ready_for_codex_verification. Return imperfect output, no auto retry, no Flow, no FX, no assembly, no commit.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('Verified archived take1 and identical guide. Kling-only handoff ready.')
