from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'out/probe_voice_trial/blender_review.py'
s=p.read_text().replace('"probe_voice_trial"','"receiver_reply_arrival_review"')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(ROOT/'out/receiver_reply_arrival_review/blender_review.py')})
