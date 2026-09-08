"""Capture physical beam paths, never pixel buffers, from accepted audio math."""
from pathlib import Path
import sys,inspect,textwrap,gzip,json,math
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'scope';D.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'tools'))
import screen_sync_phosphor as p
p.PROFILE='rosette';p.ANALOG=True;p.CRACKLE=True
samples,offset,norm=p.read_stem('Guitar','guitar',90,900)
p.GUITAR=(np.asarray(samples),offset,norm);p.GUITAR_GAIN=.30
p.PX=np.linspace(-p.base.RX,p.base.RX,1024,dtype=np.float32)
src=textwrap.dedent(inspect.getsource(p.Phosphor.deposit))
src=src[:src.index('    distance =')]+'''    self.path=np.column_stack([PX,y,.50+1.08*dwell,(.08+.92*dwell)*sweep_weight((PX+base.RX)/(2*base.RX),sec)])
'''
ns=dict(p.__dict__);exec(src,ns);p.Phosphor.deposit=ns['deposit']
src=textwrap.dedent(inspect.getsource(p.Rosette.deposit));src=src[:src.index('    angle =')]+'''
    theta=np.linspace(0,math.tau,769)
    target=np.interp(np.mod((theta+.10*(sec-base.FIRST/24))*3/math.tau,1)*512,np.arange(513),np.r_[radial,radial[0]])
    dr=np.gradient(target,theta);dwell=1/np.sqrt(1+(dr/np.maximum(target,1))**2)
    self.path=np.column_stack([target*np.cos(theta),target*np.sin(theta),.50+1.08*dwell,(.08+.92*dwell)*sweep_weight(np.mod(theta/math.tau,1),sec,True)])
'''
exec(src,ns);p.Rosette.deposit=ns['deposit']
bass=p.base.read_bass();channels=[p.Phosphor(bass,0,True),p.Rosette(bass)];records=[]
for step in range(-64,69*8):
 sec=86/24+(step+.5)/(24*8)
 for c in channels:c.deposit(sec)
 if step%2==0:records.append({'step':step,'paths':[c.path.round(5).tolist() for c in channels]})
with gzip.open(D/'paths.json.gz','wt') as f:json.dump(records,f,separators=(',',':'))
(D/'controls.json').write_text(json.dumps({'song_frames':[86,155],'fps':24,'guitar_gain':.30,'substeps':4,'original_math':'screen_sync_phosphor.py','source_image':'codex/out/obs_console_macro_b.jpg'}))
