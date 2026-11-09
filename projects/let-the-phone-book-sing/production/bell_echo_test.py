"""Three measured Bell echoes, receding hops across the clear upper-right wall."""
import hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import signal
from scipy.io import wavfile
from sing_echo_test import lettering,echo_envelopes
from build_fullframe_animatic import overlay_lyrics

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'generated/motion-graphics/belle-echo-v002'
OUT.mkdir(parents=True,exist_ok=True)
FPS=24;W=1920;H=1080
score=json.loads((BASE/'shots/shotlist.json').read_text())
insert=next(x for x in score['reviewVideoInserts'] if x['id']=='belle-continuous')
start=insert['startFrame'];end=insert['endFrameExclusive'];frames=end-start
before=hashlib.sha256((BASE/'timeline.json').read_bytes()).hexdigest()
lines=json.loads((BASE/'timeline.json').read_text())['tracks'][0]['items']
word=lines[2]['words'][0]
lead=Path('/Users/arnegleason/Downloads/Let-the-Phone-Book-Sing-clean-MIDI-split-drums-leadexport 2026-11-08 1538.wav')
sr,raw=wavfile.read(lead);samples=raw[round(start/FPS*sr):round(end/FPS*sr)]
wavfile.write(OUT/'echo-analysis-vocal.wav',sr,samples)
x=signal.resample_poly(samples.astype(float),1,6);x/=abs(x).max();rate=sr//6
anchor=word['start']-start/FPS
left=anchor+.019;right=anchor+.249
template=x[round(left*rate):round(right*rate)].mean(axis=1)
curves=[]
for ch in range(2):
 y=x[:,ch];corr=signal.correlate(y,template,mode='valid',method='fft');energy=signal.convolve(y*y,np.ones(len(template)),mode='valid');curves.append(corr/np.sqrt(np.maximum(energy*sum(template*template),1e-12)))
events=[]
for i in range(1,4):
 guess=left+.343*i;a=round((guess-.07)*rate);b=round((guess+.07)*rate)
 c=np.maximum(curves[0][a:b],curves[1][a:b]);pos=a+int(np.argmax(c));onset=pos/rate-.019
 window=x[pos:pos+len(template)];power=np.mean(window**2,axis=0)
 events.append(dict(text='BELLE',startFrame=round(onset*FPS),masterFrame=start+round(onset*FPS),measuredSeconds=onset,masterSeconds=start/FPS+onset,correlation=float(c.max()),stereoEnergyPan=float((power[1]-power[0])/(power.sum()+1e-12))))
echo_envelopes(OUT/'echo-analysis-vocal.wav',events)
config=dict(status='draft_review',shotIds=['PB-003','PB-004'],startFrame=start,endFrameExclusive=end,events=events,source=insert['source'],sourceOffsetFrames=insert['sourceOffsetFrames'],styleReference='sing-echo-v002',path='Three whole readable words take short receding arcs across upper-right wall; no orbit or letter scattering. Clear before bag pickup.',audioMethod='First Bell waveform matched against stereo vocal; three strong repeats retained; per-echo loudness is approximate due to overlapping lead.',timelineSha256=before)
(OUT/'analysis.json').write_text(json.dumps(config,indent=2)+'\n')
art=[lettering(c,'BELLE') for c in ['#f7dda2','#9dd8cf','#f0b38b']]
for i,im in enumerate(art):im.save(OUT/f'bell-lettering-{i+1}.png')
offset=insert['sourceOffsetFrames']
dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(BASE/insert['source']),'-vf',f'fps=24,trim=start_frame={offset}:end_frame={offset+frames},pad=1920:1080:2:0','-frames:v',str(frames),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
silent=OUT/'belle-word-art-silent.mp4'
enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
for f in range(frames):
 data=dec.stdout.read(W*H*3);assert len(data)==W*H*3
 picture=Image.frombytes('RGB',(W,H),data).convert('RGBA')
 for i,e in enumerate(events):
  age=(f-e['startFrame'])/FPS;life=.88
  if not 0<=age<life:continue
  u=age/life;amp=float(np.interp(age*FPS,np.arange(len(e['amplitudeEnvelope'])),e['amplitudeEnvelope']))
  # Distinct ascending/receding arcs, away from Belle's initial face and hands.
  x=1180+i*100+220*u;y=600-i*180-75*math.sin(math.pi*u)-40*u
  perspective=(1-i*.15)*(1-.24*u)
  width=round(310*perspective*(.78+.40*amp**.65))
  im=art[i].resize((width,round(width*art[i].height/art[i].width)),Image.Resampling.LANCZOS)
  im=im.rotate(7-12*u,Image.Resampling.BICUBIC,expand=True)
  alpha=min(1,age/.065,(life-age)/.27)*(.45+.55*amp**.6)
  im.putalpha(im.getchannel('A').point(lambda a:int(a*alpha)))
  picture.alpha_composite(im,(round(x-im.width/2),round(y-im.height/2)))
 if f in [12,20,28,36,44]:picture.convert('RGB').save(OUT/f'frame-{f:03}.jpg')
 enc.stdin.write(picture.convert('RGB').tobytes())
enc.stdin.close();assert enc.wait()==0;dec.stdout.close();dec.wait()
subprocess.run(['ffmpeg','-y','-v','error','-i',str(silent),'-ss',str(start/FPS),'-i',str(BASE/'generated/source/master.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-t',str(frames/FPS),'-movflags','+faststart',str(OUT/'belle-bell-echo-1080p.mp4')],check=True)
# Context preview preserves the chosen opening exactly; new effect only on Belle.
subprocess.run(['ffmpeg','-y','-v','error','-i',str(BASE/'generated/motion-graphics/sing-echo-v002/opening-word-art-silent.mp4'),'-i',str(silent),'-i',str(BASE/'generated/source/master.wav'),'-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]','-map','[v]','-map','2:a','-frames:v',str(end),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','320k','-t',str(end/FPS),'-movflags','+faststart',str(OUT/'opening-and-bell-echo-clean.mp4')],check=True)
overlay_lyrics(OUT/'opening-and-bell-echo-clean.mp4',OUT/'opening-and-bell-echo-review.mp4',lines,end)
assert hashlib.sha256((BASE/'timeline.json').read_bytes()).hexdigest()==before
print(json.dumps([{k:v for k,v in e.items() if k!='amplitudeEnvelope'} for e in events],indent=2))
