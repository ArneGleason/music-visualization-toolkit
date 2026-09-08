"""Independent vocal/guitar volumetric loops with shutter-sampled triple spin."""
import numpy as np

def smooth(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)

def draw(cv2,sf,angle,radial,vocal,guitar,guitar_level,trail):
    light=np.zeros((720,1280,3),np.float32)
    formation=smooth((sf-2330)/34)
    spinning=sf>=2366
    offsets=np.linspace(-.42,.42,6 if spinning else 2)
    for side,(entry,color) in enumerate([(2308,np.array([1.,.80,.20])),(2315,np.array([.10,.50,1.]))]):
        if sf<entry:continue
        level=vocal if side==0 else guitar_level
        waveform=radial if side==0 else guitar
        energy=np.zeros((720,1280),np.float32)
        for shutter in offsets:
            time=sf+shutter;arrival=smooth((time-entry)/28)
            progress=(time-entry)/24
            spin=6*np.pi*smooth((time-2366)/33)
            # Counter-phase breathing is modest; actual channel levels remain independent.
            counter=np.sin(progress*5+side*np.pi)
            cx=(180 if side==0 else 1100)*(1-arrival)+640*arrival
            cy=292+(1-arrival)*90*np.sin(progress*4+side*np.pi)
            radius=(24+112*arrival+25*formation)*(1+.16*level+.055*counter)
            radius_vector=radius*(1+(.14+.30*formation)*waveform+.20*formation*np.sin((5 if side==0 else 4)*angle+side))
            theta=angle+progress*.4
            px=radius_vector*np.cos(theta);py=radius_vector*np.sin(theta)
            tilt=(.28 if side==0 else 1.25)*formation
            # Audio displacement now extends normal to each loop, not just radially.
            depth_warp=radius*formation*(.24*np.sin(3*theta+progress*(1 if side==0 else -1))+.35*(waveform-.35))*level
            xyz=np.stack([px,py*np.cos(tilt)-depth_warp*np.sin(tilt),py*np.sin(tilt)+depth_warp*np.cos(tilt)],axis=1)
            yaw=spin+.45*formation
            rot=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
            xyz=xyz@rot.T
            pitch=.35+.15*np.sin(progress*1.3)*formation
            rot=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]])
            xyz=xyz@rot.T
            xy=xyz[:,:2]*(1050/(1050-xyz[:,2]))[:,None]+[cx,cy]
            sample=np.zeros_like(energy)
            for j in range(512):
                q=(j+1)%512;distance=np.linalg.norm(xy[q]-xy[j])
                dwell=1/(1+distance*.12)
                scan=.62+.55*np.exp(-np.mod(progress*3-angle[j],2*np.pi)/1.1)
                depth=.55+.45*(xyz[j,2]/max(radius,1)+1)/2
                intensity=(.85+1.25*level)*smooth((time-entry)/5)*dwell*scan*depth
                cv2.line(sample,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[q]).astype(int)),float(intensity),2 if xyz[j,2]<0 else 3,cv2.LINE_AA)
            if spinning:
                # Sparse sparks follow the same rotation and drift off the turning form.
                age=max(0,time-2366)
                for k in range(16):
                    j=(k*31+side*13)%512
                    vec=xy[j]-[cx,cy]
                    pos=np.array([cx,cy])+vec*(1+.007*age*(.3+(k%5)/5))
                    brightness=(.35+.45*level)*np.sin(np.pi*np.clip(age/33,0,1))
                    cv2.circle(sample,tuple(pos.astype(int)),1 if k%3 else 2,float(brightness),-1,cv2.LINE_AA)
            energy+=sample/len(offsets)
        trail[side]=trail[side]*(.22 if spinning else .45)+energy*.85
        beam=trail[side]*2+cv2.GaussianBlur(trail[side],(0,0),3)*2.4+cv2.GaussianBlur(trail[side],(0,0),11)*2.9
        light+=beam[:,:,None]*color
    return light
