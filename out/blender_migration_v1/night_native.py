"""Native light, noisy water-plane reflection, shutter sampling and soft iris."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
s.render.engine='BLENDER_EEVEE'
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def value(name,fun):return b.animated(name,[fun(v) for v in rows])
time=value('Song time',lambda v:v['song_frame']/24);env=value('Master energy',lambda v:v['env']);bp=value('Beat',lambda v:v['beat'])
u=value('Departure',lambda v:(v['song_frame']-4710)/72);shrink=(1-u)**1.4
px=650+280*shrink*b.op('SINE',u*math.tau*1.25);py=350+125*shrink*b.op('SINE',u*math.tau*2.5+.5)
warm=((r+g-blue*1.3-100/255)/(150/255)).clamp()*((y-280)/50).smooth()*(1-((y-405)/45).smooth())
arch=warm*(.2+.7*env)
fauna=0
for j in range(28):
 cx=100+j*40+16*b.op('SINE',time*1.1+j);cy=315+32*b.op('SINE',j*2.5+time*.4)
 fauna+=(-((x-cx)**2+(y-cy)**2)/1.5).exp()
# Authored water polygon retained as a resolution-independent analytic mask.
polygon=[(555,357),(748,357),(811,379),(958,431),(1095,560),(938,700),(280,700),(185,575),(345,430),(471,383)]
crossings=0
for (ax,ay),(zx,zy) in zip(polygon,polygon[1:]+polygon[:1]):
 if ay==zy:continue
 crossx=ax+(y-ay)*(zx-ax)/(zy-ay)
 within=b.op('GREATER_THAN',y,min(ay,zy))*b.op('LESS_THAN',y,max(ay,zy))
 crossings+=within*b.op('LESS_THAN',x,crossx)
water=b.op('FLOORED_MODULO',crossings,2)
head=380+56*shrink+(350-py)*.1;dy=y-head;length=135+175*shrink;progress=(dy/length).clamp();width=4+5*shrink+(13+10*shrink)*progress
warp=(2+3*progress)*b.op('SINE',y*.16+time*.9)+2*b.op('SINE',y*.37-time*.6)
cap=(-((y-head)/7)**2-((x-px)/(6+5*shrink))**2).exp()
trail=(-((x-px-warp)/width)**2).exp()*(-b.op('MAXIMUM',dy,0)/(length*.42)).exp()*((dy+3)/9).smooth()*(1-((dy-length*.78)/(length*.22)).smooth())
noise=b.n.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2.5;noise.inputs['Roughness'].default_value=.6
b.plug(b.combine([x/11+2*b.op('SINE',y*.027+time*.6),y/2.5+time*2,0]),noise.inputs['Vector']);b.plug(time*.03,noise.inputs['W'])
glitter=((Field(b,noise.outputs['Fac'])-.37)*3.4).clamp()**2
reflection=(cap*(.55+.7*glitter)+trail*glitter)*water*(.8+.8*bp)
beam=[0,0,0]
for j in range(9):
 dt=-.4+j*.1;us=value(f'Shutter position {j}',lambda v,dt=dt:max(0,min(1,(v['song_frame']-4710+dt)/72)));ss=(1-us)**1.4
 bx=650+280*ss*b.op('SINE',us*math.tau*1.25);by=350+125*ss*b.op('SINE',us*math.tau*2.5+.5)
 pulse=value(f'Shutter beat {j}',lambda v,j=j:v['sub_beats'][j]);dist=(x-bx)**2+(y-by)**2
 core=(-dist/(2*(1.4+3.5*ss)**2)).exp()*(2.5+2*pulse);hr=5+12*ss+4*pulse
 halo=(-dist/(2*hr**2)).exp()*(.3+.65*pulse)+(-dist/(2*(hr*2.2)**2)).exp()*(.07+.12*pulse)
 beam=[a+(core*c+halo*z)/9/255 for a,c,z in zip(beam,[245,300,225],[125,255,100])]
radius=value('Iris radius',lambda v:math.hypot(640,360)*(1-smooth((v['song_frame']-4754)/28))*(1+.005*math.sin(v['song_frame']/24*3)))
iris=b.op('LESS_THAN',((x-640)**2+(y-360)**2)**.5,radius)
for name,field in [('Architecture',arch),('Fauna',fauna),('Reflection',reflection),('Water',water),('Iris',iris)]:
 av=s.view_layers[0].aovs.add();av.name=name;av.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(field,n.inputs['Value'])
av=s.view_layers[0].aovs.add();av.name='Beam';av.type='COLOR';n=b.n.new('ShaderNodeOutputAOV');n.aov_name='Beam';b.plug(b.combine(beam),n.inputs['Color'])
em=b.n.new('ShaderNodeEmission');b.plug(tex.outputs['Color'],em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native night light and aperture','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
rl=b.n.new('CompositorNodeRLayers');pic=[b.display(v) for v in b.split(rl.outputs['Image'])]
def scalar(socket):return Field(b,socket)
arch=scalar(b.blur(rl.outputs['Architecture'],3,W));fauna=scalar(rl.outputs['Fauna'])+scalar(b.blur(rl.outputs['Fauna'],3,W))*.7
light=[arch*c/255+fauna*z/255 for c,z in zip([160,110,45],[85,120,70])]
def lit(pic,energy):return [a+(1-a)*(1-(-z).exp()) for a,z in zip(pic,energy)]
pic=lit(pic,light);ref=scalar(rl.outputs['Reflection'])+scalar(b.blur(rl.outputs['Reflection'],3,W))*.6+scalar(b.blur(rl.outputs['Reflection'],9,W))*.3
water=scalar(b.blur(rl.outputs['Water'],5,W));pic=lit(pic,[ref*c/255*water for c in [175,330,130]]);pic=lit(pic,b.split(rl.outputs['Beam']))
closing=b.animated('Iris active',[int(v['song_frame']>=4754) for v in rows]);fade=b.animated('Final extinction',[1-smooth((v['song_frame']-4779)/3) for v in rows]);iris=scalar(b.blur(rl.outputs['Iris'],15,W));aperture=(1-closing)+closing*iris*fade
end=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear((a*aperture).clamp()) for a in pic]),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.frame_set(1);s.render.filepath=str(out/'0001.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/f'night_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
