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
prior=load('out/outro_fx_notes_v2/preview_numbered_final.mp4')
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
def tv(f,which,song,shutdown=False):
    S=400;t=song/24;v=float(env[min(song,4781)]);p=beat_power(t)
    im=np.zeros((S,S,3),np.float32)
    # Helical data strands feed a constellation, with beat-expanding rings and scan.
    theta=np.linspace(0,math.tau,220)
    for k,col in enumerate([(60,180,255),(255,215,90)]):
        phase=theta+t*.8+k*math.pi
        r=1+(.08+.18*v)*np.sin(theta*5+t*3+k)
        pts=np.c_[200+125*r*np.cos(phase),200+80*r*np.sin(phase)].astype(np.int32)
        cv2.polylines(im,[pts],True,tuple(float(c*(.6+.8*p)) for c in col),2,cv2.LINE_AA)
    yy=np.linspace(65,330,100)
    for k in range(2):
        xx=200+65*np.sin(yy*.037-t*2+k*math.pi)
        cv2.polylines(im,[np.c_[xx,yy].astype(np.int32)],False,(155,210,240),1,cv2.LINE_AA)
    nodes=[]
    for j in range(11):
        ang=j*2.4+t*.13;r=55+(j%4)*25
        pt=(int(200+r*np.cos(ang)),int(200+r*np.sin(ang)))
        nodes.append(pt)
        cv2.circle(im,pt,2+int(3*p),(250,220,125),-1,cv2.LINE_AA)
        if j:cv2.line(im,nodes[j-1],pt,(75,95,75),1,cv2.LINE_AA)
    radius=int(40+140*((t*1.4)%1))
    cv2.circle(im,(200,200),radius,(float(75+120*p),float(80+100*p),65.),1,cv2.LINE_AA)
    im+=cv2.GaussianBlur(im,(0,0),3)*(1.1+p)
    if shutdown:
        u=sm(4646,4665,song)
        sy=max(.012,1-sm(0,.6,u));sx=max(.015,1-sm(.45,1,u))
        transform=np.float32([[sx,0,200*(1-sx)],[0,sy,200*(1-sy)]])
        im=cv2.warpAffine(im,transform,(S,S))
        cv2.circle(im,(200,200),2,(230.,255.,245.),-1,cv2.LINE_AA)
        im*=1-sm(4663,4671,song)
        im+=cv2.GaussianBlur(im,(0,0),4)*2
    q=np.float32([[1090,326],[1390,395],[1350,646],[1074,539]]) if which==2 else np.float32([[1110,344],[1390,406],[1350,650],[1092,544]])
    if shutdown:q=np.float32([[1038,338],[1250,388],[1235,632],[1033,546]])
    H=cv2.getPerspectiveTransform(np.float32([[0,0],[399,0],[399,399],[0,399]]),q)
    yy,xx=np.mgrid[:S,:S].astype(float)
    edge=(abs((xx-200)/200)**5+abs((yy-200)/200)**5)**.2
    mask=np.clip((.97-edge)/.22,0,1).astype(np.float32)
    projected=cv2.warpPerspective(im*mask[:,:,None],H,(1280,720))
    if shutdown:
        return light(f,projected)  # No black/darkening layer on the switch-off.
    alpha=cv2.warpPerspective(mask,H,(1280,720))*.96
    return np.clip(f*(1-alpha[:,:,None])+.10*f*alpha[:,:,None]+projected,0,255).astype(np.uint8)
def tooth(f):
    # Restrained neutral highlight reduction in mouth only, protected by white mask.
    g=f.astype(float);r=np.exp(-((x-645)/40)**6-((y-257)/16)**6)
    white=np.clip((np.min(g,axis=2)-150)/70,0,1)
    return np.clip(g*(1-.10*(r*white)[:,:,None]),0,255).astype(np.uint8)

beats=[v for bar in json.loads((ROOT/'analysis/beatmap.json').read_text())['bars'] for v in bar['beats']]
def beat_power(t):
    return max([math.exp(-max(0,t-b)/.17)*sm(-.04,0,t-b) for b in beats if -.04<=t-b<.9]+[0.0])
