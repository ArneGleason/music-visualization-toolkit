"""Expand the approved message handoff with a short, depth-changing swim."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=(ROOT/'out/meaning_orb_pass_v2/render.py').read_text()
source=source.replace('meaning_orb_pass_v2','meaning_orb_swim_v3')
start=source.index('def pose(sf):')
end=source.index('for i,sf in enumerate',start)
source=source[:start]+'''def pose(sf):
    p=np.clip((sf-2748)/88,0,1)
    travel=smooth(p)
    envelope=np.sin(np.pi*p)**2
    waiting=(1-travel)
    t=(sf-2658)/24
    # An unhurried swell while considering the reply, then two swimming curls.
    center=np.array([
        1030-770*travel + waiting*22*np.sin(t*1.7) + 155*np.sin(4*np.pi*p)*envelope,
        435+85*np.sin(np.pi*p) + waiting*27*np.sin(t*1.3) + 72*np.cos(4*np.pi*p)*envelope
    ])
    waiting_radius=48+112*smooth((sf-2668)/66)
    radius=waiting_radius*(1-travel)+118*travel-72*np.sin(np.pi*p)**2
    # Arrival gently opens again, then stops doing acrobatics.
    arrival=smooth((sf-2836)/18)
    radius+=16*np.sin(np.pi*np.clip((sf-2836)/45,0,1))*arrival
    return center,radius
'''+source[end:]
source=source.replace("yaw=.55+t*.58;pitch=.36+.15*np.sin(t*.9)",
    "swim=np.sin(np.pi*np.clip((sf-2748)/88,0,1))**2\n    yaw=.55+t*.58+.40*np.sin(t*2.6)*swim;pitch=.36+.15*np.sin(t*.9)+.25*np.sin(t*3.1)*swim")
exec(compile(source,str(OUT/'render_expanded.py'),'exec'),{'__name__':'__main__','__file__':str(OUT/'render_expanded.py')})
