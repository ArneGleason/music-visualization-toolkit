"""Native background refraction on Chorus 1's opening O; clean singer retained."""
import json
from effectcraft_session import Session, BASE

out = BASE/'generated/effectcraft-edit-v028'
out.mkdir(parents=True, exist_ok=True)
target = out/'Let-the-Phone-Book-Sing-editable-v028.ecproj'
if target.exists():
    raise SystemExit('Preserve v028')
s = Session(BASE/'generated/effectcraft-edit-v024/Let-the-Phone-Book-Sing-editable-v024.ecproj')
try:
    s.command('comp.open', {'comp':17396})
    layer = s.command('layer.newAdjustment', {'name':'Opening O — air-pressure ripples'})['layer']
    s.command('layer.arrange', {'layers':[layer], 'to':'backward'})
    fx = s.call('add_effect', {'layer':layer, 'effect':'Ripple', 'values':{
        'center':[960,426], 'conversion':1, 'speed':0,
        'waveWidth':220, 'waveHeight':0, 'radius':0, 'phase':0,
    }})['path']
    def keys(param, values):
        s.call('add_keyframe', {'layer':layer,'path':fx+'/'+param,
            'keys':[{'time':f/24,'value':v} for f,v in values], 'interpolation':'linear'})
    # Sound starts before the scene fade. Reveal an already expanding pressure field.
    keys('radius',[(821,100),(870,100)])
    keys('waveHeight',[(821,0),(826,8),(830,20),(836,24),(844,20),(852,12),(860,5),(870,0),(1098,0)])
    keys('phase',[(821,0),(870,-1080)])
    # Feather away displacement at the frame edges to retain the original plate.
    s.command('mask.new', {'layer':layer, 'vertices':[[60,60],[1860,60],[1860,1020],[60,1020]], 'closed':True})
    s.call('set_property', {'layer':layer,'path':'masks/mask/feather','value':[90,90]})
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
    for f in [832,840,850,870]:
        s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
(BASE/'production/chorus-o-ripple-v003.json').write_text(json.dumps({
    'status':'experimental_pending_user_review','shot':'PB-011','nativeProject':str(target.relative_to(BASE)),
    'cleanFallback':'generated/effectcraft-edit-v024/Let-the-Phone-Book-Sing-editable-v024.ecproj',
    'effect':'Native Ripple adjustment below singer in comp17396; source remap isolated',
    'frames':[821,870],'mouthCenterPixels':[960,426], 'waveWidth':220,'peakWaveHeight':24,
    'intent':'Expanding air-pressure refraction behind narrator on opening O; no visible drawn rings. Approximate vocal swell with manual frame-based envelope; musical edit unchanged.',
},indent=2)+'\n')
