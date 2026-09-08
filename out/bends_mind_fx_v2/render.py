"""Earlier buildup, double-strength punctuation and prismatic distortion."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'out/bends_mind_fx_v1/render.py'
code=source.read_text().replace('bends_mind_fx_v1','bends_mind_fx_v2')
code=code.replace('sf-3513','sf-3505').replace('(sf-3505)/48','(sf-3505)/56')
code=code.replace('(.18*buildup+.55*bend+.9*mind)*fade','(.08+.30*buildup+1.1*bend+1.8*mind)*fade')
code=code.replace('(2*buildup+17*bend+27*mind)*fade','(2+6*buildup+34*bend+54*mind)*fade')
code=code.replace('split=edge*strength*2.5','split=edge*(1.2*buildup+9*bend+17*mind)*fade')
code=code.replace('(mx+sign*split).astype(np.float32),my,','(mx+sign*split*dx/rad).astype(np.float32),(my+sign*split*dy/rad).astype(np.float32),')
code=code.replace('radius=185+110*buildup+85*mind','radius=190+120*buildup+150*mind')
code=code.replace('(.045+.11*bend+.19*mind)','(.06+.20*bend+.34*mind)')
code=code.replace('22*mind*np.sin','44*mind*np.sin')
code=code.replace('(180,5)','(320,5)').replace('age*(70+130*d)','age*(110+190*d)')
code=code.replace("'--end','3710'","'--end','3709'").replace('3711/24','3710/24').replace("'273'","'272'").replace('(24.,273)','(24.,272)').replace('[3438,3711]','[3438,3710]').replace("'anticipation_start':3513","'anticipation_start':3505")
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
