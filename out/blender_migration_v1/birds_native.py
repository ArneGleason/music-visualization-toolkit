"""Native image-derived lantern and moving chrome response, no FX texture inputs."""
from pathlib import Path
O=Path(__file__).resolve().parent
# Shared scene/untreated animated plate setup, before the family-specific nodes.
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
lamps=[(556,14,50,70),(774,130,48,64),(520,209,50,80),(733,275,57,78),(669,392,38,64),(609,468,60,78),(678,563,45,66)]
warm=((r-blue-.08)*4).clamp()*((r-.2)*2.8).clamp()
signal=0; regions=0
for j,(cx,cy,rx,ry) in enumerate(lamps):
    region=(-(((x-cx)/rx)**4+((y-cy)/ry)**4)).exp()
    regions=b.op('MAXIMUM',regions,region)
    gains=[(.16+.95*v['drum']+.22*v['voice']+1.65*math.exp(-((v['song_frame']-(1741+j*1.4))/4.8)**2))*v['settle'] for v in rows]
    signal=signal+region*warm*b.animated('Lamp '+str(j),gains)
hi=b.op('MAXIMUM',r,b.op('MAXIMUM',g,blue));lo=b.op('MINIMUM',r,b.op('MINIMUM',g,blue))
sat=(hi-lo)/b.op('MAXIMUM',hi,.00001)
silver=(1-sat*2.55).clamp()*((r-.32)*3).clamp()*(1-(regions*1.5).clamp())
silver=silver*b.op('GREATER_THAN',x,175)*b.op('LESS_THAN',x,1100)*b.op('GREATER_THAN',y,130)*b.op('LESS_THAN',y,705)
prev=b.n.new('ShaderNodeTexImage');prev.image=img;prev.image_user.frame_duration=count;prev.image_user.frame_start=2;prev.image_user.use_auto_refresh=True;b.plug(uv.outputs['UV'],prev.inputs['Vector'])
pr,pg,pb=[b.display(v) for v in b.split(prev.outputs['Color'],True)]
diff=b.op('ABSOLUTE',(r-pr)*.299+(g-pg)*.587+(blue-pb)*.114)
def aov(name,value):
    a=s.view_layers[0].aovs.add();a.name=name;a.type='VALUE'
    n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
aov('Silver',silver);aov('Motion',diff)
em=b.n.new('ShaderNodeEmission');b.plug(signal,em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native bird light composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers')
core=b.mix(b.blur(rl.outputs['Image'],1.3,W),(1,.43,.12,1),mode='MULTIPLY')
light=b.mix(core,b.mix(b.blur(core,10,W),(1.05,)*3+(1,),mode='MULTIPLY'))
light=b.mix(light,b.mix(b.blur(core,30,W),(.65,)*3+(1,),mode='MULTIPLY'))
motion=b.split(b.blur(rl.outputs['Motion'],4,W))[0]*18
first=b.animated('First frame motion fallback',[1]+[0]*(count-1))
motion=motion.clamp()*(1-first)+first
gain=b.animated('Chrome musical response',[(.18+.85*v['drum']+1.10*v['woke'])*v['settle'] for v in rows])
silver=b.mix(rl.outputs['Silver'],b.combine([.28+.72*motion]*3),mode='MULTIPLY')
silver=b.blur(silver,.75,W)
pearl=b.mix(silver,b.combine([gain*.86,gain*.74,gain]),mode='MULTIPLY')
pearl=b.mix(pearl,b.mix(b.blur(pearl,5,W),(1.35,)*3+(1,),mode='MULTIPLY'))
# The legacy second bloom samples the unbloomed pearl, not the first bloom.
base=b.mix(silver,b.combine([gain*.86,gain*.74,gain]),mode='MULTIPLY')
pearl=b.mix(pearl,b.mix(b.blur(base,16,W),(.65,)*3+(1,),mode='MULTIPLY'))
light=b.mix(light,pearl)
result=b.combine([b.linear((b.display(p)+e).clamp()) for p,e in zip(b.split(pic),b.split(light))])
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'birds_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
