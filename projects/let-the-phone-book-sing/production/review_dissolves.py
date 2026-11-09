"""Short picture-only dissolves centered on existing musical edit boundaries."""
import json
import math
import subprocess
from pathlib import Path
from PIL import Image


def apply_dissolves(source, target, score, assets, base, total, length=4):
    assert length == 4, 'This review uses exactly four mixed frames per transition.'
    inserts = score['reviewVideoInserts']
    shots = score['shots']
    counts = {}
    held = []

    def segment(frame):
        for item in inserts:
            if item['startFrame'] <= frame < item['endFrameExclusive']:
                return ('video', item)
        return ('still', next(s for s in shots if s['startFrame'] <= frame < s['endFrameExclusive']))

    def samples(seg, master_frames):
        kind, item = seg
        if kind == 'still':
            image = Image.open(assets/(item['id']+'.png')).convert('RGB')
            return [image] * len(master_frames)
        path = base/item['source']
        offset = item['sourceOffsetFrames']
        indices = [offset+f-item['startFrame'] for f in master_frames]
        # Belle's baked lettering has no handles; its raw source supplies the
        # two transition frames outside the bake, where no echo text is active.
        if item['id'] == 'belle-continuous' and (min(indices)<0 or max(indices)>=item['endFrameExclusive']-item['startFrame']):
            path = base/'generated/kling-tests/belle-bell-v001/belle-original-1080p.mp4'
            offset = item['originalSourceOffsetFrames']
            rate = item.get('originalSourceFramesPerEditFrame', 1)
            indices = [offset+(f-item['startFrame'])*rate for f in master_frames]
        if path not in counts:
            info = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration','-of','json',str(path)]))['streams'][0]
            counts[path] = round(float(info['duration'])*24)
        clipped = [max(0,min(counts[path]-1,n)) for n in indices]
        if clipped != indices:
            held.append(dict(id=item['id'],masterFrames=master_frames,requested=indices,used=clipped))
        first,last = math.floor(min(clipped)),math.ceil(max(clipped))
        filt=f'fps=24,trim=start_frame={first}:end_frame={last+1},setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2'
        raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',filt,'-frames:v',str(last-first+1),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
        size=1920*1080*3
        assert len(raw)==size*(last-first+1), (path,first,last,len(raw))
        images=[Image.frombytes('RGB',(1920,1080),raw[k*size:(k+1)*size]) for k in range(last-first+1)]
        return [Image.blend(images[math.floor(n)-first],images[math.ceil(n)-first],n-math.floor(n)) for n in clipped]

    edges=sorted({s['startFrame'] for s in shots}|{f for i in inserts for f in (i['startFrame'],i['endFrameExclusive'])})
    patches={};transitions=[]
    for cut in edges:
        if not 2 <= cut < total-2:
            continue
        outgoing,incoming=segment(cut-1),segment(cut)
        if outgoing[0]==incoming[0] and outgoing[1]['id']==incoming[1]['id']:
            continue  # Internal timing markers inside one continuous take.
        frames=list(range(cut-2,cut+2))
        a,b=samples(outgoing,frames),samples(incoming,frames)
        for k,f in enumerate(frames):
            assert f not in patches
            patches[f]=Image.blend(a[k],b[k],(k+1)/5).tobytes()
        transitions.append(dict(cutFrame=cut,mixedFrames=frames,outgoing=outgoing[1]['id'],incoming=incoming[1]['id']))
    reader=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-frames:v',str(total),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-i',str(source),'-map','0:v','-map','1:a','-frames:v',str(total),'-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-movflags','+faststart',str(target)],stdin=subprocess.PIPE)
    for f in range(total):
        raw=reader.stdout.read(1920*1080*3)
        assert len(raw)==1920*1080*3
        writer.stdin.write(patches.get(f,raw))
    reader.stdout.close();assert reader.wait()==0
    writer.stdin.close();assert writer.wait()==0
    report=dict(lengthFrames=4,placement='Two frames before and two at/after each fixed cut; incoming weights 20,40,60,80 percent.',audio='Unchanged; picture-only transitions.',transitions=transitions,edgeFrameHolds=held)
    (target.parent/'dissolve-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
