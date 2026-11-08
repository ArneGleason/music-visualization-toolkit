"""Install the pinned Mac EffectCraft build or run it with portable project assets."""
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import urllib.request
import zipfile

from project_media import digest

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / 'out' / 'effectcraft-0.18.0'
PROJECT = ROOT / 'projects/together-anyways/generated/animatic/Together-Anyways-lyric-animatic-v04.ecproj'
RELEASE = 'https://github.com/storytold/effectcraft/releases/download/v0.18.0/'
ASSETS = {
    'effectcraft-0.18.0-macos-universal.dmg':
        '79a0c24a644018eb39b722eddb5a15a34280c86856171f6a6415a3541b182004',
    'effectcraft-cli-0.18.0-macos-universal.zip':
        'e47937e21c060c1f7435669526e44ebb458ef3c762e904d701b733212bd8584d',
}


def setup_mac():
    if platform.system() != 'Darwin':
        raise SystemExit('setup-mac must run on the Mac; installers are universal Intel/Apple Silicon.')
    LOCAL.mkdir(parents=True, exist_ok=True)
    for name, expected in ASSETS.items():
        path = LOCAL / name
        if not path.exists() or digest(path) != expected:
            print(f'Downloading {name}', flush=True)
            partial = path.with_suffix('.download')
            urllib.request.urlretrieve(RELEASE + name, partial)
            if digest(partial) != expected:
                raise ValueError(f'Installer checksum failed: {name}')
            partial.replace(path)
    cli_dir = LOCAL / 'effectcraft-cli-0.18.0-macos-universal'
    cli = cli_dir / 'effectcraft-cli'
    if not cli.exists():
        with zipfile.ZipFile(LOCAL / 'effectcraft-cli-0.18.0-macos-universal.zip') as z:
            z.extractall(LOCAL)
    cli.chmod(0o755)
    app = Path.home() / 'Applications/EffectCraft-0.18.0.app'
    if not app.exists():
        mount = LOCAL / 'mount'
        mount.mkdir(exist_ok=True)
        subprocess.run(['hdiutil', 'attach', '-nobrowse', '-readonly', '-mountpoint',
                        str(mount), str(LOCAL / 'effectcraft-0.18.0-macos-universal.dmg')], check=True)
        try:
            apps = list(mount.glob('*.app'))
            if len(apps) != 1:
                raise ValueError('Expected one EffectCraft app in the official disk image')
            app.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['ditto', str(apps[0]), str(app)], check=True)
        finally:
            subprocess.run(['hdiutil', 'detach', str(mount)], check=True)
    candidates = [p for p in (app / 'Contents/MacOS').iterdir()
                  if p.is_file() and 'effectcraft' in p.name.lower() and 'cli' not in p.name.lower()]
    if len(candidates) != 1:
        raise ValueError(f'Cannot locate EffectCraft executable in {app}')
    config = {'cli': str(cli), 'app': str(candidates[0])}
    (LOCAL / 'install.json').write_text(json.dumps(config, indent=2) + '\n')
    print(f'Installed EffectCraft 0.18.0: {app}')
    print('First launch may require the normal macOS approval in Privacy & Security.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', help='CLI path for this invocation (or EFFECTCRAFT_CLI)')
    parser.add_argument('--project', type=Path,
                        help='Toolkit project.json or native .ecproj; defaults to Together Anyways')
    parser.add_argument('command', choices=['setup-mac', 'gui', 'info', 'mcp', 'render-frame', 'render'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == 'setup-mac':
        setup_mac()
        return
    project = PROJECT
    if args.project:
        project = args.project.resolve()
        if project.suffix == '.json':
            spec = json.loads(project.read_text(encoding='utf-8'))
            native = spec.get('sources', {}).get('effectcraftProject')
            if not native:
                parser.error('Project configuration has no sources.effectcraftProject')
            project = (project.parent / native).resolve()
    if not project.is_file():
        parser.error(f'Restore the project media bundle first; missing: {project}')
    config_file = LOCAL / 'install.json'
    config = json.loads(config_file.read_text()) if config_file.exists() else {}
    if args.command == 'gui':
        executable = os.environ.get('EFFECTCRAFT_APP') or config.get('app') or shutil.which('effectcraft')
    else:
        executable = args.cli or os.environ.get('EFFECTCRAFT_CLI') or config.get('cli') or shutil.which('effectcraft-cli')
    if not executable:
        parser.error('Run setup-mac or set EFFECTCRAFT_CLI / EFFECTCRAFT_APP for this machine')
    env = os.environ.copy()
    fonts = str(project.parent / 'assets')
    env['EFFECTCRAFT_FONT_DIRS'] = fonts + (os.pathsep + env['EFFECTCRAFT_FONT_DIRS'] if env.get('EFFECTCRAFT_FONT_DIRS') else '')
    # The native app takes a positional project; --project is CLI-only.
    command = [executable, str(project)] if args.command == 'gui' else [executable, '--project', str(project)]
    if args.command != 'gui':
        command += [args.command, *args.arguments]
        raise SystemExit(subprocess.run(command, cwd=project.parent, env=env).returncode)
    options = {'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {'start_new_session': True}
    subprocess.Popen(command, cwd=project.parent, env=env, **options)


if __name__ == '__main__':
    main()
