"""Prepare a bounded base-only handoff; never submit generation."""
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def ref(path):
    return {'file': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}

anchor = ROOT / 'out/outro_anchors_v2/astronomer.png'
first = OUT / 'first_frame.png'
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(anchor),
                '-vf', 'scale=1280:720:flags=lanczos', '-frames:v', '1', str(first)], check=True)
lock = ROOT / 'out/astronaut_reply_v1/style_lock_v2.txt'
direction = (OUT / 'direction.txt').read_bytes()
prompt = OUT / 'flow_prompt.txt'
prompt.write_bytes(direction.rstrip() + b'\n\n' + lock.read_bytes())
assert prompt.read_bytes().endswith(lock.read_bytes())
cues = json.loads((ROOT / 'generated/overlay_cues.json').read_text())
beats = [b for b in cues['beats'] if 4165 <= b['frame'] < 4357]
intervals = [b['sec'] - a['sec'] for a, b in zip(beats, beats[1:])]
manifest = {
    'schema_version': 1, 'test_id': 'outro_A1_v2', 'project_root': ROOT.as_posix(),
    'status': 'ready_for_claude_not_submitted',
    'task': 'ONE Flow base only. New approved astronomer outro anchor, quiet accomplishment. STOP before Kling.',
    'authorization': {'max_flow_submissions': 1, 'max_kling_submissions': 0,
                      'automatic_retries': False, 'production_edit_changes': False},
    'generation': {'model': 'Veo 3.1 Quality', 'mode': 'Frames', 'aspect_ratio': '16:9',
                   'resolution': '720p', 'duration_seconds': 8, 'outputs': 1,
                   'expected_credits': 100, 'stop_if_unavailable_or_cost_exceeds_expected': True},
    'inputs': {'first_frame': ref(first), 'approved_anchor': ref(anchor),
               'prompt': ref(prompt), 'lock': ref(lock)},
    'clock': {'timeline_fps': 24, 'indexing': 'zero-based, end-exclusive',
              'song_origin_frame': 4165, 'song_end_frame_exclusive': 4357,
              'requested_take_frames': 192, 'no_audio_upload': True,
              'guide_status': 'No Kling guide supplied or authorized; Codex prepares after base review.'},
    'visible_cuts': [
        {'song_frames': [4177, 4232], 'source_frames_at_24fps': [12, 67], 'phrase': 'You still there?'},
        {'song_frames': [4262, 4331], 'source_frames_at_24fps': [97, 166], 'phrase': 'Never mind / La-la-la, low light'}],
    'continuity': {'source_clock_runs_while_offscreen': True, 'speed': 1,
                   'lead_frames': 12, 'exit_frames_after_last_visible_cut': 26,
                   'future_A2_anchor_source_frame_at_24fps': 155,
                   'do_not_generate_A2': True},
    'performance_reference': {'phrase_times_source': 'shots/outro_coverage.json takes.A1; approximate acting only, not a verified new Kling guide',
                              'beat_source': 'generated/overlay_cues.json',
                              'local_median_bpm': 60 / statistics.median(intervals) if intervals else None,
                              'beats': beats},
    'polling': {'first_check_seconds': 30, 'default_interval_seconds': 20,
                'at_90_percent_seconds': 10, 'exponential_backoff': False,
                'note': 'Count tool time toward interval. Read visible progress; download promptly when ready. Do not submit duplicates.'},
    'output': {'base': 'out/outro_A1_v2/base.mp4', 'receipt': 'out/outro_A1_v2/RECEIPT.md',
               'preserve_original_download': True, 'do_not_trim': True, 'do_not_retime': True},
    'review': {'return_even_if_imperfect': True, 'flag_defects_without_retry': True,
               'checks': ['identity and outfit', 'engaged restrained acting, not grinning or puppet stillness',
                          'mouth activity at voiced intervals and quiet listening gaps',
                          'TV unobstructed, dim and stable', 'no prop/hand morphing',
                          'no cuts or gesture reset; usable later frame155']},
    'return_protocol': 'Write RECEIPT.md and claude_result with paths, SHA256, native fps/frame count/duration, media ID, settings, actual credits and visual observations. Flip status to claude_done_ready_for_codex_verification. No assembly, no commit, no Kling.'
}
(OUT / 'handoff.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'first_frame': ref(first), 'local_bpm': manifest['performance_reference']['local_median_bpm'], 'prompt_lock_verified': True}))
