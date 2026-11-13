"""Review new Hedra hands/ink take through preferred A key, without added stroke."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI

out = BASE / 'generated/effectcraft-edit-v040'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v040.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v040')
s = Session(BASE / 'generated/effectcraft-edit-v037/Let-the-Phone-Book-Sing-editable-v037.ecproj')
try:
    s.command('comp.open', {'comp': 19862})
    src = BASE / 'generated/avatar-tests/chorus-two-v002/hedra-original-1080p.mp4'
    item = s.command('file.import', {'paths': [str(src)], 'sequence': False})['items'][0]
    s.command('layer.replaceSource', {'layer': 19805, 'item': item})
    s.call('set_property', {'layer': 19805, 'path': 'timeRemap', 'expression': 'Math.max(0,time-1606/24)'})
    s.command('layer.setSwitch', {'layers': [19805], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': 19805, 'path': 'effects/#1/screenColor', 'value': [0,249/255,1/255,1]})
    s.call('set_property', {'layer': 19805, 'path': 'layerStyles/stroke/opacity', 'value': 0})
    s.call('set_property', {'layer':19805,'path':'effects/#1/edgeColor','value':1})
    s.call('set_property', {'layer':19805,'path':'effects/#1/screenShrinkGrow','value':-1.0})
    s.call('set_property', {'layer':19805,'path':'effects/#1/despill','value':0})
    s.call('set_property', {'layer':19805,'path':'effects/#1/screenSoftness','value':.5})
    s.call('set_property', {'layer':19805,'path':'effects/#1/screenPreblur','value':0})
    s.command('effect.toggle', {'layer':19805,'effect':2,'value':False})
    s.command('layer.setSwitch', {'layers':[19725],'switch':'video','value':False})
    s.command('comp.settings', {'comp': 19862, 'name': 'Chorus 2 — matte only, source colors, no cleanup or added stroke'})
    s.call('save_project', {'path': str(target)})
    for f in [1634,1690,1820,1890]:
        s.call('render_frame', {'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
subprocess.run([str(CLI),'render','--project',str(target),'--gpu','--comp','1554',
                '--start',str(1596/24),'--end',str(1898/24),'--out',str(out/'chorus-two-lighter-trim-review.mp4'),
                '--format','h264','--bitrate','10000','--audio','on'],check=True)
record = {'status':'pending_review','project':str(target.relative_to(BASE)),
          'review':'generated/effectcraft-edit-v040/chorus-two-lighter-trim-review.mp4',
          'source':'generated/avatar-tests/chorus-two-v002/hedra-original-1080p.mp4',
          'key':'Source edge color; despill0; Key Cleaner disabled; hair color correction disabled; shrink-1; softness0.5; preblur0; RGB[0,249,1]',
          'addedStrokeOpacity':0,'sourceStartFrame':1606,'reviewFrames':[1596,1898],
          'fps':24,'notes':'Same background, ripple, joint scene fade and song timing. Earlier take preserved.'}
(BASE/'production/chorus-two-lighter-trim-v001.json').write_text(json.dumps(record,indent=2)+'\n')
