"""Procedural lens-height gradient, native Blender displacement and dispersion."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
t=b.animated('Exact music time',[(v['song_frame']+.5)/24 for v in rows])
def height(px,py):
    h=0
    radius=((px-640)**2+((py-425)*1.65)**2)**.5
    wrinkle=6*b.op('SINE',px*.025+py*.019+t*2)*b.op('SINE',py*.031-t*1.4)
    for event in data['events']:
        ages=[(v['song_frame']+.5)/24-event['song_sec'] for v in rows]
        strength=b.animated('Attack envelope',[event['strength']*(1-math.exp(-a/.025))*min(1,(.65-a)/.13)*3000 if 0<a<.65 else 0 for a in ages])
        age=t-event['song_sec'];q=(radius+wrinkle-(110+age*750))/48
        h=h+strength*(-q*q*.5).exp()
    return h
dx=(height(x+1,y)-height(x-1,y))/2;dy=(height(x,y+1)-height(x,y-1))/2
boundary=((y-120)/100).clamp()*((590-y)/110).clamp()*(x/90).clamp()*((1279-x)/90).clamp()
person=(((((x-635)/175)**2+((y-610)/220)**2)**.5-1)/.3).clamp()
dx=dx*boundary*person;dy=dy*boundary*person
length=(dx*dx+dy*dy)**.5
limit=b.op('MINIMUM',1,b.op('DIVIDE',60,b.op('MAXIMUM',length,.001)))
def aov(name,value):
    a=s.view_layers[0].aovs.add();a.name=name;a.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
aov('DX',dx*limit*W/1280);aov('DY',-dy*limit*W/1280)
em=b.n.new('ShaderNodeEmission');em.inputs[0].default_value=(0,0,0,1);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native pressure lens','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers');channels=[]
for index,factor in enumerate([1.06,1,.94]):
    field=b.combine([Field(b,rl.outputs['DX'])*factor,Field(b,rl.outputs['DY'])*factor,0])
    dis=b.n.new('CompositorNodeDisplace');dis.inputs['Interpolation'].default_value='Bicubic';dis.inputs['Extension X'].default_value='Extend';dis.inputs['Extension Y'].default_value='Extend';b.plug(pic,dis.inputs['Image']);b.plug(field,dis.inputs['Displacement'])
    channels.append(b.split(dis.outputs[0])[index])
end=b.n.new('NodeGroupOutput');b.plug(b.combine(channels),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'pressure_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
