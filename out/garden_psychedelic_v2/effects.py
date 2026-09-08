def flight(t):
 # Catmull-Rom trajectory, broad continuous swoops in the space ahead of her.
 anchors=np.array([[1340,150],[1300,110],[1040,105],[920,220],[1080,290],[1220,100],[1380,50]],float)
 u=float(np.clip(t/4.25*4,0,3.9999));k=int(u)+1;q=u-int(u)
 a,b,c,d=anchors[k-1:k+3]
 return .5*((2*b)+(-a+c)*q+(2*a-5*b+4*c-d)*q*q+(-a+3*b-3*c+d)*q**3)

def second_light(pic,sf,voice):
 t=(sf-1412)/24
 accent=pulse(sf,1475,1501)
 # Two motion samples, tapered short wake; does not claim physical scene light.
 glow=np.zeros((720,1280),np.float32)
 for sample in [-.25,.25]:
  for age in range(6):
   position=flight(max(0,t+sample/24-age*.025))
   d=(xx-position[0])**2+(yy-position[1])**2
   size=(5+2*np.sin(t*1.7)**2)*(1-age*.08)
   weight=np.exp(-age*.7)/2
   glow+=np.exp(-d/(2*size**2))*weight*.6
  position=flight(t+sample/24)
  d=(xx-position[0])**2+(yy-position[1])**2
  glow+=(np.exp(-d/(2*18**2))*.13+np.exp(-d/(2*45**2))*.055)/2
 gain=(.65+.25*voice+1.9*accent)*smooth(t/.3)
 return np.clip(pic+glow[:,:,None]*np.array([.38,1.,.60])*gain,0,1)

def psychedelic(pic,sf):
 pic=pic.astype(np.float32)
 # A single word-shaped event, not repetitive flashing or a rainbow cycle.
 strength=float(smooth((sf-1524)/4)*(1-smooth((sf-1547)/6)))
 if strength<=0:return pic
 t=(sf-1524)/24
 nx=(xx-640)/640;ny=(yy-300)/420
 distance=np.sqrt(nx*nx+ny*ny)
 body=np.exp(-((xx-640)/160)**2-((yy-300)/245)**2)
 freedom=1-.90*body
 breath=.075*np.sin(t*7)*strength
 dx=(22*np.sin(yy/94-t*6)+13*np.sin(xx/135+yy/150+t*4))*strength*freedom
 dy=(18*np.sin(xx/110+t*5)+12*np.cos(yy/140-xx/170-t*4))*strength*freedom
 dx+=(xx-640)*breath*freedom
 dy+=(yy-300)*breath*freedom
 mx=np.clip(xx+dx,6,1273).astype(np.float32);my=np.clip(yy+dy,6,713).astype(np.float32)
 result=cv2.remap(pic,mx,my,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
 fringe=(4.5*strength*freedom).astype(np.float32)
 result[:,:,0]=cv2.remap(pic[:,:,0],mx+fringe,my-fringe*.3,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
 result[:,:,2]=cv2.remap(pic[:,:,2],mx-fringe,my+fringe*.3,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
 # Soft, limited green/violet edge iridescence, concentrated in the surroundings.
 gray=cv2.cvtColor(result.astype(np.float32),cv2.COLOR_BGR2GRAY)
 edge=np.abs(cv2.Laplacian(gray,cv2.CV_32F,ksize=3))
 edge=cv2.GaussianBlur(np.clip(edge,0,.3),(0,0),2)*strength*freedom
 tint=(.5+.5*np.sin(distance*8-t*3))[:,:,None]
 colour=np.array([.8,.20,.55])*tint+np.array([.15,.65,.18])*(1-tint)
 return np.clip(result+edge[:,:,None]*colour*.45,0,1)
