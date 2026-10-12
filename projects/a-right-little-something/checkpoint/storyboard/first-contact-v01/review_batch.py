"""Build the still review using the shared gallery renderer; preserve the active edit."""
import importlib.util
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
plan = json.loads((HERE/'generation-plan.json').read_text(encoding='utf-8'))
renderer = Path('C:/Users/arneg/.codex/plugins/cache/openai-curated-remote/creative-production/0.1.25/scripts/review_renderer.py')
spec = importlib.util.spec_from_file_location('review_renderer', renderer)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
gallery = []
missing = []
for item in plan['items']:
    path = HERE/item['output']
    if not path.exists():
        missing.append(item['name'])
        continue
    with Image.open(path) as im:
        im.verify()
    start = (item['startFrame']-1)/24
    title = f"{item['id']} · {int(start)//60}:{start%60:04.1f} · {item['name'].replace('-', ' ').title()} · {item['option']}"
    saved_prompt = HERE/(item['name']+'.prompt.txt')
    retry_prompt = HERE/(item['name']+'.retry.prompt.txt')
    if retry_prompt.exists():
        saved_prompt = retry_prompt
    prompt = saved_prompt.read_text(encoding='utf-8') if saved_prompt.exists() else item['prompt']
    actual_file = HERE/(item['name']+'.actual-generation.json')
    if actual_file.exists():
        actual=json.loads(actual_file.read_text(encoding='utf-8'))
        if actual.get('attempts'):
            prompt=actual['attempts'][-1]['prompt']
    gallery.append(dict(id=item['id'],src='../'+item['output'],title=title,prompt=prompt,output=item['output'],description=item['direction'],route='built-in-imagegen'))
(HERE/'gallery-manifest.json').write_text(json.dumps(gallery,indent=2),encoding='utf-8')
options = dict(preset='detail-review',showCaptions=True,title='First contact and the wider galaxy — selected stills',output='index.html')
(HERE/'gallery-options.json').write_text(json.dumps(options,indent=2),encoding='utf-8')
out = HERE/'board'
out.mkdir(exist_ok=True)
module.build_review_html(out,gallery,options)
# Supplemental QA sheets only. The actual assets remain separate full-resolution images.
for page in range((len(gallery)+11)//12):
    group=gallery[page*12:(page+1)*12]
    sheet=Image.new('RGB',(1440,4*235),(24,28,34))
    draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(group):
        im=Image.open(HERE/item['output']).convert('RGB')
        im.thumbnail((470,200))
        x=(i%3)*480;y=(i//3)*235
        sheet.paste(im,(x,y))
        draw.text((x+5,y+202),item['title'].replace('·','|'),fill='white')
    sheet.save(HERE/f'qa-sheet-{page+1}.jpg')
report=dict(expected=len(plan['items']),present=len(gallery),missing=missing,dimensions={item['output']:list(Image.open(HERE/item['output']).size) for item in gallery},sha256={item['output']:hashlib.sha256((HERE/item['output']).read_bytes()).hexdigest() for item in gallery},frameCoverageContiguous=all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(plan['items'],plan['items'][1:])),missingReceipts=[item['name'] for item in plan['items'] if not (HERE/(item['name']+'.receipt.json')).exists()],identicalBasePromptLock=all(plan['promptLock'] in item['prompt'] for item in plan['items']))
(HERE/'still-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if not missing:
    source=PROJECT/'shots/shotlist.json'
    shotlist=json.loads(source.read_text(encoding='utf-8'))
    proposals=[p for p in shotlist.get('storyboardProposals',[]) if p.get('batch')!=plan['batch']]
    for item in plan['items']:
        proposals.append(dict(id=item['id'],batch=plan['batch'],type='storyboard',title=item['name'].replace('-',' ').title(),description=item['direction'],selectedOption=item['option'],startFrame=item['startFrame'],endFrameExclusive=item['endFrameExclusive'],frames=item['endFrameExclusive']-item['startFrame'],startSeconds=(item['startFrame']-1)/24,endSeconds=(item['endFrameExclusive']-1)/24,still='generated/storyboard/first-contact-v01/'+item['output'],promptFile='generated/storyboard/first-contact-v01/'+item['name']+'.prompt.txt',status='stills-ready-for-review'))
        proposal=proposals[-1]
        proposal['type']='concept'
        proposal['timingBasis']='Approved lyric grid boundaries and DAW beat-derived montage cuts; provisional still coverage'
        proposal['promptLock']=plan['promptLock']
        proposal['imagePrompt']=next(g['prompt'] for g in gallery if g['id']==item['id'])
        proposal['storyboardSegments']=[dict(asset=item['name'],image=proposal['still'],startFrame=item['startFrame'],endFrameExclusive=item['endFrameExclusive'],frames=proposal['frames'])]
        proposal['startingFrameDraft']=dict(id=item['id'],image=proposal['still'],userSelected=False,status='Generated draft for still review',generationMode='built-in ImageGen',nativeWidth=report['dimensions'][item['output']][0],nativeHeight=report['dimensions'][item['output']][1])
    shotlist['storyboardProposals']=proposals
    shotlist['firstContactSequence']=dict(batch=plan['batch'],status='stills-ready-for-review',selectedPath=plan['selectedPath'],plan='generated/storyboard/first-contact-v01/generation-plan.json',stillReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-v01/board/',imageCount=len(gallery),generationRoute='built-in-imagegen',activeEditUnchanged='v59',continuityNotes=['Harper remains physically aboard; planet-side appearance is a translucent projection.','Recognizable projection first appears in 8B reverse shot.','Creature anchor is a draft continuity design for review.','Instrumental montage uses DAW beat-derived frames and remains provisional until timed animatic review.'])
    source.write_text(json.dumps(shotlist,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    plan['status']='stills-ready-for-review'
    (HERE/'generation-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('dimensions','sha256')}))
