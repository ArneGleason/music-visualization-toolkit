#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo 'Python 3.10+ is needed. Install Python from python.org, then run this again.'
  exit 1
fi
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ is needed"'
if [ ! -x .venv/bin/python3 ]; then
  python3 -m venv .venv
fi
.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 tools/project_media.py restore projects/let-the-phone-book-sing/media-manifest.json
.venv/bin/python3 tools/project_media.py verify projects/let-the-phone-book-sing/media-manifest.json
.venv/bin/python3 tools/effectcraft.py setup-mac
.venv/bin/python3 tools/timeline.py validate projects/let-the-phone-book-sing/project.json
echo 'Let the Phone Book Sing is ready for video design.'
echo 'Read projects/let-the-phone-book-sing/CONTINUE-HERE.md.'
echo 'The large DAWproject stays on the PC; the saved timing grid is ready to use.'