def additive(f,emission):
    base=f.astype(np.float32)/255
    linear=np.where(base<=.04045,base/12.92,((base+.055)/1.055)**2.4)
    result=linear+np.maximum(emission,0)
    result=np.where(result<=.0031308,result*12.92,1.055*np.maximum(result,0)**(1/2.4)-.055)
    return np.clip(result*255,0,255).astype(np.uint8)
def green_sprite(f,px,py,size,t,power=1):
    d2=(x-px)**2+(y-py)**2
    core=np.exp(-d2/(2*max(1.7,size*.17)**2))
    body=np.exp(-d2/(2*max(3,size*.43)**2))
    halo=np.exp(-d2/(2*max(5,size*.9)**2))
    emission=core[:,:,None]*np.array([2.4,4.2,2.8])*power
    emission+=body[:,:,None]*np.array([.045,.48,.08])*power
    emission+=halo[:,:,None]*np.array([.008,.055,.012])*power
    out=additive(f,emission)
    assert np.all(out.astype(int)>=f.astype(int)-1)
    return out
b_settings=json.loads((ROOT/'out/outro_B2_afterglow_v1/settings.json').read_text())
def b_picture(i):
    folder=ROOT/'out/outro_B2_afterglow_v1'
    room=cv2.imread(str(folder/'room'/f'{i:03}.png')).astype(np.float32)
    lamps=cv2.imread(str(folder/'lights'/f'{i:03}.png')).astype(np.float32)
    record=b_settings['records'][i];cx,cy=record['center'];v=record['voice_envelope']
    # Stabilize peripheral violet motes separately from the accepted warm artifact pulse.
    outside=1-np.exp(-((x-cx)/92)**6-((y-cy)/125)**6)
    violet=np.clip((lamps[:,:,0]-lamps[:,:,1])/15,0,1)*outside
    factor=.65/(.4+.7*v)
    correction=lamps*violet[:,:,None]*(factor-1)
    return np.clip(B2[i].astype(np.float32)-.4*room+correction,0,255).astype(np.uint8)
def motes(f,t,v):
    layer=np.zeros_like(f,dtype=np.float32)
    # Uniformly staggered ages and nearly steady intensity: no population switch or audio burst.
    for j in range(85):
        age=(t*(.20+(j%7)*.025)+j/85)%1
        px=640+(1 if j%2 else -1)*(80+420*age)+55*np.sin(age*6.28+j)
        py=640-470*age+30*np.sin(age*9+j)
        strength=float(sm(0,.15,age)*(1-sm(.8,1,age))*(.85+.15*v))
        cv2.circle(layer,(int(px),int(py)),1+j%2,tuple(a*strength for a in (.45,.28,.38)),-1,cv2.LINE_AA)
    layer+=cv2.GaussianBlur(layer,(0,0),3)*2+cv2.GaussianBlur(layer,(0,0),9)*.7
    return additive(f,layer)
def b3_effect(f,song):
    t=song/24;v=env[song];g=f.astype(np.float32)
    # Source-color isolation follows warm specimen detail within its own low-frame region.
    roi=np.exp(-((x-638)/65)**6-((y-583)/90)**6)
    warm=np.clip((g[:,:,2]-g[:,:,0]-8)/45,0,1)*np.clip((g[:,:,1]-g[:,:,0]-3)/35,0,1)*roi
    glow=warm[:,:,None]*np.array([35,145,255])*(.6+1.5*v)
    glow+=cv2.GaussianBlur(glow,(0,0),5)+cv2.GaussianBlur(glow,(0,0),16)*.7
    # Reduced lingering projector, protected face and window; no claimed glass refraction.
    mask=(1-np.exp(-((x-640)/270)**6-((y-400)/390)**6))
    mask*=sm(345,470,y)+.4*(1-sm(250,360,y))*(abs(x-640)>500)
    pattern=(.5+.5*np.sin(x*.013+y*.010-t*.7+1.1*np.sin(y*.009+t*.3)))**5
    shade=np.clip(g.mean(axis=2)/140,.15,.7)*mask*pattern
    glow+=shade[:,:,None]*np.array([80,48,85])*.65
    return light(f,glow)

