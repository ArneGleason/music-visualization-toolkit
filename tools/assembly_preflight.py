"""Check actual frame coverage and protected selections before a rough render."""
import json
import pathlib
import argparse
from assembly_sources import load_decisions, resolve_clip, inspect_video
from assembly_timebase import conform_clip

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-timebase', action='store_true')
    args = parser.parse_args()
    shots = json.loads((ROOT/'shots/shotlist.json').read_text())['shots']
    cues = json.loads((ROOT/'generated/overlay_cues.json').read_text())
    indexed = {s['id']:s for s in cues['shots']}
    decisions = load_decisions(ROOT)
    fps = cues['fps']
    rows = []
    previous = 0
    for shot in shots:
        cue = indexed[shot['id']]
        start,end = round(shot['start_sec']*fps),round(shot['end_sec']*fps)
        assert start == previous and end > start, shot['id']
        assert (start,end) == (cue['start'],cue['end']), shot['id']
        assert shot['frames'] == end-start, shot['id']
        clip = resolve_clip(ROOT,shot,fps,decisions,start,end)
        clip = conform_clip(ROOT,clip,fps,prepare=args.prepare_timebase)
        path = ROOT/clip['file']
        assert path.is_file(), str(path)
        rate,count = inspect_video(str(path))
        assert rate == fps, (shot['id'],'unhandled frame rate',rate)
        required = clip.get('in_sec',0)+(end-start)/fps*clip.get('speed',1)
        assert required <= count/rate+1e-5, (shot['id'],required,count/rate)
        rows.append(f"| {shot['id']} | {start}:{end} | {clip['file']} | {count/rate-required:.3f} |")
        previous=end
    assert previous == cues['frames']
    coverage=json.loads((ROOT/'shots/outro_coverage.json').read_text())
    for row in coverage['cut']:
        if row['take']:
            origin=coverage['takes'][row['take']]['song_start_frame']
            assert round(row['clip']['in_sec']*fps)==row['start']-origin
    report=ROOT/'out/rough_preflight.md'
    report.write_text('# Rough assembly preflight\n\n'
        f'PASS: {len(shots)} shots, {previous} frames at {fps:g} fps; '
        f'{len(decisions)} protected FX selections. No gaps, overlaps or short sources.\n\n'
        'Outro take origins validated. FX deliveries are silent and cut-length only; '
        'unused source duration below is not a promise of usable lip-sync or FX handles.\n\n'
        '| Shot | Song frames (end exclusive) | Resolved picture | Unused source seconds |\n'
        '| --- | --- | --- | --- |\n'+'\n'.join(rows)+'\n',encoding='utf-8')
    print(report.read_text().splitlines()[2])


if __name__=='__main__':
    main()
