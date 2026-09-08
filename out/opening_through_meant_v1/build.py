"""Frame-exact review assembly, preserving approved preview-only effects."""
import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]

def run(args, **kwargs):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True, **kwargs)

for name in ('shotlist.json', 'overlay_cues.json'):
    (OUT/name).write_bytes((ROOT/'out/meant_cutaway_v1'/name).read_bytes())
edl = json.loads((OUT/'shotlist.json').read_text())
end = 0
for shot in edl['shots']:
    assert round(shot['start_sec']*24) == end
    end = round(shot['end_sec']*24)
assert end == 2658
adapter = (ROOT/'out/probe_voice_trial/blender_review.py').read_text()
(OUT/'blender_review.py').write_text(adapter.replace('"probe_voice_trial"', '"opening_through_meant_v1"'))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe', '-b',
         '--python-exit-code', '1', '-P', OUT/'blender_review.py', '--',
         '--proxy', '--start', '0', '--end', '2657', '--shotlist', OUT/'shotlist.json',
         '--lyric-flat', 'shots/lyric_motion_full.json', '--out', OUT/'raw.mp4'],
        stdout=log, stderr=subprocess.STDOUT)
# These two review-only treatments already contain their picture/lyrics.
# Replace their exact spans, never overlay duplicate captions or source audio.
graph = (
    '[1:v]trim=start_frame=0:end_frame=86,setpts=N/(24*TB)[a];'
    '[0:v]trim=start_frame=86:end_frame=971,setpts=N/(24*TB)[b];'
    '[2:v]trim=start_frame=0:end_frame=111,setpts=N/(24*TB)[c];'
    '[0:v]trim=start_frame=1082:end_frame=2658,setpts=N/(24*TB)[d];'
    '[a][b][c][d]concat=n=4:v=1:a=0,setsar=1[v];'
    '[3:a]atrim=start=0:end=110.75,asetpts=PTS-STARTPTS[audio]')
run(['ffmpeg', '-v', 'error', '-y', '-i', OUT/'raw.mp4',
     '-i', ROOT/'out/observatory_phosphor_start/preview.mp4',
     '-i', ROOT/'out/rosette_duet_trial/preview.mp4', '-i', ROOT/'audio/song.wav',
     '-filter_complex', graph, '-map', '[v]', '-map', '[audio]', '-frames:v', '2658',
     '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
     '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', OUT/'preview.mp4'])
run(['ffmpeg', '-v', 'error', '-i', OUT/'preview.mp4', '-f', 'null', '-'])
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
    '-show_entries','stream=nb_frames,r_frame_rate,width,height,duration','-of','json',str(OUT/'preview.mp4')]))
s = probe['streams'][0]
assert int(s['nb_frames']) == 2658 and s['r_frame_rate'] == '24/1'
assert (s['width'],s['height']) == (1280,720)
(OUT/'verification.json').write_text(json.dumps(probe,indent=2))
(OUT/'REVIEW.md').write_text('''# Opening through meant

720p, 24 fps, 2658 frames, 1:50.75. Ends after the approved artifact cutaway on meant.

Timing and source snapshot: out/meant_cutaway_v1. Includes the protected oscilloscope,
vocal receiver, probe, garden, specimen, planet, world-blossom and shop treatments.
Preserves the TV-on opening at frames 0..86 and the approved two-rosette preview
at 971..1082 by picture-only replacement. All ranges are end-exclusive.
One uninterrupted master soundtrack, no generated audio, no global beat flash,
no new mastering, no production shotlist mutation. Review-only assembly.
''')
print('Verified opening through meant: 2658 frames, 110.75 seconds.', flush=True)
