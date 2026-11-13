"""Native grayscale adjustment with accumulating circular color reveals."""
import json
import math
import subprocess
from effectcraft_session import Session, BASE, CLI

OUT = BASE/'generated/effectcraft-edit-v045'
OUT.mkdir(parents=True, exist_ok=True)
TARGET = OUT/'Let-the-Phone-Book-Sing-editable-v045.ecproj'
if TARGET.exists():
    raise SystemExit('Preserve existing v045')
# Opening master transients, rounded to the established 24fps frame grid.
HITS = [(11,(370,330),290),(13,(1510,700),330),
        (14,(1410,250),300),(16,(520,850),350),(32,(960,540),1200)]

def circle(center,radius):
    return {'t':'Path','v':{'closed':True,
        'vertices':[[center[0]+radius*math.cos(i*math.tau/128),
                     center[1]+radius*math.sin(i*math.tau/128)] for i in range(128)],
        'in_tangents':[[0,0]]*128,'out_tangents':[[0,0]]*128}}

s=Session(BASE/'generated/effectcraft-edit-v043/Let-the-Phone-Book-Sing-editable-v043.ecproj')
try:
    s.command('comp.open',{'comp':675})
    layer=s.command('layer.newAdjustment',{'name':'INTRO — drum-hit color reveal / five circular impacts'})['layer']
    s.command('layer.timing',{'layers':[layer],'in':0,'out':35/24})
    s.call('add_effect',{'layer':layer,'effect':'ec.color.huesaturation','values':{'saturation':-100}})
    s.command('mask.new',{'layer':layer,'vertices':[[-10,-10],[1930,-10],[1930,1090],[-10,1090]],'closed':True,'mode':'Add'})
    for n,(frame,center,radius) in enumerate(HITS,2):
        initial=radius*.44 if n<6 else 340
        s.command('mask.new',{'layer':layer,'vertices':circle(center,initial)['v']['vertices'],'closed':True,'mode':'Subtract'})
        path=f'masks/#{n}'
        s.call('set_property',{'layer':layer,'path':path+'/feather','value':[1.5,1.5]})
        s.call('add_keyframe',{'layer':layer,'path':path+'/opacity','keys':[
            {'time':0,'value':0},{'time':(frame-1)/24,'value':0},{'time':frame/24,'value':100}], 'interpolation':'hold'})
        s.call('add_keyframe',{'layer':layer,'path':path+'/path','keys':[
            {'time':frame/24,'value':circle(center,initial)},
            {'time':(frame+2)/24,'value':circle(center,radius)}],'interpolation':'linear'})
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(TARGET)})
    for frame in [26,31,32,33,34]:
        s.call('render_frame',{'comp':1554,'time':frame/24,'path':str(OUT/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
for name,end in [('intro-color-reveal-review.mp4',8),('animatic-through-pine-price-1080p.mp4',2451/24)]:
    subprocess.run([str(CLI),'render','--project',str(TARGET),'--gpu','--comp','1554','--start','0','--end',str(end),'--out',str(OUT/name),'--format','h264','--bitrate','10000','--audio','on'],check=True)
(BASE/'production/intro-color-reveal-v002.json').write_text(json.dumps({
    'status':'pending_user_review','nativeProject':str(TARGET.relative_to(BASE)),
    'fallback':'v043','layer':layer,'hitFrames':[h[0] for h in HITS],
    'fps':24,'expansionFrames':2,'fullColorFrame':34,
    'timingEvidence':'First four reveals unchanged; final reveal moved from frame24 to frame32 (1.333s), next strong kick attack, per user review. Full color frame34.',
    'method':'Native Hue/Saturation adjustment, full-frame Add mask and five animated Subtract circle masks. Color accumulates; no generated media or baked compositing.'},indent=2)+'\n')
