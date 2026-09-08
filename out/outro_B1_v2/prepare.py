"""Prepare one B1 Flow plus conditionally one Kling; no submissions here."""
from pathlib import Path
import hashlib,json,shutil,subprocess,wave
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists()
anchor=ROOT/'out/outro_anchors_v2/exobiologist.png'
assert hashlib.sha256(anchor.read_bytes()).hexdigest()=='ea5bc2eb64dabc0601e33769876f3b035e594ae345ede604bc694833f04c5f0b'
subprocess.run(['ffmpeg','-v','error','-n','-i',str(anchor),'-vf','scale=1280:720:flags=lanczos','-frames:v','1',str(OUT/'first_frame.png')],check=True)
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock.read_bytes())
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock.read_bytes())
# B1 has the identical absolute time window as A1. This is full vocal context,
# NOT the A-only gated guide used in old work.
guide=ROOT/'out/outro_A1_kling_v1/guide.wav'
assert hashlib.sha256(guide.read_bytes()).hexdigest()=='aec7fa16b9b240410a96b1363db4453bc24cfc355fc5b18c328c8fe7f3bff4f4'
shutil.copyfile(guide,OUT/'guide.wav')
with wave.open(str(OUT/'guide.wav')) as w: assert (w.getnframes(),w.getframerate(),w.getnchannels())==(384000,48000,1)
def ref(p): return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
h={'schema_version':1,'test_id':'outro_B1_v2','project_root':ROOT.as_posix(),'status':'ready_for_claude_not_submitted',
 'task':'ONE exobiologist B1 Flow base, inspect before ONE Kling. Pause on material face/suit/artifact defects; no retries.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':1,'kling_condition':'Base passes bounded visual review below; otherwise return base and stop for owner.','automatic_retries':False,'production_edit_changes':False},
 'generation':{'flow':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100},'kling':{'mode':'Lip Sync','character':'sole woman','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimate110 total, check actual UI for each step. No purchases.'},
 'inputs':{'first_frame':ref(OUT/'first_frame.png'),'approved_anchor':ref(anchor),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(lock),'guide':ref(OUT/'guide.wav')},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':4165,'song_end_frame_exclusive':4357,'requested_frames':192,'lead_stem_placement_offset_seconds':.178348,'raw_stem_start_seconds':4165/24-.178348,'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'guide_provenance':{'source':'Exact same full-window continuous-context guide as verified A1 test. B1 and A1 share song origin4165.','samples':384000,'processing':'Mono48k PCM16, original gaps intact, no gating, normalization or timing changes. Other speaker is intentionally present as context. Not speaker-separated.'},
 'visible_cuts':[{'song_frames':[4232,4262],'source_frames_at_24fps':[67,97],'phrase':'Define there.'}],
 'continuity':{'future_B2_anchor_source_frame_at_24fps':155,'future_B2_song_origin':4320,'do_not_generate_B2':True,'no_go_on':'B1 only contains the beginning as continuation context; production No go on4331..4362 requires B2, do not use truncated B1 or loop its tail.'},
 'base_gate':{'must_pass':['same face/plain silver suit, no chest dials or hoses','artifact same shape, stable hands, no morph or duplicated object','face readable and actively articulating Define there, not frozen puppet/humming','no camera cut or scene reset'],'tolerate_and_report':['modest warmth/smile, not a reason for endless retries','approximate scratch timing differs','minor glance or small low hand motion'],'if_material_failure':'Download and receipt base, set status=base_needs_owner_review, skip Kling; no retry.'},
 'output':{'base':'out/outro_B1_v2/base.mp4','synced':'out/outro_B1_v2/synced.mp4','receipt':'out/outro_B1_v2/RECEIPT.md','preserve_original_downloads':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'tool_time_counts':True,'no_progressive_backoff':True,'respect_rate_limits':True},
 'assembly_guard':'Codex selects only assigned B1 source67..97 and retains approved A1 TV map v2 clean once. Never shift to match scratch speech, use other-speaker context as visible B speech, or restart source clock. Native fps timestamp-conformed after download. No final media assignment here.',
 'completion':'Write RECEIPT.md with each original/copy SHA256, job ID, settings, actual credits, fps/count/duration and observations. Add claude_result and set claude_done_ready_for_codex_verification only when both done; otherwise explicit blocked/base review status. No assembly, commit, FX, B2 or auto retry.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('B1 handoff ready: one Flow plus conditionally one Kling; original8second clock retained.')
