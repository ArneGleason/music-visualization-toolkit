from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'out/probe_voice_trial/blender_review.py'
s=p.read_text().replace('"probe_voice_trial"','"shop_snap_test_v2"')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(ROOT/'out/shop_snap_test_v2/blender_review.py')})
