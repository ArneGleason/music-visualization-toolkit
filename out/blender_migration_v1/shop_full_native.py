"""Combine the accepted native optics graph with native alien-head hoops."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'orb_native.py').read_text().replace("D=O/'orb'","D=O/'shop_full'").replace('s.frame_end=128','s.frame_end=85').replace("f'orb_{W}.blend'","f'shop_full_{W}.blend'").replace('range(1,129)','range(1,86)')
code=code.replace('gain=.85','gain=.8').replace('gain*=.22 if 2271+frame-1>=2366 else .45','gain*=.38').replace('if 0<=age<8 else 0','if 0<=age<8 and frame<35 else 0')
a=code.index("im=bpy.data.images.load");z=code.index("rl=b.n.new",a)
code=code[:a]+'''
with bpy.data.libraries.load(str(O/'shop_optics'/f'shop_optics_{W}.blend'),link=False) as (src,dst):
 dst.node_groups=['Shop native optical sampling']
optics=b.n.new('CompositorNodeGroup');optics.node_tree=dst.node_groups[0]
pic=[b.display(v) for v in b.split(optics.outputs['Image'])]
'''+code[z:]
code=code.replace('(2,2,2,1)','(1.1,1.1,1.1,1)').replace('[(3,2.4),(11,2.9)]','[(3,2),(12,2.5)]').replace('[1,.5,.1]','[1,.55,.10]').replace('*1.7','*1.5')
at=code.index('cyan,amber,_=b.split(beam)')
code=code[:at]+'''
blur=[float(np.exp(-.5*((sf-2429.5)/1.5)**2)) for sf in range(2399,2484)]
samples=[]
for j in range(13):
 transform=b.n.new('CompositorNodeTransform');b.plug(beam,transform.inputs['Image'])
 for f,v in enumerate(blur,1):
  scale=1+(-.20+j*.40/12)*v
  transform.inputs['Scale'].default_value=scale;transform.inputs['Scale'].keyframe_insert('default_value',frame=f)
  transform.inputs['Y'].default_value=(1-scale)*90*W/1280;transform.inputs['Y'].keyframe_insert('default_value',frame=f)
 samples.append(transform.outputs[0])
beam=samples[0]
for i,im in enumerate(samples[1:],2):beam=b.mix(beam,im,1/i,mode='MIX')
n=b.n.new('CompositorNodeBlur');b.plug(beam,n.inputs['Image'])
for f,v in enumerate(blur,1):n.inputs['Size'].default_value=(27*v*W/1280,)*2;n.inputs['Size'].keyframe_insert('default_value',frame=f)
beam=n.outputs[0]
'''+code[at:]
code=code.replace("selected=list(map(int,args[1].split(','))) if len(args)>1 else range(1,86)","selected=[] if len(args)>1 and args[1]=='build' else list(map(int,args[1].split(','))) if len(args)>1 else range(1,86)")
exec(compile(code,str(O/'orb_native.py'),'exec'))
