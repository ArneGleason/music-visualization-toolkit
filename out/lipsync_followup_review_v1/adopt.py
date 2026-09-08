"""Build a fresh review snapshot without altering past previews or production timing."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
edl=json.loads((ROOT/'out/meant_cutaway_v1/shotlist.json').read_text())
shot=next(s for s in edl['shots'] if s['id']=='exchange_listener_audition')
assert round(shot['start_sec']*24)==2016 and round(shot['end_sec']*24)==2122
shot['clip']={'file':'out/lipsync_followup_review_v1/clean.mp4','in_sec':0,'speed':1}
shot['description']='Approved original listening lead-in, then specimen lip sync on sure/there/hard-to-find/right, with internal activation.'
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_bytes((ROOT/'out/meant_cutaway_v1/overlay_cues.json').read_bytes())
print('Review snapshot updated through2658. Previous opening preserved; accepted specimen selected.')
