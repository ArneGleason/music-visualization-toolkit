"""Number-preserving owner notes pass; new local effects, no generated footage."""
from pathlib import Path
import sys,json,subprocess,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'));sys.path.insert(0,str(ROOT/'tools'))
import cv2
from assembly_timebase import conform_clip
def load(p):
    p=conform_clip(ROOT,{'file':str(ROOT/p),'speed':1},24,prepare=True)['file'];c=cv2.VideoCapture(p);a=[]
    while True:
        ok,f=c.read()
        if not ok:break
        a.append(f)
    c.release();return a
A2=load('out/outro_A2_v2/take1/synced.mp4');A3=load('out/outro_closing_generations_v1/A3/synced.mp4')
B2=load('out/outro_B2_afterglow_v1/clean.mp4');B3=load('out/outro_closing_generations_v1/B3/base.mp4');M=load('clips/raw/colony_goodnight_cascade_v6.mp4')
exit_take=load('out/outro_closing_generations_v1/B3/take1/base.mp4')
old=load('out/outro_closing_available_v1/preview.mp4')
y,x=np.mgrid[:720,:1280].astype(np.float32)
def sm(a,b,t):
    u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'audio/song.wav'),'-ac','1','-ar','24000','-f','f32le','-'])
audio=np.frombuffer(pcm,dtype='<f4');env=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(4782)])
env=np.clip(env/(np.percentile(env[4362:4782],85)+1e-8),0,1)
def light(f,layer):return np.clip(255-(255-f.astype(float))*np.exp(-layer/255),0,255).astype(np.uint8)
def sprite(f,px,py,size,t,power=1):
    power=float(power)
    layer=np.zeros_like(f,dtype=np.float32)
    # Compact jade/pearl body with flickering wisps, not a solid green disk.
    for k in range(3):
        ang=np.linspace(0,math.tau,90);r=size*(1+.16*np.sin(ang*5+t*9+k))
        pts=np.c_[px+r*np.cos(ang+k),py+.6*r*np.sin(ang+k)].astype(np.int32)
        cv2.polylines(layer,[pts],True,(80*power,220*power,110*power),1,cv2.LINE_AA)
    cv2.circle(layer,(int(px),int(py)),max(1,int(size*.23)),(160*power,255*power,200*power),-1,cv2.LINE_AA)
    layer+=cv2.GaussianBlur(layer,(0,0),max(1,size*.5))*2+cv2.GaussianBlur(layer,(0,0),max(2,size*1.5))*2
    return light(f,layer)
def tv(f,which,song):
    S=400;im=np.zeros((S,S,3),np.float32);t=(song-4165)/24;v=env[min(song,4781)]
    theta=np.linspace(0,math.tau,200)
    for k,col in enumerate([(60,175,250),(245,230,80)]):
        r=1+.12*v*np.sin(theta*5+t*3+k)
        pts=np.c_[200+(112+15*k)*r*np.cos(theta+t*.5),200+(65+30*k)*r*np.sin(theta+t*.5)].astype(np.int32)
        cv2.polylines(im,[pts],True,col,2,cv2.LINE_AA)
    for j in range(8):
        a=t*.3+j*math.tau/8;pt=(int(200+120*np.cos(a)),int(200+120*np.sin(a)))
        cv2.circle(im,pt,3,(220,210,90),-1,cv2.LINE_AA)
    im+=cv2.GaussianBlur(im,(0,0),4)*1.4
    # Refit specifically to A2 and A3 glass, not the earlier A1 quad.
    q=np.float32([[1090,326],[1390,395],[1350,646],[1074,539]]) if which==2 else np.float32([[1110,344],[1390,406],[1350,650],[1092,544]])
    H=cv2.getPerspectiveTransform(np.float32([[0,0],[399,0],[399,399],[0,399]]),q)
    yy,xx=np.mgrid[:S,:S].astype(float);edge=(abs((xx-200)/200)**5+abs((yy-200)/200)**5)**.2
    mask=np.clip((1.0-edge)/.055,0,1).astype(np.float32)
    alpha=cv2.warpPerspective(mask,H,(1280,720))*.97
    # Small live-static remnant, much darker than the bright generated screen.
    inv=cv2.getPerspectiveTransform(q,np.float32([[0,0],[399,0],[399,399],[0,399]]))
    glass=cv2.warpPerspective(f,inv,(S,S)).astype(float)*.10
    screen=np.clip(glass+im,0,255).astype(np.uint8)
    proj=cv2.warpPerspective(screen,H,(1280,720))
    return np.clip(f*(1-alpha[:,:,None])+proj*alpha[:,:,None],0,255).astype(np.uint8)
