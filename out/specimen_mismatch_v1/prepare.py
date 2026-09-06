"""Package next hands-only work order. No paid submissions."""
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()
lock=(ROOT/'out/opening_specimen_v2/style_lock_v2.txt').read_bytes()
(OUT/'style_lock_v2.txt').write_bytes(lock)
prompt=(OUT/'direction.txt').read_text(encoding='utf-8').rstrip()+'\n\n'+lock.decode('utf-8')
(OUT/'flow_prompt.txt').write_text(prompt,encoding='utf-8')
assert (OUT/'flow_prompt.txt').read_text(encoding='utf-8').endswith(lock.decode('utf-8'))
still=ROOT/'codex/out/canal_map_macro_b.jpg'
h={
 'schema_version':1,'test_id':'specimen_mismatch_v1','project_root':ROOT.as_posix(),
 'status':'ready_for_claude_not_submitted',
 'task':'One overhead failed-fit take; no lip sync, no further shots.',
 'authorization':{'new_paid_generation':True,'max_flow_submissions':1,
     'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'inputs':{'first_frame':{'file':still.relative_to(ROOT).as_posix(),'sha256':sha(still)},
     'prompt':{'file':'out/specimen_mismatch_v1/flow_prompt.txt','sha256':sha(OUT/'flow_prompt.txt')},
     'lock':{'file':'out/specimen_mismatch_v1/style_lock_v2.txt','sha256':sha(OUT/'style_lock_v2.txt')}},
 'generation':{'model':'Veo 3.1 Quality','mode':'Frames','start_frame':still.relative_to(ROOT).as_posix(),
     'end_frame':None,'seconds':8,'aspect_ratio':'16:9','resolution':'720p','outputs':1,
     'expected_credits':100,'stop_if_cost_exceeds_expected':True},
 'proposed_review_cut':{'review_id':'specimen_mismatch','replaces_old_shot_id':'s008',
     'song_start_frame':670,'song_end_frame_exclusive':719,'duration_frames':49,
     'lyric':"Then they don't quite match.",'lyric_song_frames':[680,719],
     'candidate_source_in_frame':48,'candidate_source_out_frame_exclusive':97,
     'candidate_source_origin_song_frame':622,
     'note':'Source window is provisional until action inspection. Song cut is frame-based; do not shorten the lyric to fit generated action.'},
 'clock':{'fps':24,'indexing':'zero-based end-exclusive','speed':1,'master_audio_only':True,
     'note':'Unsynced prop take. No vocal guide and no stem offset. Candidate origin622 is editorial mapping, not a claim of music-synced generation.'},
 'coverage':{'requested_source_frames':192,'required_continuous_frames':49,
     'candidate_lead_frames':48,'candidate_exit_frames':95,'verify_real_handles':True,
     'note':'Keep the entire take. Codex can select a different contiguous normal-speed window after review; report where mismatch is clearest.'},
 'continuity':{'previous_approved_review':'out/pieces_cutaway_review/preview.mp4',
     'last_prop_insert':{'file':'clips/raw/canal_map_macro_v6.mp4','source_frames':[24,72],
         'song_frames':[562,610],'crop':'960x540 at160,180 then scaled to1280x720'},
     'intent':'New comparison after the singer cutaway, with a different turned edge and a failed result. Not exact match-on-action or a reset loop.',
     'reference_policy':'Only the approved still is uploaded as first frame. Generated video frames are planning references, not Flow start frames.'},
 'output':{'base':'out/specimen_mismatch_v1/base.mp4','receipt':'out/specimen_mismatch_v1/RECEIPT.md',
     'preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'assembly':{'owner':'Codex after download','production_assignment_requires_review':True,
     'next_phrase':'Can I send you my stuff?','next_phrase_start_frame':719,
     'note':'Preview may end719. The next signal/send shot is not authorized by this work order. Preserve protected FX and reconcile isolated cues and shotlist together.'}
}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
assert h['proposed_review_cut']['duration_frames']==97-48==719-670
print('Ready. One Flow take, expected100 credits, no Kling. Lock preserved unchanged.')
