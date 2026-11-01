"""Frame-accurate still/video artwork and handle-based transitions for reviews."""
import subprocess
from pathlib import Path
from PIL import Image, ImageOps


class Artwork:
    def __init__(self, base, shots, fps):
        self.base, self.shots, self.fps = base, shots, fps
        self.cache = {}
        self.stills = {}
        for shot in shots:
            if not shot.get('videoSource'):
                continue
            source = base / shot['videoSource']
            folder = source.parent / (source.stem + '-frames')
            folder.mkdir(exist_ok=True)
            stamp = folder / 'source-stamp.txt'
            signature = str((source.stat().st_size, source.stat().st_mtime_ns, fps))
            if not stamp.exists() or stamp.read_text() != signature:
                subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(source),
                                '-vf', f'fps={fps}', '-compression_level', '1',
                                '-start_number', '0', str(folder/'%05d.png')], check=True)
                stamp.write_text(signature)
            self.cache[shot['id']] = folder

    def frame(self, shot, master_frame):
        if shot.get('videoSource'):
            edit = shot.get('videoEdit', {})
            index = edit.get('sourceInFrame', self.fps) + master_frame - shot['startFrame']
            path = self.cache[shot['id']] / f'{index:05d}.png'
            if index < 0 or not path.exists():
                raise ValueError(f"Insufficient video handle for {shot['id']} at {master_frame}")
            with Image.open(path) as source:
                im = source.convert('RGB')
            t = max(0, min(1, (master_frame-shot['startFrame']) / max(1, shot['frames']-1)))
            t = t*t*(3-2*t)
            zoom = edit.get('zoomStart', 1)*(1-t) + edit.get('zoomEnd', 1)*t
            a, b = edit.get('focusStart', [.5,.5]), edit.get('focusEnd', [.5,.5])
            x, y = (a[0]*(1-t)+b[0]*t), (a[1]*(1-t)+b[1]*t)
            w,h = im.size
            cw,ch = w/zoom,h/zoom
            # Focus specifies the share of the cropped margin on the left/top.
            left,top = (w-cw)*x,(h-ch)*y
            im = im.resize((1792,1008),Image.Resampling.LANCZOS,box=(left,top,left+cw,top+ch))
        else:
            if shot['id'] not in self.stills:
                with Image.open(self.base/shot['starterImage']) as source:
                    self.stills[shot['id']] = ImageOps.contain(source.convert('RGB'),(1920,1008),Image.Resampling.LANCZOS)
            im = self.stills[shot['id']]
        canvas = Image.new('RGB',(1920,1008),'#101516')
        canvas.paste(im,((1920-im.width)//2,(1008-im.height)//2))
        return canvas

    def at(self, shot, master_frame):
        for before,after in zip(self.shots,self.shots[1:]):
            tr = after.get('transitionIn',{})
            if tr.get('type') != 'crossfade':
                continue
            count = tr['frames']
            start = after['startFrame']-count//2
            if start <= master_frame < start+count:
                alpha = (master_frame-start)/max(1,count-1)
                return Image.blend(self.frame(before,master_frame),self.frame(after,master_frame),alpha)
        return self.frame(shot,master_frame)
