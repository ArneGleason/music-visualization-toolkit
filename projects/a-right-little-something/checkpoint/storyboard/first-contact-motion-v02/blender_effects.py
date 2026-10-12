"""Editable V63 composites, gentle camera moves, and tracked star twinkles."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np

OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--shot',choices=['opening','travel','tidal','stars','ground'],required=True)
parser.add_argument('--preview',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=1;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.fps=24;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
cam=bpy.data.objects.new('Compositor camera',bpy.data.cameras.new('Compositor camera'))
scene.collection.objects.link(cam);scene.camera=cam
group=bpy.data.node_groups.new('V63 '+args.shot,'CompositorNodeTree')
group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
scene.compositing_node_group=group
nodes,links=group.nodes,group.links
length={'opening':68,'travel':42,'tidal':41,'stars':122,'ground':53}[args.shot]
edit_length=length-8
scene.frame_start=1;scene.frame_end=length

def image(path,sequence=0,label=''):
    node=nodes.new('CompositorNodeImage');node.name=label or path.stem
    node.image=bpy.data.images.load(str(path))
    if sequence:
        node.image.source='SEQUENCE';node.frame_duration=sequence;node.frame_start=1;node.use_auto_refresh=True
    else:node.image.pack()
    if tuple(node.image.size)!=(1920,1080):
        scale=nodes.new('CompositorNodeScale');scale.inputs['Type'].default_value='Absolute'
        scale.inputs['X'].default_value=1920;scale.inputs['Y'].default_value=1080
        scale.inputs['Interpolation'].default_value='Bicubic';links.new(node.outputs['Image'],scale.inputs['Image'])
        return scale.outputs['Image']
    return node.outputs['Image']

def sequence(name):return image(OUT/'sources'/name/'frame_0001.png',length,name)
def transform(source,label):
    node=nodes.new('CompositorNodeTransform');node.name=label
    node.inputs['Interpolation'].default_value='Bicubic'
    links.new(source,node.inputs['Image']);return node
def key(node,name,value,frame):
    node.inputs[name].default_value=value;node.inputs[name].keyframe_insert(data_path='default_value',frame=frame)
def mix(a,b,mode,label):
    node=nodes.new('ShaderNodeMix');node.data_type='RGBA';node.blend_type=mode
    node.inputs[0].default_value=1;node.name=label
    links.new(a,node.inputs[6]);links.new(b,node.inputs[7]);return node
def math_node(operation,a,b,label):
    node=nodes.new('ShaderNodeMath');node.operation=operation;node.name=label
    for i,value in enumerate([a,b]):
        if isinstance(value,(int,float)):node.inputs[i].default_value=value
        else:links.new(value,node.inputs[i])
    return node.outputs[0]
def magenta_key(source):
    separate=nodes.new('CompositorNodeSeparateColor');links.new(source,separate.inputs['Image'])
    r,g,b=[separate.outputs[x] for x in ['Red','Green','Blue']]
    minimum=math_node('MINIMUM',r,b,'Magenta common red and blue')
    excess=math_node('SUBTRACT',minimum,g,'Magenta exceeds green')
    spill=math_node('MAXIMUM',excess,0,'Only magenta spill')
    amount=math_node('DIVIDE',spill,.50,'Key tolerance')
    inverse=math_node('SUBTRACT',1,amount,'Foreground opacity')
    alpha=math_node('MAXIMUM',inverse,0,'Clamp transparent background')
    combine=nodes.new('CompositorNodeCombineColor');combine.name='Neutralize magenta spill, retain cyan and amber'
    links.new(math_node('SUBTRACT',r,spill,'Despill red'),combine.inputs['Red'])
    links.new(g,combine.inputs['Green'])
    links.new(math_node('SUBTRACT',b,spill,'Despill blue'),combine.inputs['Blue'])
    links.new(alpha,combine.inputs['Alpha'])
    return combine.outputs['Image']
def point_sprite(label,size=128,spread=1):
    y,x=np.mgrid[0:size,0:size].astype(np.float32);dx=x-(size-1)/2;dy=y-(size-1)/2
    r2=dx*dx+dy*dy
    light=np.exp(-r2/(3.5*spread**2))*.85+np.exp(-r2/(100*spread**2))*.025
    light+=np.exp(-np.abs(dx)/(10*spread)-np.abs(dy)/.7)*.26
    light+=np.exp(-np.abs(dx)/.7-np.abs(dy)/(8*spread))*.20
    rgba=np.ones((size,size,4),dtype=np.float32);rgba[:,:,:3]=light[:,:,None]*[.48,.73,1]
    im=bpy.data.images.new(label,width=size,height=size,float_buffer=True)
    im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(rgba.ravel());im.pack()
    n=nodes.new('CompositorNodeImage');n.image=im;return n.outputs['Image']

if args.shot in ('opening','travel'):
    opening=args.shot=='opening';kind='rear' if opening else 'side'
    plate=OUT/'sources'/f'warp-{kind}-plate-v01-source1'/'frame_0001.png'
    foreground=image(plate,length,'Independent native ship and Harper video') if plate.exists() else image(OUT/f'ship-{kind}-chroma.png',label='Still preflight of separate ship plate')
    ship=transform(magenta_key(foreground),'Stable ship travel / passenger animation independent')
    bg=image(OUT/f'warp-{kind}-background.png',label='Independent illustrated warp environment')
    bgmove=transform(bg,'Forward flow and slight tunnel twist')
    over=nodes.new('CompositorNodeAlphaOver');over.inputs['Factor'].default_value=1
    over.inputs['Straight Alpha'].default_value=True
    over.name='Simple two-plate composite / reflections intentionally deferred'
    links.new(bgmove.outputs['Image'],over.inputs['Background']);links.new(ship.outputs['Image'],over.inputs['Foreground'])
    result=over.outputs['Image']
    vx,vy=(264,274) if opening else (695,275)
    for f in range(1,length+1):
        t=(f-1)/(edit_length-1)
        s=1.04+(.40 if opening else .30)*t
        angle=(.018 if opening else -.012)*t
        key(bgmove,'Scale',s,f);key(bgmove,'Angle',angle,f)
        # Zoom around the tunnel's own vanishing point rather than the frame center.
        key(bgmove,'X',vx-s*(vx*math.cos(angle)-vy*math.sin(angle)),f)
        key(bgmove,'Y',vy-s*(vx*math.sin(angle)+vy*math.cos(angle)),f)
        if opening:
            key(ship,'Scale',1-.20*min(t,1),f)
            key(ship,'X',50*min(t,1),f);key(ship,'Y',60*min(t,1),f)
        else:
            key(ship,'Scale',1-.025*t,f)
            key(ship,'X',10*t,f);key(ship,'Y',3*math.sin(t*math.pi),f)
    # Drive initiation is a short localized glow, not a second ship or portal.
    if opening:
        pulse=transform(point_sprite('Compact drive initiation pulse',256,3),'Drive glow position')
        for f in range(1,length+1):
            t=min((f-1)/(edit_length-1),1)
            key(pulse,'X',(850-960)*(1-.20*t)+50*t,f)
            key(pulse,'Y',(540-682)*(1-.20*t)+60*t,f)
        add=mix(result,pulse.outputs['Image'],'ADD','Single compact initiation pulse')
        for f,power in [(1,0),(5,.5),(10,1.4),(15,.3),(18,0),(length,0)]:
            add.inputs[0].default_value=power;add.inputs[0].keyframe_insert(data_path='default_value',frame=f)
        result=add.outputs[2]
    scene['composite_note']='Independent ship/passenger native video over Blender-animated warp background. First simple composite; reflected streak synthesis deferred.'
elif args.shot in ('tidal','ground'):
    sid='contact-017' if args.shot=='tidal' else 'contact-022'
    move=transform(sequence(sid),'Gentle pan and pullout' if args.shot=='tidal' else 'Gentle grounded push')
    for f in range(1,length+1):
        t=(f-1)/(edit_length-1)
        key(move,'Scale',1.065-.04*t if args.shot=='tidal' else 1.025+.025*t,f)
        key(move,'X',-12+22*t if args.shot=='tidal' else 4-10*t,f)
        key(move,'Y',2*(1-t),f)
    result=move.outputs['Image']
else:
    result=sequence('contact-020')
    tracks=json.loads((OUT/'star-tracks.json').read_text())
    sprite=point_sprite('Subtle blue-white star scintillation')
    for i,track in enumerate(tracks):
        position=transform(sprite,f'Star {i+1} tracked to original sky')
        add=mix(result,position.outputs['Image'],'ADD',f'Independent star {i+1} twinkle')
        for f,(x,y) in enumerate(track,1):
            key(position,'X',x-960,f);key(position,'Y',540-y,f)
            t=(f-1)/24
            p=(.5+.5*math.sin(t*(2.1+i*.16)+i*1.07))**5
            add.inputs[0].default_value=.12+.72*p
            add.inputs[0].keyframe_insert(data_path='default_value',frame=f)
        result=add.outputs[2]
    scene['twinkle_note']='Six existing stars tracked through original camera motion; independent soft pulses, no new constellation.'

output=nodes.new('NodeGroupOutput');links.new(result,output.inputs['Image'])
folder=OUT/(args.shot+'-frames');folder.mkdir(exist_ok=True)
scene.render.filepath=str(folder/'frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(args.shot+'.blend')))
if args.preview:
    for f in [1,edit_length//2,edit_length]:
        scene.frame_set(f);scene.render.filepath=str(OUT/f'{args.shot}-preview-{f:03}.png')
        bpy.ops.render.render(write_still=True)
else:bpy.ops.render.render(animation=True)
