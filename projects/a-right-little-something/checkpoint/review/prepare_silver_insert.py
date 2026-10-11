import copy
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/lab-silver-v01'
direction=(out/'silver-direction.txt').read_text(encoding='utf-8')
lock=next(line for line in direction.splitlines() if line.startswith('PROMPT LOCK:'))
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-motion-v01']
assert len(shots)==9
register.setdefault('supersededStoryboardProposals',[]).extend(copy.deepcopy(shots))
for shot in shots:
    ident=shot['id']
    shot['batch']='lab-silver-v01'
    shot['promptLock']=lock
    if ident <= 'lab2-05':
        image=out/(ident+'.png')
        assert image.stat().st_size>0
        shot.setdefault('directionHistory',[]).append(dict(version='v28',image=shot['startingFrameDraft']['image'],imagePrompt=shot.get('imagePrompt','')))
        shot['startingFrameDraft']=dict(id=ident+'-silver-v01',image=image.relative_to(base).as_posix(),
            userSelected=False,status='Silver bikini wardrobe draft',generationMode='built-in ImageGen edit')
        shot['status']='Silver wardrobe draft for animatic review'
        shot['sourceDirection']+=' User revised wardrobe to opaque silver bikini following Kling tank-content rejection; preserve sealed upper chamber and internal hand/interface.'
        prompt=load(out/(ident+'.prompt.json'))['prompt']
        assert lock in prompt
        shot['imagePrompt']=prompt
    else:
        shutil.copy2(base/'generated/storyboard/lab-motion-v01'/(ident+'.mp4'),out/(ident+'.mp4'))
save(base/'shots/shotlist.json',register)
spec=load(base/'storyboard-lab-motion-v01.json')
spec.update(id='lab-silver-v01',output='generated/storyboard/lab-silver-v01',draftForReview=True,
    mediaLabel='Kling / Blender / four native ark shots / silver bikini lab drafts',
    status='Five silver bikini wardrobe still drafts plus four native ark clips',
    continuationNotes='V29 preserves v28 schematic dissolve and exact grid/master, adds four completed native ark takes and five wardrobe-revised lab stills with silver bikini. All hand/interface actions stay sealed inside at head level. Five lab native takes are next, within original approved432credit total; new images must be reviewed before upload. Exterior star pan provides a ship-free visual interlude near the bright-night ending.',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-silver-v01/animatic-through-bright-night.mp4')
save(base/'storyboard-lab-silver-v01.json',spec)
print('Prepared silver wardrobe stills and native exterior assembly')
