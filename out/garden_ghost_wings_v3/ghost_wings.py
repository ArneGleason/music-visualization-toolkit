
def ghost_wings(result,source,sf):
 envelope=float(smooth((sf-1521)/11)*(1-smooth((sf-1549)/12)))
 if envelope<=0:return result
 t=(sf-1524)/24
 b,g,r=cv2.split(source.astype(np.float32))
 # Read each frame's warm translucent wing silhouette, not a static butterfly.
 mask=((r>.55)&(g>.47)&(r>b*1.04)&(yy<460)&(yy>12)&(xx>70)&(xx<1210)).astype(np.uint8)*255
 mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
 contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
 contours=[c[:,0,:] for c in contours if cv2.contourArea(c)>1800]
 if not contours:return result
 points=np.concatenate(contours).astype(float)
 points=points[(np.abs(points[:,0]-640)>100)&(points[:,1]<435)]
 if len(points)<20:return result
 points=points[np.linspace(0,len(points)-1,min(650,len(points))).astype(int)]
 layer=np.zeros((720,1280,3),np.float32)
 for echo in range(3):
  phase=t*2*np.pi*1.7-echo*.55
  for j,point in enumerate(points):
   side=-1 if point[0]<640 else 1
   # Sweep spectral particles from thorax-rooted ghost wings, offset in phase.
   delta=point-np.array([640.,275.])
   theta=side*(.08+.19*np.sin(phase))*(1+echo*.25)
   rotation=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
   delta=rotation@delta*(1.025+echo*.032)
   delta[1]*=1+.12*np.cos(phase)
   p=delta+np.array([640.,275.])
   p+=2*np.array([np.sin(j*2.7+t*7),np.cos(j*1.9-t*6)])
   hue=(abs(delta[0])/560*.8+echo*.08+t*.055)%1
   hsv=np.array([[[hue*360,.78,1.]]],np.float32)
   color=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)[0,0]
   sparkle=.45+.55*np.sin(j*1.7+t*9)**2
   level=envelope*np.exp(-echo*.65)*sparkle*.65
   cv2.circle(layer,tuple(np.rint(p).astype(int)),1 if j%5 else 2,tuple(float(x*level) for x in color),-1,cv2.LINE_AA)
 glow=layer*1.4+cv2.GaussianBlur(layer,(0,0),2)*2.8+cv2.GaussianBlur(layer,(0,0),7)*3.5
 return np.clip(result+glow,0,1)
