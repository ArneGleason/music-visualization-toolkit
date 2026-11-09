"""Insert approved-direction avatar experiments without changing lyric/master timing."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'generated/avatar-tests/opening-v001'
W, H = 1066, 600

def composite(source, target, start_seconds, frames, background_video=None):
    bg = np.asarray(Image.open(BASE/'generated/environment-development/old-church-quarter-v006.png').convert('RGB').resize((W,H)), dtype=np.float32)
    dec = subprocess.Popen(['ffmpeg','-v','error','-ss',str(start_seconds),'-i',str(source),'-vf',f'fps=24,scale={W}:{H},tpad=stop_mode=clone:stop_duration=1','-frames:v',str(frames),'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
    bg_dec = None
    if background_video:
        bg_dec = subprocess.Popen(['ffmpeg','-v','error','-i',str(background_video),'-vf',f'fps=24,scale={W}:{H}','-frames:v',str(frames),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(target)], stdin=subprocess.PIPE)
    for i in range(frames):
        raw = dec.stdout.read(W*H*3)
        assert len(raw)==W*H*3, (source,i)
        if bg_dec:
            bg_raw=bg_dec.stdout.read(W*H*3)
            assert len(bg_raw)==W*H*3, ('short background',i)
            bg=np.frombuffer(bg_raw,np.uint8).reshape(H,W,3).astype(np.float32)
        fg = np.frombuffer(raw,np.uint8).reshape(H,W,3).astype(np.float32)
        r,g,b=fg[:,:,0],fg[:,:,1],fg[:,:,2]
        alpha=1-np.clip((g-np.maximum(r,b)-12)/55,0,1)
        fg[:,:,1]=np.minimum(g,np.maximum(r,b)+8+20*alpha)
        enc.stdin.write(np.uint8(np.clip(fg*alpha[:,:,None]+bg*(1-alpha[:,:,None]),0,255)).tobytes())
    dec.stdout.close();dec.wait();enc.stdin.close();assert enc.wait()==0
    if bg_dec:
        bg_dec.stdout.close();bg_dec.wait()

def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--version', default='v002')
    parser.add_argument('--output-subdir', default='opening-v001')
    args=parser.parse_args()
    OUT=BASE/'generated/avatar-tests'/args.output_subdir
    timeline=BASE/'timeline.json';before=hashlib.sha256(timeline.read_bytes()).hexdigest()
    score=json.loads((BASE/'shots/shotlist.json').read_text())
    inserts=score['avatarInserts']
    inputs=['ffmpeg','-y','-v','error','-i',str(BASE/'generated/visual-animatic-v001/Let-the-Phone-Book-Sing-visual-animatic-v001.mp4')]
    filters=[];previous='0:v'
    for i,item in enumerate(inserts,1):
        target=OUT/(item['id']+'-composite.mp4')
        composite(BASE/item['source'],target,item['sourceOffsetSeconds'],item['endFrameExclusive']-item['startFrame'],BASE/item['backgroundVideo'] if item.get('backgroundVideo') else None)
        inputs+=['-i',str(target)]
        filters.append(f'[{i}:v]setpts=PTS-STARTPTS+{item["startFrame"]}/24/TB[p{i}]')
        filters.append(f'[{previous}][p{i}]overlay=107:0:eof_action=pass:enable=\'gte(n,{item["startFrame"]})*lt(n,{item["endFrameExclusive"]})\'[v{i}]')
        previous=f'v{i}'
    full=BASE/f'generated/visual-animatic-{args.version}';full.mkdir(exist_ok=True)
    output=full/f'Let-the-Phone-Book-Sing-visual-animatic-{args.version}.mp4'
    subprocess.run(inputs+['-filter_complex',';'.join(filters),'-map',f'[{previous}]','-map','0:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(score['endFrameExclusive']),'-movflags','+faststart',str(output)],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(output),'-t',str(296/24),'-c','copy','-movflags','+faststart',str(OUT/'opening-composite-review.mp4')],check=True)
    assert hashlib.sha256(timeline.read_bytes()).hexdigest()==before
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height','-of','json',str(output)]))
    assert int(probe['streams'][0]['nb_read_frames'])==score['endFrameExclusive']
    (full/'validation.json').write_text(json.dumps({'timelineSha256':before,'video':probe,'inserts':inserts,'audio':'Original animatic master audio preserved without re-encoding','note':'Draft green keys; original 1080p avatar downloads retained. v001 untouched.'},indent=2)+'\n')
    print(output)

if __name__=='__main__':main()
