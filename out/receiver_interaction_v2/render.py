"""Keep arrival; morph into knob-bound scans and expanding hardware contours."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'out/receiver_reply_arrival_v1/post.py'
code=source.read_text()
code=code.replace('receiver_reply_arrival_review','receiver_interaction_v2')
code=code.replace("ROOT/'out/receiver_reply_arrival_v1/blender_review.py'", "ROOT/'out/receiver_interaction_v2/blender_review.py'")
needle="ns={'__file__':str(recipe)"
insert='''
# The incoming shape remains untouched until frame1110. It then wraps an actual
# knob perimeter instead of continuing the free-flight orbit.
code=code.replace('  xy=local@rotation.T+np.array([x,y])', """  xy=local@rotation.T+np.array([x,y])
  bind=smooth((songframe-1110)/20)
  if bind>0:
   cx=425 if self.side==0 else 832
   theta=angle+t*.8
   wiggle=np.tile(self.radial-self.radial.mean(),3)*.18
   bound=np.stack([cx+(55+wiggle)*np.cos(theta),280+(55+wiggle)*np.sin(theta)],axis=1)
   bound=bound@current_transform[:,:2].T+current_transform[:,2]
   xy=xy*(1-bind)+bound*bind""")
'''
assert needle in code
code=code.replace(needle,insert+'\n'+needle)
needle='records=[]\nfor f in range(1,131):'
insert='''
def hardware_traces(songframe,matrix,voice):
 result=np.zeros((720,1280,3),np.float32)
 for side,color in enumerate(([1.,.80,.20],[.10,.50,1.])):
  layer=np.zeros((720,1280),np.float32)
  # Two halves of the existing blue CRT, followed by each small amber meter.
  # Deliberately draw on bezel edges rather than across readable dial faces.
  for cx,cy,rx,ry,start,span in [(628,260,113,113,1137,30),
       (370 if side==0 else 890,450,55,55,1150,28)]:
   progress=float(np.clip((songframe-start)/span,0,1))
   if progress<=0:continue
   extent=np.pi if start==1137 else 2*np.pi
   theta=np.linspace(0,extent,320)+(np.pi/2 if side==0 else -np.pi/2)
   if side==1:theta=-theta
   ripple=1.0*np.sin(theta*17+songframe*.25)+.5*np.sin(theta*37-songframe*.18)
   xy=np.stack([cx+(rx+ripple)*np.cos(theta),cy+(ry+ripple)*np.sin(theta)],axis=1)
   xy=xy@matrix[:,:2].T+matrix[:,2]
   count=max(2,int(progress*len(xy)))
   for j in range(count-1):
    phase=(j/len(xy)-(songframe-start)/40)%1
    brightness=(.35+.65*phase**2)*(.5+.7*voice)
    cv2.line(layer,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[j+1]).astype(int)),float(brightness),1,cv2.LINE_AA)
  glow=layer*1.4+cv2.GaussianBlur(layer,(0,0),2)*2+cv2.GaussianBlur(layer,(0,0),7)*2.5
  result+=glow[:,:,None]*np.array(color)
 return result
records=[]
for f in range(1,131):'''
assert needle in code
code=code.replace(needle,insert)
code=code.replace('  result+=np.clip(lit+glow,0,1)*.5', '  glow+=hardware_traces(songframe+(sub+.5)/2,matrix,voice)\n  result+=np.clip(lit+glow,0,1)*.5')
code=code.replace("hp.write_text(json.dumps(h,indent=2)+'\\n')", "(OUT/'verification.json').write_text(json.dumps(h['codex_result'],indent=2))")
code=code.replace('Fresh vocal-meter response and carried duet; production unchanged.', 'Arrival preserved, knob-bound rosettes and voice-reactive bezel traces; owner review pending, production unchanged.')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
