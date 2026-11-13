"""Dial back fine-hair recovery 75 percent toward the original key."""
import json
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v033';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v033.ecproj'
if target.exists():raise SystemExit('Preserve v033')
values={'screenGain':180,'clipBlack':20,'clipWhite':82,'screenShrinkGrow':-.4875,'screenSoftness':.625,'screenPreblur':.4375}
s=Session(BASE/'generated/effectcraft-edit-v032/Let-the-Phone-Book-Sing-editable-v032.ecproj')
try:
 s.command('comp.open',{'comp':'Chorus 2 fine hair matte recovery'})
 for k,v in values.items():s.call('set_property',{'layer':20068,'path':'effects/#1/'+k,'value':v})
 s.call('save_project',{'path':str(target)})
 for f in [1688,1690,1692]:s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
finally:s.close()
(BASE/'production/chorus-two-hair-v002.json').write_text(json.dumps({'status':'pending_review','nativeProject':str(target.relative_to(BASE)),'controls':values,'interpolation':'75% original v031 +25% recovery v032','touchup':'No connecting strokes added yet; short moving gaps need tracked stroke endpoints, not a static patch.'},indent=2)+'\n')
