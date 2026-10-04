"""Insert planned illustrated boards into the full lyric animatic for review."""
import argparse
import json
import pathlib
import subprocess


def run(command, cwd=None):
    subprocess.run(command, cwd=cwd, check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=pathlib.Path)
    args=parser.parse_args()
    base=args.project.resolve().parent
    project=json.loads(args.project.read_text(encoding='utf-8'))
    root=base/'generated/animatic'
    data=json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    register=json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
    shots=[s for s in register['shots'] if s.get('batch')=='opening-notes-v01']
    source=root/'A-Right-Little-Something-lyric-timing-v03.mp4'
    fps=data['fps'];count=data['frames']
    assert shots[0]['startFrame']==1
    assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
    opening_end=shots[-1]['endFrameExclusive']-1
    work=root/'storyboard-opening-work';work.mkdir(exist_ok=True)
    entries=[]
    for shot in shots:
        start=shot['startFrame']-1;length=shot['frames']
        images=[base/shot['startingFrameRef']]
        lengths=[length]
        if shot.get('endingFrameRef'):
            images.append(base/shot['endingFrameRef'])
            first=length//2
            lengths=[first,length-first]
        for index,(image,frames) in enumerate(zip(images,lengths)):
            name=f'{shot["id"]}-{index}.mp4'
            # Full 16:9 image retained above a lyric/active-word review panel.
            run(['ffmpeg','-y','-v','error','-loop','1','-framerate',str(fps),
                 '-i',str(image),'-vf','scale=960:540,pad=1280:720:160:0:black,setsar=1',
                 '-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast',
                 '-crf','19','-pix_fmt','yuv420p',str(work/name)])
            entries.append({'shot':shot['id'],'image':str(image),'startFrame':start+1,
                            'frames':frames,'file':name})
            start+=frames
    (work/'concat.txt').write_text(''.join(f"file '{e['file']}'\n" for e in entries),encoding='utf-8')
    run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','concat.txt',
         '-c','copy','boards.mp4'],cwd=work)
    font="fontfile='C\\:/Windows/Fonts/arial.ttf':"
    filters=[]
    for shot in shots:
        name=shot['id']+'.txt';(work/name).write_text(shot['id']+' · STORYBOARD STILLS',encoding='utf-8')
        a,b=shot['startFrame']-1,shot['endFrameExclusive']-1
        filters.append(f"drawtext={font}textfile='{name}':x=24:y=18:fontsize=18:fontcolor=white:enable='gte(n,{a})*lt(n,{b})'")
    for phrase in data['phrases']:
        a,b=phrase['startFrame']-1,phrase['endFrameExclusive']-1
        if a>=opening_end:continue
        name=phrase['id']+'.txt';(work/name).write_text(phrase['text'],encoding='utf-8')
        filters.append(f"drawtext={font}textfile='{name}':x=(w-text_w)/2:y=580:fontsize=32:fontcolor=white:enable='gte(n,{a})*lt(n,{b})'")
        for index,word in enumerate(phrase['words']):
            wa,wb=word['startFrame']-1,word['endFrameExclusive']-1
            name=f'{phrase["id"]}-w{index}.txt';(work/name).write_text(word['text'],encoding='utf-8')
            filters.append(f"drawtext={font}textfile='{name}':x=(w-text_w)/2:y=645:fontsize=28:fontcolor=0xffb057:enable='gte(n,{wa})*lt(n,{wb})'")
    filters=[f'[1:v]{",".join(filters)}[opening]',
             f'[0:v]trim=start_frame={opening_end},setpts=PTS-STARTPTS[remainder]',
             '[opening][remainder]concat=n=2:v=1:a=0[video]']
    (work/'filter.txt').write_text(';'.join(filters),encoding='utf-8')
    final=root/'A-Right-Little-Something-storyboard-opening-v01.mp4'
    pending=final.with_name(final.stem+'.rendering.mp4')
    run(['ffmpeg','-y','-v','error','-i',str(source),'-i','boards.mp4',
         '-filter_complex_script','filter.txt','-map','[video]',
         '-frames:v',str(count),'-r',str(fps),'-c:v','libx264','-preset','fast',
         '-crf','19','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(pending)],cwd=work)
    # Mux separately: -frames:v can stop audio copying at the video boundary
    # and discard the master AAC stream's final packet.
    muxed=final.with_name(final.stem+'.audio.mp4')
    run(['ffmpeg','-y','-v','error','-i',str(pending),'-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(muxed)])
    muxed.replace(pending)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
         '-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(pending)]))['streams'][0]
    assert int(probe['nb_frames'])==count and probe['r_frame_rate']==f'{fps}/1',probe
    audio_hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
         '-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'])
         for path in (source,pending)]
    assert audio_hashes[0]==audio_hashes[1],'Original audio packets changed'
    pending.replace(final)
    (root/'storyboard-insert-manifest.json').write_text(json.dumps({
        'source':str(source),'video':str(final),'fps':fps,'frames':count,
        'openingEndFrameExclusive':opening_end+1,'entries':entries,
        'presentation':'Held storyboard frames; endpoints switch halfway through applicable shots; no generated motion',
        'audio':'Original lyric animatic AAC stream copied without retiming',
        'remainder':'Original lyric animatic picture from opening end onward'},indent=2)+'\n',encoding='utf-8')
    (root/'current-media.json').write_text(json.dumps({'video':final.name+f'?v={final.stat().st_mtime_ns}'}),encoding='utf-8')
    pointer=base/'generated/review/current-render.json'
    temp=pointer.with_suffix('.tmp')
    temp.write_text(json.dumps({'video':str(final),'master_start':1}),encoding='utf-8')
    temp.replace(pointer)
    print(f'{final} · {count} frames · opening {opening_end} frames')


if __name__=='__main__':main()
