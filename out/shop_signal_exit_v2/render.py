"""Unfurl the paired traces into vocal-modulated departing ribbons."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
p=ROOT/'out/shop_signal_test_v1/render.py'
s=p.read_text().replace('out/shop_signal_test_v1/clean.mp4','out/shop_signal_exit_v2/clean.mp4')
s=s.replace("flicker=1 if sf<2459 else (.45+.55*abs(np.sin((sf-2459)*1.9)))",'flicker=1')
a=s.index('  rr=radius*');b=s.index('  energy=np.zeros',a)
s=s[:a]+'''  opening=smooth((sf-2437-side*3)/19)
  leaving=smooth((sf-2450-side*3)/28)
  u=np.linspace(0,1,len(theta))
  arc=theta*(1-.72*opening)+opening*(.5 if side==0 else -.5)
  rr=radius*(1+.07*level*np.sin(arc*5+phase))
  px=rr*np.cos(arc);py=rr*np.sin(arc)
  horizontal=.90*(1-change)+.32*change
  xx=cx+px*horizontal
  yy=cy+py*(.60 if side==0 else .87)+px*(.25 if side==0 else -.25)
  # Loops open at a seam, uncoil into separate streams, then exit left.
  sign=-1 if side==0 else 1
  ribbon_x=cx+35-215*u
  ribbon_y=cy+sign*(30+115*u)+np.sin(u*9-phase*1.5)*(9+25*level)
  xx=xx*(1-opening)+ribbon_x*opening-330*leaving
  yy=yy*(1-opening)+ribbon_y*opening+sign*65*leaving
''' +s[b:]
s=s.replace('  for j in range(len(theta)):', '  for j in range(len(theta) if opening==0 else len(theta)-1):')
s=s.replace("final flicker and release.","loops open as the last phrase begins, uncoil into separately angled vocal-modulated ribbons and sweep out left on fake shit.")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
r=json.loads((OUT/'recipe.json').read_text())
r.update(unfurl_song_frames=[2437,2459],departure_song_frames=[2450,2481],previous_version='out/shop_signal_test_v1/clean.mp4')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
