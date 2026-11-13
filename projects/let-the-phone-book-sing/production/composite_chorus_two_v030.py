"""Native Chorus 2 composite: accepted gnome take and narrator B performance."""
import json,subprocess
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v030';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v030.ecproj'
if target.exists():raise SystemExit('Preserve v030')
s=Session(BASE/'generated/effectcraft-edit-v029/Let-the-Phone-Book-Sing-editable-v029.ecproj')
try:
    keycomp=s.command('project.duplicate',{'items':[17369]})['items'][0]
    s.command('comp.open',{'comp':keycomp})
    s.command('comp.settings',{'comp':keycomp,'name':'Chorus 2 — narrator B key and hair cleanup'})
    layers=s.call('get_comp',{'comp':keycomp})['layers']
    plate=next(l['id'] for l in layers if l['type']=='Footage')
    src=BASE/'generated/avatar-tests/chorus-two-v001/hedra-original-1080p.mp4'
    item=s.command('file.import',{'paths':[str(src)],'sequence':False})['items'][0]
    s.command('layer.replaceSource',{'layer':plate,'item':item})
    s.call('set_property',{'layer':plate,'path':'timeRemap','expression':'Math.max(0,time-1606/24)'})
    s.command('layer.setSwitch',{'layers':[plate],'switch':'audio','value':False})
    s.call('set_property',{'layer':plate,'path':'effects/#1/screenColor','value':[0,211/255,0,1]})
    scene=s.command('comp.new',{'name':'Chorus 2 — Park Orchard singer and gnome','width':1920,'height':1080,'frameRate':24,'duration':180.8333333333})['comp']
    bg=BASE/'generated/kling-tests/chorus-two-v001/gnome-original-1080p.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(bg)]))['streams'][0]
    item=s.command('file.import',{'paths':[str(bg)],'sequence':False})['items'][0]
    back=s.command('layer.addItem',{'item':item,'index':1})['layer']
    s.command('layer.rename',{'layer':back,'name':'Approved gnome take — full frame'})
    s.command('layer.setSwitch',{'layers':[back],'switch':'audio','value':False})
    scale=max(1920/probe['width'],1080/probe['height'])*100
    s.call('set_property',{'layer':back,'path':'transform/scale','value':[scale,scale,100]})
    s.command('layer.timing',{'layers':[back],'out':1900/24})
    s.command('layer.enableTimeRemap',{'layers':[back],'value':True})
    s.call('set_property',{'layer':back,'path':'timeRemap','expression':'Math.max(0,time-1606/24)'})
    singer=s.command('layer.addItem',{'item':keycomp,'index':1})['layer']
    s.command('layer.rename',{'layer':singer,'name':'Approved narrator B — original plate framing'})
    s.command('comp.open',{'comp':675})
    s.command('layer.setSwitch',{'layers':[1018,1041],'switch':'video','value':False})
    main=s.command('layer.addItem',{'item':scene,'index':55})['layer']
    s.command('layer.timing',{'layers':[main],'in':1620/24,'out':1900/24})
    s.call('add_keyframe',{'layer':main,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(1620,0),(1626,100),(1896,100),(1900,0)]],'interpolation':'linear'})
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
    for f in [1630,1690,1820]:s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
    rec={'status':'composite_pending_review','nativeProject':str(target.relative_to(BASE)),'keyComp':keycomp,'sceneComp':scene,'sceneLayer':main,'plateLayer':plate,'backgroundLayer':back,'sourceStartMasterFrame':1606,'visiblePickupFrame':1620,'fadeInFrames':[1620,1626],'musicalEndFrameExclusive':1898,'notes':'Full gnome background, no split; approved native key/hair/ink reused. Whole scene fades together for improvised O. Prior scenes retained.'}
    (BASE/'production/chorus-two-composite-v001.json').write_text(json.dumps(rec,indent=2)+'\n')
finally:s.close()
