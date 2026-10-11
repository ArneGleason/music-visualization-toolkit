"""Record user acceptance and expose the existing full-song working edit."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
path=PROJECT/'shots/shotlist.json'
register=load(path)
shot=next(s for s in register['storyboardProposals'] if s['id']=='lab2-08')
selection=shot['motionSelection']
assert selection['id']=='lab2-08-escape-approach-motion-v01'
selection.update(userSelected=True,draftForReview=False,status='User accepted escape setup for the full animatic')
for test in shot['motionTests']:
    if test['id']==selection['id']:
        test.update(userSelected=True,draftForReview=False,status=selection['status'])
shot['animaticPlacement']['userSelected']=True
shot['status']='User accepted native escape setup in full animatic V37'
shot['motionReview']['notes']='User accepted the escape setup. Native glance/turn beside the lit pod hatch; departure remains planned after Bright night. '+selection['reviewNotes']
departure=next(s for s in register['storyboardProposals'] if s['id']=='escape-001')
departure['description']='Harper’s pod is cut loose, dropped or ejected from the original robot laboratory ship, then establishes a flight path into the next part of the song'
departure['sourceDirection']='User explicitly placed departure after Bright night, then requested full-song playback before choosing the next starting frames and flight path. Ejection/release direction added October10.'
departure['status']='Planned after full-animatic review; pod identity, release mechanism and flight path undecided; no starting frame or motion generated'
register['reviewEdits']['v37']['userAcceptedWorkingEdit']=True
register['activeReviewEdit']='v37'
save(path,register)
opening_path=PROJECT/'generated/animatic/current-opening.json'
opening=load(opening_path)
byid={s['id']:s for s in register['storyboardProposals']}
for item in opening['shots']:
    if item['id'] in ['lab2-06','lab2-07','lab2-08','lab2-09']:
        source=byid[item['id']]
        notes=source['motionReview'] if item['id']=='lab2-08' else dict(notes='Native original graphite robot laboratory ship footage. '+source['motionSelection']['reviewNotes'])
        item['review']=notes
        if item['id']!='lab2-08':
            source['motionReview']=notes
save(opening_path,opening)
save(path,register)
project_path=PROJECT/'project.json'
project=load(project_path)
assert project['production']['animatic']=='generated/animatic/A-Right-Little-Something-selected-motion-v37.mp4'
project['production']['animaticReview']='http://127.0.0.1:8768/'
project['production']['escapeSetup']['status']='User accepted approach in full V37 animatic; awaiting full-song review before departure frames/path'
project['production']['escapeSetup']['departureIntent']='Pod cut loose, dropped or ejected; follow-on trajectory to be developed from timed notes'
save(project_path,project)
print('V37 full-song edit accepted; no picture/audio re-render needed; departure design deferred for timed-note review')
