"""Seeded painted-looking deep-space backdrop, not an image generation."""
import numpy as np

def make_space(cv2, x, y):
    rng=np.random.default_rng(91273)
    def noise():
        field=np.zeros(x.shape,np.float32)
        for size,weight in [(5,.48),(11,.25),(23,.14),(47,.08),(95,.05)]:
            grid=rng.random((size,max(3,int(size*1.78))),dtype=np.float32)
            field+=cv2.resize(grid,(1280,720),interpolation=cv2.INTER_CUBIC)*weight
        return np.clip(field,0,1)
    n1,n2,n3=noise(),noise(),noise()
    diagonal=(y-(570-.38*x+100*(n2-.5)))
    band=np.exp(-(diagonal/145)**2)
    filament=np.maximum(0,n1-.24)**1.6
    dust=np.exp(-((diagonal+20+90*(n3-.5))/28)**2)*.72
    center=1-.62*np.exp(-(((x-640)/320)**2+((y-324)/260)**2))
    density=band*filament*(1-dust)*center
    violet=np.array([.64,.28,.47],np.float32)
    teal=np.array([.47,.43,.17],np.float32)
    blend=np.clip(x/1280*.75+n2*.4,0,1)
    color=violet[None,None,:]*(1-blend[:,:,None])+teal[None,None,:]*blend[:,:,None]
    space=np.zeros((720,1280,3),np.float32)+np.array([.026,.016,.021],np.float32)
    space+=density[:,:,None]*color*3.4
    # A diffuse warmer patch adds distance without becoming another focal object.
    patch=np.exp(-(((x-1080)/240)**2+((y-110)/135)**2))*np.maximum(0,n3-.28)
    space+=patch[:,:,None]*np.array([.14,.20,.28],np.float32)*.35
    points=np.zeros_like(space)
    for _ in range(1600):
        px=int(rng.integers(0,1280));py=int(rng.integers(0,720))
        if rng.random()>.30+.65*band[py,px]:continue
        value=float(rng.uniform(.07,.28))
        points[py,px]+=np.array([value,value*.94,value*.90])
    for _ in range(72):
        px=int(rng.integers(4,1276));py=int(rng.integers(4,716))
        value=float(rng.uniform(.32,.85));warm=rng.random()>.65
        c=(value*.75,value*.86,value) if warm else (value,value*.95,value*.85)
        cv2.circle(points,(px,py),1,c,-1,cv2.LINE_AA)
    space+=points+cv2.GaussianBlur(points,(0,0),1.5)*.55
    return space.astype(np.float32)
