"""Prepare bounded B2 continuation, retaining the shared song clock."""
from pathlib import Path
import hashlib, json, subprocess, wave
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists(), 'Do not reset submitted work'
def ref(p):
    return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
base=ROOT/'out/outro_B1_v2/base.mp4'
assert ref(base)['sha256']=='2ed1a1b84dafd68a77b7141768ae580661a4039b83552fad54a1cdc1493c92b7'
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
assert ref(lock)['sha256']=='6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496'
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock.read_bytes())
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock.read_bytes())
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stems=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav')); assert len(stems)==1
start=4320/24-.178348
subprocess.run(['ffmpeg','-v','error','-n','-i',str(stems[0]),'-af',f'atrim=start={start}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'guide.wav')],check=True)
with wave.open(str(OUT/'guide.wav')) as w:
    assert (w.getnframes(),w.getframerate(),w.getnchannels())==(384000,48000,1)
h=json.loads((ROOT/'out/outro_B1_v2/handoff.json').read_text())
h.pop('claude_result',None)
h.update(test_id='outro_B2_v2',status='ready_for_claude_not_submitted',task='ONE B2 continuation Flow base, inspect before ONE Kling. No automatic retry or other take.')
h['inputs']={'first_frame':ref(OUT/'first_frame.png'),'continuation_base':ref(base),'approved_anchor':ref(ROOT/'out/outro_anchors_v2/exobiologist.png'),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(lock),'guide':ref(OUT/'guide.wav')}
h['clock']={'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':4320,'song_end_frame_exclusive':4512,'requested_frames':192,'lead_stem_placement_offset_seconds':.178348,'raw_stem_start_seconds':start,'guide_already_aligned':True,'additional_audio_offset_seconds':0}
h['guide_provenance']={'source':str(stems[0]),'samples':384000,'processing':'Fresh continuous eight-second mono48k PCM16 slice. No gating, normalization, trimming gaps or time stretching. Stem placement offset applied once. Contains other speaker as context, NOT speaker-separated.'}
h['visible_cuts']=[{'song_frames':[a,b],'source_frames_at_24fps':[a-4320,b-4320],'phrase':s} for a,b,s in [(4331,4362,'No, go on.'),(4400,4431,'You did.'),(4461,4504,"Da-da-dum / Could've been.")]]
h['continuity']={'anchor_base_source_frame_at_24fps':155,'anchor_song_frame':4320,'anchor_inspection':'Face, plain suit and stable artifact accepted for continuation; mouth naturally open. From untreated BASE, not Kling or composited FX.','future_B3_anchor_source_frame_at_24fps':180,'future_B3_song_origin':4500,'do_not_generate_B3':True}
h['base_gate']['must_pass'][2]='readable active articulation on all three assigned passages, not frozen puppet or continuous humming'
h['base_gate']['tolerate_and_report']=['modest warmth or smile, no endless retries','approximate scratch timing differs','small natural low hand movement, no prop morph']
h['output']={'base':'out/outro_B2_v2/base.mp4','synced':'out/outro_B2_v2/synced.mp4','receipt':'out/outro_B2_v2/RECEIPT.md','preserve_original_downloads':True,'do_not_trim':True,'do_not_retime':True}
h['assembly_guard']='Use only source11..42,80..111,141..184 at24fps after timestamp conform. Clock advances offscreen, never restart source on a return or shift to generated scratch speech. Clean FX continuation added by Codex after review using song time; no baked FX input. Preserve native returned duration, even239frames at30fps. No assembly assignment here.'
h['completion']='Write RECEIPT.md with input checks, original/copy hashes, job IDs, settings, actual credits, native fps/frame count/video and audio durations, base gate and lip sync observations for all three visible cuts. Add claude_result and set claude_done_ready_for_codex_verification when both stages done; otherwise specific blocked/base review status. No A2, B3, auto retries, assembly, FX or commit.'
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
(OUT/'verification.json').write_text(json.dumps({'guide_samples':384000,'guide_seconds':8,'song_origin':4320,'base_anchor_frame':155,'anchor_song_frame':4165+155,'lock_byte_identical_suffix':True,'raw_stem_start_seconds':start,'additional_offset':0,'visible_ranges_fit_requested_take':all(c['source_frames_at_24fps'][1]<=192 for c in h['visible_cuts'])},indent=2))
print('B2 ready: source155 -> song4320, fresh8second guide, lock verified.')
