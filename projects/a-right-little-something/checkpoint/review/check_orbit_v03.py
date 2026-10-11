from pathlib import Path
import json,sys,math
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path('tools').resolve()))
from build_orbit_flight import continuous_flight

base=Path('projects/a-right-little-something').resolve()
plan=json.loads((base/'orbit-blender-v03.json').read_text(encoding='utf-8'))
out=base/plan['output']/'hybrid'
data=json.loads((out/'trajectory.json').read_text(encoding='utf-8'))
points=[Vector(p) for p in data['points']]
times=data['passageTimes']
_,spans=continuous_flight(plan['worlds'],metadata=True)
checks=[]
for world,start,end in zip(plan['worlds'][1:],spans[::2],spans[1::2]):
    center=Vector(world['centre'])
    momentum=[]
    for i in range(math.ceil(start*600)+2,math.floor(end*600)-2):
        velocity=(points[i+1]-points[i-1])/(times[i+1]-times[i-1])
        momentum.append((points[i]-center).cross(velocity).length)
    spread=(max(momentum)-min(momentum))/(sum(momentum)/len(momentum))
    assert spread<.02
    checks.append(dict(world=world['name'],relativeAngularMomentumSpread=spread))
data['loopSpans']=spans
(out/'trajectory.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(out/'velocity-check.json').write_text(json.dumps(dict(loopChecks=checks,interpretation='Nearly constant angular momentum within each loop supports Kepler-consistent relative speed. Transfers and world scale remain authored.'),indent=2)+'\n',encoding='utf-8')
print('Loop angular momentum spreads:',[round(c['relativeAngularMomentumSpread']*100,3) for c in checks],'percent')
