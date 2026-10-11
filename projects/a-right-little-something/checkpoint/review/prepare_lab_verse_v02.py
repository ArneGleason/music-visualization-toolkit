import copy
import json
from pathlib import Path
import shutil

base = Path('projects/a-right-little-something')
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

old = base/'generated/storyboard/lab-verse-v01'
out = base/'generated/storyboard/lab-verse-v02'
out.mkdir(exist_ok=True)
register = load(base/'shots/shotlist.json')
shots = [s for s in register['storyboardProposals'] if s.get('batch')=='lab-verse-v01']
assert len(shots)==9
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
for shot in shots:
    ident = shot['id']
    shot['batch'] = 'lab-verse-v02'
    shot['directionHistory'] = shot.get('directionHistory',[]) + [dict(
        version='v26',description=shot['description'],motionDirection=shot['motionDirection'],
        image=shot['startingFrameDraft']['image'],imagePrompt=shot.get('imagePrompt',''))]
    if ident in ('lab2-03','lab2-04'):
        shot['startingFrameDraft'] = dict(id=ident+'-v02',
            image=f'generated/storyboard/lab-verse-v02/{ident}.png',
            userSelected=False,status='Revised internal-interface draft',generationMode='built-in ImageGen')
        shot['status'] = 'Revised draft awaiting animatic review'
        shot['sourceDirection'] += ' Latest user correction: all human hands and virtual calculations inside sealed upper chamber, at head level; no hand portal.'
    else:
        shot['startingFrameDraft'].update(userSelected=True,status='User accepted v26 still')
        shutil.copy2(old/(ident+'.mp4'),out/(ident+'.mp4'))
    if ident=='lab2-03':
        shot['description']='Outside the sealed tank, a caretaker operates its side control. Harper raises one hand beside her face inside culture fluid; an internal cyan lattice responds with an irregular warm branching pulse.'
        shot['motionDirection']='Robot tool depresses exterior control; Harper raises fingers inside the upper chamber, disrupting the internal constraint lattice. Preserve uninterrupted glass and fluid across hand and face; no human limb crosses the wall.'
    if ident=='lab2-04':
        shot['description']='Head-level close detail through uninterrupted tank glass: her submerged fingers pinch and rotate a cyan/violet geometric calculation floating INSIDE the chamber; her face is soft behind it.'
        shot['motionDirection']='Index and thumb rotate one suspended calculation ring, then align a node inside the fluid. Keep hand, forearm and all virtual elements behind sealed chamber glass; no cuff, hole or portal.'
    shot['generationApproach']=shot['motionDirection']+' Later native animation requires 24 source frames each side and animatic review first.'
save(base/'shots/shotlist.json',register)
spec = load(base/'storyboard-lab-verse-v01.json')
spec.update(id='lab-verse-v02',output='generated/storyboard/lab-verse-v02',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v26.mp4',
    status='V27 preparation; revised stills pending',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-verse-v02/animatic-through-bright-night.mp4',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/lab-verse-v02/review-board.html',
    continuationNotes='V27 retains v26 timing, accepted ark and seven unchanged stills, replaces only constraint and finger-calculation views with hand/interface inside sealed chamber at head level. Draft revised images await review. Original master audio and full5265frames preserved.')
save(base/'storyboard-lab-verse-v02.json',spec)
for name in ('lab2-01.prompt.json','lab2-02-prompt.json','lab2-05-prompt.txt','space-stills-prompts.json'):
    shutil.copy2(old/name,out/name)
helper = (base/'generated/review/finish_lab_verse.py').read_text(encoding='utf-8')
helper=helper.replace("lab-verse-v01","lab-verse-v02").replace("v26","v27").replace("v25","v26")
helper=helper.replace("src=image.name,href=image.name", "src=Path(__import__('os').path.relpath(image,out)).as_posix(),href=Path(__import__('os').path.relpath(image,out)).as_posix()")
helper=helper.replace("User: pretty good; accepted orbit revision and requested headquarters-origin verse continuation.",
    "User liked lab verse and submarine-like ark; requested hand/interface inside sealed tank on shots03/04, rest accepted.")
# Preserve approval on seven reused stills; new compositions remain draft.
helper=helper.replace("register['reviewEdits']['v26']['userReview']", "\nfor shot in register['storyboardProposals']:\n    if shot.get('batch')=='lab-verse-v02' and shot['id'] not in ('lab2-03','lab2-04'):\n        for key in ('startingFrameDraft','startingFrameSelection','animaticPlacement'):\n            shot[key]['userSelected']=True\n        shot['status']='User accepted v26 still, retained in v27'\nregister['reviewEdits']['v26']['userReview']")
(base/'generated/review/finish_lab_verse_v02.py').write_text(helper,encoding='utf-8')
print('Prepared v27; seven unchanged camera chunks retained')
