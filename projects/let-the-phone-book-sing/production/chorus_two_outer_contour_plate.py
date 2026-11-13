"""Native outer silhouette stroke on approved original cutout, no redraw."""
from effectcraft_session import Session, BASE
out = BASE/'generated/avatar-tests/chorus-two-v003'
out.mkdir(parents=True, exist_ok=True)
target=out/'narrator-outer-contour.ecproj'
if target.exists(): raise SystemExit('Preserve existing starter')
s=Session(BASE/'generated/avatar-tests/chorus-two-v001/narrator-green.ecproj')
try:
    s.command('comp.open',{'comp':1})
    layer=next(x['id'] for x in s.call('get_comp',{'comp':1})['layers'] if x['type']!='Solid')
    # Remove almost-transparent alpha dust before generating the silhouette stroke.
    # Alpha-specific parameter; generic inBlack would alter RGB as well.
    s.call('add_effect',{'layer':layer,'effect':'ec.color.levels','values':{'channel':4,'alphaInBlack':.15}})
    s.command('layer.style.stroke',{'layers':[layer]})
    for key,value in [('color',[0,0,0,1]),('size',3),('opacity',100),('position',0)]:
        s.call('set_property',{'layer':layer,'path':'layerStyles/stroke/'+key,'value':value})
    s.call('save_project',{'path':str(target)})
    s.call('render_frame',{'comp':1,'time':0,'path':str(out/'narrator-outer-contour.png'),'inline':False,'max_side':1920})
finally:s.close()
