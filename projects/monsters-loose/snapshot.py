"""Snapshot lightweight production sources; leave large generated media external."""
import argparse, hashlib, json, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

TEXT = {'.py', '.ps1', '.json', '.md', '.txt', '.html', '.js', '.vtt', '.csv'}
BINARY = {'.blend', '.ttf'}
URL = re.compile(r'https?://[^\s<>"\x27\\)]+')
SECRET = re.compile(r'("(?:api_key|access_token|refresh_token|authorization|client_secret)"\s*:\s*")[^"\r\n]+', re.I)

def sanitize(text):
    def clean(match):
        value = match.group(0)
        parts = urlsplit(value)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, '', '')) if parts.query else value
    return SECRET.sub(r'\1[REDACTED]', URL.sub(clean, text))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    dest = Path(__file__).resolve().parent / 'recovery'
    dest.mkdir(exist_ok=True)
    entries = []
    for path in sorted(source.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative = path.relative_to(source)
        size = path.stat().st_size
        keep = path.suffix.lower() in TEXT | BINARY and size <= 5_000_000
        entry = {'path': relative.as_posix(), 'bytes': size, 'included': keep}
        if keep:
            target = dest / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix.lower() in TEXT:
                content = sanitize(path.read_text(encoding='utf-8-sig'))
                if not target.exists() or target.read_text(encoding='utf-8') != content:
                    target.write_text(content, encoding='utf-8')
            else:
                if not target.exists() or target.read_bytes() != path.read_bytes():
                    shutil.copy2(path, target)
            entry['snapshot_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        entries.append(entry)
    (dest.parent / 'inventory.json').write_text(json.dumps({'source_root': str(source), 'files': entries}, indent=2)+'\n')
    kept = [e for e in entries if e['included']]
    print(f'Snapshotted {len(kept)} files, {sum(e["bytes"] for e in kept)/1024**2:.2f} MiB; excluded media recorded in inventory.json')

if __name__ == '__main__':
    main()
