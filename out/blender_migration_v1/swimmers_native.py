"""Native pearl/violet swimmer masks, tracked controls and opposed musical sectors."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
if data['overhead']:
    hi=b.op('MAXIMUM',r,b.op('MAXIMUM',g,blue));lo=b.op('MINIMUM',r,b.op('MINIMUM',g,blue))
    silver=((lo-.24)/.45).clamp()*(1-(hi-lo)/.25).clamp()
    rr=(((x-640)/450)**2+((y-350)/300)**2)**.5
    region=((1-rr)/.13).clamp()*((rr-.10)/.08).clamp()
    angle=b.op('ARCTAN2',y-350,x-640);pulse=0
    t=b.animated('Exact master sample time',[(v['song_frame']+.5)/24 for v in rows])
    for j,hit in enumerate(data['events']):
        age=t-hit+.15*(1+b.op('COSINE',2*angle-j*math.pi/2))
        positive=b.op('MAXIMUM',0,age)
        pulse=pulse+(1-(-positive/.025).exp())*(-positive/.14).exp()*b.op('GREATER_THAN',age,0)*b.op('LESS_THAN',age,.65)
    signal=region*silver*pulse*1.9
else:
    lum=sum(b.split(tex.outputs['Color'],True))/3
    highlights=((lum-.07)/.32).clamp()**1.3;signal=0
    for k,(rx,ry) in enumerate([(45,22),(55,24),(55,24),(70,30)]):
        cx=b.animated(f'Track{k} X',[v['groups'][k]['centre'][0] for v in rows]);cy=b.animated(f'Track{k} Y',[v['groups'][k]['centre'][1] for v in rows])
        p=b.animated(f'Track{k} accepted pulse',[v['groups'][k]['pulse'] for v in rows])
        signal=signal+(-2*(((x-cx)/rx)**2+((y-cy)/ry)**2)).exp()*highlights*p*1.9
em=b.n.new('ShaderNodeEmission');b.plug(signal,em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native swimmer additive composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers');core=rl.outputs['Image']
halo=b.mix(b.mix(b.blur(core,6,W),(.75,.75,.75,1),mode='MULTIPLY'),b.mix(b.blur(core,17,W),(.30,.30,.30,1),mode='MULTIPLY'))
color=tuple(data['palette_linear_rgb']['violet'])+(1,)
light=b.mix(b.mix(core,(.968,1.012,1.1,1),mode='MULTIPLY'),b.mix(halo,color,mode='MULTIPLY'))
result=b.mix(pic,light)
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'{family}_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
