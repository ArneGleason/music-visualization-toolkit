"""Review this single test without modifying the production edit."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from assembly_timebase import conform_clip


def run(args):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True)


def samples(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4')


def main():
    synced = OUT / 'synced.mp4'
    guide = ROOT / 'out/opening_sync_test/guide.wav'
    x, y = samples(guide), samples(synced)
    n = min(len(x), len(y))
    corr = float(np.corrcoef(x[:n], y[:n])[0, 1])
    lag_scores = []
    for lag in range(-2400, 2401, 48):
        first, last = max(0, -lag), min(len(x), len(y)-lag)
        score = float(np.corrcoef(x[first:last], y[first+lag:last+lag])[0, 1])
        lag_scores.append((score, lag))
    score, lag = max(lag_scores)
    report = {'guide_samples':len(x), 'embedded_samples':len(y),
        'zero_lag_correlation':corr, 'best_lag_ms':lag/48,
        'best_lag_correlation':score, 'song_origin_frame':143, 'fps':24,
        'lead_handle_frames':12}
    (OUT/'audio_check.json').write_text(json.dumps(report, indent=2))
    if corr < .98 or abs(lag) > 48:
        raise RuntimeError('Guide alignment check failed; inspect before preview')
    clip = conform_clip(ROOT, {'file':str(synced), 'in_sec':0, 'speed':1}, 24, prepare=True)
    # Timestamp conversion preserves speed. Never reinterpret 30fps as 24fps.
    common = ['-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',
              '-c:a','aac','-b:a','256k','-movflags','+faststart']
    graph = ('[0:v]setpts=PTS-STARTPTS,scale=640:360,pad=640:400:0:40:black,'
        "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='BASE - before lip sync':x=12:y=10:fontsize=20:fontcolor=white[l];"
        '[1:v]setpts=PTS-STARTPTS,scale=640:360,pad=640:400:0:40:black,'
        "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='KLING - same guide clock':x=12:y=10:fontsize=20:fontcolor=white[r];"
        '[l][r]hstack[v];[2:a]asetpts=PTS-STARTPTS[a]')
    run(['ffmpeg','-v','error','-y','-i',OUT/'base.mp4','-i',clip['file'],
        '-i',guide,'-filter_complex',graph,'-map','[v]','-map','[a]',
        '-shortest',*common,OUT/'comparison_guide.mp4'])
    graph = ('[0:v]setpts=PTS-STARTPTS[v];[1:a]'
        'atrim=start=5.958333333333:end=13.958333333333,asetpts=PTS-STARTPTS[a]')
    run(['ffmpeg','-v','error','-y','-i',clip['file'],'-i',ROOT/'audio/song.wav',
        '-filter_complex',graph,'-map','[v]','-map','[a]','-shortest',*common,
        OUT/'master_preview.mp4'])
    run(['ffmpeg','-v','error','-y','-i',synced,'-vf',
        'fps=2,scale=640:360,tile=4x4','-frames:v','1',OUT/'codex_synced_contact.jpg'])
    edl_path = ROOT/'shots/shotlist.json'
    before = hashlib.sha256(edl_path.read_bytes()).hexdigest()
    edl = json.loads(edl_path.read_text())
    for shot in edl['shots']:
        if shot['id'] == 's003':
            shot['clip'] = dict(clip, in_sec=12/24)
    snap = OUT/'review_shotlist.json'
    snap.write_text(json.dumps(edl,indent=2))
    raw = OUT/'assembly_raw.mp4'
    with (OUT/'assembly.log').open('w') as log:
        subprocess.run([sys.executable,'tools/blender_comp.py','--proxy',
            '--start','0','--end','292','--shotlist',str(snap),
            '--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)],
            cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    graph = ('[0:v]setpts=PTS-STARTPTS[v];[1:a]'
        'atrim=start=0:end=12.208333333333,asetpts=PTS-STARTPTS[a]')
    run(['ffmpeg','-v','error','-y','-i',raw,'-i',ROOT/'audio/song.wav',
        '-filter_complex',graph,'-map','[v]','-map','[a]','-frames:v','293',
        *common,OUT/'assembly_preview.mp4'])
    assert before == hashlib.sha256(edl_path.read_bytes()).hexdigest()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
