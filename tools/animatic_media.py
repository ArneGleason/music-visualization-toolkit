"""Frame-accurate still/video artwork and handle-based transitions for reviews."""
import subprocess
from pathlib import Path
from PIL import Image, ImageOps


class Artwork:
    def __init__(self, base, shots, fps, full_frame=False):
        self.base, self.shots, self.fps = base, shots, fps
        self.full_frame = full_frame
        self.size = (1920, 1080) if full_frame else (1920, 1008)
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
            if getattr(self, 'full_frame', False):
                ratio = self.size[0]/self.size[1]
                if cw/ch > ratio:
                    cw = ch*ratio
                else:
                    ch = cw/ratio
            # Focus specifies the share of the cropped margin on the left/top.
            left,top = (w-cw)*x,(h-ch)*y
            im = im.resize(self.size if getattr(self, 'full_frame', False) else (1792,1008),Image.Resampling.LANCZOS,box=(left,top,left+cw,top+ch))
        else:
            if shot['id'] not in self.stills:
                with Image.open(self.base/shot['starterImage']) as source:
                    fit = ImageOps.fit if self.full_frame else ImageOps.contain
                    self.stills[shot['id']] = fit(source.convert('RGB'),self.size,Image.Resampling.LANCZOS)
            im = self.stills[shot['id']]
        width,height = self.size
        canvas = Image.new('RGB',self.size,'#101516')
        canvas.paste(im,((width-im.width)//2,(height-im.height)//2))
        return canvas

    def at(self, shot, master_frame):
        for before,after in zip(self.shots,self.shots[1:]):
            tr = after.get('transitionIn',{})
            if tr.get('type') == 'impact_blackout':
                boundary = after['startFrame']
                rise = tr.get('whiteRiseFrames', 8)
                fall = tr.get('whiteFallFrames', 4)
                hold = tr.get('blackHoldFrames', 4)
                reveal = tr.get('revealFrames', 14)
                if min(rise, fall, reveal) < 2 or hold < 0:
                    raise ValueError('Invalid impact transition frame counts')
                if rise > before['frames'] or fall+hold+reveal > after['frames']:
                    raise ValueError('Impact transition exceeds its shots')
                relative = master_frame-boundary
                if -rise <= relative < 0:
                    im = self.frame(before, master_frame)
                    # Small alternating jolt, cropped inward to avoid exposed edges.
                    step = relative+rise
                    offsets = [(0,0), (9,-5), (-8,6), (5,-4), (-3,2), (0,0)]
                    dx,dy = offsets[min(step,len(offsets)-1)]
                    shake_frames = tr.get('shakeFrames', len(offsets))
                    if shake_frames > len(offsets) and step < shake_frames:
                        dx,dy = offsets[step % (len(offsets)-1)]
                        strength = .5 + .5*step/max(1,shake_frames-1)
                        dx,dy = round(dx*strength),round(dy*strength)
                    w,h = im.size
                    im = im.resize((w,h), Image.Resampling.BICUBIC,
                                   box=(18+dx,18+dy,w-18+dx,h-18+dy))
                    return Image.blend(im, Image.new('RGB',im.size,'white'), step/(rise-1))
                if 0 <= relative < fall:
                    value = round(255*(1-relative/(fall-1)))
                    return Image.new('RGB',getattr(self, 'size', (1920,1008)),(value,value,value))
                if fall <= relative < fall+hold:
                    return Image.new('RGB',getattr(self, 'size', (1920,1008)),'black')
                if fall+hold <= relative < fall+hold+reveal:
                    alpha = (relative-fall-hold)/(reveal-1)
                    alpha = alpha*alpha*(3-2*alpha)
                    incoming = self.frame(after,master_frame)
                    return Image.blend(Image.new('RGB',incoming.size,'black'),incoming,alpha)
                continue
            if tr.get('type') not in ('crossfade', 'soft_wipe'):
                continue
            count = tr['frames']
            alignment = tr.get('alignment', 'center')
            if alignment not in ('center', 'start'):
                raise ValueError(f"Unsupported transition alignment: {alignment}")
            start = after['startFrame'] - (count//2 if alignment == 'center' else 0)
            if start <= master_frame < start+count:
                alpha = (master_frame-start)/max(1,count-1)
                outgoing = self.frame(before,master_frame)
                incoming = self.frame(after,master_frame)
                if tr['type'] == 'crossfade':
                    return Image.blend(outgoing, incoming, alpha)
                direction = tr.get('direction', 'left_to_right')
                if direction not in ('left_to_right', 'right_to_left', 'bottom_to_top', 'top_to_bottom'):
                    raise ValueError(f"Unsupported wipe direction: {direction}")
                width, height = incoming.size
                vertical = direction in ('bottom_to_top', 'top_to_bottom')
                extent = height if vertical else width
                feather = max(1, extent * tr.get('featherFraction', .1))
                edge = -feather/2 + alpha * (extent + feather)
                values = [round(255 * max(0, min(1, (edge-x)/feather + .5)))
                          for x in range(extent)]
                if direction in ('right_to_left', 'bottom_to_top'):
                    values.reverse()
                mask = Image.new('L', (1, height) if vertical else (width, 1))
                mask.putdata(values)
                return Image.composite(incoming, outgoing, mask.resize((width, height)))
        return self.frame(shot,master_frame)
