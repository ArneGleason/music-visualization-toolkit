"""FX-02: local feature tracking and linear-light meter augmentation.

Run with Python; requires numpy and opencv-python-headless. Local test dependencies
may live in out/fx_tracking_deps. Does not alter source footage or assembly.
"""
import json
import math
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'out/fx_tracking_deps'))
import cv2
import numpy as np

OUT = ROOT / 'out/tracked_light_receiver'


def run(args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def linear(a):
    return np.where(a <= .04045, a / 12.92, ((a + .055) / 1.055) ** 2.4)


def display(a):
    a = np.clip(a, 0, 1)
    return np.where(a <= .0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - .055)


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    (OUT / 'frames').mkdir(exist_ok=True)
    cues = json.loads((ROOT / 'generated/overlay_cues.json').read_text())
    cue = next(s for s in cues['shots'] if s['id'] == 's010')
    first, end, fps = cue['start'], cue['end'], int(cues['fps'])
    shot = next(s for s in json.loads((ROOT / 'shots/shotlist.json').read_text())['shots']
                if s['id'] == 's010')
    assert shot['setup'] == 'receiver_dial_macro' and shot['frames'] == end-first
    assert shot['clip']['speed'] == 1, 'Retimed source needs explicit mapping'
    source = ROOT / shot['clip']['file']
    cap = cv2.VideoCapture(str(source))
    assert abs(cap.get(cv2.CAP_PROP_FPS)-fps) < .01
    cap.set(cv2.CAP_PROP_POS_FRAMES, round(shot['clip']['in_sec']*fps))
    frames = []
    for _ in range(end-first):
        ok, frame = cap.read()
        assert ok, 'Insufficient source coverage'
        frames.append(frame)
    cap.release()
    h, w = frames[0].shape[:2]
    assert (w, h) == (1280, 720), 'Re-author initial mask for different resolution'

    local = json.loads((ROOT / 'projects/rivers-of-mars/project.local.json').read_text())
    stems = list(pathlib.Path(local['sources']['stems']).glob('*Drum Kit*restored.wav'))
    assert len(stems) == 1
    raw = run(['ffmpeg', '-v', 'error', '-i', str(stems[0]), '-ac', '1', '-af',
               'highpass=f=100,lowpass=f=2800,aresample=8000', '-f', 'f32le', '-'])
    audio = np.frombuffer(raw, dtype='<f4')
    wave = json.loads((ROOT / 'projects/rivers-of-mars/generated/waveforms.json').read_text())
    offset = next(t['offsetSec'] for t in wave['tracks'] if t['id'] == 'drums')
    times = np.arange(first/fps-.6, end/fps, 1/192)
    rms = []
    for t in times:
        i = int((t-offset)*8000)
        rms.append(np.sqrt(np.mean(audio[max(0,i-80):i+1]**2)))
    rms = np.asarray(rms)
    onset = np.maximum(rms-np.roll(rms,4),0); onset[:4]=0
    candidates = [i for i in range(1,len(onset)-1) if onset[i]>onset[i-1]
                  and onset[i]>=onset[i+1] and onset[i]>np.quantile(onset,.88)]
    selected = []
    for i in sorted(candidates,key=lambda i:onset[i],reverse=True):
        if all(abs(times[i]-times[j])>=.22 for j in selected):
            selected.append(i)
    events = [(float(times[i]),float(onset[i]/max(onset.max(),1e-6)))
              for i in sorted(selected)]

    gray0 = cv2.cvtColor(frames[0],cv2.COLOR_BGR2GRAY)
    region = np.zeros((h,w),np.uint8)
    region[375:667,440:810]=255
    region[410:545,475:770]=0  # avoid illuminated face and animated needle
    original = cv2.goodFeaturesToTrack(gray0,120,.015,7,mask=region)
    assert original is not None and len(original)>=12
    points=original.copy(); previous=gray0
    yy,xx=np.mgrid[:h,:w]
    shape=(((xx-621)/155)**2+((yy-557)/149)**2<1)&(yy<536)
    # Track the aperture, but sample its changing needle/texture in each frame.
    mask=shape.astype(np.float32)
    mask=cv2.GaussianBlur(mask,(0,0),1.4)
    records=[]
    for f,frame in enumerate(frames):
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if f:
            moved,status,_=cv2.calcOpticalFlowPyrLK(previous,gray,points,None,
                winSize=(25,25),maxLevel=3)
            back,back_status,_=cv2.calcOpticalFlowPyrLK(gray,previous,moved,None,
                winSize=(25,25),maxLevel=3)
            good=(status.ravel()>0)&(back_status.ravel()>0)&(
                np.linalg.norm(back-points,axis=2).ravel()<1.)
            points=moved[good]; original=original[good]
        assert len(points)>=12, f'Track lost at frame {f}'
        transform,inliers=cv2.findHomography(original,points,cv2.RANSAC,1.5)
        assert transform is not None and inliers.sum()>=10
        predicted=cv2.perspectiveTransform(original,transform)
        residual=np.linalg.norm(predicted-points,axis=2).ravel()[inliers.ravel()>0]
        assert np.median(residual)<1., f'Track residual too high at {f}'
        tracked=cv2.warpPerspective(mask,transform,(w,h))
        b,g,r=cv2.split(frame.astype(np.float32)/255)
        tracked*=np.clip((r-b-.12)*4,0,1)
        t=(first+f+.5)/fps
        pulse=min(1.,sum(v*(1-math.exp(-(t-e)/.018))*math.exp(-(t-e)/.19)
                         for e,v in events if 0<=t-e<1.2))
        strength=.08+1.25*pulse
        rgb=linear(frame[:,:,::-1].astype(np.float32)/255)
        # Multiplicative core preserves native markings; soft light is additive.
        core=rgb*tracked[:,:,None]*strength*.65
        halo=(cv2.GaussianBlur(tracked,(0,0),10)*.13+
              cv2.GaussianBlur(tracked,(0,0),30)*.075)*strength
        glow=halo[:,:,None]*np.array([1.,.46,.10],np.float32)
        result=(display(rgb+core+glow)*255+.5).astype(np.uint8)[:,:,::-1]
        cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
        if f in (0,24,end-first-1):
            check=frame.copy()
            contour=np.array([[[467.,532.],[490.,458.],[548.,415.],
                                [621.,405.],[695.,425.],[748.,470.],[773.,532.]]],np.float32)
            contour=cv2.perspectiveTransform(contour,transform).astype(np.int32)
            cv2.polylines(check,contour,True,(0,255,0),2)
            cv2.imwrite(str(OUT/f'track_check_{f:04d}.jpg'),check)
        records.append({'frame':first+f,'pulse':pulse,'strength':strength,
                        'inliers':int(inliers.sum()),'median_error_px':float(np.median(residual)),
                        'homography':transform.tolist()})
        previous=gray
    run(['ffmpeg','-y','-v','error','-framerate',str(fps),'-i',str(OUT/'frames/%04d.png'),
         '-ss',str(first/fps),'-i',str(ROOT/'audio/song.wav'),'-t',str((end-first)/fps),
         '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
         '-movflags','+faststart',str(OUT/'receiver_light.mp4')])
    (OUT/'tracking.json').write_text(json.dumps({'shot':'s010','source':str(source),
        'source_in_frame':round(shot['clip']['in_sec']*fps),'song_frames':[first,end],
        'fps':fps,'stem_offset_sec':offset,'events':events,'frames':records,
        'method':'local optical flow plus RANSAC homography; not camera solve',
        'delivery':'flattened review only; no assembly change'},indent=2))
    print(f'DONE: {len(records)} frames; max median track error '
          f'{max(r["median_error_px"] for r in records):.3f}px')


if __name__=='__main__':
    main()
