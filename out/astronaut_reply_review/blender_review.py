from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
p=ROOT/'out/probe_voice_trial/blender_review.py'
s=p.read_text().replace('"probe_voice_trial"','"astronaut_reply_review"')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'blender_review.py')})
