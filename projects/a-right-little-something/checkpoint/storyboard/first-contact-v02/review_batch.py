"""Review five revised stills in context; leave accepted motion edit intact."""
import hashlib
import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'first-contact-v01'
PROJECT=HERE.parents[2]
CHANGED={4:'Replace double planet with a small flat terrain control; no real planet in this insert.',7:'Medium interior framing with Harper clearly in front of the far dome boundary.',11:'Cool low-angle side profile against open sky, contrasting with frame 10.',13:'Creature POV across its home valley, interrupting the repeated conversation framing.',26:'Close rear-over-shoulder inside the sphere; exclude ambiguous full-body rail geometry.'}
ACCEPTED=[1,2,3,5,6,8,9,*range(16,26),*range(27,33)]
plan=json.loads((BASE/'generation-plan.json').read_text(encoding='utf-8'))
oldgallery=json.loads((BASE/'gallery-manifest.json').read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('review_renderer',Path('C:/Users/arneg/.codex/plugins/cache/openai-curated-remote/creative-production/0.1.25/scripts/review_renderer.py'))
renderer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
gallery=[]
comparison=[]
missing=[]
for n,(item,old) in enumerate(zip(plan['items'],oldgallery),1):
    folder=HERE if n in CHANGED else BASE
    image=folder/item['output']
    if not image.exists():
        missing.append(item['name'])
        continue
    with Image.open(image) as im:
        im.verify()
    entry=dict(old)
    entry['src']=('../' if n in CHANGED else '../../first-contact-v01/')+item['output']
    if n in CHANGED:
        entry['title']+=' — revised'
        entry['description']=CHANGED[n]
        prompt=folder/(item['name']+'.prompt.txt')
        if prompt.exists():
            entry['prompt']=prompt.read_text(encoding='utf-8')
        actual=folder/(item['name']+'.actual-generation.json')
        if actual.exists():
            data=json.loads(actual.read_text(encoding='utf-8'))
            if data.get('attempts'):
                entry['prompt']=data['attempts'][-1]['prompt']
        previous=dict(old,src='../../first-contact-v01/'+item['output'],title=old['title']+' — previous')
        comparison.extend([previous,entry])
    gallery.append(entry)
    item['image']=image.relative_to(PROJECT).as_posix()
    item['reviewStatus']='revision-for-review' if n in CHANGED else ('user-approved' if n in ACCEPTED else 'retained')
    if n in CHANGED:
        item['direction']=CHANGED[n]
        item['prompt']=entry['prompt']
plan.update(batch='first-contact-v02',sourceBatch='first-contact-v01',status='revisions-ready-for-review' if not missing else 'revisions-in-progress',revisedGalleryNumbers=list(CHANGED),userApprovedGalleryNumbers=ACCEPTED)
(HERE/'generation-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
options=dict(preset='detail-review',showCaptions=True,title='First contact — revised shots 4, 7, 11, 13 and 26',output='index.html')
(HERE/'gallery-options.json').write_text(json.dumps(options,indent=2),encoding='utf-8')
(HERE/'gallery-manifest.json').write_text(json.dumps(gallery,indent=2),encoding='utf-8')
(HERE/'review-manifest.json').write_text(json.dumps(comparison,indent=2),encoding='utf-8')
for name,entries in [('board',gallery),('compare',comparison)]:
    out=HERE/name;out.mkdir(exist_ok=True)
    renderer.build_review_html(out,entries,options)
# Small QA sheet presents previous/revised pairs; never replaces actual frames.
sheet=Image.new('RGB',(960,5*290),(24,28,34));draw=ImageDraw.Draw(sheet)
for i,entry in enumerate(comparison):
    path=(HERE/'compare'/entry['src']).resolve()
    im=Image.open(path).convert('RGB');im.thumbnail((470,264))
    x=(i%2)*480;y=(i//2)*290;sheet.paste(im,(x,y))
    draw.text((x+4,y+266),entry['title'].replace('—','-').replace('·','|'),fill='white')
sheet.save(HERE/'revision-qa.jpg')
report=dict(expectedRevisions=5,presentRevisions=len(comparison)//2,missing=missing,totalGalleryImages=len(gallery),approvedFilesPreserved=all(hashlib.sha256((BASE/plan['items'][n-1]['output']).read_bytes()).hexdigest()==json.loads((BASE/'still-validation.json').read_text(encoding='utf-8'))['sha256'][plan['items'][n-1]['output']] for n in ACCEPTED))
(HERE/'still-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if not missing:
    source=PROJECT/'shots/shotlist.json'
    shots=json.loads(source.read_text(encoding='utf-8'))
    for proposal in shots['storyboardProposals']:
        if proposal.get('batch')!='first-contact-v01':continue
        n=int(proposal['id'].split('-')[-1]);item=plan['items'][n-1]
        if n in ACCEPTED:
            proposal['status']='User-approved still'
            proposal['startingFrameSelection']=dict(proposal['startingFrameDraft'],userSelected=True,status='User-approved still')
        if n in CHANGED:
            if proposal.get('stillRevision')!='first-contact-v02':
                proposal.setdefault('stillHistory',[]).append(dict(proposal['startingFrameDraft']))
            proposal.update(still=item['image'],description=item['direction'],imagePrompt=item['prompt'],stillRevision='first-contact-v02',status='Revised still for review',promptFile='generated/storyboard/first-contact-v02/'+item['name']+'.prompt.txt')
            proposal['storyboardSegments'][0]['image']=item['image']
            w,h=Image.open(PROJECT/item['image']).size
            proposal['startingFrameDraft']=dict(id=item['id']+'-v02',image=item['image'],userSelected=False,status='Revised still for review',generationMode='built-in ImageGen',nativeWidth=w,nativeHeight=h)
    shots['firstContactSequence'].update(currentStillRevision='first-contact-v02',status='Five revised stills ready for review',stillReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-v02/board/',comparisonUrl='http://127.0.0.1:8768/storyboard/first-contact-v02/compare/',plan='generated/storyboard/first-contact-v02/generation-plan.json',userApprovedGalleryNumbers=ACCEPTED,revisedGalleryNumbers=list(CHANGED))
    source.write_text(json.dumps(shots,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report))
