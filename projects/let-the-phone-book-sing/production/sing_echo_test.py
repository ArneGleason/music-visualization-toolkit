"""Deterministic illustrated echo lettering with narrator-plane occlusion."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage, signal
from scipy.io import wavfile

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'generated/motion-graphics/sing-echo-v001'
W, H, FPS = 1920, 1080, 24


def analyze(path, start):
    sr, samples = wavfile.read(path)
    x = samples[:8 * sr].astype(np.float64)
    x /= np.max(np.abs(x))
    x = signal.resample_poly(x, 1, 6)
    sr //= 6
    template = x[round((start+.015)*sr):round((start+.335)*sr)].mean(axis=1)
    curves = []
    for channel in range(2):
        y = x[:, channel]
        corr = signal.correlate(y, template, mode='valid', method='fft')
        energy = signal.convolve(y*y, np.ones(len(template)), mode='valid')
        curves.append(corr / np.sqrt(np.maximum(energy*sum(template*template), 1e-12)))
    events = []
    # Local correlation searches follow the audible delay train; they do not
    # rewrite the accepted primary lyric edges or tempo grid.
    for i in range(1, 10):
        guess = start + .343*i
        a, b = round((guess-.085)*sr), round((guess+.085)*sr)
        score = np.maximum(curves[0][a:b], curves[1][a:b])
        pos = a + int(np.argmax(score))
        onset = pos/sr-.015
        window = x[pos:pos+len(template)]
        power = np.mean(window**2, axis=0)
        pan = float((power[1]-power[0])/(power.sum()+1e-12))
        events.append(dict(text='SING', startFrame=round(onset*FPS),
                           measuredSeconds=round(onset, 5), stereoEnergyPan=round(pan, 3),
                           correlation=round(float(score.max()), 3)))
    return events


def echo_envelopes(path, events):
    """Measure each onset up to the next echo, then give its own tail a release.

    The mixed vocal cannot fully separate overlapping delay returns. Limiting
    measurement to one repeat avoids making old words pulse to later echoes.
    """
    sr, raw = wavfile.read(path)
    raw = raw[:8*sr].astype(np.float64)
    raw /= max(np.max(np.abs(raw)), 1)
    peaks = []
    for i, event in enumerate(events):
        start = event['measuredSeconds']
        end = events[i+1]['measuredSeconds'] if i+1<len(events) else start+.343
        count = max(2, round((end-start)*FPS))
        values = []
        for j in range(count):
            center = round((start+j/FPS)*sr)
            segment = raw[max(0,center-round(.020*sr)):center+round(.020*sr)]
            values.append(float(np.sqrt(np.mean(segment**2))))
        values = ndimage.gaussian_filter1d(values, .65)
        peaks.append(float(max(values)))
        # Continue the last measured energy as a decaying independent tail.
        tail = [float(values[-1])*math.exp(-(j+1)/FPS/.20)
                for j in range(round(1.18*FPS)-count+1)]
        event['amplitudeEnvelope'] = list(map(float,values))+tail
    reference = max(peaks)
    for event in events:
        event['amplitudeEnvelope'] = [round(min(1,v/reference),5) for v in event['amplitudeEnvelope']]


def ink_matte(alpha, texture):
    """A narrow, softly antialiased contour; stable spatial variation, no jitter."""
    alpha = ndimage.gaussian_filter(alpha, 1.0)
    narrow = ndimage.maximum_filter(alpha, size=5)
    wide = ndimage.maximum_filter(alpha, size=7)
    outer = ndimage.gaussian_filter(narrow*(1-texture)+wide*texture, .75)
    inner = ndimage.minimum_filter(alpha, size=3)
    edge = np.clip((alpha-inner)*.72, 0, 1)
    return alpha, outer, edge


def lettering(color, text='SING'):
    """Individually posed block letters, ink contour and small print hatching."""
    canvas = Image.new('RGBA', (max(660,len(text)*160+20), 275))
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf', 165)
    pen = 0
    for i, letter in enumerate(text):
        angle = [-5, 3, -3, 5][i%4]
        glyph = Image.new('RGBA', (210, 240))
        draw = ImageDraw.Draw(glyph)
        draw.text((18, 14), letter, font=font, fill='#292536', stroke_width=11, stroke_fill='#292536')
        draw.text((12, 5), letter, font=font, fill=color, stroke_width=6, stroke_fill='#292536')
        glyph = glyph.rotate(angle, Image.Resampling.BICUBIC, expand=False)
        canvas.alpha_composite(glyph, (pen, [12, 0, 8, 1][i%4]))
        pen += round(font.getlength(letter)) + 7
    box = canvas.getbbox()
    canvas = canvas.crop(box)
    # Hatching is clipped to opaque letter interiors, never the transparent field.
    pix = np.array(canvas)
    yy, xx = np.indices(pix.shape[:2])
    mask = (pix[:,:,3] > 240) & (pix[:,:,0] > 100) & (yy > pix.shape[0]*.70) & ((xx+2*yy)%22 < 2)
    pix[mask,:3] = (104, 85, 67)
    return Image.fromarray(pix)


def rubber_warp(word, angle, u, strong=False):
    """Area-preserving stretch along the projected path, with elastic shear."""
    depth = 1/(1+.24*math.cos(angle))
    vx = 625*(math.cos(angle)*depth+.24*math.sin(angle)**2*depth**2)
    vy = 175*math.sin(angle)
    direction = np.array([vx,vy],dtype=float)
    speed = np.linalg.norm(direction)
    direction /= max(speed,1)
    stretch = 1+.25*min(speed/700,1)-.10*abs(math.sin(angle))
    stretch += .09*math.sin(22*u)*math.exp(-2.8*u)
    if strong:
        stretch = 1+.95*min(speed/700,1)-.28*abs(math.sin(angle))
        stretch += .24*math.sin(15*u)*math.exp(-1.5*u)
        stretch = max(.65,min(2.15,stretch))
    perpendicular = np.array([-direction[1],direction[0]])
    matrix = stretch*np.outer(direction,direction)+(1/stretch)*np.outer(perpendicular,perpendicular)
    matrix[0,1] += (.24 if strong else .075)*math.sin(16*u)*math.exp(-1.6*u)
    inverse = np.linalg.inv(matrix)
    size = (math.ceil(word.width*(2.6 if strong else 1.55)),math.ceil(word.height*(3.4 if strong else 2.1)))
    source_center = np.array(word.size)/2
    target_center = np.array(size)/2
    offset = source_center-inverse@target_center
    coefficients = (inverse[0,0],inverse[0,1],offset[0],inverse[1,0],inverse[1,1],offset[1])
    warped = word.transform(size,Image.Transform.AFFINE,coefficients,Image.Resampling.BICUBIC)
    return warped


def orbital_letters(age, event, index, glyphs):
    """Separate 3D ellipses and traveling pulse, then constant object scale."""
    life = 1.35
    side = 1 if event['stereoEnergyPan'] >= 0 else -1
    direction = 1 if index%2 else -1
    envelope = event['amplitudeEnvelope']
    peak = max(envelope)
    layers = []
    for j,glyph in enumerate(glyphs):
        # Each glyph has its own phase, orbit radius, speed and vertical plane.
        phi = side*math.pi/2 + direction*math.pi*1.35*(age/life)*(1+.035*j)+(j-1.5)*.17
        z = -math.cos(phi)
        perspective = 1/(1-.38*z)
        radius = 545+20*j
        x = W*.5 + radius*math.sin(phi)*perspective+(j-1.5)*44
        y = 585 + 155*z + [-25,12,-10,30][j] + 18*math.sin(phi+j*.4)
        local_age = age-j*.10
        # Single legible wave: S peaks first, then I, N, G. After each
        # pulse the object's scale is fixed; only perspective changes it.
        pulse = math.exp(-((local_age-.13)/.085)**2) if 0<=local_age<.38 else 0
        strength = .8+.4*peak
        base = max(.65,1-index*.035)*perspective
        sx = base*(1+.72*strength*pulse)
        sy = base*(1+1.10*strength*pulse)
        height = 71
        im = glyph.resize((max(1,round(height*glyph.width/glyph.height*sx)),max(1,round(height*sy))),Image.Resampling.LANCZOS)
        im = im.rotate(-side*8*math.cos(phi)+5*pulse,Image.Resampling.BICUBIC,expand=True)
        opacity = min(1,age/.065,(life-age)/.45)
        im.putalpha(im.getchannel('A').point(lambda a:int(a*opacity)))
        layers.append((z,im,round(x-im.width/2),round(y-im.height/2)))
    return layers


def sprites(frame, events, art, rubber=False, strong=False, letter_art=None, letter_orbits=False):
    layers = []
    for i, event in enumerate(events):
        age = (frame-event['startFrame'])/FPS
        life = 1.35 if letter_orbits else (1.65 if strong else 1.18)
        if not 0 <= age < life:
            continue
        if letter_orbits:
            layers.extend(orbital_letters(age,event,i,letter_art[i%len(letter_art)]))
            continue
        u = age/life
        side = 1 if event['stereoEnergyPan'] >= 0 else -1
        # Begin at the measured pan side. Alternating arcs travel in front of
        # or behind the body, then cross its plane at the side of the ellipse.
        angle = side*math.pi/2 + (1 if i%2 else -1)*math.pi*(.90 if strong else 1.35)*u
        z = -math.cos(angle)
        depth = 1/(1-.24*z)
        decay = max(.58, 1-i*.045)
        envelope = event.get('amplitudeEnvelope')
        amplitude = float(np.interp(age*FPS, np.arange(len(envelope)), envelope)) if envelope else 1
        scale = depth*decay*(.58+.65*amplitude**.65)
        x = W*.50 + 625*math.sin(angle)*depth
        y = 570 + 175*z - 28*math.sin(math.pi*u)
        if letter_art:
            glyphs = letter_art[i%len(letter_art)]
            # Four independent glyphs, not a transformed word-sized rectangle.
            # The audio envelope propagates across the letters with 100ms lag.
            widths = [g.width/g.height*78 for g in glyphs]
            total = sum(widths)+18
            pen = -total/2
            base_scale = depth*decay*(.80+.16*amplitude**.65)
            for j,glyph in enumerate(glyphs):
                lag = j*.10
                local_age = age-lag
                amp = float(np.interp(max(0,local_age)*FPS,np.arange(len(envelope)),envelope)) if local_age>=0 else 0
                pulse = math.exp(-((local_age-.15)/.115)**2) if local_age>=0 else 0
                rebound = math.sin(max(0,local_age-.23)*22)*math.exp(-max(0,local_age-.23)*7) if local_age>.23 else 0
                swell = 1+.48*amp+.55*pulse
                sx = base_scale*swell*(1-.14*pulse+.06*rebound)
                sy = base_scale*swell*(1+.24*pulse-.10*rebound)
                im = glyph.resize((max(1,round(widths[j]*sx)),max(1,round(78*sy))),Image.Resampling.LANCZOS)
                tilt = -side*9*math.cos(angle)+7*math.sin(local_age*14)*pulse
                im = im.rotate(tilt,Image.Resampling.BICUBIC,expand=True)
                offset = (pen+widths[j]/2)*base_scale
                gx = x+offset
                gy = y+offset*.12*math.sin(angle)-22*pulse*base_scale
                # A slight depth spread makes the glyphs cross the narrator
                # plane individually while retaining the established orbit.
                gz = z+.035*(j-1.5)*math.sin(angle)
                fade = min(1,age/.065,(life-age)/.26)*(.30+.70*max(amplitude,amp)**.6)
                im.putalpha(im.getchannel('A').point(lambda a:int(a*fade)))
                layers.append((gz,im,round(gx-im.width/2),round(gy-im.height/2)))
                pen += widths[j]+6
            continue
        word = art[i%len(art)]
        width = int(305*scale)
        word = word.resize((width, round(width*word.height/word.width)), Image.Resampling.LANCZOS)
        if rubber:
            word = rubber_warp(word,angle,u,strong)
        word = word.rotate(-side*9*math.cos(angle), Image.Resampling.BICUBIC, expand=True)
        fade = min(1, age/.065, (life-age)/.26)*(.30+.70*amplitude**.6)
        word.putalpha(word.getchannel('A').point(lambda a: int(a*fade)))
        layers.append((z, word, round(x-word.width/2), round(y-word.height/2)))
    return sorted(layers, key=lambda layer: layer[0])


def decode(path, frames, pad=False):
    vf = f'fps={FPS},' + ('pad=1920:1080:2:0' if pad else 'scale=1920:1080')
    return subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vf',vf,
        '-frames:v',str(frames),'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)


def main():
    global OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--echo-vocal', required=True)
    parser.add_argument('--version', default='v002')
    parser.add_argument('--rubber', action='store_true')
    parser.add_argument('--rubber-strong', action='store_true')
    parser.add_argument('--letter-wave', action='store_true')
    parser.add_argument('--letter-orbits', action='store_true')
    args = parser.parse_args()
    OUT = BASE / f'generated/motion-graphics/sing-echo-{args.version}'
    OUT.mkdir(parents=True, exist_ok=True)
    timeline_path = BASE/'timeline.json'
    timeline_hash = hashlib.sha256(timeline_path.read_bytes()).hexdigest()
    timeline = json.loads(timeline_path.read_text())
    word = timeline['tracks'][0]['items'][0]['words'][-1]
    score = json.loads((BASE/'shots/shotlist.json').read_text())
    insert = score['avatarInserts'][0]
    frames = insert['endFrameExclusive']-insert['startFrame']
    events = analyze(args.echo_vocal, word['start'])
    echo_envelopes(args.echo_vocal, events)
    config = dict(status='draft_review', frames=frames, fps=FPS, primaryWord=word,
        events=events, panMethod='L/R energy over matched echo windows in supplied stereo vocal export; indicative, not isolated delay-bus automation.',
        timingPolicy='Existing primary lyric timing unchanged. Echo attacks measured separately and quantized to edit frames.',
        depthPolicy='Perspective-scaled ellipse; negative z below narrator matte, positive z above. Face avoided.',
        timelineSha256=timeline_hash,
        amplitudePolicy='40ms stereo RMS windows; each repeat measured only until next onset, normalized jointly, smoothed and followed by independent 200ms release. Approximation from mixed vocal, not isolated echo stems.',
        outlinePolicy='Near-black 2–3px outer ink contour at native 1080p, gently varying width, softened subpixel edge and narrow inner edge treatment.',
        motionBlur=False,
        rubberMotion=args.rubber,
        letterWave=args.letter_wave,
        independentLetterOrbits=args.letter_orbits,
        independentOrbitPolicy='Individual phase/radius/speed/height and per-letter perspective/occlusion. S-I-N-G pulses 100ms apart; fixed object scale after pulse, perspective remains active; opacity-only tail fade.' if args.letter_orbits else None,
        letterPolicy='Independent glyph layers; 100ms staggered audio envelope and elastic swell from S through I, N, G. Original 1.18s curved orbit; no whole-word warp.' if args.letter_wave else None,
        rubberStrong=args.rubber_strong,
        travelPolicy='1.65 second lifetime, 0.90 pi arc; about 48 percent of previous angular speed, stretch up to 2.15x.' if args.rubber_strong else 'Original travel',
        rubberPolicy='Projected-velocity directional stretch, reciprocal perpendicular squash, compression through turns and damped elastic rebound/shear.' if args.rubber else None)
    (OUT/'analysis.json').write_text(json.dumps(config,indent=2)+'\n')
    art = [lettering(c) for c in ['#f7dda2','#9dd8cf','#f0b38b']]
    letter_art = [[lettering(c,ch) for ch in 'SING'] for c in ['#f7dda2','#9dd8cf','#f0b38b']] if args.letter_wave or args.letter_orbits else None
    for i, sprite in enumerate(art): sprite.save(OUT/f'sing-lettering-{i+1}.png')
    fgdec = decode(BASE/insert['source'],frames)
    bgdec = decode(BASE/insert['backgroundVideo'],frames,pad=True)
    silent = OUT/'opening-word-art-silent.mp4'
    enc = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
        '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
        '-crf','18','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
    yy,xx=np.indices((H,W),dtype=np.float32)
    texture=(.5+.5*np.sin(xx*.031+np.sin(yy*.024)))*.65
    ink=np.array([19,17,22],dtype=np.float32)
    for frame in range(frames):
        fgraw=fgdec.stdout.read(W*H*3); bgraw=bgdec.stdout.read(W*H*3)
        assert len(fgraw)==len(bgraw)==W*H*3
        fg=np.frombuffer(fgraw,np.uint8).reshape(H,W,3).astype(np.float32)
        back=Image.frombytes('RGB',(W,H),bgraw).convert('RGBA')
        layers=sprites(frame,events,art,args.rubber,args.rubber_strong,letter_art,args.letter_orbits)
        for z,im,x,y in layers:
            if z<0: back.alpha_composite(im,(x,y))
        r,g,b=fg[:,:,0],fg[:,:,1],fg[:,:,2]
        alpha=1-np.clip((g-np.maximum(r,b)-12)/55,0,1)
        fg[:,:,1]=np.minimum(g,np.maximum(r,b)+8+20*alpha)
        alpha,outer,edge=ink_matte(alpha,texture)
        fg=fg*(1-edge[:,:,None])+ink*edge[:,:,None]
        bg=np.asarray(back)[:,:,:3].astype(np.float32)
        # The outer contour is part of the narrator plane and therefore also
        # correctly occludes lettering that travels behind her.
        bg=ink*outer[:,:,None]+bg*(1-outer[:,:,None])
        rgb=np.uint8(np.clip(fg*alpha[:,:,None]+bg*(1-alpha[:,:,None]),0,255))
        picture=Image.fromarray(rgb).convert('RGBA')
        for z,im,x,y in layers:
            if z>=0: picture.alpha_composite(im,(x,y))
        if frame in [96,104,112,120,128,136,144,152]:
            picture.convert('RGB').resize((960,540)).save(OUT/f'frame-{frame:03}.jpg')
        if frame==112:
            picture.convert('RGB').save(OUT/'outline-detail.png')
        enc.stdin.write(picture.convert('RGB').tobytes())
    enc.stdin.close();assert enc.wait()==0
    for dec in [fgdec,bgdec]: dec.stdout.close();dec.wait()
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(silent),'-i',str(BASE/'generated/source/master.wav'),
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-t',str(frames/FPS),
        '-movflags','+faststart',str(OUT/'opening-sing-echo-1080p.mp4')],check=True)
    # Keep the existing lyric footer intact for the timing-review version.
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(BASE/'generated/visual-animatic-v005/Let-the-Phone-Book-Sing-visual-animatic-v005.mp4'),
        '-i',str(silent),'-filter_complex','[1:v]scale=1066:600[art];[0:v][art]overlay=107:0:shortest=1[v]',
        '-map','[v]','-map','0:a','-frames:v',str(frames),'-c:v','libx264','-crf','18','-c:a','copy',
        '-movflags','+faststart',str(OUT/'opening-sing-echo-review.mp4')],check=True)
    assert hashlib.sha256(timeline_path.read_bytes()).hexdigest()==timeline_hash
    print(json.dumps(events,indent=2))


if __name__ == '__main__': main()
