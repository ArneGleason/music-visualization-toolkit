"""Native MILES lettering follows BELLE's receding echo arcs and envelope swell."""
import json
import math
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import gaussian_filter1d
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v021'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v021.ecproj'
if target.exists():
    raise SystemExit('Preserve v021')
sr, raw = wavfile.read('/Users/arnegleason/Downloads/Let-the-Phone-Book-Sing-clean-MIDI-split-drums-leadexport 2026-11-08 1538.wav')
events = []
for f, onset in [(1372, 57.176875), (1380, 57.499125), (1390, 57.896875)]:
    env = []
    for n in range(9):
        center = round((onset + n/24)*sr)
        segment = raw[center-round(.02*sr):center+round(.02*sr)].astype(float)
        env.append(float(np.sqrt(np.mean(segment**2))))
    env = list(gaussian_filter1d(env, .65))
    env += [env[-1]*math.exp(-(j+1)/24/.20) for j in range(14)]
    events.append(dict(masterFrame=f, measuredSeconds=onset, amplitudeEnvelope=env))
peak = max(max(e['amplitudeEnvelope']) for e in events)
s = Session(BASE / 'generated/effectcraft-edit-v020/Let-the-Phone-Book-Sing-editable-v020.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    for i, e in enumerate(events):
        e['amplitudeEnvelope'] = [round(x/peak, 5) for x in e['amplitudeEnvelope']]
        # Individual native glyphs preserve BELLE's lightly irregular ink lettering;
        # they share one trajectory and never scatter or exchange reading order.
        widths = [137, 46, 92, 110, 110]
        full_width = sum(widths) + 28
        cursor = -full_width/2
        e['layers'] = []
        for j, (letter, glyph_width) in enumerate(zip('MILES', widths)):
            local_x = cursor + glyph_width/2
            cursor += glyph_width + 7
            lid = s.command('layer.newText', dict(name=f'MILES echo {i+1} / {letter}{j+1}', text=letter, font='Arial Bold Italic', size=165, fill=['#f7dda2','#9dd8cf','#f0b38b'][i], position=[0,0], justify='center'))['layer']
            e['layers'].append(lid)
            s.command('layer.style.stroke', {'layers':[lid]})
            for path,value in [('layerStyles/stroke/color','#292536'),('layerStyles/stroke/size',6)]:
                s.call('set_property', dict(layer=lid,path=path,value=value))
            f=e['masterFrame']; life=.88
            s.command('layer.timing', {'layers':[lid],'out':(f+22)/24})
            s.command('layer.timing', {'layers':[lid],'in':f/24})
            values={p:[] for p in ['position','scale','rotation','opacity']}
            for n in range(23):
                age=n/24; u=min(1,age/life); amp=e['amplitudeEnvelope'][n]
                width=310*(1-i*.15)*(1-.24*u)*(.78+.40*amp**.65)
                scale=width/full_width
                x=1490+i*70+150*u; y=600-i*180-75*math.sin(math.pi*u)-40*u
                angle=-(7-12*u); theta=math.radians(angle)
                dx=local_x*scale; dy=[12,0,8,1,12][j]*scale
                fade=max(0,min(1,age/.065,(life-age)/.27))*(.45+.55*amp**.6)
                vals=dict(position=[x+dx*math.cos(theta)-dy*math.sin(theta), y+dx*math.sin(theta)+dy*math.cos(theta),0],scale=[100*scale,100*scale,100],rotation=angle+[-5,3,-3,5,-5][j],opacity=fade*100)
                for p,v in vals.items(): values[p].append(dict(time=(f+n)/24,value=v))
            for p,v in values.items():
                s.call('add_keyframe',dict(layer=lid,path='transform/'+p,keys=v,interpolation='linear'))
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
finally:
    s.close()
(BASE/'production/miles-echo-v001.json').write_text(json.dumps(dict(status='draft_music_review',text='MILES',styleReference='belle-echo-v006',concept='Three readable whole-word receding arcs over open canal, matching BELLE palette, irregular glyph poses and measured amplitude swell. Native text, stroke and keyframes.',timingMethod='Approximate normalized stereo vocal waveform matching near expected delay intervals; quantized to24fps. Mixed vocal envelopes include overlapping lead.',events=events,nativeProject=str(target.relative_to(BASE))),indent=2)+'\n')
