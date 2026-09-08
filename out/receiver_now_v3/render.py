from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=ROOT/'out/receiver_interaction_v2/render.py'
s=p.read_text().split("exec(compile(code,str(source),'exec')")[0]
s=s.replace('receiver_interaction_v2','receiver_now_v3')
ns={'__file__':str(p)}
exec(compile(s,str(p),'exec'),ns)
code=ns['code']
fx=(OUT/'burst.py').read_text()
code=code.replace('def hardware_traces(songframe,matrix,voice):',fx+'\ndef hardware_traces(songframe,matrix,voice):')
code=code.replace('ripple=1.0*np.sin(theta*17+songframe*.25)+.5*np.sin(theta*37-songframe*.18)',
 'ripple=(1+5*now_pulse(songframe))*(1.0*np.sin(theta*17+songframe*.25)+.5*np.sin(theta*37-songframe*.18))')
code=code.replace('  result+=np.clip(lit+glow,0,1)*.5',
 '  at=songframe+(sub+.5)/2\n  glow=glow*(1+2.2*now_pulse(at))+receiver_burst(at,matrix)\n  result+=np.clip(lit+glow,0,1)*.5')
code=code.replace('owner review pending, production unchanged.', 'NOW burst at song1175; owner review pending, production unchanged.')
exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
