"""Alien-head signal travels with the crop and exits during the punch-in."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
p=ROOT/'out/shop_signal_test_v1/render.py'
s=p.read_text().replace('out/shop_signal_test_v1/clean.mp4','out/shop_push_signal_v4/clean.mp4')
s=s.replace('cx=210*(1-change)+145*change;cy=325*(1-change)+389*change\n radius=52*(1-change)+83*change',
 '''# Match the wide shot crop exactly; the head travels left out of frame.
 crop_a=float(np.clip((sf-2424)/6,0,1)**1.8)
 crop_width=1280+(800/1.2-1280)*crop_a
 zoom=1280/crop_width
 cx=(382-520*crop_a)*zoom
 cy=(262-(64/1.2)*crop_a)*zoom
 radius=88*zoom''')
s=s.replace('fade=smooth((sf-2399+2)/5)*(1-smooth((sf-2472)/11))',
 'fade=smooth((sf-2399+2)/5)*(1-smooth((sf-2427)/5))')
s=s.replace("flicker=1 if sf<2459 else (.45+.55*abs(np.sin((sf-2459)*1.9)))",'flicker=1')
s=s.replace('horizontal=.90*(1-change)+.32*change','horizontal=.90')
s=s.replace(' trail=trail*.38+light*.8', ''' trail=trail*.38+light*.8
 if sf>=2433:trail.fill(0)''')
s=s.replace(' blur=float(np.exp(-.5*((sf-2430.5)/1.25)**2))',
 ' blur=float(np.exp(-.5*((sf-2429.5)/1.5)**2))')
s=s.replace('Amber/cyan globe traces morph into peripheral window reflection; continuous phase and envelope across source switch, blur follows punch; final flicker and release.',
 'Larger amber/cyan traces on gray alien head follow the actual wide crop leftward, streak with the punch and clear by2433, before the close-up landing. No reflection or vapor tail.')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
r=json.loads((OUT/'recipe.json').read_text())
r.update(subject='gray alien souvenir head',effect_clear_frame=2433,push_complete_frame=2436,
 previous_version='out/shop_vapor_test_v3/clean.mp4',
 limitations='Static head coordinate follows known local crop. No tracked 3D geometry. Close-up has no added signal.')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
