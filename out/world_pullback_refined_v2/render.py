"""Small refinement: silhouette departure, lifted planet, signal arrivals."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=ROOT/'out/world_pullback_test_v1/render.py'
s=p.read_text().replace('world_pullback_test_v1','world_pullback_refined_v2')
def replace(old,new):
    global s
    assert old in s,old
    s=s.replace(old,new)
replace('for i,sf in enumerate(range(2122,2199)):', '''# Authored soft silhouette matte for this brief fixed-image departure.
subject=np.zeros((720,1280),np.float32)
outline=np.array([(558,70),(599,63),(623,82),(623,108),(632,137),
 (608,162),(616,187),(629,235),(622,286),(615,313),(631,375),
 (645,406),(648,432),(638,444),(625,425),(614,397),(606,370),
 (604,421),(616,483),(637,591),(650,642),(663,670),(699,673),
 (710,684),(690,698),(628,716),(618,698),(613,662),(590,607),
 (570,541),(556,498),(529,551),(507,605),(497,654),(500,678),
 (527,691),(524,702),(492,704),(451,691),(452,672),(468,626),
 (478,573),(500,512),(527,448),(538,425),(533,396),(531,332),
 (532,269),(536,203),(548,174),(539,141),(533,112),(542,86)],np.int32)
cv2.fillPoly(subject,[outline],1)
# Preserve the carried lantern, without retaining the surrounding garden.
cv2.ellipse(subject,(550,510),(23,46),0,0,360,1,-1)
subject=cv2.GaussianBlur(subject,(0,0),2.2)
cv2.imwrite(str(OUT/'subject_matte.png'),(subject*255).astype(np.uint8))
for i,sf in enumerate(range(2122,2199)):''')
replace('shade=.22+.78*np.clip(-.40*nx-.28*ny+.82*nz,0,1)',
        'shade=.34+.82*np.clip(-.40*nx-.28*ny+.82*nz,0,1)')
replace('planet=surface*shade[:,:,None]', 'planet=np.power(surface,.91)*shade[:,:,None]*1.12')
replace('radius/5)**2)*.25','radius/7)**2)*.38')
start=s.index('    soft=np.exp(')
end=s.index('    pic=pic*(1-alpha',start)
s=s[:start]+'''    # Garden dissolves before its shrinking frame can become a rectangle.
    irregular=.5+.16*np.sin(x*.013+y*.009)+.13*np.sin(y*.025-x*.017)
    garden_alpha=1-smooth((sf-2125)/6+irregular*.26)
    figure_alpha=1-smooth((sf-2137)/7)
    matte=cv2.warpAffine(subject,matrix,(1280,720))
    alpha=np.maximum(garden_alpha,matte*figure_alpha)
    # The garden fades in its original full-frame position; only she departs.
    pic=pic*(1-garden_alpha[:,:,None])+garden*garden_alpha[:,:,None]
    alpha=matte*figure_alpha*(1-garden_alpha)
'''+s[end:]
replace('strength=(.25+.75*np.exp(-np.mod(a-theta,2*np.pi)/1.7))*amount',
        'strength=(.34+1.3*np.exp(-np.mod(a-theta,2*np.pi)/1.1))*amount')
replace('    pic+=glow+cv2.GaussianBlur(glow,(0,0),5)*1.1+cv2.GaussianBlur(glow,(0,0),15)*.6', '''    # Two luminous messages, not spacecraft or explosive impacts.
    for entry,landing,p0,p1,target,color in [
        (2147,2161,(-60.,95.),(260.,30.),(-.40,-.25),(.28,.72,1.)),
        (2155,2170,(1340.,195.),(1010.,65.),(.42,.12),(1.,.85,.35))]:
        if sf<entry: continue
        endpt=np.array([640+210*target[0],324+210*target[1]])
        def point(t):
            return (1-t)**2*np.array(p0)+2*t*(1-t)*np.array(p1)+t*t*endpt
        progress=np.clip((sf-entry)/(landing-entry),0,1)
        if sf<=landing:
            for j in range(24):
                t=max(0,progress-j*.011)
                a1=point(t);a2=point(max(0,t-.011))
                intensity=1.65*np.exp(-j/7)
                cv2.line(glow,tuple(a1.astype(int)),tuple(a2.astype(int)),
                         tuple(float(c*intensity) for c in color),2,cv2.LINE_AA)
            cv2.circle(glow,tuple(point(progress).astype(int)),3,tuple(float(c*1.7) for c in color),-1,cv2.LINE_AA)
        if landing<=sf<landing+13:
            age=sf-landing
            cv2.ellipse(glow,tuple(endpt.astype(int)),(int(5+age*2),int(3+age)),
                        -20,0,360,tuple(float(c*.65*(1-age/13)) for c in color),1,cv2.LINE_AA)
    pic+=glow*1.15+cv2.GaussianBlur(glow,(0,0),5)*1.7+cv2.GaussianBlur(glow,(0,0),17)*1.05''')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
import json
r=json.loads((OUT/'recipe.json').read_text())
r.update(status='refinement_owner_review_pending',
         improvements='Early irregular garden fade, separately shrinking soft silhouette with lantern; lifted planetary midtones/fill/rim; brighter orbit cores and bloom; two curved incoming signal trails with small arrival responses.',
         signal_entries=[2147,2155],signal_landings=[2161,2170],
         limitations='Hand-authored silhouette matte for fast fixed-still pullback, not final roto. Temporary planet texture; geography not solved. No paid generation; no production changes.')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
