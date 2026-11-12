"""Native background refraction on Chorus 1's opening O; clean singer retained."""
import json
from effectcraft_session import Session, BASE

out = BASE/'generated/effectcraft-edit-v026'
out.mkdir(parents=True, exist_ok=True)
target = out/'Let-the-Phone-Book-Sing-editable-v026.ecproj'
if target.exists():
    raise SystemExit('Preserve v026')
s = Session(BASE/'generated/effectcraft-edit-v024/Let-the-Phone-Book-Sing-editable-v024.ecproj')
try:
    s.command('comp.open', {'comp':17396})
    layer = s.command('layer.newAdjustment', {'name':'Opening O — air-pressure ripples'})['layer']
    s.command('layer.arrange', {'layers':[layer], 'to':'backward'})
    fx = s.call('add_effect', {'layer':layer, 'effect':'Ripple', 'values':{
        'center':[.5,.395], 'conversion':1, 'speed':0,
        'waveWidth':180, 'waveHeight':0, 'radius':0, 'phase':0,
    }})['path']
    def keys(param, values):
        s.call('add_keyframe', {'layer':layer,'path':fx+'/'+param,
            'keys':[{'time':f/24,'value':v} for f,v in values], 'interpolation':'linear'})
    # Sound starts before the scene fade. Reveal an already expanding pressure field.
    keys('radius',[(821,0),(826,13),(834,38),(842,66),(850,90),(858,100)])
    keys('waveHeight',[(821,0),(826,3),(830,8),(836,10),(842,8),(848,5),(854,2),(858,0),(1098,0)])
    keys('phase',[(821,0),(858,-740)])
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
    for f in [832,840,850,860]:
        s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
(BASE/'production/chorus-o-ripple-v001.json').write_text(json.dumps({
    'status':'experimental_pending_user_review','shot':'PB-011','nativeProject':str(target.relative_to(BASE)),
    'cleanFallback':'generated/effectcraft-edit-v024/Let-the-Phone-Book-Sing-editable-v024.ecproj',
    'effect':'Native Ripple adjustment below singer in comp17396; source remap isolated',
    'frames':[821,858],'mouthCenterNormalized':[.5,.395], 'waveWidth':180,'peakWaveHeight':10,
    'intent':'Expanding air-pressure refraction behind narrator on opening O; no visible drawn rings. Approximate vocal swell with manual frame-based envelope; musical edit unchanged.',
},indent=2)+'\n')
