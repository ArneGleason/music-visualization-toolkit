"""Later TV registrations and additive switch-off; native paths and masks."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'tv_native.py').read_text()
# The existing builder is reused, then its constructed scene script is specialized.
code=code[:code.rindex('exec(compile(code,')]
ns={'__file__':str(O/'tv_native.py')};exec(compile(code,'build_native_tv','exec'),ns);source=ns['code']
source=source.replace("D=O/'tv'","D=O/'tv_late'").replace('s.frame_end=191','s.frame_end=105').replace('range(1,192)','range(1,106)').replace('n.frame_duration=191','n.frame_duration=105').replace("f'tv_{W}.blend'","f'tv_late_{W}.blend'")
source=source.replace('gain=1.0264','gain=1').replace('gain=.3264*.68**age','gain=0').replace('age<14','age<1').replace('(fi+15,True)','(fi+2,True)')
source=source.replace("h=json.loads((D/'controls.json').read_text())['inverse']", "data=json.loads((D/'controls.json').read_text());h=[[pb.animated(f'Inverse {i}.{j}',[row['inverse'][i][j] for row in data['frames']]) for j in range(3)] for i in range(3)]")
source=source.replace('(tx-360)/360','(tx-200)/200').replace('(ty-360)/360','(ty-200)/200').replace('(.98-edge)/.19','(.97-edge)/.22').replace("mask=b.split(mask_image.outputs['Image'])[0]*.82","mask=b.split(mask_image.outputs['Image'])[0];shutdown=b.animated('Additive switch-off',[row['shutdown'] for row in data['frames']])")
source=source.replace('[(2.1,1.0),(6.6,.5)]','[(2.1,1.5)]')
source=source.replace('a*(1-mask*.13)+(1-a*.87)*(1-(-z*255/220).exp())*mask','(a*(1-mask*.864)+z*mask)*(1-shutdown)+(a+(1-a)*(1-(-z*mask).exp()))*shutdown')
exec(compile(source,str(O/'tv_native.py'),'exec'))
