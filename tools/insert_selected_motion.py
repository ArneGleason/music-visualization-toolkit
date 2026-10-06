"""Insert an explicitly selected test into the current animatic by song frames."""
import argparse
import copy
import json
import pathlib
import shutil
import subprocess

from lyric_overlay import write_lyrics


def run(args,cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=cwd,check=True)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=pathlib.Path)
    parser.add_argument('--shot',required=True);parser.add_argument('--test',required=True)
    parser.add_argument('--version',required=True)
    args=parser.parse_args();base=args.project.resolve().parent
    project=json.loads(args.project.read_text(encoding='utf-8'))
    register_path=base/'shots/shotlist.json';register=json.loads(register_path.read_text(encoding='utf-8'))
    shot=next(s for s in register['storyboardProposals'] if s['id']==args.shot)
    selected=next(t for t in shot['motionTests'] if t['id']==args.test)
    raw=base/selected['motionRef'];root=base/'generated/animatic'
    current=json.loads((root/'current-media.json').read_text(encoding='utf-8'))
    source=root/current['video'].split('?',1)[0]
    final=root/f'A-Right-Little-Something-selected-motion-{args.version}.mp4'
    if source==final:
        source=pathlib.Path(register['reviewEdits'][args.version]['source'])
    data=json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    fps=data['fps'];count=data['frames'];a=shot['startFrame']-1;b=shot['endFrameExclusive']-1
    lead=shot['handles']['leadInFrames'];work=root/('selected-motion-'+args.version);work.mkdir(exist_ok=True)
    info=probe(raw)
    assert info['height']==1080 and info['width']<=1920
    assert int(info['nb_frames'])>=lead+(b-a)+shot['handles']['leadOutFrames']
    run(['-i',str(raw),'-vf',f'fps={fps},trim=start_frame={lead}:end_frame={lead+b-a},setpts=N/({fps}*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1',
         '-frames:v',str(b-a),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(work/'motion.mp4')])
    captions=copy.deepcopy(data);captions['phrases']=[p for p in captions['phrases'] if a+1<=p['startFrame']<b+1]
    for p in captions['phrases']:
        for item in [p]+p['words']:
            item['startFrame']-=a;item['endFrameExclusive']-=a
    style=project['production']['lyricPresentation'];write_lyrics(captions,style,work/'lyrics.ass')
    fonts=work/'fonts';fonts.mkdir(exist_ok=True);shutil.copy2(style['fontFile'],fonts/pathlib.Path(style['fontFile']).name)
    run(['-i','motion.mp4','-vf','ass=lyrics.ass:fontsdir=fonts','-an','-c:v','libx264','-preset','fast','-crf','18','lettered.mp4'],cwd=work)
    for name,start,end in [('before',0,a),('after',b,count)]:
        run(['-reinit_filter','0','-i',str(source),'-vf',f'trim=start_frame={start}:end_frame={end},setpts=N/({fps}*TB),setsar=1',
             '-frames:v',str(end-start),'-r',str(fps),'-an','-c:v','libx264','-preset','fast','-crf','18',str(work/(name+'.mp4'))])
    (work/'concat.txt').write_text("file 'before.mp4'\nfile 'lettered.mp4'\nfile 'after.mp4'\n",encoding='utf-8')
    run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','picture.mp4'],cwd=work)
    pending=final.with_name(final.stem+'.rendering.mp4')
    run(['-i',str(work/'picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(pending)])
    result=probe(pending);assert int(result['nb_frames'])==count and result['r_frame_rate']==f'{fps}/1'
    hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']) for p in (source,pending)]
    assert hashes[0]==hashes[1],'Original master packets changed'
    pending.replace(final)
    selected['status']='user selected for animatic'
    shot['motionRef']=selected['motionRef'];shot['motionSelection']=dict(selected,userSelected=True)
    shot['motionReview']={'notes':f'Current working selection: {selected["id"]}. '+selected.get('reviewNotes','')}
    register.setdefault('reviewEdits',{})[args.version]={'source':str(source),'video':str(final),'shot':shot['id'],'selectedTest':args.test,'startFrame':a+1,'endFrameExclusive':b+1,'sourceEditStartFrame':lead+1,'frames':count,'fps':fps,'audio':'Original master AAC packets preserved'}
    temp=register_path.with_suffix('.tmp');temp.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');temp.replace(register_path)
    (root/'current-media.json').write_text(json.dumps({'video':final.name+f'?v={final.stat().st_mtime_ns}'}),encoding='utf-8')
    pointer=base/'generated/review/current-render.json';temp=pointer.with_suffix('.tmp');temp.write_text(json.dumps({'video':str(final),'master_start':1}),encoding='utf-8');temp.replace(pointer)
    opening_path=root/'current-opening.json';opening=json.loads(opening_path.read_text(encoding='utf-8'))
    opening['version']=args.version;opening['mediaLabel']='Kling / Blender beats'
    next(s for s in opening['shots'] if s['id']==shot['id'])['review']=shot['motionReview']
    opening_path.write_text(json.dumps(opening,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Ready:',final,'·',count,'frames · master audio verified')


if __name__=='__main__':
    main()
