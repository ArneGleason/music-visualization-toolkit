"""Prepare one bounded orbital continuity retry; no external submissions."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def pointer(path):
    return {'file': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}

lock = (ROOT / 'out/astronaut_reply_v1/style_lock_v2.txt').read_bytes()
(OUT / 'style_lock_v2.txt').write_bytes(lock)
(OUT / 'image_prompt.txt').write_bytes((OUT / 'image_direction.txt').read_bytes().rstrip() + b'\n\n' + lock)
shutil.copy2(ROOT / 'out/message_into_rockets_v3/rocket_design_reference.jpg', OUT / 'landing_design_reference.jpg')
direction = '''Orbital descent, the same THREE silver rockets that appear in the approved landing shot. Animate the supplied first frame without redesigning its vehicles or changing their number. Preserve the smooth tapered pointed noses (no needle antenna), slim polished silver bodies, long black vertical rounded-top slots, small curved swept fins and compact engine bases. No circular portholes, extra fins, boosters, deployed parts or morphing hardware.

An eight-second uninterrupted practical-miniature space shot above coral Mars with blue-green rivers. The three rockets are braking and DESCENDING TAIL FIRST toward the planet, noses upright and away from the planet, not launching or climbing. Begin the descent immediately, no static introductory hold. Keep the formation and all three complete silhouettes readable throughout, especially source 0.5 to 2.458 seconds which is the intended edit window. Use a restrained slow symmetrical camera move and a slight downward drift of the vehicles relative to the horizon, with believable miniature parallax. Compact, narrow amber braking jets flicker gently only BELOW the engine bases. Engines never engulf the hulls; no smoke, fireballs, explosions, mushroom clouds or atmospheric reentry flames. Do not reach the ground, cut to a landing or transform this into the next shot. The landing already exists.

Keep the orbital composition, curved horizon, rivers, settlements, stars, striped planet and moons consistent with the supplied start frame. No person, face, helmet or foreground character. No text, no added FX overlay, no titles, no sudden camera moves. Maintain vehicle geometry through the entire shot. No lip-sync performance.''' 
(OUT / 'flow_prompt.txt').write_bytes(direction.encode('utf-8') + b'\n\n' + lock)
manifest = {
    'schema_version': 1, 'test_id': 'orbital_continuity_v1', 'project_root': str(ROOT),
    'status': 'ready_for_claude_not_submitted',
    'task': 'One Flow-only replacement of orbital s035, matching the approved landing rockets. This new authorization supersedes the old landing handoff instruction not to regenerate orbital. Do not regenerate the landing.',
    'authorization': {'max_flow_submissions': 1, 'max_kling_submissions': 0, 'automatic_retries': False, 'production_edit_changes': False},
    'generation': {'flow': {'model': 'Veo 3.1 Quality', 'mode': 'Frames', 'aspect_ratio': '16:9', 'resolution': '720p', 'duration_seconds': 8, 'outputs': 1, 'expected_credits': 100}, 'stop_if_unavailable_or_cost_exceeds_expected': True, 'cost_note': 'Historical estimate; verify actual UI. No purchases. No Kling.'},
    'inputs': {'first_frame': pointer(OUT / 'first_frame.png'), 'design_reference_inspect_only': pointer(OUT / 'landing_design_reference.jpg'), 'prompt': pointer(OUT / 'flow_prompt.txt'), 'lock': pointer(OUT / 'style_lock_v2.txt')},
    'input_guard': 'Use first_frame.png as the sole Flow START frame. Landing reference is for visual QA only, never the END frame. No end frame or audio guide.',
    'clock': {'timeline_fps': 24, 'indexing': 'zero-based end-exclusive', 'song_origin_frame': 2869, 'song_origin_seconds': 2869 / 24, 'additional_audio_offset_seconds': 0, 'note': 'Editorial source clock only; this is not lip-synced. No audio guide required.'},
    'cut': {'shot_id': 's035', 'lyric': 'Things clap overhead', 'song_frames': [2881, 2928], 'source_frames_at_24fps': [12, 59], 'lead_handle_frames': 12, 'exit_handle_frames_if_192_delivered': 133, 'speed': 1},
    'approved_landing': {'source': pointer(ROOT / 'out/rocket_landing_retry_v1/synced.mp4'), 'preview': 'out/message_into_rockets_v3/preview.mp4', 'owner_accepted': True, 'song_frames_in_current_preview': [2928, 3027], 'preserve_pressure_lens_fx': True},
    'quality_gate': ['Inspect first frame and frames through the intended source0.5..2.458s window, then the full clip.', 'Exactly three matching smooth silver rockets, black vertical slots, short curved fins, no new portholes or needles.', 'Descent tail-first, not ascent; restrained motion already present in the intended window.', 'No fire or smoke around hulls, no morphing or disappearing rockets.', 'Do not reject merely for subtle camera variation; record minor deviations for owner review. Material design mismatch: save result and stop, no automatic retry.'],
    'output': {'base': 'out/orbital_continuity_v1/base.mp4', 'receipt': 'out/orbital_continuity_v1/RECEIPT.md', 'preserve_original_download': True, 'do_not_trim': True, 'do_not_retime': True},
    'polling': {'first_check_seconds': 30, 'default_interval_seconds': 20, 'at_90_percent_seconds': 10, 'no_progressive_backoff': True, 'tool_time_counts': True, 'respect_rate_limits': True},
    'assembly_guard': 'Codex will timestamp-conform if needed and replace only s035 in the SAME 2786..3027 local preview. Keep message handoff, landing source/offsets, pressure-lens FX, lyric timing and master audio unchanged. Do not assemble or alter production registers.',
    'completion': 'Save untouched download and byte-identical base.mp4. Record IDs, settings, actual credits, hashes, native fps, frame count, dimensions and duration, visual QA and defects in RECEIPT.md. Add claude_result and flip status to claude_done_ready_for_codex_verification (or explicit blocked status). No commit, purchase or acceptance claim.'
}
assert (OUT / 'flow_prompt.txt').read_bytes().endswith(lock)
assert (OUT / 'image_prompt.txt').read_bytes().endswith(lock)
(OUT / 'handoff.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Prepared handoff; inputs hashed, original style lock preserved. No submission made.')
