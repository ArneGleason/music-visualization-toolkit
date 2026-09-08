"""Reframe the garden around its generated pollen bloom, without lip sync."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# Reuse the approved green guide, retaining its song-time choreography.
guide_path = ROOT / 'out/garden_begin_guide_v2/render.py'
guide_source = guide_path.read_text().split("p=ROOT/'out/garden_begin_light_v1/render.py'")[0]
namespace = {'__file__': str(OUT / 'render.py')}
exec(compile(guide_source, str(guide_path), 'exec'), namespace)

source_path = ROOT / 'out/garden_begin_light_v1/render.py'
s = source_path.read_text().replace('garden_begin_light_v1', 'garden_begin_bloom_v3')

def replace(old, new):
    global s
    assert old in s, old
    s = s.replace(old, new)

# Source108 (4.5 seconds, broad flowering burst) lands on song1828, begin.
# Native24fps, real-time speed; visible source66..134 -> song1786..1854.
replace('records=[]', 'cap.set(cv2.CAP_PROP_POS_FRAMES,66)\nrecords=[]')
replace('range(1786,1841)', 'range(1786,1854)')
replace("'55','-an'", "'68','-an'")
replace('end_sec=1841/24,dur_sec=55/24,frames=55', 'end_sec=1854/24,dur_sec=68/24,frames=68')
replace("'end':1841", "'end':1854")
replace("1841/24;cues['frames']=1841", "1854/24;cues['frames']=1854")
replace("'1840'", "'1853'")
replace('end=76.708333333333', 'end=77.25')
replace("'131','-c:v'", "'144','-c:v'")
replace('result=pic+(core+bloom)*protection[:,:,None]',
        'result=pic+(core+bloom)*protection[:,:,None]\n result=guide(result,sf,x,y,protection)')
replace('Garden lantern light wave arrives on begin, then releases.',
        'Original unsynced garden take advanced to pollen release on begin. Green guide and song-timed lights retained.')
replace('garden_begin_light_audition', 'garden_begin_bloom_audition')
# Write the actual mapping after the shared renderer completes.
exec(compile(s, str(source_path), 'exec'),
     {'__name__': '__main__', '__file__': str(OUT / 'render.py'), 'guide': namespace['guide']})
recipe = json.loads((OUT / 'recipe.json').read_text())
recipe.update(song_frames=[1786,1854], source_frames=[66,134],
              source_song_origin_frame=1720, speed=1,
              preview_song_frames=[1710,1854], preview_frames=144,
              begin_frame=1828, source_bloom_anchor_frame=108,
              release_frames_after_lyric=13,
              lip_sync_used=False,
              lip_sync_alternate='out/garden_begin_lipsync_v1/synced.mp4',
              method='Original generated pollen release aligned to begin by source selection, not time stretching. Existing lantern/flower response and excited green guide reapplied at original song-time cues.',
              status='owner_review_pending')
(OUT / 'recipe.json').write_text(json.dumps(recipe, indent=2))
print('Bloom preview complete:144frames, bird then pollen release.')
