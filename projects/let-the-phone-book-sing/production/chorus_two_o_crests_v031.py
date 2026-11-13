"""Fast isolated pressure crests, built as native masked adjustment layers."""
import json
import math
from effectcraft_session import Session, BASE

OUT = BASE / 'generated/effectcraft-edit-v031'
OUT.mkdir(parents=True, exist_ok=True)
TARGET = OUT / 'Let-the-Phone-Book-Sing-editable-v031.ecproj'
if TARGET.exists():
    raise SystemExit('Preserve v031')
CENTER = (960, 390)

def circle(radius):
    return [[CENTER[0]+radius*math.cos(2*math.pi*i/96),
             CENTER[1]+radius*math.sin(2*math.pi*i/96)] for i in range(96)]

def path(radius):
    vertices = circle(radius+12) + list(reversed(circle(max(1,radius-12))))
    return {'t':'Path','v':{'closed':True,'vertices':vertices,
            'in_tangents':[[0,0]]*len(vertices),'out_tangents':[[0,0]]*len(vertices)}}

s = Session(BASE/'generated/effectcraft-edit-v030/Let-the-Phone-Book-Sing-editable-v030.ecproj')
try:
    s.command('comp.open', {'comp':19864})
    for n, onset in enumerate([1621,1628,1633],1):
        layer = s.command('layer.newAdjustment', {'name':f'O pressure crest {n} — background only'})['layer']
        s.command('layer.arrange', {'layers':[layer],'to':'backward'})
        # Scaling about the mouth yields purely outward displacement. Only the
        # feathered annulus reveals it; the rest of the scene is unchanged.
        fx = s.call('add_effect', {'layer':layer,'effect':'ec.distort.transform','values':{
            'anchor':list(CENTER),'position':list(CENTER),'uniform':True,
            'scaleHeight':100,'scaleWidth':100,'sampling':1}})['path']
        s.command('mask.new', {'layer':layer,'vertices':path(45)['v']['vertices'],'closed':True})
        s.call('set_property', {'layer':layer,'path':'masks/mask/feather','value':[9,9]})
        def keys(prop, pairs):
            s.call('add_keyframe', {'layer':layer,'path':prop,'keys':[
                {'time':f/24,'value':value} for f,value in pairs], 'interpolation':'linear'})
        frames = range(onset,onset+17)
        keys('masks/mask/path', [(f,path(45+(f-onset)*78)) for f in frames])
        keys(fx+'/scaleHeight', [(f,100+650/(45+(f-onset)*78)) for f in frames])
        keys('transform/opacity', [(0,0),(onset,0),(onset+2,100),
            (onset+6,100),(onset+12,40),(onset+16,0),(1898,0)])
    s.command('comp.open', {'comp':1554})
    s.call('save_project', {'path':str(TARGET)})
    for frame in [1628,1634,1640,1646,1650]:
        s.call('render_frame',{'comp':1554,'time':frame/24,
            'path':str(OUT/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
(BASE/'production/chorus-two-o-crests-v001.json').write_text(json.dumps({
    'status':'pending_user_review','shot':'PB-019',
    'nativeProject':str(TARGET.relative_to(BASE)), 'cleanFallback':'v030',
    'method':'Three feathered annular native Transform adjustment layers below narrator',
    'mouthCenterPixels':CENTER,'onsetFrames':[1621,1628,1633],
    'radialSpeedPixelsPerFrame':78,'bandWidthPixels':24,'featherPixels':9,
    'peakRadialDisplacementPixels':6.5,'lastEffectFrameExclusive':1649,
    'intent':'Isolated positive crests with flat gaps; strong on chorus dissolve, damped by regular lyrics.',
},indent=2)+'\n')
