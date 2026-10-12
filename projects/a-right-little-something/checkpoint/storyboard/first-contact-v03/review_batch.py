"""Revised cabin stills and an alternating travel finale with separate end plates."""
import hashlib
import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
BASE=HERE.parent/'first-contact-v02'
REVISED={4,7,9,26}
plan=json.loads((BASE/'generation-plan.json').read_text(encoding='utf-8'))
oldgallery=json.loads((BASE/'gallery-manifest.json').read_text(encoding='utf-8'))
beats=json.loads((PROJECT/'generated/beatmap.json').read_text(encoding='utf-8'))
beatframes=sorted({round(t*24)+1 for bar in beats['bars'] for t in bar['beats']})
spec=importlib.util.spec_from_file_location('review_renderer',Path('C:/Users/arneg/.codex/plugins/cache/openai-curated-remote/creative-production/0.1.25/scripts/review_renderer.py'))
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
gallery=[];changes=[];items=[];missing=[]

def prompt_for(name,fallback=''):
    actual=HERE/(name+'.actual-generation.json')
    if actual.exists():
        data=json.loads(actual.read_text(encoding='utf-8'))
        if data.get('attempts'):return data['attempts'][-1]['prompt']
        if data.get('prompt'):return data['prompt']
    retry=HERE/(name+'.retry.prompt.txt')
    path=retry if retry.exists() else HERE/(name+'.prompt.txt')
    return path.read_text(encoding='utf-8') if path.exists() else fallback

def add(item,index,title,revised=False):
    path=PROJECT/item['image']
    if not path.exists():
        missing.append(item['name']);return
    with Image.open(path) as im:im.verify()
    start=(item['startFrame']-1)/24
    entry=dict(id=item['id'],index=index,src='../../'+path.parent.name+'/'+path.name,title=f"{title} · {int(start)//60}:{start%60:04.1f}"+(' · revised' if revised else ''),prompt=item.get('prompt',''),output=path.name,route='built-in-imagegen')
    gallery.append(entry)
    if revised:changes.append(entry)

for n,(item,old) in enumerate(zip(plan['items'],oldgallery),1):
    item=dict(item);item['galleryIndex']=n
    if n in REVISED:
        item['image']='generated/storyboard/first-contact-v03/'+item['output']
        item['prompt']=prompt_for(item['name'],item['prompt'])
        item['reviewStatus']='revision-for-review'
    if 27<=n<=31:
        original_end=item['endFrameExclusive']
        available=[f for f in beatframes if item['startFrame']<f<original_end]
        transition_start=available[-2]
        item['endFrameExclusive']=transition_start
        transition=dict(id=f'contact-{n:03d}-travel',name=f'travel-{n}',galleryIndex=f'{n}T',option='ending A travel bridge',startFrame=transition_start,endFrameExclusive=original_end,image=f'generated/storyboard/first-contact-v03/travel-{n}.png',prompt=prompt_for(f'travel-{n}'),reviewStatus='new-for-review')
    items.append(item)
    title=item['name'].replace('-',' ').title()
    if n==32:title='Finale — cosmic background plate'
    add(item,n,title,n in REVISED)
    if 27<=n<=31:
        items.append(transition)
        travel_titles={27:'Warp toward the binary suns',28:'Flight into the stellar nursery',29:'Emerging toward the red star',30:'Crossing toward the galactic view',31:'Approaching the next destination'}
        add(transition,f'{n}T',travel_titles[n],True)

