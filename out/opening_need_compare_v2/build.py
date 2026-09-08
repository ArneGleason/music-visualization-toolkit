"""Delay both comparison cutaways by 22 frames, preserving their duration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'out/opening_need_compare_v1/build.py'
code = source.read_text()
code = code.replace("template = (SOURCE / 'render.py').read_text()", "template = (SOURCE / 'render.py').read_text().replace('183', '205').replace('225', '247')")
code = code.replace('opening_need_static_{label}_v1', 'opening_need_static_{label}_v2')
code = code.replace('opening_need_static_a_v1', 'opening_need_static_a_v2')
code = code.replace('opening_need_static_b_v1', 'opening_need_static_b_v2')
code = code.replace("OUT / 'horizon.png'", "ROOT / 'out/opening_need_compare_v1/horizon.png'")
code = code.replace("'cutaway_song_frames':[183,225]", "'cutaway_song_frames':[205,247],'delay_frames':22,'delay_seconds':22/24")
exec(compile(code, str(source), 'exec'), {'__file__': __file__, '__name__': '__main__'})
