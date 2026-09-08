"""Native dancing green light, sampled wake, beat bloom and foliage interruption."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
core=0;halo=0
for k in range(2):
    gain=b.animated(f'Beat brightness {k}',[.8+1.7*math.exp(-(v['samples'][k]['head'][3]%1)/.23) for v in rows])
    for age in range(9):
        points=[v['samples'][k]['tail'][age] for v in rows]
        cx=b.animated(f'Wake{k}/{age}X',[p[0] for p in points]);cy=b.animated(f'Wake{k}/{age}Y',[p[1] for p in points]);radius=b.animated(f'Wake{k}/{age}radius',[p[2]*(1-age*.055) for p in points])
        d=(x-cx)**2+(y-cy)**2
        core=core+(-d/(2*radius**2)).exp()*math.exp(-age*.48)*.34*gain
        if age==0:halo=halo+((-d/(2*19**2)).exp()*.22+(-d/(2*43**2)).exp()*.085)*gain*.5
gray=r*.299+g*.587+blue*.114
occlusion=(1-((gray-.045)/.075).smooth())*((g-r+.005)/.045).smooth()
def aov(name,value):
    a=s.view_layers[0].aovs.add();a.name=name;a.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
aov('Halo',halo);aov('Foliage',occlusion)
em=b.n.new('ShaderNodeEmission');b.plug(core,em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native green guide composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers')
light=b.mix(b.mix(rl.outputs['Image'],(.57,1,.40,1),mode='MULTIPLY'),b.mix(rl.outputs['Halo'],(.36,1,.21,1),mode='MULTIPLY'))
occ=1-b.split(b.blur(rl.outputs['Foliage'],1.8,W))[0]*.70
def sm(v):v=max(0,min(1,v));return v*v*(3-2*v)
arrival=b.animated('Soft arrival',[.4+.6*sm(i/5) for i in range(count)])
light=b.mix(light,b.combine([occ*arrival]*3),mode='MULTIPLY')
result=b.combine([b.linear((b.display(p)+e).clamp()) for p,e in zip(b.split(pic),b.split(light))])
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'guide_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
