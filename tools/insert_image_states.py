"""Place illustrated scale states into a full animatic at authored frame edges."""
import argparse
import copy
import html
import json
import pathlib
import shutil
import subprocess

from lyric_overlay import write_lyrics


def run(args,cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=cwd,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=pathlib.Path);parser.add_argument('plan',type=pathlib.Path)
    args=parser.parse_args();base=args.project.resolve().parent
    project=json.loads(args.project.read_text(encoding='utf-8'))
    plan=json.loads(args.plan.read_text(encoding='utf-8'))
    root=base/'generated/animatic';out=base/plan['output'];work=out/'work';work.mkdir(exist_ok=True)
    data=json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    fps=data['fps'];count=data['frames'];a=plan['startFrame']-1;b=plan['endFrameExclusive']-1
    images=plan['images'];source=base/plan['sourceVideo']
    assert images[0]['startFrame']==a+1 and images[-1]['endFrameExclusive']==b+1
    assert all(x['endFrameExclusive']==y['startFrame'] for x,y in zip(images,images[1:]))
    for image in images:
        length=image['endFrameExclusive']-image['startFrame']
        run(['-loop','1','-framerate',str(fps),'-i',str(base/image['image']),'-vf','scale=1920:1080,setsar=1',
             '-frames:v',str(length),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(work/(image['id']+'.mp4'))])
    (work/'states.txt').write_text(''.join(f"file '{i['id']}.mp4'\n" for i in images),encoding='utf-8')
    run(['-f','concat','-safe','0','-i','states.txt','-c','copy','states.mp4'],cwd=work)
    captions=copy.deepcopy(data);captions['phrases']=[p for p in captions['phrases'] if a+1<=p['startFrame']<b+1]
    for p in captions['phrases']:
        for item in [p]+p['words']:
            item['startFrame']-=a;item['endFrameExclusive']-=a
    style=project['production']['lyricPresentation'];write_lyrics(captions,style,work/'lyrics.ass')
    fonts=work/'fonts';fonts.mkdir(exist_ok=True);shutil.copy2(style['fontFile'],fonts/pathlib.Path(style['fontFile']).name)
    run(['-i','states.mp4','-vf','ass=lyrics.ass:fontsdir=fonts','-frames:v',str(b-a),'-an','-c:v','libx264','-preset','fast','-crf','18','lettered.mp4'],cwd=work)
    for name,start,end in [('before',0,a),('after',b,count)]:
        # Joined source clips can change codec headers. Preserve the filter's
        # frame counter across those boundaries so trim uses song frames.
        run(['-reinit_filter','0','-i',str(source),'-vf',f'trim=start_frame={start}:end_frame={end},setpts=N/({fps}*TB),setsar=1',
             '-frames:v',str(end-start),'-r',str(fps),'-an','-c:v','libx264','-preset','fast','-crf','18',str(work/(name+'.mp4'))])
    (work/'full.txt').write_text("file 'before.mp4'\nfile 'lettered.mp4'\nfile 'after.mp4'\n",encoding='utf-8')
    run(['-f','concat','-safe','0','-i','full.txt','-c','copy','picture.mp4'],cwd=work)
    final=root/plan['videoName'];pending=final.with_name(final.stem+'.rendering.mp4')
    run(['-i',str(work/'picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(pending)])
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(pending)]))['streams'][0]
    assert int(info['nb_frames'])==count and info['r_frame_rate']==f'{fps}/1'
    assert (info['width'],info['height'])==(1920,1080)
    hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']) for p in (source,pending)]
    assert hashes[0]==hashes[1],'Master audio changed'
    pending.replace(final)
    register_path=base/'shots/shotlist.json';register=json.loads(register_path.read_text(encoding='utf-8'))
    shot=next(s for s in register['storyboardProposals'] if s['id']==plan['shot'])
    shot['illustratedStates']=[{k:i[k] for k in ('id','image','startFrame','endFrameExclusive')} for i in images]
    shot['startingFrameRef']=images[0]['image'];shot['endingFrameRef']=images[-1]['image']
    shot['imageGenerationPlan']=args.plan.name
    register.setdefault('reviewEdits',{})['hologram-boards-v05']={'source':str(source),'video':str(final),
         'startFrame':a+1,'endFrameExclusive':b+1,'images':shot['illustratedStates'],'presentation':plan['description']}
    temp=register_path.with_suffix('.tmp');temp.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');temp.replace(register_path)
    (root/'current-media.json').write_text(json.dumps({'video':final.name+f'?v={final.stat().st_mtime_ns}'}),encoding='utf-8')
    pointer=base/'generated/review/current-render.json';temp=pointer.with_suffix('.tmp')
    temp.write_text(json.dumps({'video':str(final),'master_start':1}),encoding='utf-8');temp.replace(pointer)
    opening_path=root/'current-opening.json';opening=json.loads(opening_path.read_text(encoding='utf-8'))
    opening['version']='v05';opening['mediaLabel']='Kling / Blender / illustrated beats'
    next(s for s in opening['shots'] if s['id']==plan['shot'])['review']['notes']=plan['description']
    opening_path.write_text(json.dumps(opening,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    cards=''.join(f'<figure><img src="{pathlib.Path(i["image"]).name}"><figcaption>{html.escape(i["id"])} · frames {i["startFrame"]}–{i["endFrameExclusive"]-1}</figcaption></figure>' for i in images)
    (out/'index.html').write_text('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hologram scale states</title><style>body{background:#10262d;color:#eee2c6;font:16px/1.5 system-ui;margin:24px auto;max-width:1200px;padding:16px}a{color:#9cd9e5}figure{margin:24px 0}img{width:100%}</style><h1>Planet → system → neighboring stars</h1><p><a href="/">Full animatic v05 & notes</a> · <a href="/storyboard/space-notes-v01/">Blender blocking</a></p><p>Three ImageGen scale-state references in one locked oblique view. Celestial icons are enlarged and spacing compressed. Amber locator preserves the selected home location. Held frames test appearance and timing, not animation.</p>'''+cards,encoding='utf-8')
    print('Ready:',final,'·',count,'frames · master packets verified')


if __name__=='__main__':
    main()
