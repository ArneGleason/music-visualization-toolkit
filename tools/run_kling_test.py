"""Submit an explicit Kling test plan once, or collect its existing tasks."""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

CLI = ['C:/Program Files/nodejs/node.exe',
       'C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js']


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--submit', action='store_true')
    args = parser.parse_args()
    project = args.plan.resolve().parent
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    for shot in plan['shots']:
        out = project / plan['output'] / shot['id']
        out.mkdir(parents=True, exist_ok=True)
        submission = out / 'submission.json'
        if args.submit:
            # A persisted attempt blocks duplicate charges, including uncertain outcomes.
            if (out / 'request.json').exists():
                print(shot['id'], 'already attempted; collection only', flush=True)
                continue
            argv = [*CLI, 'image_to_video', '--image', str(project / shot['firstImage'])]
            if shot.get('tailImage'):
                argv += ['--tailImage', str(project / shot['tailImage'])]
            for key in ('model', 'duration', 'resolution', 'imageCount',
                        'enable_audio', 'prefer_multi_shots'):
                value = shot[key]
                argv += ['--' + key, str(value).lower() if isinstance(value, bool) else str(value)]
            argv.append(shot['prompt'])
            save(out / 'request.json', shot)
        else:
            data = json.loads(submission.read_text(encoding='utf-8'))
            task = data['body']['generationId']
            argv = [*CLI, 'query_tasks', task]
        result = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8')
        (out / ('submission.stderr.txt' if args.submit else 'query.stderr.txt')).write_text(
            result.stderr, encoding='utf-8')
        target = submission if args.submit else out / 'result.json'
        target.write_text(result.stdout, encoding='utf-8')
        if result.returncode:
            raise SystemExit(f'{shot["id"]}: CLI failed; recorded outcome, no resubmission.')
        data = json.loads(result.stdout)
        if not data.get('ok'):
            raise SystemExit(f'{shot["id"]}: request failed; see {target}')
        body = data.get('body', {})
        print(shot['id'], body.get('status'), 'credits', body.get('creditsConsumed'),
              'task', body.get('generationId', ''), flush=True)
        if not args.submit:
            for i, work in enumerate(body.get('works', []), 1):
                clean_url = work.get('urlWithoutWatermark') or work.get('url_without_watermark')
                url = clean_url or work.get('url')
                if url:
                    suffix = '-clean' if clean_url else ''
                    dest = out / f'{shot["id"]}-{i:02}{suffix}.mp4'
                    if not dest.exists():
                        urllib.request.urlretrieve(url, dest)
                    print('SAVED', dest, flush=True)


if __name__ == '__main__':
    main()
