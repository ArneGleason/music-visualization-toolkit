"""FX-04 depth procession: detected brass rims and anticipatory musical arrivals."""
import json
import math
import pathlib
import sys
import colorsys
import argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
import numpy as np
from tracked_light_pilot import run,linear,display
OUT=ROOT/'out/tunnel_arrival_pilot'
INTENSE='--intense' in sys.argv
if INTENSE:
    OUT=ROOT/'out/tunnel_arrival_intense'
TWO_COLOR='--two-color' in sys.argv
if TWO_COLOR:
    INTENSE=True
    OUT=ROOT/'out/tunnel_arrival_amber_cyan'


def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--shot')
    parser.add_argument('--two-color', action='store_true')
    parser.add_argument('--intense', action='store_true')
    args=parser.parse_args()
    if args.shot:
        OUT=ROOT/'out'/('tunnel_arrival_'+args.shot)
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'frames').mkdir(exist_ok=True)
    saved=json.loads((ROOT/'out/musical_contour_tunnel_analog/tracking.json').read_text())
    first,end=saved['song_frames']; count=end-first
    if args.shot:
        shot=next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots'] if s['id']==args.shot)
        assert shot['setup']=='telescope_time_tunnel' and shot['clip']['speed']==1
        first,end=round(shot['start_sec']*24),round(shot['end_sec']*24)
        count=end-first
        saved['source']=shot['clip']
        local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
        paths=list(pathlib.Path(local['sources']['stems']).glob('*Drum Kit*restored.wav'))
        assert len(paths)==1
        drums=np.frombuffer(run(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-af',
            'highpass=f=90,lowpass=f=1800,aresample=8000','-f','f32le','-']),'<f4')
        tracks=json.loads((ROOT/'projects/rivers-of-mars/generated/waveforms.json').read_text())['tracks']
        offset=next(t['offsetSec'] for t in tracks if t['id']=='drums')
        ts=np.arange(first/24-.5,end/24,1/192)
        envelope=np.array([np.sqrt(np.mean(drums[max(0,int((t-offset)*8000)-80):int((t-offset)*8000)+1]**2)) for t in ts])
        onset=np.maximum(envelope-np.roll(envelope,4),0); onset[:4]=0
        chosen=[]
        for i in np.argsort(onset)[::-1]:
            if onset[i]<np.quantile(onset,.90): break
            if all(abs(ts[i]-ts[j])>.3 for j in chosen): chosen.append(int(i))
        saved['events']=[(float(ts[i]),float(onset[i]/max(onset.max(),1e-6))) for i in sorted(chosen)]
    events=[(t,v) for t,v in saved['events'] if first/24+.5<=t<end/24-.3 and v>.6]
    assert events
    pulse_colors=[]
    for j,(hit,_) in enumerate(events):
        # Warm/cool opposition, with only +/- two degrees of long-period hue drift.
        hue=(.095 if j%2==0 else .515)+math.sin((hit-first/24)*math.tau/12)*2/360
        pulse_colors.append(np.array(colorsys.hsv_to_rgb(hue,.90,1.),np.float32))
    local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
    paths=list(pathlib.Path(local['sources']['stems']).glob('*Guitar*restored.wav')); assert len(paths)==1
    raw=run(['ffmpeg','-v','error','-i',str(paths[0]),'-ac','1','-af',
             'highpass=f=90,lowpass=f=1800,aresample=8000','-f','f32le','-'])
    guitar=np.frombuffer(raw,'<f4'); go=saved['guitar_offset']
    norm=max(float(np.quantile(np.abs(guitar[int((first/24-go)*8000):int((end/24-go)*8000)]),.97)),1e-5)
    cap=cv2.VideoCapture(str(ROOT/saved['source']['file']))
    cap.set(cv2.CAP_PROP_POS_FRAMES,round(saved['source']['in_sec']*24))
    theta=np.arange(512)*math.tau/512
    radii=np.arange(65,610,dtype=np.float32)
    mx=(630+np.cos(theta)[None,:]*radii[:,None]).astype(np.float32)
    my=(315+np.sin(theta)[None,:]*radii[:,None]*172/174).astype(np.float32)
    records=[]
    for f in range(count):
        ok,frame=cap.read(); assert ok
        t=(first+f)/24
        b,g,r=cv2.split(frame.astype(np.float32)/255)
        gold=np.maximum(r-b,0)*(.3+.7*g)
        sampled=cv2.remap(gold,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
        valid=(mx>=0)&(mx<1280)&(my>=0)&(my<720)
        profile=(sampled.sum(axis=1)/np.maximum(valid.sum(axis=1),1)).astype(np.float32)
        smooth=cv2.GaussianBlur(profile[:,None],(1,9),1.5).ravel()
        candidates=[i for i in range(2,len(radii)-2) if smooth[i]>smooth[i-1]
                    and smooth[i]>=smooth[i+1] and smooth[i]>.06]
        chosen=[]
        for i in sorted(candidates,key=lambda i:smooth[i],reverse=True):
            if all(abs(radii[i]-radii[j])>19 for j in chosen): chosen.append(i)
        rings=sorted(float(radii[i]) for i in chosen)
        beam=np.zeros((1440,2560,3),np.float32)
        layers=[np.zeros_like(beam) for _ in range(3)] if INTENSE else None
        signal=np.interp((t-go-.064+np.arange(512)/8000)*8000,np.arange(len(guitar)),guitar)/norm
        signal=np.tanh(signal*1.35+.14*signal**2)*np.sin(theta/2)**2
        arrivals=[]
        for event_id,(hit,strength) in enumerate(events):
            age=t-hit
            if -.5<=age<=.2:
                progress=np.clip((age+.5)/.5,0,1)
                arrivals.append((75*(480/75)**progress,math.exp(-max(age,0)/.075),age,event_id))
        for k,radius in enumerate(rings):
            # Detected per frame, not cloned with a common scale: depth has parallax.
            travel=sum(weight*math.exp(-.5*(math.log(radius/rr)/.19)**2) for rr,weight,age,event_id in arrivals)
            travel_color=np.zeros(3,np.float32)
            if TWO_COLOR:
                for rr,weight,age,event_id in arrivals:
                    travel_color+=pulse_colors[event_id]*weight*math.exp(-.5*(math.log(radius/rr)/.19)**2)
            amp=2+min(radius/70,5)
            if INTENSE:
                amp*=10
            offset=signal*amp+.35*np.sin(theta*53+f*.8)
            points=np.column_stack((630+(radius+offset)*np.cos(theta),
                                    315+(radius+offset)*np.sin(theta)*172/174))
            derivative=(np.roll(offset,-1)-np.roll(offset,1))/(2*math.tau/512*radius)
            dwell=1/np.sqrt(1+derivative**2)
            scan=.23+.77*np.exp(-((f/24*.65+k*.11-theta/math.tau)%1)/.38)
            amount=(.24+.22*min(radius/480,1))*scan+travel*2.5
            depth=min(radius/480,1)
            if INTENSE:
                amount*=.65+1.8*depth**1.4
            target=layers[0 if radius<160 else 1 if radius<320 else 2] if INTENSE else beam
            for i in range(512):
                value=float(amount[i]*dwell[i])
                color=tuple(float(v*value) for v in (.40,.88,.65))
                if TWO_COLOR:
                    ambient=(.24+.22*depth)*scan[i]*np.array([.23,.39,.38])
                    colored=(ambient+travel_color*2.5)*(.65+1.8*depth**1.4)*dwell[i]
                    color=tuple(float(v) for v in colored)
                a=tuple(np.round(points[i]*2).astype(int)); z=tuple(np.round(points[(i+1)%512]*2).astype(int))
                width=1+int(2*dwell[i]+min(travel,1)*2)
                if INTENSE:
                    width+=int(depth*2)
                cv2.line(target,a,z,color,width,cv2.LINE_AA)
        small=cv2.resize(beam,(1280,720),interpolation=cv2.INTER_AREA)
        glow=small+cv2.GaussianBlur(small,(0,0),2)*.6+cv2.GaussianBlur(small,(0,0),8)*.25
        if INTENSE:
            glow=np.zeros((720,1280,3),np.float32)
            for band,layer in enumerate(layers):
                core=cv2.resize(layer,(1280,720),interpolation=cv2.INTER_AREA)
                # Wider optical scatter in the near field, without blurring the plate.
                glow+=core+cv2.GaussianBlur(core,(0,0),2+band*1.5)*1.2
                glow+=cv2.GaussianBlur(core,(0,0),8+band*5)*(.65+band*.25)
                glow+=cv2.GaussianBlur(core,(0,0),22+band*9)*(.25+band*.15)
        result=(display(linear(frame[:,:,::-1].astype(np.float32)/255)+glow)*255+.5).astype(np.uint8)[:,:,::-1]
        cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
        records.append({'frame':first+f,'detected_radii':rings,'travel_radii':[float(a[0]) for a in arrivals]})
    cap.release()
    run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/'frames/%04d.png'),
         '-frames:v',str(count),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p',
         '-an','-movflags','+faststart',str(OUT/'clean.mp4')])
    run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/'frames/%04d.png'),
         '-ss',str(first/24),'-i',str(ROOT/'audio/song.wav'),'-t',str(count/24),'-c:v','libx264',
         '-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(OUT/'tunnel_arrivals.mp4')])
    (OUT/'controls.json').write_text(json.dumps({'song_frames':[first,end],'events':events,
        'intense':INTENSE,'waveform_gain':10 if INTENSE else 1,
        'two_color':TWO_COLOR,'pulse_colors_linear_rgb':[c.tolist() for c in pulse_colors] if TWO_COLOR else None,
        'palette_policy':'alternating amber/cyan; fixed hue per event; +/-2 degree drift over 12 sec; muted teal ambient' if TWO_COLOR else None,
        'depth_emission_gain':'.65 + 1.8 * depth**1.4' if INTENSE else 'original',
        'lead_seconds':.5,'arrival_radius_px':480,'method':'per-frame radial brass-edge detection; no persistent ring identity',
        'limitations':'authored centre; no spoke occlusion; simplified scan/bloom, no temporal phosphor history',
        'frames':records},indent=2))
    print('DONE',count)


if __name__=='__main__': main()
