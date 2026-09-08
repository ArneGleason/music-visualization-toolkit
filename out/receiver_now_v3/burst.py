# Inserted into the existing renderer, where numpy and cv2 are already loaded.
def now_pulse(frame):
 t=frame-1175
 if t<0:return 0.
 return float((1-np.exp(-t/1.1))*np.exp(-max(0,t-3)/12))

def receiver_burst(frame,matrix):
 pulse=now_pulse(frame)
 result=np.zeros((720,1280,3),np.float32)
 if pulse<=0:return result
 # Rounded cabinet perimeter, split cyan/amber with a soft shared seam.
 boundary=[]
 for cx,cy,start in [(998,120,-90),(998,637,0),(267,637,90),(267,120,180)]:
  theta=np.linspace(np.deg2rad(start),np.deg2rad(start+90),32)
  boundary.extend(np.stack([cx+25*np.cos(theta),cy+25*np.sin(theta)],axis=1))
 # Resample the straight edges as well, so travelling weight never skips them.
 points=[]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):
  points.extend(np.linspace(a,b,max(2,int(np.linalg.norm(np.array(b)-a)/2)),endpoint=False))
 points=np.array(points)
 for side,color in enumerate(([1.,.80,.20],[.10,.50,1.])):
  layer=np.zeros((720,1280),np.float32)
  path=points@matrix[:,:2].T+matrix[:,2]
  for j in range(len(path)):
   mix=float(np.clip((points[j,0]-590)/85,0,1))
   weight=(1-mix if side==0 else mix)*pulse
   scan=.7+.3*((j/len(path)-(frame-1175)/28)%1)
   cv2.line(layer,tuple(np.rint(path[j]).astype(int)),tuple(np.rint(path[(j+1)%len(path)]).astype(int)),float(weight*scan),2,cv2.LINE_AA)
  # Remaining controls answer together, not an unrelated full-screen flash.
  rings=[(325 if side==0 else 935,178,53),(333 if side==0 else 927,270,27),
         (370 if side==0 else 890,604,38),(628,600,78)]
  for cx,cy,r in rings:
   theta=np.linspace(0,2*np.pi,320)
   radius=r+pulse*3*np.sin(theta*13+frame*.4)
   xy=np.stack([cx+radius*np.cos(theta),cy+radius*np.sin(theta)],axis=1)
   xy=xy@matrix[:,:2].T+matrix[:,2]
   for j in range(len(xy)-1):
    level=pulse*(.55+.45*((j/320-frame/24)%1))
    if cx==628:level*=.5
    cv2.line(layer,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[j+1]).astype(int)),float(level),2,cv2.LINE_AA)
  glow=layer*1.7+cv2.GaussianBlur(layer,(0,0),3)*3.5+cv2.GaussianBlur(layer,(0,0),12)*6
  result+=glow[:,:,None]*np.array(color)
 return result
