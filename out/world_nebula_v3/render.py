"""Preserve approved pullback/planet/signals; replace only star background."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
ns={}
exec(compile((OUT/'space.py').read_text(),str(OUT/'space.py'),'exec'),ns)
p=ROOT/'out/world_pullback_refined_v2/render.py'
s=p.read_text().replace('world_pullback_refined_v2','world_nebula_v3')
old="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})"
assert old in s
new="s=s.replace('for i,sf in enumerate(range(2122,2199)):', 'stars=make_space(cv2,x,y)\\ncv2.imwrite(str(OUT/\\\"background.png\\\"),np.clip(stars*255,0,255).astype(np.uint8))\\nfor i,sf in enumerate(range(2122,2199)):')\nexec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py'),'make_space':make_space})"
s=s.replace(old,new)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py'),'make_space':ns['make_space']})
r=json.loads((OUT/'recipe.json').read_text())
r['background']='Seeded multiscale violet/teal clouds, diagonal star band with dark dust lane, soft warm distant patch, varied tiny stars. Static backdrop, no rainbow cycling; central contrast reserved for planet/signals.'
r['status']='nebula_refinement_owner_review_pending'
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
