"""Frame-timed chorus revision: coverage, camera drift, transitions and routes."""
import argparse
import copy
import html
import json
import math
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFilter
from lyric_overlay import write_lyrics


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def run(args, cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=cwd,check=True)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]


def encode(args, count, target, cwd=None):
    run([*args,'-frames:v',str(count),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(target)],cwd)


def route_overlay(out, frames, track):
    """One moving ship and its exact curve, anchored to observed world positions."""
    out.mkdir(exist_ok=True)
    def anchors(frame):
        a,b = track[0],track[-1]
        for left,right in zip(track,track[1:]):
            if left['frame']<=frame<=right['frame']:
                a,b = left,right
                break
        t=max(0,min(1,(frame-a['frame'])/max(1,b['frame']-a['frame'])))
        return [tuple((1-t)*x+t*y for x,y in zip(p,q)) for p,q in zip(a['anchors'],b['anchors'])]
    def bezier(p0,p1,p2,p3,t):
        return tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3))
    for frame in range(frames):
        a,b,c=anchors(frame)
        p1=(a[0]+(b[0]-a[0])*.2,a[1]-(a[1]-b[1])*.8)
        p2=(b[0]-(b[0]-a[0])*.2,b[1]-.05)
        p3=(b[0]+(c[0]-b[0])*.35,b[1]+.05)
        p4=(c[0]-.12,c[1]-.02)
        points=[bezier(a,p1,p2,b,i/100) for i in range(101)]
        points += [bezier(b,p3,p4,c,i/100) for i in range(1,101)]
        points=[(x*3840,y*2160) for x,y in points]
        u=max(0,min(1,(frame-12)/max(1,frames-36)))
        u=u*u*(3-2*u)
        index=min(199,int(u*200))
        layer=Image.new('RGBA',(3840,2160))
        draw=ImageDraw.Draw(layer)
        draw.line(points,fill=(90,200,255,55),width=2)
        if index:
            draw.line(points[:index+1],fill=(255,185,100,180),width=4)
        x,y=points[index]
        draw.ellipse((x-6,y-6,x+6,y+6),fill=(180,245,255,220))
        glow=layer.filter(ImageFilter.GaussianBlur(7))
        layer=Image.alpha_composite(glow,layer)
        draw=ImageDraw.Draw(layer)
        # Tiny spherical craft: transparent field, equatorial band and rear arc.
        draw.ellipse((x-9,y-9,x+9,y+9),outline=(130,230,255,200),width=2)
        draw.ellipse((x-12,y-3,x+12,y+3),outline=(255,209,135,255),width=3)
        draw.arc((x-4,y-11,x+5,y+1),90,270,fill=(120,250,255,255),width=2)
        layer.resize((1920,1080),Image.Resampling.LANCZOS).save(out/f'{frame+1:04}.png')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path)
    parser.add_argument('revision',type=Path)
    parser.add_argument('--publish-version',default='v21')
    parser.add_argument('--reuse-prepared',action='store_true',help='Reuse already rendered route and shot chunks from this unchanged recipe.')
    parser.add_argument('--prepare-only',action='store_true',help='Prepare available shot chunks without publishing, while external effects are rendering.')
    args=parser.parse_args()
    base=args.project.resolve().parent
    project=load(args.project)
    spec=load(args.revision)
    register_path=base/'shots/shotlist.json'
    register=load(register_path)
    shots={s['id']:s for s in register['storyboardProposals']}
    out=base/spec['output'];out.mkdir(parents=True,exist_ok=True)
    fps=spec['fps'];first=spec['startFrame'];end=spec['endFrameExclusive']
    source=base/spec['sourceAnimatic']
    assert probe(source)['nb_frames']=='5265'
    pullback=base/spec['orbitMotion']
    n=int(probe(pullback)['nb_frames'])
    assert n>=24+138+24
    routes=out/'route-frames'
    orbit_composite=base/spec['orbitComposite'] if spec.get('orbitComposite') else out/'orbit-composite-handles.mp4'
    if not args.reuse_prepared and not spec.get('orbitComposite'):
        route_overlay(routes,n,spec['cameraTrack'])
        encode(['-i',str(pullback),'-framerate','24','-i',str(routes/'%04d.png'),'-filter_complex','[0:v]pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v];[v][1:v]overlay=0:0:shortest=1'],n,out/'orbit-composite-handles.mp4')
    if orbit_composite.exists():
        assert int(probe(orbit_composite)['nb_frames'])==n
    else:
        assert args.prepare_only and spec.get('orbitComposite')
    image_map={x['id']:(base/x['path'] if x.get('path') else base/spec['output']/x['output']) for x in spec['images']}
    entries=[
        dict(id='portrait-short',start=789,end=854,path=base/shots['space-009']['motionRef'],lead=24),
        dict(id='scale-reveal',start=854,end=912,path=base/spec['scaleMotion'],lead=134),
        dict(id='arms-tide',start=912,end=1046,path=base/shots['space-011']['motionRef'],lead=24),
        dict(id='mission-drift',start=1046,end=1170,path=base/shots['chorus1-01']['motionRef'],lead=24,drift=True),
        dict(id='small-intervention',start=1170,end=1228,path=base/shots['chorus1-02']['motionRef'],lead=24),
        dict(id='creature-view',start=1228,end=1263,path=image_map['creature-view'],still=True),
        dict(id='right-little-something',start=1263,end=1292,path=image_map['right-little-something'],still=True,reveal=True),
        dict(id='orbit-first',start=1292,end=1412,path=base/shots['chorus1-04']['motionRef'],lead=24),
        dict(id='orbit-pullback',start=1412,end=1550,path=orbit_composite,lead=24)
    ]
    for item in reversed(spec.get('leadingEntries',[])):
        entries.insert(0,dict(item,path=base/item['path']))
    for item in entries:
        item.update(spec.get('entryOverrides',{}).get(item['id'],{}))
        if isinstance(item['path'],str):
            item['path']=base/item['path']
        if item['id'] in spec.get('cameraMoves',{}):
            item['cameraMove']=spec['cameraMoves'][item['id']]
    # A six-frame transition protects the short key-phrase reveal.
    widths={1046:10,1170:10,1228:10,1263:6,1292:6,1412:10}
    if spec.get('transitionFramesByBoundary'):
        widths={int(k):v for k,v in sorted(spec['transitionFramesByBoundary'].items(),key=lambda x:int(x[0]))}
    files=[]
    for item in entries:
        head=widths.get(item['start'],0)//2
        tail=widths.get(item['end'],0)//2
        count=item['end']-item['start']+head+tail
        item.update(head=head,tail=tail,renderFrames=count)
        target=out/(item['id']+'.mp4')
        if args.prepare_only and not item['path'].exists():
            print('Waiting for external source:',item['id'])
            continue
        if item.get('still'):
            inputs=['-loop','1','-framerate','24','-i',str(item['path'])]
            filters='scale=1920:1080,setsar=1'
        else:
            lead=item['lead']-head
            assert lead>=0 and int(probe(item['path'])['nb_frames'])>=lead+count
            inputs=['-i',str(item['path'])]
            filters=f'fps=24,trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
        if item.get('cameraMove'):
            move=item['cameraMove']
            t=f'min(1,max(0,on/{max(1,count-1)}))'
            ease=f'(({t})*({t})*(3-2*({t})))'
            def expression(values):
                return f'{values[0]}+({values[1]}-{values[0]})*{ease}'
            z,x,y=[expression(move[k]) for k in ('zoom','panX','panY')]
            filters+=f",scale=3840:2160,zoompan=z='{z}':x='(iw-iw/zoom)*({x})':y='(ih-ih/zoom)*({y})':d=1:s=1920x1080:fps=24"
        elif item.get('drift') or item.get('still'):
            zoom=f'1.01+0.025*on/{max(1,count-1)}'
            if item.get('reveal'):
                zoom=f'1.05-0.035*on/{max(1,count-1)}'
            filters+=f",zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=24"
        if not args.reuse_prepared or not target.exists():
            encode([*inputs,'-vf',filters],count,target)
        assert int(probe(target)['nb_frames'])==count
        files.append(target)
    if args.prepare_only:
        print('Prepared',len(files),'shot chunks; no edit published')
        return
    if spec.get('transitionFramesByBoundary'):
        inputs=files
        join_entries=entries[1:]
        initial_frames=entries[0]['renderFrames']
    else:
        # Preserve the older recipe's three direct coverage cuts.
        (out/'prefix.txt').write_text(''.join(f"file '{p.name}'\n" for p in files[:3]),encoding='utf-8')
        run(['-f','concat','-safe','0','-i','prefix.txt','-c','copy','prefix.mp4'],out)
        inputs=[out/'prefix.mp4',*files[3:]]
        join_entries=entries[3:]
        initial_frames=sum(x['renderFrames'] for x in entries[:3])
    data=load(base/'generated/animatic/animatic-data.json')
    captions=copy.deepcopy(data)
    captions['phrases']=[p for p in captions['phrases'] if first<=p['startFrame']<end]
    for phrase in captions['phrases']:
        for item in [phrase]+phrase['words']:
            item['startFrame']-=first-1;item['endFrameExclusive']-=first-1
    style=project['production']['lyricPresentation']
    write_lyrics(captions,style,out/'lyrics.ass')
    (out/'fonts').mkdir(exist_ok=True)
    shutil.copy2(style['fontFile'],out/'fonts'/Path(style['fontFile']).name)
    for mode in spec['transitionTypes']:
        chain=[]
        for i in range(len(inputs)):
            chain.append(f'[{i}:v]settb=1/24,setpts=N,fps=24,format=yuv444p[v{i}]')
        total=initial_frames
        previous='v0'
        for i,item in enumerate(join_entries,1):
            width=widths[item['start']]
            offset=(total-width)/fps
            name=f'x{i}'
            # Built-in zoomin enlarges the outgoing image almost infinitely
            # at the cut. A bounded zoom pulse keeps the subject readable.
            transition='fade'
            chain.append(f'[{previous}][v{i}]xfade=transition={transition}:duration={width/fps}:offset={offset}[{name}]')
            total+=item['renderFrames']-width
            previous=name
        assert total==end-first
        if mode=='zoom-blur':
            commands=[]
            pulses=[]
            for boundary,width in widths.items():
                centre=boundary-first
                pulses.append(f'max(0,1-abs(on-{centre})/{width/2})')
                for frame in range(centre-width//2,centre+width//2+1):
                    sigma=10*max(0,1-abs(frame-centre)/(width/2))
                    commands.append(f'{(frame-.001)/fps:.8f} gblur@pulse sigma {sigma:.4f};')
            (out/'blur-commands.txt').write_text('\n'.join(commands),encoding='utf-8')
            pulse=pulses[0]
            for value in pulses[1:]:
                pulse=f'max({pulse},{value})'
            chain.append(f"[{previous}]zoompan=z='1+0.08*({pulse})':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=24,sendcmd=f=blur-commands.txt,gblur@pulse=sigma=0:steps=2[fx]")
            previous='fx'
        argv=[]
        for file in inputs:
            argv+=['-i',str(file)]
        encode([*argv,'-filter_complex_threads','2','-filter_complex',';'.join(chain),'-map',f'[{previous}]'],end-first,out/(mode+'-picture.mp4'),out)
        run(['-i',mode+'-picture.mp4','-i',str(source),'-filter_complex',f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(first-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
             '-map','[v]','-map','[a]','-frames:v',str(end-first),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',mode+'-review.mp4'],out)
        assert int(probe(out/(mode+'-review.mp4'))['nb_frames'])==end-first
    # Publish the requested transition trial, preserving exact master audio.
    working=spec.get('workingTransition','zoom-blur')
    assert working in spec['transitionTypes']
    for name,a,b in [('before',0,first-1),('after',end-1,data['frames'])]:
        encode(['-reinit_filter','0','-i',str(source),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB),setsar=1'],b-a,out/(name+'.mp4'))
    (out/'full.txt').write_text(f"file 'before.mp4'\nfile '{working}-review.mp4'\nfile 'after.mp4'\n",encoding='utf-8')
    run(['-f','concat','-safe','0','-i','full.txt','-an','-c:v','copy','full-picture.mp4'],out)
    final=base/'generated/animatic'/f'A-Right-Little-Something-selected-motion-{args.publish_version}.mp4'
    pending=final.with_name(final.stem+'.rendering.mp4')
    run(['-i',str(out/'full-picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(pending)])
    info=probe(pending)
    assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate'])==(5265,1920,1080,'24/1')
    hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']) for p in [source,pending]]
    assert hashes[0]==hashes[1]
    pending.replace(final)
    proposal=dict(id=spec['id'],status=spec.get('reviewStatus','Review draft; imagery and transitions await user choice'),source=spec['sourceAnimatic'],startFrame=first,endFrameExclusive=end,entries=[{k:(v.relative_to(base).as_posix() if isinstance(v,Path) else v) for k,v in e.items()} for e in entries],transitions=[dict(boundaryFrame=b,frames=w) for b,w in widths.items()],routeMotion=dict(source=spec['orbitMotion'],cameraTrack=spec.get('cameraTrack',[]),overlay='Shared exact route curve and ship position'),previews={m:f"{spec['output']}/{m}-review.mp4" for m in spec['transitionTypes']})
    if 'zoom-blur' in spec['transitionTypes']:
        proposal['zoomBlur']=dict(baseTransition='fade',maximumZoom=1.08,maximumBlurSigma=10)
    if spec.get('transitionLanguage'):
        proposal['transitionLanguage']=spec['transitionLanguage']
        register['transitionLanguage']=spec['transitionLanguage']
    proposal['routeMotion']['trackingNotes']=spec['cameraTrackNotes']
    proposal['workingTransition']=working
    if spec.get('nativeOrbitPlan'):
        proposal['routeMotion']['nativePlan']=spec['nativeOrbitPlan']
        proposal['routeMotion']['composite']=spec['orbitComposite']
        proposal['routeMotion']['overlay']='Native Blender ship, trajectory geometry and particle wakes, with 3D sphere depth occlusion'
    register.setdefault('editProposals',{})[spec['id']]=proposal
    register.setdefault('reviewEdits',{})[args.publish_version]=dict(source=str(source),video=str(final),proposal=spec['id'],frames=5265,fps=24,draftForReview=True,audio='Original master AAC packets preserved',startFrame=first,endFrameExclusive=end)
    register['activeReviewEdit']=args.publish_version
    if spec.get('nativeOrbitPlan'):
        orbit_plan=load(base/spec['nativeOrbitPlan'])
        register['reviewEdits'][args.publish_version]['nativeEffects']=orbit_plan['output']+'/hybrid/orbit-hybrid.blend'
    save(register_path,register)
    root=base/'generated/animatic'
    save(root/'current-media.json',{'video':final.name+f'?v={final.stat().st_mtime_ns}'})
    save(base/'generated/review/current-render.json',{'video':str(final),'master_start':1})
    review_url='http://127.0.0.1:8768/storyboard/'+out.name+'/'
    project['production'].update(animatic=final.relative_to(base).as_posix(),chorusRevisionReview=review_url,continuationNotes=spec.get('continuationNotes','V21 review draft: shorter portrait, reused scale pullback, mission camera drift, two new creature/impact stills, fade and zoom-blur comparisons, clean Kling orbit pullback with authored ship/path overlay. Master unchanged. V20 preserved; proposals await user choice.'))
    save(args.project,project)
    opening=load(root/'current-opening.json');opening['version']=args.publish_version
    opening['mediaLabel']=spec.get('mediaLabel','Kling / composition stills / transition and route draft')
    opening['shots']=[s for s in opening['shots'] if not first<=s['startFrame']<end]
    opening['shots'] += [dict(id=e['id'],title=e['id'].replace('-',' '),startFrame=e['start'],frames=e['end']-e['start'],review={'notes':e.get('reviewNotes',spec.get('entryReviewNotes','Chorus revision proposal; two creature/impact views are still composition drafts.'))}) for e in entries]
    opening['shots'].sort(key=lambda s:s['startFrame']);save(root/'current-opening.json',opening)
    save(out/'manifest.json',proposal)
    # Reuse the project's existing inspection layout, with explicit draft labels.
    old=(base/'generated/storyboard/chorus1-ideas-v01/index.html').read_text(encoding='utf-8')
    shell=old[:old.index('<main>')]
    title=spec.get('reviewTitle','Chorus revision · fade and zoom-blur comparison')
    intro=spec.get('reviewIntro','Draft: creature-level and key-phrase views are still images with gentle image-plane motion. Other shots use existing Kling footage plus the new clean pullback. Caption timing and master audio are retained. Routes and tiny ship are authored together and anchored to observed world positions.')
    shell=shell.replace('Chorus 1 · mission, intervention and orbit echoes',html.escape(title))
    cards=''
    for item in spec['images']:
        image_url='/storyboard/'+image_map[item['id']].relative_to(base/'generated/storyboard').as_posix()
        cards+=f'<article><h2>{html.escape(item["id"])}</h2><img src="{image_url}" alt="{html.escape(item["id"])}"><p>Source composition · frame {item["startFrame"]} · {(item["startFrame"]-1)/fps:.2f}s</p></article>'
    body=f'<main><h1>{html.escape(title)}</h1><p><a href="/">Full {args.publish_version} animatic</a></p><p class="label">{html.escape(intro)}</p>'
    for link in spec.get('reviewLinks',[]):
        body+=f'<p><a href="{html.escape(link["href"],quote=True)}">{html.escape(link["title"])}</a></p>'
    for mode in spec['transitionTypes']:
        stamp=(out/(mode+'-review.mp4')).stat().st_mtime_ns
        body+=f'<h2>{html.escape(mode)}</h2><video controls preload="metadata" src="{mode}-review.mp4?v={stamp}"></video>'
    body+=f'<p>Song {(first-1)/fps:.2f}–{(end-1)/fps:.2f}s. Scale reveal 35.54s · mission pan 43.54s · creature view 51.12s · key wide 52.58s · orbit flight 58.79s. Earlier drafts remain available for comparison.</p>'+cards+'</main></html>'
    (out/'index.html').write_text(shell+body,encoding='utf-8')
    print('Ready',final,'· 5265 frames · exact master audio ·',', '.join(spec['transitionTypes']))


if __name__=='__main__':
    main()
