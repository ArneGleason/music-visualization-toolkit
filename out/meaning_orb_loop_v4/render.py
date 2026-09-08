"""One true closed aerial loop, with stronger music-responsive message points."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=(ROOT/'out/meaning_orb_pass_v2/render.py').read_text().replace('meaning_orb_pass_v2','meaning_orb_loop_v4')
start=source.index('def pose(sf):');end=source.index('for i,sf in enumerate',start)
source=source[:start]+'''def pose(sf):
    t=(sf-2658)/24
    if sf<2748:
        center=np.array([1030+22*np.sin(t*1.7),435+27*np.sin(t*1.3)])
        radius=48+112*smooth((sf-2668)/66)
    elif sf<2768:
        q=smooth((sf-2748)/20)
        start_t=(2748-2658)/24
        start=np.array([1030+22*np.sin(start_t*1.7),435+27*np.sin(start_t*1.3)])
        center=start*(1-q)+np.array([680.,555.])*q
        radius=160-80*q
    elif sf<=2818:
        # Full closed circle. No sideways drift can flatten this into a wave.
        q=smooth((sf-2768)/50)
        theta=2*np.pi*q
        center=np.array([680-145*np.sin(theta),410+145*np.cos(theta)])
        radius=80+14*np.sin(np.pi*q)**2
    else:
        q=smooth((sf-2818)/32)
        center=np.array([680-420*q,555-90*q])
        radius=80+48*q+10*np.sin(np.pi*q)
    return center,radius
'''+source[end:]
source=source.replace('yaw=.55+t*.58;pitch=.36+.15*np.sin(t*.9)',
    'loop_angle=2*np.pi*smooth((sf-2768)/50)\n    yaw=.55+t*.58;pitch=.36+.15*np.sin(t*.9)+.28*np.sin(loop_angle)')
source=source.replace('size=3','size=6')
source=source.replace("opacity=(.35+.35*levels[k%2])*(.8+.2*depth[0]/radius)*entrance",
    "loop_emphasis=np.sin(np.pi*np.clip((sf-2768)/50,0,1))**2\n            opacity=(.28+.60*levels[k%2])*(1+.25*loop_emphasis)*(.85+.15*depth[0]/radius)*entrance")
source=source.replace('size=4+(k%3)','size=7+2*(k%3)')
source=source.replace('cv2.circle(light,point,2,tuple(color),-1,cv2.LINE_AA)',
    'cv2.circle(light,point,3 if leak else 3+int(levels[k%2]),tuple(color),-1,cv2.LINE_AA)')
source=source.replace('cv2.line(light,a,b,tuple(color),1,cv2.LINE_AA)','cv2.line(light,a,b,tuple(color),2,cv2.LINE_AA)')
source=source.replace('tuple(color),1,cv2.LINE_AA)','tuple(color),2,cv2.LINE_AA)')
source=source.replace("'travel_frames':[2748,2836]","'travel_frames':[2748,2850],'closed_loop_frames':[2768,2818]")
exec(compile(source,str(OUT/'render_expanded.py'),'exec'),{'__name__':'__main__','__file__':str(OUT/'render_expanded.py')})
