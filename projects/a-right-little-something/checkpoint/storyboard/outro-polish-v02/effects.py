"""V65: three-layer sphere optics, departure light, camera push, portrait slip."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np

OUT=Path(__file__).resolve().parent
V63=OUT.parent/'first-contact-motion-v02'
V64=OUT.parent/'outro-polish-v01'
parser=argparse.ArgumentParser()
parser.add_argument('--shot',choices=['opening','travel','planet-push','system-departure','finale'],required=True)
parser.add_argument('--preview',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
counts={'opening':68,'travel':42,'planet-push':46,'system-departure':173,'finale':235}
count=counts[args.shot]
edit_count=count-(0 if args.shot=='finale' else 8)
source_blend={
    'opening':V63/'opening.blend','travel':V63/'travel.blend',
    'system-departure':V64/'contact-027.blend','finale':V64/'finale.blend'}
if args.shot in source_blend:
    bpy.ops.wm.open_mainfile(filepath=str(source_blend[args.shot]))
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=1
    scene.cycles.use_denoising=False
    cam=bpy.data.objects.new('Compositor camera',bpy.data.cameras.new('Compositor camera'))
    scene.collection.objects.link(cam)
    scene.camera=cam
    group=bpy.data.node_groups.new('V65 planet push','CompositorNodeTree')
    group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    scene.compositing_node_group=group
    group.nodes.new('NodeGroupOutput')

scene=bpy.context.scene
group=scene.compositing_node_group
nodes,links=group.nodes,group.links
output=next(n for n in nodes if n.bl_idname=='NodeGroupOutput')
scene.render.threads_mode='FIXED'
scene.render.threads=8
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.render.fps=24
scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.frame_start=1
scene.frame_end=count

def sequence(path,label):
    n=nodes.new('CompositorNodeImage')
    n.name=label
    n.image=bpy.data.images.load(str(path))
    if path.suffix=='.exr':
        n.image.colorspace_settings.name='Non-Color'
    n.image.source='SEQUENCE'
    n.frame_duration=count
    n.frame_start=1
    n.use_auto_refresh=True
    return n.outputs['Image']

def key(node,name,value,frame):
    node.inputs[name].default_value=value
    node.inputs[name].keyframe_insert(data_path='default_value',frame=frame)

def transform(source,label):
    n=nodes.new('CompositorNodeTransform')
    n.name=label
    n.inputs['Interpolation'].default_value='Bicubic'
    links.new(source,n.inputs['Image'])
    return n

def mix(a,b,mode,label):
    n=nodes.new('ShaderNodeMix')
    n.data_type='RGBA'
    n.blend_type=mode
    n.name=label
    n.inputs[0].default_value=1
    links.new(a,n.inputs[6])
    links.new(b,n.inputs[7])
    return n

if args.shot in ['opening','travel']:
    opening=args.shot=='opening'
    over=next(n for n in nodes if n.bl_idname=='CompositorNodeAlphaOver')
    original_result=output.inputs['Image'].links[0].from_socket
    # Realize the background alone, retaining the identical V63 foreground
    # graph. The middle optics never process Harper, hull, or ship lighting.
    if opening:
        background_folder=OUT/'opening-background-frames'
        background_folder.mkdir(exist_ok=True)
        links.new(over.inputs['Background'].links[0].from_socket,output.inputs['Image'])
        scene.render.filepath=str(background_folder/'frame_')
        bpy.ops.render.render(animation=True)
        links.new(original_result,output.inputs['Image'])
    else:
        background_folder=V64/'travel-background-frames'
    background=sequence(background_folder/'frame_0001.png','1 / Independent warp background')
    maps=OUT/(args.shot+'-sphere-maps')
    maps.mkdir(exist_ok=True)
    y,x=np.mgrid[0:1080,0:1920].astype(np.float32)
    uv=bpy.data.images.new('Sphere refraction data',1920,1080,float_buffer=True)
    tint=bpy.data.images.new('Dark blue cyan transmission data',1920,1080,float_buffer=True)
    for im in [uv,tint]:
        im.colorspace_settings.name='Non-Color'
        im.file_format='OPEN_EXR'
    for f in range(1,count+1):
        t=(f-1)/(edit_count-1)
        if opening:
            t=min(t,1)
            s=1-.20*t
            cx=960+(930-960)*s+50*t
            cy=540+(542-540)*s+60*t
            rx,ry=365*s,355*s
        else:
            s=1-.025*t
            cx=960+(840-960)*s+10*t
            cy=540+(522-540)*s+3*math.sin(t*math.pi)
            rx=ry=350*s
        r2=((x-cx)/rx)**2+((y-cy)/ry)**2
        mask=np.clip((1-r2)/.055,0,1)
        mask=mask*mask*(3-2*mask)
        curve=np.maximum(0,1-r2)**1.15
        pixels=np.ones((1080,1920,4),dtype=np.float32)
        pixels[:,:,0]=(x+.5-(x-cx)*.028*curve)/1920
        pixels[:,:,1]=(y+.5-(y-cy)*.028*curve)/1080
        uv.pixels.foreach_set(pixels.ravel())
        uv.filepath_raw=str(maps/f'uv_{f:04}.exr')
        uv.save()
        depth=mask*(.90+.10*np.clip(r2,0,1))
        # Stronger than V64's .36/.20/.13 absorption. This is linear-light
        # background transmission, not a color wash over the foreground plate.
        pixels[:,:,:3]=1-depth[:,:,None]*np.array([.90,.77,.60],dtype=np.float32)
        tint.pixels.foreach_set(pixels.ravel())
        tint.filepath_raw=str(maps/f'tint_{f:04}.exr')
        tint.save()
    refract=nodes.new('CompositorNodeMapUV')
    refract.name='2a / Sphere-local refraction of background only'
    links.new(background,refract.inputs['Image'])
    links.new(sequence(maps/'uv_0001.exr','Middle layer / refraction mask'),refract.inputs['UV'])
    transmission=mix(refract.outputs['Image'],sequence(maps/'tint_0001.exr','Middle layer / transmission mask'),'MULTIPLY','2b / Dark cyan optical transmission')
    links.new(transmission.outputs[2],over.inputs['Background'])
    over.name='3 / Unaltered ship and Harper foreground above optics'
    scene['layer_stack']='1 warp background; 2 masked spherical refraction and dark cyan transmission; 3 original keyed ship and Harper. Foreground is untouched.'
    scene['linear_absorption']=[.90,.77,.60]
elif args.shot=='planet-push':
    move=transform(sequence(OUT/'sources/planet-push/frame_0001.png','Retained V64 Harper / planet source'),'Push and pan toward planet side')
    for f in range(1,count+1):
        t=(f-1)/(edit_count-1)
        key(move,'Scale',1.015+.075*t,f)
        key(move,'X',-8-56*t,f)
        key(move,'Y',12*t,f)
    links.new(move.outputs['Image'],output.inputs['Image'])
elif args.shot=='finale':
    portrait=next(n for n in nodes if n.bl_idname=='CompositorNodeImage' and 'harper-portrait' in n.name)
    portrait.image=bpy.data.images.load(str(OUT/'sources/harper-advanced/frame_0001.png'))
    portrait.image.source='SEQUENCE'
    portrait.frame_duration=count
    portrait.frame_start=1
    portrait.frame_offset=0
    portrait.use_auto_refresh=True
    portrait.name='Harper source advanced 48 frames / starts native frame73'
    scene['production_note']='V65 portrait slips forward two seconds in its source. Cosmic input and 3:34–3:36 fade remain unchanged. Held portrait tail is already fully invisible.'
else:
    result=output.inputs['Image'].links[0].from_socket
    # Reference centers are measured from V64's realized camera move; the
    # departure anchor follows the planet before the light escapes its orbit.
    anchors=[(1,957,550,198),(82,932,560,200),(165,904,570,199)]
    def planet(f):
        a,b=anchors[:2] if f<=82 else anchors[1:]
        t=(f-a[0])/(b[0]-a[0])
        return [a[i]+(b[i]-a[i])*t for i in range(1,4)]
    def sprite(label,flare=False):
        size=192 if flare else 96
        y,x=np.mgrid[0:size,0:size].astype(np.float32)
        dx=x-(size-1)/2
        dy=y-(size-1)/2
        r2=dx*dx+dy*dy
        if flare:
            light=np.exp(-r2/10)*2+np.exp(-r2/240)*.14
            light+=np.exp(-abs(dx)/20-abs(dy)/1.2)*.8
            light+=np.exp(-abs(dx)/1.2-abs(dy)/16)*.7
        else:
            light=np.exp(-r2/3.0)*3+np.exp(-r2/55)*.12
        rgba=np.ones((size,size,4),dtype=np.float32)
        rgba[:,:,:3]=light[:,:,None]*[.32,.80,1.0]
        im=bpy.data.images.new(label,size,size,float_buffer=True)
        im.colorspace_settings.name='Non-Color'
        im.pixels.foreach_set(rgba.ravel())
        im.pack()
        n=nodes.new('CompositorNodeImage')
        n.image=im
        return n.outputs['Image']
    flare=transform(sprite('Cyan departure swell and twinkle',True),'Departure twinkle anchored to central world')
    add_flare=mix(result,flare.outputs['Image'],'ADD','Brief orbit departure twinkle')
    dot=transform(sprite('Small departing ship point'),'Accelerating curved escape trajectory')
    add_dot=mix(add_flare.outputs[2],dot.outputs['Image'],'ADD','Small ship light after twinkle')
    tracks=[]
    for f in range(1,count+1):
        global_frame=4483+f
        cx,cy,r=planet(f)
        ax=cx+(r+13)*math.cos(math.radians(-20))
        ay=cy+(r+13)*math.sin(math.radians(-20))
        pulse=max(0,1-abs(global_frame-4567)/22)**1.7 if global_frame>=4550 else 0
        key(flare,'X',ax-960,f)
        key(flare,'Y',540-ay,f)
        key(flare,'Scale',.45+1.25*pulse,f)
        key(add_flare,0,1.7*pulse,f)
        u=max(0,min(1,(global_frame-4583)/(4648-4583)))**1.85
        bx=3*(1-u)**2*u*60+3*(1-u)*u*u*310+u**3*630
        by=3*(1-u)**2*u*(-90)+3*(1-u)*u*u*(-90)+u**3*(-25)
        key(dot,'X',ax+bx-960,f)
        key(dot,'Y',540-(ay+by),f)
        key(dot,'Scale',1-.2*u,f)
        power=max(0,min(1,(global_frame-4557)/10))
        key(add_dot,0,1.4*power,f)
        tracks.append(dict(frame=global_frame,x=round(ax+bx,3),y=round(ay+by,3),escapeProgress=round(u,5)))
    links.new(add_dot.outputs[2],output.inputs['Image'])
    manifest=json.loads((OUT/'source-manifest.json').read_text(encoding='utf-8'))
    manifest['systemDeparture']['tracks']=tracks
    (OUT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    scene['departure_note']='Twinkle peaks on DAW bar72 beat3 (4567); light accelerates from beat4 (4583) into a curved outward trajectory, no route line.'

folder=OUT/(args.shot+'-frames')
folder.mkdir(exist_ok=True)
scene.render.filepath=str(folder/'frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(args.shot+'.blend')))
if args.preview:
    frames={'system-departure':[84,117,165],'finale':[1,72,130,155]}.get(args.shot,[1,edit_count//2,edit_count])
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath=str(OUT/f'{args.shot}-preview-{f:03}.png')
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