def tooth(f):
    # Restrained neutral highlight reduction in mouth only, protected by white mask.
    g=f.astype(float);r=np.exp(-((x-645)/40)**6-((y-257)/16)**6)
    white=np.clip((np.min(g,axis=2)-150)/70,0,1)
    return np.clip(g*(1-.10*(r*white)[:,:,None]),0,255).astype(np.uint8)
rows=[(1,4362,4400,'Astronomer: Thought I heard something.','TV refit + stronger static suppression'),(2,4400,4431,'Exobiologist: You did.','Subtle teeth highlight reduction'),(3,4431,4449,'Astronomer: Was it you?','Ends 12 frames earlier'),(4,4449,4516,'Exobiologist: Da-da-dum / Could have been.','Green sprite; extended reaction covers next Say pickup'),(5,4516,4547,'Astronomer: Say goodnight.','12 frames later; provisional final-t cut; TV restored'),(6,4547,4574,'Exobiologist offscreen: To who?','Artifact insert begins earlier'),(7,4574,4622,'Astronomer offscreen: La-la-la-la-la','Continuous artifact + green dancer'),(8,4622,4644,'Exobiologist: You first.','UNRESOLVED: no Kling pass exists'),(9,4644,4671,'Astronomer: Night.','Approved shot retained'),(10,4671,4710,'Exobiologist: Night.','All remaining footage + 18-frame final hold for dimming'),(11,4710,4782,'Mars night: final response','Light pulses, distant fauna, green guide goes home'),(12,4782,4854,'Closing title','Existing layout placeholder')]
w=cv2.VideoWriter(str(OUT/'silent.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(1280,720));assert w.isOpened()
for song in range(4362,4854):
    num,a,b,line,note=next(r for r in rows if r[1]<=song<r[2]);t=song/24;v=env[min(song,4781)]
    if num in (1,3):f=tv(A2[song-4320].copy(),2,song)
    elif num==2:f=tooth(B2[song-4320].copy())
    elif num==4:
        f=B2[min(song-4320,190)].copy();u=(song-4449)/67
        f=sprite(f,990+100*np.sin(u*math.tau*1.5),365-120*np.sin(u*math.tau*2),9+3*v,t,.8+.6*v)
    elif num==5:f=tv(A3[song-4492].copy(),3,song)
    elif num in (6,7):
        # 75 uninterrupted frames from same take; no looping or take-change jump.
        f=cv2.resize(B2[32+song-4547][475:700,445:845],(1280,720))
        if num==7:
            u=(song-4574)/48
            f=sprite(f,640+340*np.sin(u*math.tau*1.6),220+105*np.sin(u*math.tau*3.2),13+5*v,t,1.2)
    elif num==8:f=B3[song-4500].copy()
    elif num==9:f=old[song-4362].copy()
    elif num==10:
        f=exit_take[153+song-4671].copy()
        note='B3 TAKE 1 natural light-down / action insert, no lip sync'
    elif num==11:
        i=song-4710;u=i/72;f=M[i].copy();layer=np.zeros_like(f,dtype=float)
        # Only luminous architecture responds; sky/ground do not flash globally.
        g=f.astype(float);roi=sm(280,330,y)*(1-sm(405,450,y))
        warm=np.clip((g[:,:,2]+g[:,:,1]-g[:,:,0]*1.3-100)/150,0,1)*roi
        pulse=.2+.7*v
        layer+=cv2.GaussianBlur(warm,(0,0),3)[:,:,None]*np.array([45,110,160])*pulse
        for j in range(28):
            px=100+j*40+16*np.sin(t*1.1+j);py=315+32*np.sin(j*2.5+t*.4)
            cv2.circle(layer,(int(px),int(py)),1,(70,120,85),-1,cv2.LINE_AA)
        layer+=cv2.GaussianBlur(layer,(0,0),3)*.7;f=light(f,layer)
        shrink=(1-u)**1.4
        px=650+420*shrink*np.sin(u*math.tau*2.1);py=350+205*shrink*np.sin(u*math.tau*4.2+.5)
        # Artistic water-plane proxy. Reflection tracks projected light position
        # and depth, with long near-camera streaks breaking into short distant ones.
        water=np.zeros((720,1280),np.uint8)
        cv2.fillPoly(water,[np.array([[555,357],[748,357],[811,379],[958,431],[1095,560],[938,700],[280,700],[185,575],[345,430],[471,383]],np.int32)],255)
        wm=cv2.GaussianBlur(water.astype(np.float32)/255,(0,0),5)
        rx=640+(px-640)*.76
        ry=374+200*shrink+(350-py)*.12
        dx=x-rx;dy=y-ry
        # Wavy horizontal glitter with a vertical falloff, not a duplicate sprite.
        warp=10*shrink*np.sin(y*.14+t*2.3)+6*np.sin(y*.31-t*1.8)
        footprint=np.exp(-((dx-warp)/(12+34*shrink))**2-((dy)/(12+72*shrink))**2)
        bands=np.clip(np.sin(y*(.45+.2*u)+t*5+np.sin(x*.035+t)*1.1),0,1)**5
        breakup=.35+.65*(.5+.5*np.sin(x*.07+y*.17-t*3.7))
        strength=footprint*bands*breakup*wm*(.5+1.1*shrink)
        reflection=strength[:,:,None]*np.array([100,245,135])
        reflection+=cv2.GaussianBlur(reflection,(0,0),2)*.7
        reflection+=cv2.GaussianBlur(reflection,(0,0),8)*.35
        # Reapply water mask after bloom so rocks do not become reflective.
        f=light(f,reflection*wm[:,:,None])
        f=sprite(f,px,py,2+23*shrink,t,(1-u)*1.6+.1)
        rad=math.hypot(640,360)*(1-sm(4754,4782,song))
        iris=np.clip((rad-np.hypot(x-640,y-360))/4,0,1);f=(f*iris[:,:,None]).astype(np.uint8)
    else:f=old[song-4362].copy()
    cv2.rectangle(f,(0,0),(1280,91),(12,12,12),-1)
    cv2.putText(f,line,(16,29),cv2.FONT_HERSHEY_SIMPLEX,.73,(245,245,245),2,cv2.LINE_AA)
    cv2.putText(f,note,(16,57),cv2.FONT_HERSHEY_SIMPLEX,.51,(170,210,240),1,cv2.LINE_AA)
    cv2.putText(f,f'Song {song} | {song/24:.3f}s',(16,80),cv2.FONT_HERSHEY_SIMPLEX,.46,(175,175,175),1,cv2.LINE_AA)
    cv2.circle(f,(1230,43),32,(0,0,0),-1);cv2.putText(f,str(num),(1213 if num<10 else 1206,54),cv2.FONT_HERSHEY_SIMPLEX,.9,(255,255,255),2,cv2.LINE_AA)
    w.write(f)
    if song in [4714,4722,4730,4740]:cv2.imwrite(str(OUT/f'check_{song}.jpg'),f)
w.release()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'silent.mp4'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={4362/24}:end={4782/24},asetpts=PTS-STARTPTS,apad=whole_dur=20.5[a]','-map','0:v','-map','[a]','-t','20.5','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
(OUT/'cut_map.json').write_text(json.dumps(rows,indent=2));print('Revised numbered preview ready. Shot8 intentionally unresolved; no audio moved.')
