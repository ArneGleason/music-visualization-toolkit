from pathlib import Path
import sys

sys.path.insert(0, str(Path('tools').resolve()))
from build_chorus_revision import encode, load, probe

base = Path('projects/a-right-little-something').resolve()
out = base/'generated/storyboard/lab-silver-motion-v01'
shots = {s['id']: s for s in load(base/'shots/shotlist.json')['storyboardProposals']
         if s.get('batch') == 'lab-silver-v01'}
for take in load(out/'sources.json'):
    shot = shots[take['shotId']]
    target = out/(shot['id']+'.mp4')
    head = 0 if shot['id'] == 'lab2-01' else 2
    count = shot['frames']+head+2
    if target.exists() and int(probe(target)['nb_frames']) == count:
        continue
    lead = (42 if shot['id'] == 'lab2-05' else 24)-head
    move = shot['cameraMove']
    t = f'min(1,max(0,on/{count-1}))'
    ease = f'(({t})*({t})*(3-2*({t})))'
    def expr(values):
        return f'{values[0]}+({values[1]}-{values[0]})*{ease}'
    z, x, y = [expr(move[k]) for k in ('zoom','panX','panY')]
    vf = (f'fps=24,trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB),'
          'pad=1920:1080:(ow-iw)/2:(oh-ih)/2,scale=3840:2160,setsar=1,'
          f"zoompan=z='{z}':x='(iw-iw/zoom)*({x})':y='(ih-ih/zoom)*({y})':d=1:s=1920x1080:fps=24")
    encode(['-i',str(base/take['motionRef']),'-vf',vf],count,target)
    assert int(probe(target)['nb_frames']) == count
    print('Prepared', shot['id'], count, 'frames', flush=True)
