"""Launch this project's shared frame-review UI; reuse its existing server."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
PORT = 8778
URL = f'http://127.0.0.1:{PORT}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    config = json.loads((PROJECT / 'production/review-config.json').read_text())
    video = PROJECT / config['video']
    if not video.is_file():
        raise SystemExit('Restore the v020 media snapshot first; review video is missing.')
    output = PROJECT / 'generated/frame-review'
    output.mkdir(parents=True, exist_ok=True)
    score = json.loads((PROJECT / 'shots/shotlist.json').read_text())
    shots = []
    for number, original in enumerate(score['shots'], 1):
        shot = dict(original)
        shot['shotNumber'] = number
        shot['title'] = f"{shot['id']} · {shot['title']}"
        insert = next((v for v in score.get('reviewVideoInserts', [])
                       if v['startFrame'] <= shot['startFrame'] < v['endFrameExclusive']), None)
        if insert:
            shot['videoSource'] = insert['source']
            source_start = insert.get('originalSourceOffsetFrames', insert.get('sourceOffsetFrames', 0))
            rate = insert.get('originalSourceFramesPerEditFrame', 1)
            shot['videoEdit'] = {'sourceInFrame': source_start + (shot['startFrame'] - insert['startFrame']) * rate}
        shots.append(shot)
    index = output / 'navigation.json'
    index.write_text(json.dumps({'fps': 24, 'frameIndexBase': 0, 'shots': shots}, indent=2)+'\n')
    state = output / 'current.json'
    state.write_text(json.dumps({'video': str(video), 'master_start': 0})+'\n')

    def running():
        try:
            with urllib.request.urlopen(URL + '/api', timeout=1) as response:
                data = json.load(response)
            if data['name'] != video.name:
                raise SystemExit(f'Port {PORT} belongs to a different review. Leave it running and choose another port.')
            return True
        except (OSError, ValueError):
            return False

    if not running():
        command = [sys.executable, str(ROOT / 'tools/frame_review.py'),
                   '--video', str(video), '--notes', str(PROJECT / 'production/frame-review-notes.json'),
                   '--master-start', '0', '--master-frame-base', '0', '--port', str(PORT),
                   '--state', str(state), '--shotlist', str(index),
                   '--lyrics', str(PROJECT / 'generated/timeline.compiled.json')]
        with (output / 'server.log').open('a') as log:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=log,
                                       stdin=subprocess.DEVNULL, start_new_session=True)
        for _ in range(40):
            if running():
                break
            if process.poll() is not None:
                raise SystemExit(f'Review failed to start; see {output / "server.log"}')
            time.sleep(.25)
        else:
            raise SystemExit('Review server did not become ready.')
    if not args.no_browser:
        webbrowser.open(URL)
    print(URL)


if __name__ == '__main__':
    main()
