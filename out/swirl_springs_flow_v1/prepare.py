"""One bounded Flow retry of the overhead spiral, with geothermal surface detail."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
shutil.copy2(ROOT/'codex/out/canal_junction_turn_b.jpg',OUT/'first_frame.jpg')
shutil.copy2(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt',OUT/'style_lock_v2.txt')
lock=(OUT/'style_lock_v2.txt').read_bytes()
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock)
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock)
def asset(name):
    p=OUT/name;return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
old=json.loads((ROOT/'out/spring_geyser_flow_v1/handoff.json').read_text())
m={k:old[k] for k in ['schema_version','project_root','authorization','generation','polling','completion']}
m.update(test_id='swirl_springs_flow_v1',status='ready_for_claude_not_submitted',task='One Flow-only replacement of overhead spiral turn, no Kling. Improve swimmer persistence and add restrained geothermal surface activity.')
m['inputs']={'first_frame':asset('first_frame_surface.png'),'formation_reference_inspect_only':asset('first_frame.jpg'),'prompt':asset('flow_prompt.txt'),'lock':asset('style_lock_v2.txt')}
m['input_guard']='Revision2: use first_frame_surface.png as sole START. Original first_frame.jpg is inspect-only reference for the surfaced spiral, never an END frame. No audio. Prompt verbatim including lock. This supersedes the already-surfaced starting direction.'
m['clock']={'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':4030,'song_origin_seconds':4030/24,'additional_audio_offset_seconds':0,'note':'NEW take clock. Source0 maps to4030; do not inherit the old source24-frame offset.'}
m['cut']={'shot_id':'turn_phrase','setup':'canal_junction_turn','song_frames':[4030,4073],'source_frames_at_24fps':[0,43],'duration_seconds':43/24,'lead_handle_frames':0,'exit_handle_frames_if_192_delivered':149,'speed':1}
m['lyric_targets']=[{'word':'Then','song_frame':4038,'source_seconds':8/24},{'word':'turns','song_frame':4045,'source_seconds':15/24}]
m['timing_guard']='The preview uses only the first1.792seconds. Begin physically surfacing immediately, become a readable turning spiral around1second. No long setup or delayed reveal. Exact beat matching will be reviewed locally, no retiming by Claude. Preserve full8second download.'
m['quality_gate']=['Inspect intended source0..43 densely, then the full take. Follow several swimmers across consecutive frames: no pop-in/out, duplicates, merging, disappearance or body morph.','Keep overhead spiral readable with stable perimeter geography. No substitution of oblique aerial, underwater shot or new formation.','Geothermal bubbles, low water puffs and thin steam remain peripheral, not hiding swimmers.','Save and report defects even if the result is imperfect. No automatic second attempt; owner chooses whether minor flaws matter in the actual cut.']
m['output']={'base':'out/swirl_springs_flow_v1/base.mp4','receipt':'out/swirl_springs_flow_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True}
m['assembly_guard']='Codex will replace ONLY turn_phrase4030..4073 in out/swimming_to_outro_review_v1/shotlist.json for comparison. New source0..43, not old source24..67. Preserve plunge, following underwater shot, tunnel FX timing and outro clips. Discard Veo audio in assembly; master/lyrics once. No production edits or acceptance claims by Claude.'
m['deferred_fx']='Vectorscope/rosette treatment may be explored separately after reviewing the replacement. Do not bake it into the generation.'
m['revision']=2
m['revision_note']='Owner added surfacing-to-spiral continuity from preceding underwater shot. Same single authorized submission, not permission for an extra generation. If an earlier version was already submitted, preserve/report it and stop before another paid submission.'
(OUT/'handoff.json').write_text(json.dumps(m,indent=2))
print('Swirl retry handoff ready, not submitted.')
