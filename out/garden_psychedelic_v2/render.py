from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
old=ROOT/'out/garden_light_moth_v1/render.py'
code=old.read_text().replace('garden_light_moth_v1','garden_psychedelic_v2')
code=code.replace('records=[];last=',(OUT/'effects.py').read_text()+'\nrecords=[];last=')
# Stop promoting the awkward generated light's path; preserve the source itself.
code=code.replace('strength=((.2+.32*voice)+2.3*accent)*visibility','strength=.12*voice*visibility')
needle="  cv2.imwrite(str(folder/'frames'/f'{i:04d}.png'),np.rint(result*255).astype(np.uint8));records.append(rec)"
assert needle in code
code=code.replace(needle,"  result=second_light(result,sf+.5,voice) if name=='walk' else psychedelic(result,sf+.5)\n"+needle)
exec(compile(code,str(old),'exec'),{'__file__':str(OUT/'render.py'),'__name__':'__main__'})
