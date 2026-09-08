"""Four temporal samples of native procedural CRT acquisition, clean picture only."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
def ease(a,z,t):
    v=max(0,min(1,(t-a)/(z-a)));return v*v*(3-2*v)
samples=[]
for k in range(4):
    values=[]
    for f in range(count):
        t=(f+(k+.5)/4)/24
        wx=5+(1280*1.025-5)*ease(.14,.53,t);hy=3+(720*1.018-3)*ease(.42,1.03,t)
        settle=ease(1.03,1.2,t);wx=wx*(1-settle)+1280*settle;hy=hy*(1-settle)+720*settle
        values.append(dict(wx=wx,hy=hy,cx=640+(1-ease(.25,.95,t))*1.5*math.sin(t*97),cy=360+(1-ease(.3,.95,t))*1.1*math.sin(t*83),picture=ease(.26,.66,t),dot=(1-ease(.25,.55,t))*(.73+.19*math.sin(t*91)+.08*math.sin(t*213+.4)),line=ease(.13,.28,t)*(1-ease(.48,.88,t)),active=float(t<1.2)))
    a={name:b.animated(f'Sample {k} {name}',[v[name] for v in values]) for name in values[0]}
    dx=x-a['cx'];dy=y-a['cy'];wx=a['wx'];hy=a['hy']
    coords=b.combine([dx/wx+.5,.5-dy/hy,0])
    mapped=b.n.new('ShaderNodeTexImage');mapped.image=img;mapped.extension='CLIP';mapped.image_user.frame_duration=count;mapped.image_user.frame_start=1;mapped.image_user.use_auto_refresh=True;b.plug(coords,mapped.inputs['Vector'])
    rgb=[b.display(v) for v in b.split(mapped.outputs[0],True)]
    edge=((wx/2-b.op('ABSOLUTE',dx))/2).clamp()*((hy/2-b.op('ABSOLUTE',dy))/2).clamp()
    dot=(-(dx*dx+dy*dy)/(2*2.2**2)).exp()+(-(dx*dx+dy*dy)/(2*15**2)).exp()*.15
    bar=(-(dy/1.8)**2).exp()*(-(dx/b.op('MAXIMUM',4,wx*.38))**8).exp()
    bloom=(-(dy/11)**2).exp()*(-(dx/b.op('MAXIMUM',10,wx*.39))**8).exp()*.19
    light=dot*a['dot']+(bar+bloom)*a['line']
    original=[r,g,blue]
    samples.append([((p*edge*a['picture']+light*c*1.6).clamp()*a['active']+o*(1-a['active'])) for p,c,o in zip(rgb,[1,222/255,155/255],original)])
result=b.combine([b.linear(sum(sample[c] for sample in samples)/4) for c in range(3)])
em=b.n.new('ShaderNodeEmission');b.plug(result,em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'opening_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
