from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
old=ROOT/'out/garden_light_moth_v1/render.py'
code=old.read_text().replace('garden_light_moth_v1','garden_ghost_wings_v3')
fx=(ROOT/'out/garden_psychedelic_v2/effects.py').read_text()
fx=fx.replace('smooth((sf-1524)/4)*(1-smooth((sf-1547)/6))','smooth((sf-1521)/13)*(1-smooth((sf-1549)/12))')
fx=fx.replace('freedom=1-.90*body','freedom=np.exp(-((xx-640)/430)**2-((yy-290)/300)**2)*(1-.60*body)')
fx+=(OUT/'ghost_wings.py').read_text()
code=code.replace('records=[];last=',fx+'\nrecords=[];last=')
code=code.replace('strength=((.2+.32*voice)+2.3*accent)*visibility','strength=.12*voice*visibility')
needle="  cv2.imwrite(str(folder/'frames'/f'{i:04d}.png'),np.rint(result*255).astype(np.uint8));records.append(rec)"
code=code.replace(needle,"  result=second_light(result,sf+.5,voice) if name=='walk' else ghost_wings(psychedelic(result,sf+.5),pic,sf+.5)\n"+needle)
exec(compile(code,str(old),'exec'),{'__file__':str(OUT/'render.py'),'__name__':'__main__'})
