"""Prepare one new astronaut performance contract; no submission."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import wave
import numpy as np

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
assert not (OUT/'handoff.json').exists(), 'Versioned contract already exists; do not reset it'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def pcm(p,start=0):
 return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af',
  f'atrim=start={start:.12f}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-f','s16le','-'])
prior=json.loads((ROOT/'out/pieces_performance_v1/handoff.json').read_text())
source=Path(prior['guide_provenance']['source'])
assert sha(source)==prior['guide_provenance']['source_sha256']
test=np.frombuffer(pcm(source,143/24-.178348),dtype='<i2').astype(float)
ref=np.frombuffer(pcm(ROOT/'out/opening_sync_test/guide.wav'),dtype='<i2').astype(float)
corr=float(np.corrcoef(test,ref)[0,1]); assert corr>.995
origin,start,end=899,911,1030
with wave.open(str(OUT/'guide.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
 w.writeframes(pcm(source,origin/24-.178348))
with wave.open(str(OUT/'guide.wav')) as w: assert w.getnframes()==384000
lock=(ROOT/'out/opening_performance_v3/style_lock_v2.txt').read_bytes()
(OUT/'style_lock_v2.txt').write_bytes(lock)
(OUT/'flow_prompt.txt').write_text((OUT/'direction.txt').read_text().rstrip()+'\n\n'+lock.decode(),encoding='utf-8')
assert (OUT/'flow_prompt.txt').read_text(encoding='utf-8').endswith(lock.decode())
still=ROOT/'codex/out/astronaut_close_sync_a.jpg'
h={k:copy.deepcopy(prior[k]) for k in ['schema_version','project_root','authorization','generation','assembly']}
h.update(test_id='astronaut_reply_v1',status='ready_for_claude_not_submitted',
 task='One new astronaut singing base then one Kling pass; no later shots.',
 clock={'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':origin,
 'song_origin_seconds':origin/24,'requested_take_seconds':8,'requested_take_frames':192,
 'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':origin/24-.178348,
 'guide_already_aligned':True,'guide_upload_start_seconds':0,'additional_audio_offset_seconds':0},
 cut={'shot_id':'s012','song_start_frame':start,'song_end_frame_exclusive':end,
 'source_in_frame_at_24fps':12,'source_out_frame_exclusive_at_24fps':131,'duration_frames':119,'speed':1},
 phrases=[{'text':text,'song_frames':[a,b],'source_seconds':[(a-origin)/24,(b-origin)/24],'use':use}
  for text,a,b,use in [("I don't see anything.",920,971,'visible'),('Think you forgot to attach it.',971,1030,'visible'),
  ("If you've got it, give it.",1030,1082,'spare continuation only; next planned shot remains separate')]],
 inputs={'first_frame':{'file':still.relative_to(ROOT).as_posix(),'sha256':sha(still)},
 'guide':{'file':'out/astronaut_reply_v1/guide.wav','sha256':sha(OUT/'guide.wav'),'sample_rate':48000,'channels':1,'samples':384000},
 'prompt':{'file':'out/astronaut_reply_v1/flow_prompt.txt','sha256':sha(OUT/'flow_prompt.txt')},
 'lock':{'file':'out/astronaut_reply_v1/style_lock_v2.txt','sha256':sha(OUT/'style_lock_v2.txt')}},
 guide_provenance={'source':source.as_posix(),'source_sha256':sha(source),'opening_guide_correlation':corr,
 'processing':'Uninterrupted eight-second mono48k PCM16 extraction. No gates, normalization, removed silence or extra offset.'},
 output={'base':'out/astronaut_reply_v1/base.mp4','synced':'out/astronaut_reply_v1/synced.mp4',
 'receipt':'out/astronaut_reply_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 coverage_guard='Visible picture must cover through source131/24=5.458333s. Preserve full actual returned duration including real lead and tail. No held-head padding.',
 assembly_caveat='Prior assembly ends911; new cut911..1030. Do not use old s012 cut912..1047 or old guide origin. Latest preferred receiver is out/receiver_voice_review. No production edits.',
 polling={'applies_to':['Flow','Kling'],'first_check_seconds':30,'default_interval_seconds':20,
 'near_completion_threshold_percent':90,'near_completion_interval_seconds':10,'maximum_routine_interval_seconds':30,
 'progress_estimate':'With increasing percent, estimate remaining=(100-current)/(percent gain/elapsed seconds). Next check=max(10,min(20,0.5*estimated remaining)). Percent is approximate; default20 if unusable.',
 'no_exponential_backoff':True,'no_repeated_page_refresh':True,
 'exceptions':'Honor explicit rate limits and retry-after. Tool latency counts as waiting. No overlapping checks. No resubmission for unchanged status.',
 'stalled_job':'At15 minutes pending report status to owner, keep20-30s checks if tools allow; explicit service errors require stopping and reporting, never automatic retry.'})
beats=[b for b in json.loads((ROOT/'generated/overlay_cues.json').read_text())['beats'] if origin<=b['frame']<origin+192]
h['performance']={'prompt_bpm':84,'measured_local_bpm':float(60/np.mean(np.diff([b['sec'] for b in beats]))),
 'gesture_spacing_beats':[2,4],'beat_grid':[dict(b,source_sec=b['sec']-origin/24) for b in beats],
 'benchmark':'out/opening_performance_v3; expression and real singing, not quiet closed-mouth posing'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print(json.dumps({'status':h['status'],'guide_sha256':sha(OUT/'guide.wav'),'origin':origin/24,'raw_extract':origin/24-.178348,
 'correlation':corr,'local_bpm':h['performance']['measured_local_bpm'],'cut':[start,end]},indent=2))
