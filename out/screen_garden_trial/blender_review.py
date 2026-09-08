from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'out/probe_voice_trial/blender_review.py'
s=p.read_text().replace('"probe_voice_trial"','"screen_garden_trial"')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(ROOT/'out/screen_garden_trial/blender_review.py')})
