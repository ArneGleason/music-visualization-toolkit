"""Prepare a single non-speaking replacement take with explicit source timing."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
ref=ROOT/'codex/out/astronaut_inspect_medium_a.jpg'
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
action=(OUT/'action_prompt.txt').read_text()
(OUT/'flow_prompt.txt').write_bytes(action.encode()+b'\n\n'+lock.read_bytes())
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock.read_bytes())
h=json.loads((ROOT/'out/garden_walk_return_v1/handoff.json').read_text())
h.pop('claude_result',None)
h.update(test_id='specimen_discovery_v1',status='ready_for_claude_not_submitted',
         task='ONE new Flow silent listening/discovery performance. No Kling. Replace repetitive specimen stroking with one rotation, discovery hold, knowing look up.')
h['inputs']={'first_frame':{'file':str(ref.relative_to(ROOT)).replace('\\','/'),
                          'sha256':sha(ref),'provenance':'Owner selected A in codex/out/still_favorites.md; Codex inspected. Existing specimen and set continuity.'},
             'prompt':{'file':'out/specimen_discovery_v1/flow_prompt.txt','sha256':sha(OUT/'flow_prompt.txt')},
             'lock':{'file':'out/astronaut_reply_v1/style_lock_v2.txt','sha256':sha(lock)}}
h['clock'].update(song_origin_frame=2004)
h['proposed_cut']={'shot_id':'exchange_listener_discovery','setup':'astronaut_inspect_medium',
                  'song_frames':[2016,2122],'source_frames_after_timestamp_conform':[12,118],
                  'duration_frames':106,'lead_handle_frames':12,'requested_exit_handle_frames':74,
                  'status':'Candidate replacement only; existing specimen-table cut1854..2016 is approved and unchanged.'}
h.pop('phrase',None)
h['phrases']=[{'text':text,'speaker':'Them1 offscreen; pictured Them2 listens',
               'song_frames':[a,b],'source_seconds':[(a-2004)/24,(b-2004)/24]}
              for text,a,b in [('Do you see a pattern?',2020,2059),("I'm sure it's there.",2059,2084),('Hard to find, right?',2084,2122)]]
h['output'].update(base='out/specimen_discovery_v1/base.mp4',receipt='out/specimen_discovery_v1/RECEIPT.md')
h['assembly_guard']='Candidate only. Song2016..2122 uses source12..118 at24fps after timestamp conform. No source audio or lip sync. Do not move phrase cuts to suit generated action without review. Inspect actual gesture timing. Codex adds a restrained spiral glimmer during discovery after tracking the returned specimen. No automatic production replacement.'
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('Single Flow handoff ready; selected A and unchanged lock verified.')
