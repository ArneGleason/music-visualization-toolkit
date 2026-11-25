#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-}" in
  "") restore_bitwig=false ;;
  --with-bitwig) restore_bitwig=true ;;
  *) echo "Usage: $0 [--with-bitwig]" >&2; exit 2 ;;
esac

if ! command -v python3 >/dev/null || ! python3 -c 'import sys; sys.exit(sys.version_info < (3,10))'; then
  echo 'Python 3.10 or newer is required.' >&2
  exit 1
fi
if [ ! -x .venv/bin/python3 ]; then
  python3 -m venv .venv
fi

project=projects/open-up-the-secret-room
.venv/bin/python3 tools/project_media.py restore "$project/media-manifest.json"
if $restore_bitwig; then
  .venv/bin/python3 tools/project_media.py restore "$project/bitwig-source-manifest.json"
fi
.venv/bin/python3 tools/timeline.py compile "$project/project.json"
.venv/bin/python3 tools/timeline.py validate "$project/project.json"
echo 'Open Up the Secret Room is ready. Read projects/open-up-the-secret-room/CONTINUE-HERE.md.'
