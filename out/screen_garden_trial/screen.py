screen_cap=cv2.VideoCapture(str(ROOT/'clips/raw/interference_bloom_v6.mp4'))
screen_frames=[]
while True:
 ok,frame=screen_cap.read()
 if not ok:break
 screen_frames.append(frame)
screen_cap.release()
assert len(screen_frames)==192
def texture(sf):
 # Crop only the luminous display, never the incompatible surrounding cabinet.
 i=max(0,sf-1201);assert i<len(screen_frames)
 crop=screen_frames[i][100:620,380:900]
 return cv2.resize(crop,(1280,720),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
def screen_transition(result,sf,matrix):
 if sf<1201:return result
 tex=texture(sf)
 alpha=float(ns['smooth']((sf-1201)/12))
 center=matrix@np.array([628.,260.,1.])
 radius=99*matrix[0,0]
 # Circular replacement at the original CRT, tracked with this take.
 transform=np.array([[2*radius/1280,0,center[0]-radius],[0,2*radius/720,center[1]-radius]],np.float32)
 mapped=cv2.warpAffine(tex,transform,(1280,720))
 distance=np.sqrt((xx-center[0])**2+(yy-center[1])**2)
 mask=np.clip((radius-distance)/2,0,1)*alpha
 result=result*(1-mask[:,:,None])+mapped*mask[:,:,None]
 # Punctuation on deal1246: expand the established screen image into the frame.
 growth=float(ns['smooth']((sf-1246)/12))
 if growth>0:
  r=radius+(820-radius)*growth
  c=center*(1-growth)+np.array([640.,360.])*growth
  tx=np.array([[2*r/1280,0,c[0]-r],[0,2*r/720,c[1]-r]],np.float32)
  expanded=cv2.warpAffine(tex,tx,(1280,720),borderMode=cv2.BORDER_REFLECT_101)
  m=np.clip((r-np.sqrt((xx-c[0])**2+(yy-c[1])**2))/3,0,1)
  # End exactly at the full-frame crop, with no new frame or source-time jump.
  expanded=expanded*(1-growth)+tex*growth
  result=result*(1-m[:,:,None])+expanded*m[:,:,None]
 return result
