"""Prepare A2 without inheriting completed B2 state."""
from pathlib import Path
import json,hashlib,wave
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists()
def ref(p):
    return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
base=ROOT/'out/outro_A1_v3/base.mp4'; lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
assert ref(base)['sha256']=='99124a5780cd629cb086e9d362db2e1d78bb5afa2a9d89ca41fc09a428c13767'
assert ref(lock)['sha256']=='6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496'
assert ref(OUT/'guide.wav')['sha256']=='ce7b1cd73c5ba2adab1f3609b4ed7108ed4e94c855da56c6278913df73043004'
with wave.open(str(OUT/'guide.wav')) as w:
    assert (w.getnframes(),w.getframerate(),w.getnchannels())==(384000,48000,1)
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock.read_bytes())
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock.read_bytes())
b=json.loads((ROOT/'out/outro_B2_v2/handoff.json').read_text())
h={'schema_version':1,'test_id':'outro_A2_v2','project_root':ROOT.as_posix(),'status':'ready_for_claude_not_submitted',
 'task':'ONE astronomer A2 Flow continuation, base review then ONE Kling if usable. No automatic retries.',
 'authorization':b['authorization'],'generation':b['generation'],'clock':b['clock'],'guide_provenance':b['guide_provenance'],'polling':b['polling'],
 'inputs':{'first_frame':ref(OUT/'first_frame.png'),'continuation_base':ref(base),'approved_anchor':ref(ROOT/'out/outro_anchors_v2/astronomer.png'),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(lock),'guide':ref(OUT/'guide.wav')},
 'visible_cuts':[{'song_frames':[4362,4400],'source_frames_at_24fps':[42,80],'phrase':'Thought I heard something.'},{'song_frames':[4431,4461],'source_frames_at_24fps':[111,141],'phrase':'Was it you?'}],
 'continuity':{'anchor_base_frame_at_24fps':155,'anchor_song_frame':4320,'inspection':'Same face, wardrobe, stable clear TV and low hands. Mild closed smile; require active articulation in new take. Untreated BASE frame, no Kling or baked TV FX.','future_A3_anchor_source_frame_at_24fps':172,'future_A3_song_origin':4492,'do_not_generate_A3':True,'say_goodnight':'Only beginning is context here. Full line belongs to A3; never stretch or loop A2 to cover it.'},
 'base_gate':{'must_pass':['same face and brown study wardrobe, not silver suit','TV geometry and specimen/chart/room remain stable, hands do not obscure screen','active readable articulation through BOTH main lines, no persistent closed smile or head turned away','locked continuous shot, no scene reset'], 'tolerate_and_report':['modest warmth, not grounds for repeated retries','approximate scratch timing mismatch','small eye glance or subtle screen-light fluctuation'], 'if_material_failure':'Download and receipt base, set base_needs_owner_review, stop before Kling. No auto retry.'},
 'output':{'base':'out/outro_A2_v2/base.mp4','synced':'out/outro_A2_v2/synced.mp4','receipt':'out/outro_A2_v2/RECEIPT.md','preserve_original_downloads':True,'do_not_trim':True,'do_not_retime':True},
 'assembly_guard':'Song origin4320, guide offset already applied once. Clock runs while offscreen. Source42..80 and111..141 only, no sliding to scratch speech. Native returned fps retained for Codex timestamp conform. No wipes or pushes, straight cuts planned. TV FX added once locally after review, not generated here.',
 'completion':'Write RECEIPT.md with originals/copies SHA256, job IDs, settings, actual credits, native fps/decoded frame counts/dimensions/video and audio durations/start times, base gate and both sync windows. Add claude_result, set claude_done_ready_for_codex_verification after both stages; otherwise explicit blocked/base-review status. No A3/B3, FX, retries, assembly edits, commit or push.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('Verified A1 base, unchanged lock, shared B2 guide, A2 source windows42..80 and111..141.')
