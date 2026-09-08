"""Native compositor proof of the accepted two-plate snap zoom, without FX."""
import bpy,sys,math,json
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
from native_nodes import Builder
D=O/'shop_optics'; args=sys.argv[sys.argv.index('--')+1:]; W=int(args[0]); H=W*9//16
frames=list(range(2399,2484)); ratio=W/1280
def smooth(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=W;s.render.resolution_y=H
s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=85
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
bpy.ops.object.camera_add(location=(0,0,10));s.camera=bpy.context.object
tree=bpy.data.node_groups.new('Shop native optical sampling','CompositorNodeTree')
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=tree
b=Builder(tree)
def animate(socket,values):
    for f,v in enumerate(values,1):socket.default_value=v;socket.keyframe_insert('default_value',frame=f)
def sequence(name,offset):
    im=bpy.data.images.load(str(D/name/'0001.png'));im.source='SEQUENCE'
    node=b.n.new('CompositorNodeImage');node.image=im;node.frame_duration=len(list((D/name).glob('*.png')))
    node.frame_start=1;node.frame_offset=offset;node.use_auto_refresh=True
    size=b.n.new('CompositorNodeScale');size.inputs['Type'].default_value='Absolute';b.plug(node.outputs['Image'],size.inputs['Image'])
    size.inputs['X'].default_value=W;size.inputs['Y'].default_value=H
    # Match approved display-space resampling, then convert back at output.
    return b.combine([b.display(v) for v in b.split(size.outputs[0])])
wide=sequence('wide',12)
# Start the close sequence at local frame 27, its song-frame origin 2425.
close=sequence('close',0)
for node in b.n:
    if node.bl_idname=='CompositorNodeImage' and 'close' in node.image.filepath:node.frame_start=27
switch=b.animated('Hard switch at song frame 2431',[int(sf>=2431) for sf in frames])
plate=b.mix(wide,close,switch,mode='MIX')
def transform(image,scale,x,y,label):
    n=b.n.new('CompositorNodeTransform');n.label=label;b.plug(image,n.inputs['Image'])
    n.inputs['Extension X'].default_value='Extend';n.inputs['Extension Y'].default_value='Extend'
    animate(n.inputs['Scale'],scale);animate(n.inputs['X'],[v*ratio for v in x]);animate(n.inputs['Y'],[v*ratio for v in y])
    return n.outputs[0]
def average(images):
    result=images[0]
    for i,img in enumerate(images[1:],2):result=b.mix(result,img,1/i,mode='MIX')
    return result
samples=[]
for sample in range(17):
    dt=-.65+sample*1.3/16;zs=[];xs=[];ys=[]
    for sf in frames:
        if sf<2424 or sf>=2436:z=1;left=top=0
        elif sf<2431:
            a=max(0,min(1,(sf+dt-2424)/6))**1.8
            z=1280/(1280+(800/1.2-1280)*a);left=520*a;top=(64/1.2)*a
        else:
            z=1+.075*(1-smooth((sf+dt-2431)/5))
            left=(1280-1280/z)*.5;top=(720-720/z)*.4
        zs.append(z);xs.append((640-left)*z-640);ys.append(360-(360-top)*z)
    samples.append(transform(plate,zs,xs,ys,f'Optical shutter sample {sample+1}/17'))
picture=average(samples); streaks=[]
for j in range(13):
    scales=[1+(-.1+j*.2/12)*math.exp(-.5*((sf-2430.5)/1.25)**2) if 2424<=sf<2436 else 1 for sf in frames]
    streaks.append(transform(picture,scales,[0]*85,[(1-v)*90 for v in scales],f'Radial streak {j+1}/13'))
picture=average(streaks)
n=b.n.new('CompositorNodeBlur');b.plug(picture,n.inputs['Image'])
animate(n.inputs['Size'],[(3*max(.1,11*math.exp(-.5*((sf-2430.5)/1.25)**2))*ratio,)*2 if 2424<=sf<2436 else (0,0) for sf in frames])
out=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear(v.clamp()) for v in b.split(n.outputs[0])]),out.inputs['Image'])
dest=D/f'native_{W}';dest.mkdir(exist_ok=True);s.frame_set(1);s.render.filepath=str(dest/'0001.png')
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'shop_optics_{W}.blend'))
selected=list(map(int,args[1].split(','))) if len(args)>1 else range(1,86)
for f in selected:s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
