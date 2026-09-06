"""FX-03: native Blender compositor displacement driven by a shallow lens field."""
import json
import math
import pathlib
import sys
import bpy
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import garden_dust_pilot as audio
from screen_sync_pilot import command

ROOT=audio.ROOT
OUT=ROOT/'out/pressure_lens_rockets'
EXAGGERATED='--exaggerated' in sys.argv
if EXAGGERATED:
    OUT=ROOT/'out/pressure_lens_rockets_exaggerated'


def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'frames').mkdir(exist_ok=True)
    cues=json.loads((ROOT/'generated/overlay_cues.json').read_text())
    cue=next(s for s in cues['shots'] if s['id']=='s037')
    first,end=cue['start'],cue['end']; count=end-first
    shot=next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots'] if s['id']=='s037')
    assert shot['frames']==count and shot['clip']['speed']==1
    audio.FIRST,audio.END=first,end
    times,bass,events=audio.controls()
    if EXAGGERATED:
        # Two isolated actual attacks, with quiet gaps to reveal the added effect.
        selected=[]
        for target in (.6,1.8):
            candidates=[e for e in events if first/24<=e['song_sec']<end/24
                        and e['strength']>.3]
            event=min(candidates,key=lambda e:abs(e['song_sec']-first/24-target))
            if event not in selected:
                selected.append(event)
        events=selected
    raw=command(['ffmpeg','-v','error','-ss',str(shot['clip']['in_sec']),'-i',str(ROOT/shot['clip']['file']),
        '-frames:v',str(count),'-vf','scale=1280:720','-f','rawvideo','-pix_fmt','rgb24','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(count,720,1280,3)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene; sc.render.engine='BLENDER_EEVEE'
    sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.render.fps=24
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='None'
    bpy.ops.object.camera_add(); sc.camera=bpy.context.object
    tree=bpy.data.node_groups.new('Localized pressure lens','CompositorNodeTree')
    sc.compositing_node_group=tree
    tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    output=tree.nodes.new('NodeGroupOutput')
    source=bpy.data.images.new('Source motion',1280,720,float_buffer=True)
    source.colorspace_settings.name='Non-Color'
    source_node=tree.nodes.new('CompositorNodeImage'); source_node.image=source
    combine=tree.nodes.new('CompositorNodeCombineColor')
    maps=[]
    for index,factor in enumerate([1.06,1.,.94]):
        field=bpy.data.images.new('Lens vector '+str(index),1280,720,float_buffer=True)
        field.colorspace_settings.name='Non-Color'; maps.append((field,factor))
        map_node=tree.nodes.new('CompositorNodeImage'); map_node.image=field
        displace=tree.nodes.new('CompositorNodeDisplace')
        displace.inputs['Interpolation'].default_value='Bicubic'
        displace.inputs['Extension X'].default_value='Extend'
        displace.inputs['Extension Y'].default_value='Extend'
        tree.links.new(source_node.outputs['Image'],displace.inputs['Image'])
        tree.links.new(map_node.outputs['Image'],displace.inputs['Displacement'])
        split=tree.nodes.new('CompositorNodeSeparateColor')
        tree.links.new(displace.outputs[0],split.inputs[0]); tree.links.new(split.outputs[index],combine.inputs[index])
    combine.inputs[3].default_value=1
    tree.links.new(combine.outputs[0],output.inputs[0])
    yy,xx=np.mgrid[:720,:1280].astype(np.float32)
    # Broad background exhaust corridor; foreground performer and frame edges protected.
    boundary=np.clip((yy-120)/100,0,1)*np.clip((590-yy)/110,0,1)
    boundary*=np.clip(xx/90,0,1)*np.clip((1279-xx)/90,0,1)
    person=np.clip((np.sqrt(((xx-635)/175)**2+((yy-610)/220)**2)-1)/.3,0,1)
    boundary*=person
    diagnostics=[]
    for f in range(count):
        t=(first+f+.5)/24
        height=np.zeros_like(xx)
        for event in events:
            age=t-event['song_sec']
            duration=.65 if EXAGGERATED else .9
            if 0<age<duration:
                # Elliptical expanding wave, with small coherent irregularities.
                r=np.sqrt((xx-640)**2+((yy-425)*1.65)**2)
                wrinkle=6*np.sin(xx*.025+yy*.019+t*2)*np.sin(yy*.031-t*1.4)
                radius=110+age*750 if EXAGGERATED else 35+age*470
                q=(r+wrinkle-radius)/(48 if EXAGGERATED else 35)
                envelope=np.exp(-age/1.0)
                if EXAGGERATED:
                    envelope=(1-math.exp(-age/.025))*min(1,(duration-age)/.13)
                height+=event['strength']*envelope*np.exp(-q*q*.5)*(3000 if EXAGGERATED else 350)
        dy,dx=np.gradient(height)
        dx*=boundary; dy*=boundary
        # Cap displacement to a readable, local optical bend, never a frame zoom.
        length=np.hypot(dx,dy); limit=np.minimum(1,(60 if EXAGGERATED else 14)/np.maximum(length,.001))
        dx*=limit; dy*=limit
        rgb=frames[f].astype(np.float32)/255
        rgb=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
        rgba=np.concatenate([rgb,np.ones((720,1280,1),np.float32)],axis=2)
        source.pixels.foreach_set(rgba[::-1].ravel()); source.update()
        for field,factor in maps:
            data=np.zeros((720,1280,4),np.float32); data[:,:,3]=1
            data[:,:,0]=dx*factor; data[:,:,1]=-dy*factor
            field.pixels.foreach_set(data[::-1].ravel()); field.update()
        sc.render.filepath=str(OUT/'frames'/f'{f:04d}.png')
        bpy.ops.render.render(write_still=True)
        diagnostics.append({'song_frame':first+f,'max_displacement_px':float(np.max(np.hypot(dx,dy)))})
    command(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/'frames/%04d.png'),
        '-ss',str(first/24),'-i',str(ROOT/'audio/song.wav'),'-t',str(count/24),
        '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
        '-movflags','+faststart',str(OUT/'pressure_lens.mp4')])
    (OUT/'controls.json').write_text(json.dumps({'shot':'s037','source':shot['clip'],
        'song_frames':[first,end],'events':events,'diagnostics':diagnostics,
        'exaggerated':EXAGGERATED,
        'method':'Blender Displace compositor, lens-height gradient; not ray-traced glass',
        'mask':'authored background corridor and foreground exclusion; not tracked',
        'dispersion_factors':[1.06,1,.94],'assembly_change':False},indent=2))


if __name__=='__main__':
    main()
