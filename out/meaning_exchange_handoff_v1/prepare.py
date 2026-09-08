"""Prepare two fresh motion plates and one speaker-only sync with exact clocks."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
lock=(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt').read_bytes()
(OUT/'style_lock_v2.txt').write_bytes(lock)
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
jobs=[]
for name,image,origin,visible,sync in [
 ('astronaut','astronaut_close_sync_a.jpg',2646,[2658,2826],True),
 ('astronomer','astronomer_desk_sync_b.jpg',2774,[2786,2881],False)]:
    folder=OUT/name;folder.mkdir(exist_ok=True)
    direction=(OUT/f'{name}_direction.txt').read_bytes()
    (folder/'flow_prompt.txt').write_bytes(direction+b'\n\n'+lock)
    assert (folder/'flow_prompt.txt').read_bytes().endswith(lock)
    guide=None
    if sync:
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem),'-af',f'atrim=start={origin/24-.178348}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(folder/'guide.wav')],check=True)
        with wave.open(str(folder/'guide.wav')) as w:assert w.getnframes()==384000
        guide=ref(folder/'guide.wav')
    h={'schema_version':1,'test_id':f'meaning_exchange_v1_{name}','status':'ready_for_claude_not_submitted',
       'project_root':str(ROOT),'task':('One new Flow singing plate, then one Kling sync if the plate passes usability checks.' if sync else 'One new Flow listening plate. NO Kling. No dialogue.'),
       'authorization':{'max_flow_submissions':1,'max_kling_submissions':int(sync),'automatic_retries':False,'production_edit_changes':False},
       'generation':{'flow':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100},
         'kling':({'mode':'Lip Sync','character':'sole real woman','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10} if sync else None),
         'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical expectations only; verify actual UI. No purchases or auto-retries.'},
       'inputs':{'first_frame':ref(ROOT/'codex/out'/image),'prompt':ref(folder/'flow_prompt.txt'),'lock':ref(OUT/'style_lock_v2.txt'),'guide':guide},
       'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':origin,'song_origin_seconds':origin/24,
         'lead_stem_placement_offset_seconds':.178348 if sync else None,'raw_stem_extract_start_seconds':origin/24-.178348 if sync else None,
         'guide_already_aligned':sync,'additional_audio_offset_seconds':0,'source_duration_frames':192},
       'cut':{'visible_song_frames':visible,'visible_source_frames_at_24fps':[x-origin for x in visible],
         'lead_handle_frames':12,'exit_handle_frames':192-(visible[1]-origin),'speed':1,
         'panel_push_song_frames':[2786,2826],'overlap_is_intentional':True},
       'camera':('Gentle axial pullback from close first frame,15-20percent smaller head by source6seconds.' if sync else 'Gentle axial push-in from wider first frame,10-15percent larger head by source4.5seconds.'),
       'quality_gate_before_kling':('Review full base for actual singing, full phrase coverage through source7.5, natural teeth, visible face, stable identity and gentle pullback. If silent, clamped-mouth, missing phrase, identity/prop failure, or unusable camera move, stop and report base only; no automatic Flow retry or Kling spend.' if sync else 'No Kling under any circumstances. Confirm closed relaxed mouth after source0.5 and live attentive listening.'),
       'output':{'base':(folder/'base.mp4').relative_to(ROOT).as_posix(),'synced':(folder/'synced.mp4').relative_to(ROOT).as_posix() if sync else None,
         'receipt':(folder/'RECEIPT.md').relative_to(ROOT).as_posix(),'preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
       'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
       'completion':'Save untouched original downloads and byte-identical base/synced copies. Record hashes, native fps, dimensions, frames, stream start times/durations, settings, job IDs, actual credits and visual defects. Add claude_result and set status=claude_done_ready_for_codex_verification. Partial failure stays explicit. No assembly, grading, FX, crop, commit or approval claim.'}
    (folder/'handoff.json').write_text(json.dumps(h,indent=2));jobs.append(ref(folder/'handoff.json'))
(OUT/'handoff.json').write_text(json.dumps({'status':'ready_for_claude_not_submitted','jobs':jobs,'max_total_flow':2,'max_total_kling':1,
 'reference_choreography':'out/meaning_orb_loop_v4/preview.mp4','current_request':'Fresh opposing axial camera moves plus coordinated offering/listening. Local sideways panel push and looping object remain separate.',
 'speaker_guard':'All four lines are Them2 astronaut. Astronomer listens. No words duplicated across faces.',
 'eight_second_guard':'Astronaut origin2646 ends2838. Only visible through2826, so source covers the full on-screen part including transition. Remaining Words leave words continues on master while astronomer listens; do not squeeze the whole phrase into8seconds or stretch the picture.'},indent=2))
print('Two handoffs prepared:2 Flow maximum,1 Kling maximum. Nothing submitted.')
