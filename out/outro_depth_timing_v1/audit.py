from pathlib import Path
import json,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
records=[]
paths=list((ROOT/'tools').glob('*.py'))+list((ROOT/'out').glob('*/*.py'))
for p in paths:
    if any(v in str(p).lower() for v in ['deps','site-packages']):continue
    text=p.read_text(errors='replace')
    bpy=bool(re.search(r'\bimport bpy\b|\bfrom bpy\b',text))
    raster=bool(re.search(r'cv2\.(GaussianBlur|remap|warpPerspective|polylines|line|circle|resize)|ImageDraw|drawImage|putImageData',text))
    if not(bpy or raster):continue
    evidence=[]
    for n,line in enumerate(text.splitlines(),1):
        if re.search(r'import bpy|cv2\.(GaussianBlur|remap|warpPerspective|polylines)|resolution_[xy]|1280|1920|new_image|new_movie',line):
            evidence.append({'line':n,'text':line.strip()[:180]})
            if len(evidence)>=8:break
    records.append({'recipe':p.relative_to(ROOT).as_posix(),'category':'hybrid' if bpy and raster else 'Blender present' if bpy else 'raster operations','evidence':evidence})
(OUT/'renderer_inventory.json').write_text(json.dumps(records,indent=2))
print('Recipe inventory:',len(records),'entries. Classification is a source-code screen, not certification of active selections.')
