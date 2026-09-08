from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
d=ROOT/'out/outro_A2_tv_v1'
p=d/'settings.json';s=json.loads(p.read_text());s.update(source_origin_song_frame=4320,resolve_source_seconds=[1.85,2.82],live_glass_weight=.45,point_punctuation_source_frames=[60,79]);p.write_text(json.dumps(s,indent=2))
p=d/'burst_timing.json';s=json.loads(p.read_text());s.update(song_peak_frame=4320+s['source_peak_frame'],live_glass_weight=.45,notes='Measured source TV switch-on occurs while A is offscreen. Authored graphic punctuation uses Gaussian peak source68, sigma6 frames, not this measured flash envelope.',authored_peak_source_frame=68,authored_peak_song_frame=4388);p.write_text(json.dumps(s,indent=2))
