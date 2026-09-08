"""Native garden wave, pollen punctuation and green conductor above her head."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
depth=b.op('MAXIMUM',b.op('ABSOLUTE',x-640)/620,(y-230)/480).clamp()
body=1-(((((x-640)/125)**2+((y-415)/330)**2)**.5-.92)/.25).smooth()
face=(-(((x-640)/92)**4+((y-182)/83)**4)).exp();protect=1-b.op('MAXIMUM',body,face)
pods=[(193,320,24),(270,320,23),(310,265,13),(287,365,16),(355,393,31),(283,423,29),(355,485,27),(402,540,22),(342,581,32),(250,632,30),(149,680,30),(79,550,40),(24,456,31)]
region=0
for cx,cy,rad in pods:
    for px in (cx,1280-cx):region=b.op('MAXIMUM',region,(-(((x-px)/rad)**4+((y-cy)/(rad*1.25))**4)).exp())
far=(1-((b.op('ABSOLUTE',x-640)-150)/100).smooth())*(1-((y-380)/70).smooth())
warm=((r-blue-.06)*4).clamp()*((r-.32)*3).clamp()*b.op('MAXIMUM',region,far*((r-.62)*4).clamp()*.5)*protect
pink=((r-g-.06)*4).clamp()*((blue-g-.025)*5).clamp()*((r-.34)*3).clamp()*protect
sf=b.animated('Master frame',[v['song_frame'] for v in rows])
wave=(-((sf-(1790+38*depth))/6.5)**2).exp();begin=((sf-1825)/3).smooth()*(1-((sf-1831)/10).smooth());invitation=((sf-1786)/8).smooth()
gain=.10*invitation+.85*wave+.95*begin;flowergain=.40*wave+.60*begin
core=0;halo=0
for k in range(2):
    brightness=b.animated(f'Conductor brightness{k}',[1.05+1.25*math.exp(-(v['samples'][k]['head'][3]%1)/.23)+1.15*v['samples'][k]['head'][4] for v in rows])
    for age in range(12):
        points=[v['samples'][k]['tail'][age] for v in rows]
        cx=b.animated(f'Wake{k}/{age}X',[p[0] for p in points]);cy=b.animated(f'Wake{k}/{age}Y',[p[1] for p in points]);radius=b.animated(f'Wake{k}/{age}radius',[p[2]*(1-age*.045) for p in points])
        d=(x-cx)**2+(y-cy)**2
        core=core+(-d/(2*radius**2)).exp()*math.exp(-age*.38)*.25*brightness
        if age==0:halo=halo+((-d/(2*19**2)).exp()*.20+(-d/(2*35**2)).exp()*.065)*brightness*.5
clearance=1-((y-119)/24).smooth()
def aov(name,value):
    a=s.view_layers[0].aovs.add();a.name=name;a.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
for name,value in [('Warm',warm),('Pink',pink),('WarmGain',gain),('PinkGain',flowergain),('Protect',protect),('GuideCore',core*clearance),('GuideHalo',halo*clearance)]:aov(name,value)
em=b.n.new('ShaderNodeEmission');em.inputs[0].default_value=(0,0,0,1);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Garden bloom composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers')
warm=b.mix(b.blur(rl.outputs['Warm'],1.1,W),rl.outputs['WarmGain'],mode='MULTIPLY')
pink=b.mix(b.blur(rl.outputs['Pink'],1.2,W),rl.outputs['PinkGain'],mode='MULTIPLY')
garden=b.mix(b.mix(warm,(1,.60,.22,1),mode='MULTIPLY'),b.mix(pink,(.78,.43,.82,1),mode='MULTIPLY'))
light=b.mix(garden,b.mix(b.blur(garden,7,W),(.75,.75,.75,1),mode='MULTIPLY'))
light=b.mix(light,b.mix(b.blur(garden,23,W),(.50,.50,.50,1),mode='MULTIPLY'))
light=b.mix(light,rl.outputs['Protect'],mode='MULTIPLY')
guide=b.mix(b.mix(rl.outputs['GuideCore'],(.57,1,.40,1),mode='MULTIPLY'),b.mix(rl.outputs['GuideHalo'],(.36,1,.21,1),mode='MULTIPLY'))
light=b.mix(light,guide)
result=b.combine([b.linear((b.display(p)+e).clamp()) for p,e in zip(b.split(pic),b.split(light))])
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'bloom_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
