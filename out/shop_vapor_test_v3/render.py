"""Highlight the alien souvenir, then unmake the signal into vapor."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
p=ROOT/'out/shop_signal_exit_v2/render.py'
builder=p.read_text().split("exec(compile(s,str(p),'exec')")[0]
ns={'__file__':str(OUT/'render.py')}
exec(compile(builder,str(p),'exec'),ns)
s=ns['s'].replace('out/shop_signal_exit_v2/clean.mp4','out/shop_vapor_test_v3/clean.mp4')
s=s.replace('cx=210*(1-change)+145*change;cy=325*(1-change)+389*change',
 'cx=382*(1-change)+145*change;cy=262*(1-change)+369*change')
s=s.replace('radius=52*(1-change)+83*change','radius=88*(1-change)+106*change')
s=s.replace('-330*leaving','-75*leaving')
s=s.replace('+sign*65*leaving','+sign*40*leaving')
s=s.replace('val=(.3+1.1*level)*fade*flicker*scan',
 '''dissolve=smooth((sf-2448-side*3)/24)
   breakup=.65+.35*np.sin(theta[j]*13+sf*.35+side)
   val=(.3+1.1*level)*fade*scan*(1-dissolve)**1.4*max(0,1-dissolve*breakup)''')
s=s.replace('  light+=energy[:,:,None]*color', '''  light+=energy[:,:,None]*color
  # Soft overlapping puffs detach from the dissolving path, not bright sparks.
  dissolve=smooth((sf-2448-side*3)/24)
  vapor=np.zeros((720,1280),np.float32)
  for k in range(72):
   j=(k*37+side*19)%len(theta)
   age=max(0,sf-(2448+side*3+(k%9)))
   if age<=0:continue
   drift=age*(1.3+.7*np.sin(k*2.1))
   vx=xx[j]-drift+np.sin(k*1.7+age*.13)*age*.8
   vy=yy[j]-age*(.7+.6*np.cos(k)) + np.cos(k*2.3+age*.17)*age*.8
   radius_puff=3+age*.55+(k%4)
   opacity=.06*(.45+.55*level)*np.sin(np.pi*min(1,age/34))*(1-smooth((sf-2474)/9))
   puff=np.zeros_like(vapor)
   cv2.circle(puff,(round(vx),round(vy)),round(radius_puff),float(opacity),-1,cv2.LINE_AA)
   vapor+=puff
  vapor=cv2.GaussianBlur(vapor,(0,0),5+10*dissolve)
  light+=vapor[:,:,None]*color*1.5''')
s=s.replace('loops open as the last phrase begins, uncoil into separately angled vocal-modulated ribbons and sweep out left on fake shit.',
 'larger traces highlight gray alien souvenir; open on final phrase and dissolve into soft drifting vocal-responsive vapor, not an intact offscreen exit.')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
r=json.loads((OUT/'recipe.json').read_text())
r.update(subject='gray alien souvenir head',unfurl_song_frames=[2437,2459],vapor_song_frames=[2448,2483],previous_version='out/shop_signal_exit_v2/clean.mp4')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
