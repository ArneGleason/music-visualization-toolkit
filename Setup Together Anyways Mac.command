#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo 'Python 3.10+ is needed. Install Python from python.org, then run this again.'
  exit 1
fi
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ is needed"'
python3 tools/project_media.py restore projects/together-anyways/media-manifest.json
python3 tools/effectcraft.py setup-mac
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then
    brew install ffmpeg
  else
    echo 'Media and EffectCraft restored. Install FFmpeg before rebuilding timeline previews.'
    echo 'With Homebrew: brew install ffmpeg'
    exit 1
  fi
fi
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 tools/timeline.py validate projects/together-anyways/project.json
echo 'Together Anyways is ready. Read projects/together-anyways/CONTINUE-HERE.md.'
