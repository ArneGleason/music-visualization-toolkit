"""Two bounded, original-source lip-sync comparison handoffs."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
local = json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem = next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
lyrics = json.loads((ROOT/'shots/lyric_motion_full.json').read_text())['phrases']

def ref(path):
    return {'file':path.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

for name, original, origin, visible, replace in [
    ('opening', 'out/opening_performance_v3/base.mp4',143,[155,334],[155,334]),
    ('specimen', 'out/specimen_discovery_v1/base.mp4',2004,[2016,2122],[2059,2122]),
]:
    folder = OUT/name
    folder.mkdir(exist_ok=True)
    source = ROOT/original
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0','-c:v','copy','-an',str(folder/'base.mp4')],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem),'-af',
        f'atrim=start={origin/24-.178348}:duration=8,asetpts=PTS-STARTPTS',
        '-ac','1','-ar','48000','-c:a','pcm_s16le',str(folder/'guide.wav')],check=True)
    with wave.open(str(folder/'guide.wav')) as audio:
        assert audio.getnframes()==384000 and audio.getframerate()==48000
    manifest = {
        'schema_version':1,'test_id':f'lipsync_review_followup_v1_{name}',
        'project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
        'task':'One fresh Kling Lip Sync using the supplied original-performance video and aligned guide. NO Flow. Never resync an already synced file.',
        'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
        'generation':{'kling':{'mode':'Lip Sync','character':'sole real woman','guide_start_seconds':0,
            'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},
            'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimate only; verify UI. No purchases.'},
        'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':origin,
            'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':origin/24-.178348,
            'guide_already_aligned':True,'additional_audio_offset_seconds':0},
        'inputs':{'base':ref(folder/'base.mp4'),'guide':ref(folder/'guide.wav')},'source':ref(source),
        'guide_provenance':{'source':str(stem),'processing':'Continuous 8-second mono48k PCM16 slice. No gating, normalization, silence removal, stretch or added offsets.'},
        'phrases':[{'text':p['text'],'song_frames':[p['on'],p['off']],
            'source_seconds':[(p['on']-origin)/24,(p['off']-origin)/24]} for p in lyrics if p['on']<replace[1] and p['off']>replace[0]],
        'cut':{'visible_song_frames':visible,'replace_song_frames':replace,
            'replace_source_frames_at_24fps':[x-origin for x in replace],'speed':1},
        'output':{'synced':(folder/'synced.mp4').relative_to(ROOT).as_posix(),
            'receipt':(folder/'RECEIPT.md').relative_to(ROOT).as_posix(),
            'preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
        'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,
            'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
        'assembly_guard':'Codex verifies original download, guide alignment, every word and timestamp-based 24fps conform. Keep current assembly until owner comparison. No changes to cuts or master audio.',
        'specific_review':('Current opening allocation is155..334, NOT the historical155..293. Preserve the full important phrase. Assess natural mouth/teeth, missed words, phrase starts and ends. Do not brighten teeth or alter acting.' if name=='opening' else
            'Only2059..2122 becomes a speaking shot. Preserve original listening2016..2059. Reapply approved specimen_signal_v1 artifact glow AFTER sync. Never upload the FX composite. The original is a quiet listening performance, so report any puppet-like mouth or skipped words rather than retrying automatically.'),
        'completion':'Download full result and untouched original, record paths, hashes, dimensions, native fps, duration, credits and observed issues in RECEIPT.md. Add claude_result and set status=claude_done_ready_for_codex_verification. No assembly, commit, or approval claims.'
    }
    (folder/'handoff.json').write_text(json.dumps(manifest,indent=2))
print('Two handoffs ready; nothing submitted.')
