"""Reduced room projection, stable motes, additive green actor and teeth guard."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'afterglow_native.py').read_text()
code=code.replace("*(.4+.7*voice);nucleus", "*.65;nucleus")
code=code.replace("room=[a+term*c for a,c in zip(room,[1,.52,.13])]", "room=[a+term*c for a,c in zip(room,[1,.52,.13])]")
marker="for name,val in [('Core',core)"
at=code.index(marker)
code=code[:at]+'''
room=[v*.6 for v in room]
song=b.animated('Locked song frame',[r['song_frame'] for r in rows]);u=(song-4449)/67
px=990+100*sin(u*math.tau*1.5);py=365-120*sin(u*math.tau*2)
size=10;d2=(x-px)**2+(y-py)**2
green=[(-d2/(2*(size*.17)**2)).exp()*a+(-d2/(2*(size*.43)**2)).exp()*z+(-d2/(2*(size*.9)**2)).exp()*q for a,z,q in zip([2.8,4.2,2.4],[.08,.48,.045],[.012,.055,.008])]
green=[v*((song-4448).clamp())*(1+.5*voice) for v in green]
av=s.view_layers[0].aovs.add();av.name='Green';av.type='COLOR';node=b.n.new('ShaderNodeOutputAOV');node.aov_name='Green';b.plug(b.combine(green),node.inputs['Color'])
mouth=(-((x-645)/40)**6-((y-257)/16)**6).exp();white=((b.op('MINIMUM',r,b.op('MINIMUM',g,blue))-.588)/.275).clamp();teeth=1-.10*mouth*white*(1-((song-4430).clamp()))
av=s.view_layers[0].aovs.add();av.name='Teeth';av.type='VALUE';node=b.n.new('ShaderNodeOutputAOV');node.aov_name='Teeth';b.plug(teeth,node.inputs['Value'])
'''+code[at:]
needle="s.render.image_settings.file_format='PNG'"
at=code.index(needle)
code=code[:at]+'''
result=b.combine([(a+b.linear(z.clamp())+b.linear(q.clamp())).clamp() for a,z,q in zip(b.split(rl.outputs['Image']),delta,roomdelta)])
# Apply the tiny local highlight correction in the material instead of an AOV multiplier.
b.plug(b.mix(result,rl.outputs['Green']),outnode.inputs['Image'])
'''+code[at:]
code=code.replace("b.plug(warped.outputs['Color'],em.inputs[0])", "b.plug(b.mix(warped.outputs['Color'],b.combine([teeth]*3),mode='MULTIPLY'),em.inputs[0])")
exec(compile(code,str(O/'afterglow_native.py'),'exec'))
