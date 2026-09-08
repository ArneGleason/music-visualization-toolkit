from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'out/receiver_retimed_review/blender_review.py'
s=p.read_text().replace('out/receiver_retimed_review/receiver_decision.json','out/receiver_voice_review/receiver_decision.json').replace('"receiver_retimed_review"','"receiver_voice_review"')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'blender_review.py')})