rows=[(1,4362,4400,'Astronomer: Thought I heard something.','TV refit + stronger static suppression'),(2,4400,4431,'Exobiologist: You did.','Subtle teeth highlight reduction'),(3,4431,4449,'Astronomer: Was it you?','Ends 12 frames earlier'),(4,4449,4516,'Exobiologist: Da-da-dum / Could have been.','Green sprite; extended reaction covers next Say pickup'),(5,4516,4547,'Astronomer: Say goodnight.','12 frames later; provisional final-t cut; TV restored'),(6,4547,4574,'Exobiologist offscreen: To who?','Artifact insert begins earlier'),(7,4574,4622,'Astronomer offscreen: La-la-la-la-la','Continuous artifact + green dancer'),(8,4622,4644,'Exobiologist: You first.','UNRESOLVED: no Kling pass exists'),(9,4644,4671,'Astronomer: Night.','Approved shot retained'),(10,4671,4710,'Exobiologist: Night.','Natural take1 light-down, source153..192'),(11,4710,4782,'Mars night: final response','Light pulses, distant fauna, green guide goes home'),(12,4782,4854,'Closing title','Existing layout placeholder')]
w=cv2.VideoWriter(str(OUT/'silent.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(1280,720));assert w.isOpened()
for song in range(4362,4854):
    num,a,b,line,note=next(r for r in rows if r[1]<=song<r[2]);t=song/24;v=env[min(song,4781)]
    if num in (1,3):f=tv(A2[song-4320].copy(),2,song)
    elif num==2:f=tooth(b_picture(song-4320))
    elif num==4:
        f=b_picture(min(song-4320,190));u=(song-4449)/67
        f=green_sprite(f,990+100*np.sin(u*math.tau*1.5),365-120*np.sin(u*math.tau*2),9+3*v,t,1+.5*v)
    elif num==5:f=tv(A3[song-4492].copy(),3,song)
    elif num in (6,7):
        # 75 uninterrupted frames from same take; no looping or take-change jump.
        f=cv2.resize(b_picture(32+song-4547)[475:700,445:845],(1280,720))
        f=motes(f,t,float(np.mean(env[max(0,song-6):song+7])))
        if num==7:
            u=(song-4574)/48
            f=green_sprite(f,800+280*np.sin(u*math.tau*.8),220+100*np.sin(u*math.tau*1.6),38+6*v,t,1.2)
    elif num==8:f=b3_effect(B3[song-4500].copy(),song)
    elif num==9:f=tv(A3[song-4492].copy(),3,song,shutdown=True)
    elif num==10:
        f=exit_take[153+song-4671].copy()
        note='B3 TAKE 1 natural light-down / action insert, no lip sync'
    elif num==11:f=prior[song-4362].copy()
    else:f=old[song-4362].copy()
    cv2.rectangle(f,(0,0),(1280,91),(12,12,12),-1)
    cv2.putText(f,line,(16,29),cv2.FONT_HERSHEY_SIMPLEX,.73,(245,245,245),2,cv2.LINE_AA)
    cv2.putText(f,note,(16,57),cv2.FONT_HERSHEY_SIMPLEX,.51,(170,210,240),1,cv2.LINE_AA)
    cv2.putText(f,f'Song {song} | {song/24:.3f}s',(16,80),cv2.FONT_HERSHEY_SIMPLEX,.46,(175,175,175),1,cv2.LINE_AA)
    cv2.circle(f,(1230,43),32,(0,0,0),-1);cv2.putText(f,str(num),(1213 if num<10 else 1206,54),cv2.FONT_HERSHEY_SIMPLEX,.9,(255,255,255),2,cv2.LINE_AA)
    w.write(f)
    if song in [4404,4412,4424,4480,4550,4573,4574,4600]:cv2.imwrite(str(OUT/f'check_{song}.jpg'),f)
w.release()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'silent.mp4'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={4362/24}:end={4782/24},asetpts=PTS-STARTPTS,apad=whole_dur=20.5[a]','-map','0:v','-map','[a]','-t','20.5','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
(OUT/'cut_map.json').write_text(json.dumps(rows,indent=2));print('Revised numbered preview ready. Shot8 intentionally unresolved; no audio moved.')
