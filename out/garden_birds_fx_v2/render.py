"""Stronger bird/lantern treatment; preserve the quieter v1 for comparison."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
p=ROOT/'out/garden_birds_fx_v1/render.py'
s=p.read_text().replace('garden_birds_fx_v1','garden_birds_fx_v2')
changes={
 '(.14+.36*state+.10*voice_level+.75*ack)':
 '(.16+.95*state+.22*voice_level+1.65*ack)',
 'cv2.GaussianBlur(core,(0,0),8)*.58+cv2.GaussianBlur(core,(0,0),24)*.28':
 'cv2.GaussianBlur(core,(0,0),10)*1.05+cv2.GaussianBlur(core,(0,0),30)*.65',
 '(.16+.32*state+.40*woke)':
 '(.18+.85*state+1.10*woke)',
 'pearl+=cv2.GaussianBlur(pearl,(0,0),4)*.8':
 'pearl+=cv2.GaussianBlur(pearl,(0,0),5)*1.35+cv2.GaussianBlur(pearl,(0,0),16)*.65',
 "'fx':'Warm localized":
 "'strength_revision':'Owner requested much stronger treatment: roughly 2.5x musical gains and broader/stronger bloom; timing and release unchanged.','fx':'Warm localized"
}
for old,new in changes.items():
 assert old in s,old
 s=s.replace(old,new)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