final=items[-1]
portrait=dict(id='contact-032-portrait',name='ending-harper-portrait',galleryIndex='32P',image='generated/storyboard/first-contact-v03/ending-harper-portrait.png',prompt=prompt_for('ending-harper-portrait'),startFrame=final['startFrame'],endFrameExclusive=final['endFrameExclusive'],role='concurrent portrait source plate, not an additional sequential shot')
add(portrait,'32P','Finale — separate Harper portrait plate',True)
plan.update(batch='first-contact-v03',sourceBatch='first-contact-v02',items=items,auxiliaryPlates=[portrait],status='ready-for-review' if not missing else 'in-progress',revisedGalleryNumbers=sorted(REVISED),travelInserts=[f'{n}T' for n in range(27,32)],numberingNote='Original contact-sheet indices 1–32 stay fixed. T denotes an inserted travel shot; 32P is a concurrent source plate for shot 32, not the next shot.')
(HERE/'generation-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
assembly=dict(status='still review; future separate video generation and Blender compositing',fps=24,frameConvention='one-based half-open',endingTimeline=[dict(id=i['id'],galleryIndex=i['galleryIndex'],image=i['image'],startFrame=i['startFrame'],endFrameExclusive=i['endFrameExclusive'],frames=i['endFrameExclusive']-i['startFrame']) for i in items if i['startFrame']>=4446],finale=dict(startFrame=final['startFrame'],endFrameExclusive=final['endFrameExclusive'],frames=final['endFrameExclusive']-final['startFrame'],videoInputs=[dict(id='cosmic-background',still=final['image'],direction='Slow forward cosmic drift toward the light. No Harper, portrait, face or double exposure.'),dict(id='harper-portrait',still=portrait['image'],direction='Harper close-up with subtle breath, eye movement and quiet awe. Keep near-black background clean. No cosmic scenery or double exposure.')],separateVideoGenerations=True,compositingApplication='Blender',compositingDirection='Animate both clean inputs separately, trim to the same exact frame range, then layer Harper over the cosmic plate with a controlled matte and opacity. Adjust framing, blend and fade in Blender. Never bake the superimposition into either still or ask Kling to generate the composite.',generatedCompositeStill=False))
(HERE/'assembly-plan.json').write_text(json.dumps(assembly,indent=2),encoding='utf-8')
options=dict(preset='detail-review',showCaptions=True,title='First contact — hexagonal cabin and travelling finale',output='index.html')
(HERE/'gallery-options.json').write_text(json.dumps(options,indent=2),encoding='utf-8')
for filename,data in [('gallery-manifest.json',gallery),('review-manifest.json',changes)]:
    (HERE/filename).write_text(json.dumps(data,indent=2),encoding='utf-8')
ending_gallery=[e for e in gallery if int(str(e['index']).rstrip('TP'))>=26]
for folder,data in [('board',gallery),('changes',changes),('ending',ending_gallery)]:
    dest=HERE/folder;dest.mkdir(exist_ok=True);renderer.build_review_html(dest,data,options)
sheet=Image.new('RGB',(1440,4*290),(24,28,34));draw=ImageDraw.Draw(sheet)
for j,e in enumerate(changes):
    path=(HERE/'changes'/e['src']).resolve();im=Image.open(path).convert('RGB');im.thumbnail((470,264));x=(j%3)*480;y=(j//3)*290;sheet.paste(im,(x,y));draw.text((x+4,y+266),str(e['index'])+' '+e['title'].replace('·','|'),fill='white')
sheet.save(HERE/'revision-qa.jpg')
source_checks=json.loads((HERE.parent/'first-contact-v01/still-validation.json').read_text(encoding='utf-8'))['sha256']
originals_preserved=all(hashlib.sha256((HERE.parent/'first-contact-v01'/name).read_bytes()).hexdigest()==digest for name,digest in source_checks.items())
report=dict(expectedNewImages=10,presentNewImages=len(changes),missing=missing,totalGalleryImages=len(gallery),timelineContiguous=all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(items,items[1:])),separateFinalePlates=True,originalStillsPreserved=originals_preserved)
(HERE/'still-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if not missing:
    source=PROJECT/'shots/shotlist.json';shots=json.loads(source.read_text(encoding='utf-8'))
    existing={p['id']:p for p in shots['storyboardProposals']}
    for item in items:
        pid=item['id'];index=item['galleryIndex']
        if index not in REVISED and not isinstance(index,str) and not 27<=index<=32:continue
        p=existing.get(pid)
        if p is None:
            p=dict(id=pid,batch='first-contact-v01',type='concept',selectedOption='ending A travel bridge');shots['storyboardProposals'].append(p)
        elif p.get('stillRevision')!='first-contact-v03' and 'startingFrameDraft' in p:
            p.setdefault('stillHistory',[]).append(dict(p['startingFrameDraft']))
        p.update(title=item['name'].replace('-',' ').title(),galleryIndex=index,startFrame=item['startFrame'],endFrameExclusive=item['endFrameExclusive'],frames=item['endFrameExclusive']-item['startFrame'],startSeconds=(item['startFrame']-1)/24,endSeconds=(item['endFrameExclusive']-1)/24,still=item['image'],status='V03 still and travel edit for review')
        p['storyboardSegments']=[dict(asset=item['name'],image=item['image'],startFrame=item['startFrame'],endFrameExclusive=item['endFrameExclusive'],frames=p['frames'])]
        if index in REVISED or isinstance(index,str):
            w,h=Image.open(PROJECT/item['image']).size
            p.update(stillRevision='first-contact-v03',imagePrompt=item['prompt'],promptLock=plan['promptLock'],promptFile=f"generated/storyboard/first-contact-v03/{item['name']}.prompt.txt",startingFrameDraft=dict(id=pid+'-v03',image=item['image'],userSelected=False,status='Revised still for review',generationMode='built-in ImageGen',nativeWidth=w,nativeHeight=h))
        if index==32:p['compositePlan']=assembly['finale']
    shots['firstContactSequence'].update(currentStillRevision='first-contact-v03',status='Revised cabin and travelling finale ready for review',stillReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-v03/board/',changesUrl='http://127.0.0.1:8768/storyboard/first-contact-v03/changes/',endingReviewUrl='http://127.0.0.1:8768/storyboard/first-contact-v03/ending/',plan='generated/storyboard/first-contact-v03/generation-plan.json',assemblyPlan='generated/storyboard/first-contact-v03/assembly-plan.json',revisedGalleryNumbers=sorted(REVISED),travelInsertIds=[i['id'] for i in items if isinstance(i['galleryIndex'],str)],finaleSeparateVideoPlates=True,imageCount=len(gallery),timelineShotCount=len(items))
    source.write_text(json.dumps(shots,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report))
