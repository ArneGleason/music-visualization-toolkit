"""Package a bounded Flow task without submitting generation."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
for source, name in [
    ('out/opening_need_compare_v1/horizon.png', 'first_frame.png'),
    ('out/opening_need_aerial_v1/first_frame.png', 'downward_reference.png'),
    ('out/astronaut_reply_v1/style_lock_v2.txt', 'style_lock_v2.txt'),
]:
    shutil.copy2(ROOT/source, OUT/name)
lock = (OUT/'style_lock_v2.txt').read_bytes()
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock)
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock)
def asset(name):
    p=OUT/name
    return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest={
    'schema_version':1,'test_id':'opening_aerial_flow_v1','project_root':str(ROOT),
    'status':'ready_for_claude_not_submitted',
    'task':'Generate one continuous Mars aerial push-in for the approved opening cutaway. Flow only, no Kling or assembly.',
    'authorization':{'max_flow_submissions':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
    'generation':{'flow':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical settings and cost. Verify current UI; no purchase or silent substitution.'},
    'inputs':{'first_frame':asset('first_frame.png'),'composition_reference_inspect_only':asset('downward_reference.png'),'prompt':asset('flow_prompt.txt'),'lock':asset('style_lock_v2.txt')},
    'input_guard':'Upload first_frame.png as the sole START frame. Inspect downward_reference.png for destination angle, not exact geography. Do not attach it as END frame or ingredient. No audio input. Two independently generated views are not calibrated camera endpoints; avoid forced morphing.',
    'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':205,'song_origin_seconds':205/24,'additional_audio_offset_seconds':0,'note':'Editorial mapping only, no lip sync. Source timestamp zero maps to song frame205.'},
    'cut':{'shot_id':'opening_need_landscape','song_frames':[205,282],'source_frames_at_24fps':[0,77],'duration_seconds':77/24,'lead_handle_frames':0,'exit_handle_frames_if_192_delivered':115,'speed':1,'return':'Astronomer returns at282, two frames before Its important cue284.'},
    'motion_requirement':'Useful viewpoint change must occur within source0..3.208seconds, not first arrive at8seconds. Begin with visible horizon, move forward and smoothly pitch downward to a closer terrain-dominant view by about3seconds. Remaining footage continues naturally as reusable B-roll. No freeze, cut, speed ramp or snap.',
    'quality_gate':[
        'Inspect first frame, 1s, 2s, 3.2s and the full clip. Save a contact sheet if practical.',
        'Horizon visible initially; purposeful aerial progress and increasingly downward view within the actual first3.208seconds.',
        'Terrain, waterways, domes and oasis remain stable; no morphing, erupting buildings, new characters, spacecraft or giant light objects.',
        'Destination reference is directional, not pixel matching. Minor composition differences are acceptable. Record defects without auto-retrying or withholding the downloaded result.',
        'Camera motion is the explicit shot-specific exception to the generic flat staging in the unchanged lock. Do not edit the lock.'
    ],
    'optional_codex_fx':{'status':'small local test proposed, not part of Flow generation','idea':'One tiny restrained green glimmer in the garden canopy, suggesting a signal worth investigating. Track its placement after reviewing generated camera motion. No beam, floating orb, repeated strobe, large glow or green recoloring of the oasis. Omit if distracting.','owner_note':'User suggested a little green flash, not a prominent added object.'},
    'output':{'base':'out/opening_aerial_flow_v1/base.mp4','receipt':'out/opening_aerial_flow_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
    'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
    'assembly_guard':'Codex verifies and timestamp-conforms if necessary. Use source0..77 at24fps for song205..282 at speed1. Do not stretch an8second move into3.208seconds. Keep original face source clock, all lyrics and master timing intact; master audio once. Current preview out/opening_need_compare_v3/compare.mp4 is approved for timing. No assembler/register changes by Claude.',
    'completion':'Save untouched original and byte-identical base.mp4 even if imperfect. Record media ID, actual settings/cost, download paths, SHA256, native fps/frame count/dimensions/duration, progress and visual QA in RECEIPT.md. Add claude_result and set status claude_done_ready_for_codex_verification, or explicit blocked status with reason. No automatic retries, commit, purchase or owner-acceptance claim.'
}
(OUT/'handoff.json').write_text(json.dumps(manifest,indent=2))
print('Handoff ready; no generation submitted.')
