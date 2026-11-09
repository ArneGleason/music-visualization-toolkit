"""Author the shotlist as native EffectCraft layers, effects and keyframes.

Python only orchestrates EffectCraft and measures existing artwork/text. It does
not composite pixels or render video. Existing approved artwork remains intact.
"""
import hashlib
import json
import math
import os
from pathlib import Path
from PIL import Image, ImageFont
from effectcraft_session import Session, BASE

OUT = BASE / 'generated/effectcraft-edit-v001'
FPS = 24


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    score = json.loads((BASE/'shots/shotlist.json').read_text())
    timeline = BASE/'timeline.json'
    timing_hash = hashlib.sha256(timeline.read_bytes()).hexdigest()
    total = score['endFrameExclusive']
    s = Session()
    cmd = s.command
    imported = {}

    def comp(name):
        return cmd('comp.new', dict(name=name, width=1920, height=1080,
                                   frameRate=FPS, duration=total/FPS))['comp']

    def prop(lid, path, value):
        s.call('set_property', dict(layer=lid, path=path, value=value))

    def keys(lid, path, pairs, interpolation='linear'):
        s.call('add_keyframe', dict(layer=lid, path=path,
            keys=[dict(time=f/FPS, value=v) for f,v in pairs], interpolation=interpolation))

    def add(path, name):
        path = str((BASE/path).resolve())
        if path not in imported:
            imported[path] = cmd('file.import', {'paths':[path], 'sequence':False})['items'][0]
        lid = cmd('layer.addItem', {'item':imported[path], 'index':1})['layer']
        cmd('layer.rename', dict(layer=lid, name=name))
        cmd('layer.setSwitch', dict(layers=[lid], switch='audio', value=False))
        return lid

    def timing(lid, a, b):
        cmd('layer.timing', {'layers':[lid], 'in':a/FPS, 'out':b/FPS})

    def video(path, name, start, offset, rate=1):
        lid=add(path,name)
        cmd('layer.enableTimeRemap',dict(layers=[lid],value=True))
        # Explicit master-time mapping avoids trim/PTS ambiguity entirely.
        s.call('set_property',dict(layer=lid,path='timeRemap',
            expression=f'Math.max(0, (time-{start/FPS!r})*{rate!r}+{offset/FPS!r})'))
        timing(lid,0,total)
        if rate!=1:cmd('layer.frameBlending',dict(layers=[lid],mode='frameMix'))
        return lid

    def key_narrator(lid):
        s.call('add_effect',dict(layer=lid,effect='ec.key.linearcolor',
            values=dict(keyColor='#00b33f',matchColors=0,tolerance=25,softness=8)))
        cmd('layer.style.stroke',dict(layers=[lid]))
        prop(lid,'layerStyles/stroke/color','#131116')
        prop(lid,'layerStyles/stroke/size',2.5)

    sing=json.loads((BASE/'generated/motion-graphics/sing-echo-v002/analysis.json').read_text())
    belle=json.loads((BASE/'production/belle-echo-v006.json').read_text())

    def words(events, kind, plane=None):
        for i,event in enumerate(events):
            if kind=='sing':
                path=f'generated/motion-graphics/sing-echo-v002/sing-lettering-{i%3+1}.png'
                first=event['startFrame'];life=1.18
            else:
                path=f'generated/motion-graphics/belle-echo-v006/bell-lettering-{i%3+1}.png'
                first=event['masterFrame'];life=.88
            lid=add(path,f'{kind.upper()} echo {i+1}' + (f' — {plane}' if plane else ''))
            w=Image.open(BASE/path).width
            positions=[];scales=[];rotations=[];opacity=[]
            for n in range(math.ceil(life*FPS)+1):
                age=n/FPS;u=age/life
                env=event['amplitudeEnvelope'];amp=env[min(n,len(env)-1)]
                if kind=='sing':
                    side=1 if event['stereoEnergyPan']>=0 else -1
                    angle=side*math.pi/2+(1 if i%2 else -1)*math.pi*1.35*u
                    z=-math.cos(angle);depth=1/(1-.24*z)
                    width=305*depth*max(.58,1-i*.045)*(.58+.65*amp**.65)
                    x=960+625*math.sin(angle)*depth;y=570+175*z-28*math.sin(math.pi*u)
                    angle=side*9*math.cos(angle)
                    fade=max(0,min(1,age/.065,(life-age)/.26))*(.30+.70*amp**.6)
                    if (plane=='behind' and z>=0) or (plane=='front' and z<0):fade=0
                else:
                    width=310*(1-i*.15)*(1-.24*u)*(.78+.40*amp**.65)
                    x=1180+i*100+220*u;y=600-i*180-75*math.sin(math.pi*u)-40*u
                    angle=-(7-12*u)
                    fade=max(0,min(1,age/.065,(life-age)/.27))*(.45+.55*amp**.6)
                f=first+n
                positions.append((f,[x,y,0]));scales.append((f,[100*width/w]*2+[100]))
                rotations.append((f,angle));opacity.append((f,fade*100))
            timing(lid,first,first+math.ceil(life*FPS))
            for p,values in [('position',positions),('scale',scales),('rotation',rotations),('opacity',opacity)]:
                keys(lid,'transform/'+p,values,'hold' if p=='opacity' else 'linear')

    opening=comp('01 — Narrator / editable SING v002 interpretation')
    video(score['avatarInserts'][0]['backgroundVideo'],'Original street footage',0,0)
    words(sing['events'],'sing','behind')
    narrator=video(score['avatarInserts'][0]['source'],'Narrator / green key + ink outline',0,0)
    key_narrator(narrator)
    words(sing['events'],'sing','front')

    belle_comp=comp('02 — Belle / original footage + editable echoes')
    video('generated/kling-tests/belle-bell-v001/belle-original-1080p.mp4',
          'Belle / source 42–166, continuous motion',296,42,124/140)
    # Use saved masterFrame; startFrame is local to the Belle shot.
    words(belle['events'],'belle')

    chorus=comp('Chorus — temporary Hedra test / editable key')
    bgpath='generated/environment-development/old-church-quarter-v006.png'
    bg=add(bgpath,'Church quarter / original still')
    bw,bh=Image.open(BASE/bgpath).size
    prop(bg,'transform/scale',[1920/bw*100,1080/bh*100,100]);timing(bg,0,total)
    test=score['avatarInserts'][1]
    fg=video(test['source'],'Temporary watermarked Hedra test',828,test['sourceOffsetSeconds']*FPS)
    item=next(i for i in s.call('get_project')['items'] if i['id']==imported[str((BASE/test['source']).resolve())])
    prop(fg,'transform/scale',[1920/item['size'][0]*100,1080/item['size'][1]*100,100])
    key_narrator(fg)

    main=comp('MASTER — full-frame edit / 24fps / native dissolves')
    inserts=score['reviewVideoInserts']
    segments=[]
    for shot in score['shots']:
        if any(v['startFrame']<=shot['startFrame']<v['endFrameExclusive'] for v in inserts):continue
        segments.append(dict(startFrame=shot['startFrame'],endFrameExclusive=shot['endFrameExclusive'],shot=shot))
    segments+=inserts
    segments.sort(key=lambda v:v['startFrame'])
    records=[]
    for seg in segments:
        a,b=seg['startFrame'],seg['endFrameExclusive']
        if seg.get('id') in ['approved-opening','belle-continuous','chorus-test']:
            cid=opening if a==0 else (belle_comp if a==296 else chorus)
            lid=cmd('layer.addItem',dict(item=cid,index=1,time=0))['layer']
        elif 'shot' in seg:
            sh=seg['shot'];lid=add(sh['image'],sh['id']+' — '+sh['title'])
            w,h=Image.open(BASE/sh['image']).size;x0,y0,x1,y1=sh['crop']
            scale=max(1920/(w*(x1-x0)),1080/(h*(y1-y0)))
            prop(lid,'transform/anchor',[w*(x0+x1)/2,h*(y0+y1)/2,0])
            prop(lid,'transform/scale',[100*scale,100*scale,100])
        else:
            lid=video(seg['source'],seg['id'],a,seg['sourceOffsetFrames'])
        timing(lid,max(0,a-2),min(total,b+2))
        if a:keys(lid,'transform/opacity',[(a-3,0),(a-2,20),(a-1,40),(a,60),(a+1,80),(a+2,100)])
        records.append(dict(layer=lid,startFrame=a,endFrameExclusive=b))
        cmd('comp.addMarker',dict(time=a/FPS,comment=seg.get('id') or seg['shot']['id']))
    audio=add('generated/source/master.wav','MASTER AUDIO — approved original')
    cmd('layer.setSwitch',dict(layers=[audio],switch='audio',value=True));timing(audio,0,total)

    review=comp('REVIEW — removable lyric overlay')
    cmd('layer.addItem',dict(item=main,index=1,time=0))
    lines=next(t['items'] for t in json.loads(timeline.read_text())['tracks'] if t['id']=='lyrics')
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',34)
    for li,line in enumerate(lines):
        words_=line['words'];a=max(0,words_[0]['startFrame']-6)
        b=min(total,words_[-1]['endFrameExclusive']+8)
        if li+1<len(lines):b=min(b,max(0,lines[li+1]['words'][0]['startFrame']-6))
        widths=[font.getlength(w['text']) for w in words_];gap=font.getlength(' ')
        x=(1920-sum(widths)-gap*(len(widths)-1))/2
        for word,width in zip(words_,widths):
            lid=cmd('layer.newText',dict(name='Lyric — '+word['text'],text=word['text'],
                font='Arial',size=34,fill='#d5d5d5',position=[x,1035],justify='left'))['layer']
            timing(lid,a,b)
            cmd('layer.style.stroke',dict(layers=[lid]))
            prop(lid,'layerStyles/stroke/color','#141118');prop(lid,'layerStyles/stroke/size',2)
            cmd('layer.addTextAnimator',dict(layer=lid,properties=['fillColor'],name='Approved word timing'))
            keys(lid,'text/animators/animator/properties/fillColor',[(a,'#d5d5d5'),(word['startFrame'],'#ffd46b'),(word['endFrameExclusive'],'#ffffff')],'hold')
            x+=width+gap
    cmd('layer.select',dict(layers=[]));cmd('time.set',dict(time=0))
    cmd('comp.workArea',dict(start=0,end=740/FPS))
    target=OUT/'Let-the-Phone-Book-Sing-editable-v001.ecproj'
    s.call('save_project',dict(path=str(target)))
    report=dict(project=str(target.relative_to(BASE)),mainComp=main,reviewComp=review,
        openingComp=opening,belleComp=belle_comp,segments=records,timelineSha256=timing_hash,
        status='native migration draft; render verification pending',
        native=['picture edit','four-frame opacity dissolves','source time remapping','green key','ink stroke','SING and BELLE transforms and measured envelope keys','lyric text'],
        limitations=['Chorus rebuilt from original temporary watermarked Hedra test; its lower-resolution source remains temporary.',
            'Native key and uniform 2.5px stroke require visual approval against the approved custom matte.',
            'SING depth uses paired front/behind layers, preserving whole-word readability.'])
    (OUT/'migration-report.json').write_text(json.dumps(report,indent=2)+'\n')
    assert hashlib.sha256(timeline.read_bytes()).hexdigest()==timing_hash
    for f in [112,310,436,437,600]:
        s.call('render_frame',dict(comp=review,time=f/FPS,path=str(OUT/f'check-{f}.png'),inline=False,max_side=960))
    s.close()
    # Footage links remain portable within the project media tree.
    def relative(value):
        if isinstance(value, str) and value.startswith(str(BASE)+'/') and Path(value).is_file():
            return os.path.relpath(value, OUT)
        if isinstance(value, dict):
            return {k: relative(v) for k,v in value.items()}
        if isinstance(value, list):
            return [relative(v) for v in value]
        return value
    target.write_text(json.dumps(relative(json.loads(target.read_text())), ensure_ascii=False)+'\n')
    print(target)

if __name__=='__main__':build()
