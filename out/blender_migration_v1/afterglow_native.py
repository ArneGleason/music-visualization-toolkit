"""Native artifact tracking, protected optical ripple and room-depth projection."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
import random
s.render.engine='BLENDER_EEVEE'
def sin(v):return b.op('SINE',v)
def cos(v):return b.op('COSINE',v)
time=b.animated('Continuous room time',[(v['source_frame']+data['time_offset'])/24 for v in rows]);voice=b.animated('Verified own-phrase envelope',[v['voice_envelope'] for v in rows])
cx=b.animated('Tracked artifact X',[v['center'][0] for v in rows]);cy=b.animated('Tracked artifact Y',[v['center'][1] for v in rows]);dx=x-cx;dy=y-cy;dist=(dx*dx+dy*dy)**.5
inner=1-(-((dx/83)**6+(dy/108)**6)).exp();region=(-((dx/245)**2+(dy/200)**2)).exp()*inner*((y-355)/60).smooth()
displacement=sin(dist*.055-time*3.4)*(.9+2.3*voice)*region
wx=x+displacement*dx/b.op('MAXIMUM',dist,1);wy=y+displacement*dy/b.op('MAXIMUM',dist,1)
warped=b.n.new('ShaderNodeTexImage');warped.image=img;warped.image_user.frame_duration=count;warped.image_user.frame_start=1;warped.image_user.use_auto_refresh=True;warped.extension='EXTEND';b.plug(b.combine([wx/1280,1-wy/720,0]),warped.inputs['Vector'])
roi=(-((dx/48)**6+(dy/81)**6)).exp()*(1-((dy-56)/23).smooth());warm=((r-blue-.045)*7).clamp()*((g-blue-.015)*9).clamp()*roi
theta=b.op('ARCTAN2',dy,dx);sweep=.65+.35*(-b.op('FLOORED_MODULO',time*2.3-theta,math.tau)/1.1).exp();core=warm*sweep*(.65+2.1*voice)
spill=(-.5*((dx/80)**2+(dy/85)**2)).exp()*(.02+.10*voice)
# Match the original deterministic population; smoothly fading native Gaussian nuclei.
import numpy as np
rng=np.random.default_rng(917);motes=[0,0,0]
for j in range(38):
 phase,life,angle,size,side=rng.uniform(0,1),rng.uniform(2.3,4.2),rng.uniform(0,math.tau),rng.uniform(.8,1.8),rng.choice([-1,1])
 age=b.op('FLOORED_MODULO',time/life+phase,1);px=cx+int(side)*(25+165*age)+35*sin(age*math.tau+float(angle))*age;py=cy-15-200*age+12*sin(age*math.tau*1.3+float(angle))
 fade=b.op('MAXIMUM',0,sin(math.pi*age))**1.4*(.4+.7*voice);nucleus=(-((x-px)**2+(y-py)**2)/(max(1,int(size))**2*.8)).exp()*fade
 motes=[a+nucleus*c for a,c in zip(motes,[.8,.56,1] if j%3 else [1,.93,.88])]
window=1-((((x-650)/540)**2+((y-190)/245)**2-.95)/.17).smooth();person=1-((((x-650)/255)**4+((y-425)/385)**4-.78)/.26).smooth();guard=(1-window)*(1-person)
bed=((y-410)/80).smooth()*(1-((x-1060)/110).smooth())*((x-70)/90).smooth();wall=3.4-1.6*b.op('ABSOLUTE',(x-640)/640).clamp()**1.7
beddepth=b.op('MINIMUM',2.7,b.op('MAXIMUM',1.25,2.7-(y-440)*.0045));depth=wall*(1-bed)+beddepth*bed
X=(x-640)/780*depth;Y=(360-y)/780*depth-.65;Z=depth-.4;az=b.op('ARCTAN2',X,Z);el=b.op('ARCTAN2',Y,(X*X+Z*Z)**.5);u=az*5.5-time*.95;w=el*7
def noise(offset):
 n=b.n.new('ShaderNodeTexNoise');n.noise_dimensions='4D';n.inputs['Scale'].default_value=1.35;n.inputs['Detail'].default_value=2;n.inputs['Roughness'].default_value=.55;b.plug(b.combine([u+offset,w+offset*.71,0]),n.inputs['Vector']);b.plug(time*.2,n.inputs['W']);return Field(b,n.outputs['Fac'])*2-1
n=noise(0);m=noise(17.3);du=u+.85*n;dw=w+.65*m;field=sin(du*2+1.1*sin(dw*1.6+time*.23))+.65*cos(dw*2.2-du*.65)+.5*n
violet=(-((field-.50)/.34)**2).exp();teal=(-((field+.72)/.38)**2).exp();reflect=b.op('MINIMUM',.85,b.op('MAXIMUM',.20,(r+g+blue)/3*1.9));strength=(2.5+.65*voice)*guard*reflect*b.op('MINIMUM',1.35,b.op('MAXIMUM',.65,1+.38*m))
room=[(violet*a+teal*z)*strength for a,z in zip([.5,.16,.65],[.1,.62,.45])]
fixtures=[(1231,164,9),(1224,276,8),(1251,285,7),(1267,305,8),(1197,415,9),(1213,438,9),(1252,453,10),(1236,494,10),(1163,503,9),(1182,510,8),(1203,525,7)]
for j,(px,py,rr) in enumerate(fixtures):
 d2=(x-px)**2+(y-py)**2;pulse=(.5+.5*sin(time*(2.1+j*.17)+j*2.4))**5;level=.10+.8*pulse+.85*voice*(.5+.5*sin(j*1.7+time*2))
 term=((-d2/(rr*rr*.75)).exp()*((r-.10)*3).clamp()+(-d2/(rr*rr*12)).exp()*.13)*level
 room=[a+term*c for a,c in zip(room,[1,.52,.13])]
for name,val in [('Core',core),('Spill',spill),('Gate',((y-340)/50).smooth())]:
 av=s.view_layers[0].aovs.add();av.name=name;av.type='VALUE';node=b.n.new('ShaderNodeOutputAOV');node.aov_name=name;b.plug(val,node.inputs['Value'])
for name,val in [('Motes',motes),('Room',room),('Source',[r,g,blue])]:
 av=s.view_layers[0].aovs.add();av.name=name;av.type='COLOR';node=b.n.new('ShaderNodeOutputAOV');node.aov_name=name;b.plug(b.combine(val),node.inputs['Color'])
em=b.n.new('ShaderNodeEmission');b.plug(warped.outputs['Color'],em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native afterglow light composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t);rl=b.n.new('CompositorNodeRLayers')
core=Field(b,b.blur(rl.outputs['Core'],.75,W));core+=Field(b,b.blur(rl.outputs['Core'],5,W))+Field(b,b.blur(rl.outputs['Core'],17,W))*.70
spill=Field(b,rl.outputs['Spill']);motes=b.mix(rl.outputs['Motes'],(1.2,1.2,1.2,1),mode='MULTIPLY')
for sigma,gain in [(3,3),(9,1.7)]:motes=b.mix(motes,b.mix(b.blur(rl.outputs['Motes'],sigma,W),(gain,gain,gain,1),mode='MULTIPLY'))
gate=Field(b,rl.outputs['Gate']);effect=[(core*c+spill*z+p)*gate for c,z,p in zip([1,.55,.1],[.8,.45,.17],b.split(motes))]
source=b.split(rl.outputs['Source']);delta=[(1-a)*(1-(-e).exp()) for a,e in zip(source,effect)];room=b.split(b.blur(rl.outputs['Room'],5,W));roomdelta=[(1-a)*(1-(-e).exp()) for a,e in zip(source,room)]
# The old Blender VSE added these independently encoded light deltas in linear space.
outnode=b.n.new('NodeGroupOutput');b.plug(b.combine([(a+b.linear(z.clamp())+b.linear(q.clamp())).clamp() for a,z,q in zip(b.split(rl.outputs['Image']),delta,roomdelta)]),outnode.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.frame_set(1);s.render.filepath=str(out/'0001.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/f'{family}_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
