"""Hold the landscape until just before the return to It's important."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'out/opening_need_compare_v1/build.py'
code = source.read_text()
code = code.replace("template = (SOURCE / 'render.py').read_text()", "template = (SOURCE / 'render.py').read_text().replace('183', '205').replace('225', '282').replace('42', '77').replace('1.75', str(77/24))")
code = code.replace('opening_need_static_{label}_v1', 'opening_need_static_{label}_v3')
code = code.replace('opening_need_static_a_v1', 'opening_need_static_a_v3')
code = code.replace('opening_need_static_b_v1', 'opening_need_static_b_v3')
code = code.replace("OUT / 'horizon.png'", "ROOT / 'out/opening_need_compare_v1/horizon.png'")
code = code.replace("'-frames:v','42'", "'-frames:v','77'")
code = code.replace("'cutaway_song_frames':[183,225]", "'cutaway_song_frames':[205,282],'cutaway_duration_seconds':77/24,'return_before_its_important_frames':2")
exec(compile(code, str(source), 'exec'), {'__file__': __file__, '__name__': '__main__'})
