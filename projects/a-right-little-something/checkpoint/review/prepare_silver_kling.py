from pathlib import Path
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
old=load(base/'kling-lab-motion-v01.json')
direction=(base/'generated/storyboard/lab-silver-v01/silver-direction.txt').read_text(encoding='utf-8')
lock=next(line for line in direction.splitlines() if line.startswith('PROMPT LOCK:'))
plan=dict(status='Five silver bikini lab takes prepared; revised wardrobe animatic review required before upload',
    fps=24,output='generated/kling-tests/lab-silver-motion-v01',reviewOutput='generated/storyboard/lab-silver-motion-v01',
    estimatedCredits=240,approvedOriginalBatchMaximum=432,priorExteriorCredits=192,
    authorization='User approved nine uploads and432credits, then directed silver bikini wardrobe after first tank request rejection. Revised five image/prompt payloads are prepared for review.',
    shots=[])
shared=' One uninterrupted six-second illustrated laboratory shot. Preserve the exact adult face and opaque silver swimwear shown in the revised starting frame, with secure unchanged silver straps and top. Preserve existing modest framing and opaque lower tank armor. The chamber stays sealed: all human hands, forearms and virtual calculations remain inside the fluid behind continuous glass. Robot machinery and physical controls remain outside. Motion starts immediately and continues throughout for a central editorial trim. No cuts, internal fades, talking, shake, zoom blur, added people, captions, logos, watermark, added body exposure or generated audio. Match the exact painterly graphic-novel finish. Locked native camera; the planned editorial pan will be added afterwards.'
for item in old['shots'][:5]:
    shot=dict(item)
    ident=item['shotId']
    shot['id']=ident+'-silver-motion-v01'
    shot['firstImage']='generated/storyboard/lab-silver-v01/'+ident+'.png'
    assert (base/shot['firstImage']).stat().st_size>0
    action=item['prompt'].split(' One uninterrupted six-second shot,',1)[0]
    shot['prompt']=action+shared+'\n\n'+lock
    plan['shots'].append(shot)
assert len({s['prompt'].split('PROMPT LOCK:',1)[1] for s in plan['shots']})==1
save(base/'kling-lab-silver-motion-v01.json',plan)
print('Prepared five revised swimsuit lab uploads,240credits; original432cap including192exteriors.')
