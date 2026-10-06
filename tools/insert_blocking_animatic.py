"""Insert a proposed Blender batch into the current full-song review movie."""
import argparse
import copy
import json
import pathlib
import shutil
import subprocess

from lyric_overlay import write_lyrics


def run(args, cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=cwd,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=pathlib.Path)
    parser.add_argument('batch',type=pathlib.Path)
    args=parser.parse_args()
    base=args.project.resolve().parent
    project=json.loads(args.project.read_text(encoding='utf-8'))
    spec=json.loads(args.batch.read_text(encoding='utf-8'))
    register_path=base/'shots/shotlist.json'
    register=json.loads(register_path.read_text(encoding='utf-8'))
    shots=[s for s in register['storyboardProposals'] if s['batch']==spec['id']]
    assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
    root=base/'generated/animatic'
    data=json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    fps=data['fps'];count=data['frames'];start=shots[0]['startFrame'];end=shots[-1]['endFrameExclusive']
    source=root/'A-Right-Little-Something-opening-motion-v03.mp4'
    work=root/'space-blocking-work';work.mkdir(exist_ok=True)
    entries=[]
    for shot in shots:
        raw=base/spec['output']/(shot['id']+'-handles.mp4')
        lead=shot['handles']['leadInFrames'];length=shot['frames']
        name=shot['id']+'.mp4'
        run(['-i',str(raw),'-vf',f'trim=start_frame={lead}:end_frame={lead+length},setpts=PTS-STARTPTS,scale=1920:1080,setsar=1',
             '-frames:v',str(length),'-an','-c:v','libx264','-preset','fast','-crf','18',str(work/name)])
        entries.append({'shot':shot['id'],'startFrame':shot['startFrame'],'frames':length,
                        'source':str(raw),'sourceEditStartFrame':lead+1,'file':name})
    (work/'blocking.txt').write_text(''.join(f"file '{e['file']}'\n" for e in entries),encoding='utf-8')
    run(['-f','concat','-safe','0','-i','blocking.txt','-c','copy','blocking.mp4'],cwd=work)
    captions=copy.deepcopy(data)
    captions['phrases']=[p for p in captions['phrases'] if start<=p['startFrame']<end]
    for phrase in captions['phrases']:
        for item in [phrase]+phrase['words']:
            item['startFrame']-=start-1;item['endFrameExclusive']-=start-1
    style=project['production']['lyricPresentation']
    write_lyrics(captions,style,work/'lyrics.ass')
    fonts=work/'fonts';fonts.mkdir(exist_ok=True)
    shutil.copy2(style['fontFile'],fonts/pathlib.Path(style['fontFile']).name)
    run(['-i','blocking.mp4','-vf','ass=lyrics.ass:fontsdir=fonts','-frames:v',str(end-start),'-an',
         '-c:v','libx264','-preset','fast','-crf','18','lettered-blocking.mp4'],cwd=work)
    # Render all picture parts with the same settings for reliable concatenation.
    for name,a,b in [('before',0,start-1),('after',end-1,count)]:
        run(['-reinit_filter','0','-i',str(source),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/({fps}*TB),setsar=1',
             '-frames:v',str(b-a),'-an','-c:v','libx264','-preset','fast','-crf','18',str(work/(name+'.mp4'))])
    (work/'full.txt').write_text("file 'before.mp4'\nfile 'lettered-blocking.mp4'\nfile 'after.mp4'\n",encoding='utf-8')
    run(['-f','concat','-safe','0','-i','full.txt','-c','copy','picture.mp4'],cwd=work)
    final=root/'A-Right-Little-Something-space-blocking-v04.mp4'
    pending=final.with_name(final.stem+'.rendering.mp4')
    run(['-i',str(work/'picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c','copy','-movflags','+faststart',str(pending)])
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(pending)]))['streams'][0]
    assert int(info['nb_frames'])==count and info['r_frame_rate']==f'{fps}/1'
    assert (info['width'],info['height'])==(1920,1080)
    hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']) for p in (source,pending)]
    assert hashes[0]==hashes[1],'Original master audio packets changed'
    pending.replace(final)
    review={'id':'space-blocking-v04','batch':spec['id'],'source':str(source),'video':str(final),
            'startFrame':start,'endFrameExclusive':end,'frames':count,'fps':fps,'entries':entries,
            'presentation':'Accepted Kling opening followed by rough Blender motion; small bottom lyrics',
            'sourceResolution':'Blender proxies 640x360 scaled to 1080p review canvas; not final footage',
            'audio':'Original master AAC packets copied without retiming'}
    register.setdefault('reviewEdits',{})['space-blocking-v04']=review
    temp=register_path.with_suffix('.tmp');temp.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');temp.replace(register_path)
    (root/'blocking-insert-manifest.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
    (root/'current-media.json').write_text(json.dumps({'video':final.name+f'?v={final.stat().st_mtime_ns}'}),encoding='utf-8')
    pointer=base/'generated/review/current-render.json';temp=pointer.with_suffix('.tmp')
    temp.write_text(json.dumps({'video':str(final),'master_start':1}),encoding='utf-8');temp.replace(pointer)
    rows=[]
    for s in register['shots']:
        if s.get('batch')!='opening-notes-v01' or s['startFrame']>=start:continue
        rows.append({'id':s['id'],'title':s['title'],'startFrame':s['startFrame'],
                     'frames':min(s['endFrameExclusive'],start)-s['startFrame'],
                     'review':{'notes':'Existing illustrated animation; trimmed at the proposed continuation.'}})
    rows += [{'id':s['id'],'title':s['title'],'startFrame':s['startFrame'],'frames':s['frames'],
              'review':{'notes':'Rough Blender blocking · '+s['blocking']['transition']}} for s in shots]
    (root/'current-opening.json').write_text(json.dumps({'version':'v04','mediaLabel':'Kling + Blender beats',
        'fps':fps,'endFrameExclusive':end,'shots':rows},indent=2),encoding='utf-8')
    print('Ready:',final,'·',count,'frames · audio packets verified')


if __name__=='__main__':
    main()
