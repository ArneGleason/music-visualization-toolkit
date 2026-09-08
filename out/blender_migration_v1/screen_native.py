"""Extend the accepted native message recipe with a tracked native screen map."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'message_native.py').read_text()
needle="em=b.n.new('ShaderNodeEmission'); em.inputs[0].default_value=(0,0,0,1)"
assert code.count(needle)==1
code=code.replace(needle,(O/'screen_fields.py').read_text()+'\n'+needle)
needle="result=b.combine([b.linear((a+z).clamp()) for a,z in zip(b.split(lit),b.split(glow))]); end=b.n.new('NodeGroupOutput'); b.plug(result,end.inputs['Image'])"
replacement="""fade=b.animated('Receiver effect settles',[1-smooth((v['song_frame']-1201)/24) for v in rows])
base=[(a+z*fade).clamp() for a,z in zip(b.split(lit),b.split(glow))]
grow=b.animated('DEAL screen expansion',[smooth((v['song_frame']-1246)/12) for v in rows])
small=[b.display(v) for v in b.split(rl['sprite'].outputs['ScreenSmall'])]
large=[b.display(v) for v in b.split(rl['sprite'].outputs['ScreenExpanded'])]
full=[b.display(v) for v in b.split(rl['sprite'].outputs['ScreenFull'])]
mask=b.split(rl['sprite'].outputs['ScreenMask'])[0]; expanded=b.split(rl['sprite'].outputs['ExpandedMask'])[0]
result=b.combine([b.linear(((a*(1-mask)+z*mask)*(1-expanded)+(q*(1-grow)+r*grow)*expanded).clamp()) for a,z,q,r in zip(base,small,large,full)])
end=b.n.new('NodeGroupOutput'); b.plug(result,end.inputs['Image'])"""
assert code.count(needle)==1; code=code.replace(needle,replacement).replace("f'message_{W}.blend'","f'screen_{W}.blend'")
exec(compile(code,str(O/'message_native.py'),'exec'))
